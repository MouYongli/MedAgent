import json
import os
import re
from datetime import datetime
from urllib.parse import unquote

import requests
from PyPDF2 import PdfReader

from general.helper.logging import logger
from general.data_model.guideline_metadata import GuidelineMetadata, GuidelineValidityInformation, GuidelineDownloadInformation

UPDATE_EXISTING_ENTRIES = True

def parse_filename(filename):
    """
    Parse metadata from a PDF filename (without extension) based on the naming convention.

    Expected naming convention:
      AWMFRegisterNumber_Class_TitleTokens...[_abgelaufen]_CreatedDate[-abgelaufen]
    """
    pattern = r"(\d{3}-\d{3}[^_]*)_(?:(S[^_]+)[_-])?(.*)_(\d{4}\-\d+)(.*)"
    match = re.search(pattern, filename)

    if not match:
        raise ValueError('Invalid filename (expect certain pattern)')

    awmf_register_number = match.group(1)
    awmf_class = match.group(2) if match.group(2) is not None else ""
    title = match.group(3)
    date_part = match.group(4)
    additional = match.group(5) if match.group(5) else ""

    title = title.replace('-', ' ').replace('_', ' ')
    title = unquote(title)

    still_valid = 'abgelaufen' not in additional.lower()
    extended_validity = 'verlaengert' in additional.lower()

    # Parse the date
    try:
        guidelines_creation_date = datetime.strptime(date_part, "%Y-%m")
    except ValueError:
        raise ValueError(f"Date '{date_part}' in filename does not match format 'YYYY-MM'.")

    # logger.success("Extracted metadata from PDF filename '{}'".format(filename))
    return {
        "title": title,
        "awmf_register_number": awmf_register_number,
        "awmf_class": awmf_class,
        "validity_information": {
            "valid": still_valid,
            "extended_validity": extended_validity,
            "guidelines_creation_date": guidelines_creation_date
        }
    }

def get_pdf_pagecount(file_path):
    """Return the number of pages in the given PDF file."""
    try:
        with open(file_path, 'rb') as f:
            reader = PdfReader(f)
            return len(reader.pages)
    except Exception as e:
        logger.error(f"Error reading {file_path}: {e}")
        return None

def get_plain_text_from_pdf(pdf_file_path, text_output_dir):
    base_name = os.path.basename(pdf_file_path)
    file_name_without_extension = os.path.splitext(base_name)[0]
    text_file_path = os.path.join(text_output_dir, f"{file_name_without_extension}.txt")

    if os.path.exists(text_file_path):
        # Read and return the existing text file content
        with open(text_file_path, 'r', encoding='utf-8') as text_file:
            text = text_file.read()
        # logger.info(f"Text file already exists. Reading from {text_file_path}")
        return text

    text = ""
    with open(pdf_file_path, 'rb') as file:
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()

    with open(text_file_path, 'w', encoding='utf-8') as text_file:
        text_file.write(text)

    return text

def download_pdf(url, pdf_output_dir):
    """Download a PDF from the given URL and save it to the filesystem."""
    response = requests.get(url)
    if response.status_code == 200:
        filename = os.path.join(pdf_output_dir, os.path.basename(url))
        with open(filename, 'wb') as file:
            file.write(response.content)
        return filename
    else:
        logger.error(f"Could not download {url}")
        raise Exception(f"Failed to download PDF from {url}, status code: {response.status_code}")

def store_document(guideline_collection, metadata: GuidelineMetadata, pdf_output_dir, text_output_dir):
    """
    For the given URL, use the file on disk if it exists (to avoid re-downloading)
    but always parse the metadata from the filename and update the MongoDB record.
    """
    url = metadata.download_information.url
    file_path = os.path.join(pdf_output_dir, os.path.basename(url))
    if UPDATE_EXISTING_ENTRIES or not(os.path.exists(file_path)):
        download_pdf(url, pdf_output_dir)

    base_filename, _ = os.path.splitext(os.path.basename(file_path))
    try:
        filename_info = parse_filename(base_filename)
    except ValueError as ve:
        logger.error(f"Failed to parse filename '{base_filename}': {ve}")
        return None

    page_count = get_pdf_pagecount(file_path)
    plain_text = get_plain_text_from_pdf(file_path, text_output_dir)
    current_time = datetime.now()

    metadata.awmf_register_number = filename_info["awmf_register_number"]
    metadata.awmf_class = filename_info["awmf_class"]
    metadata.title = filename_info["title"]
    metadata.validity_information = GuidelineValidityInformation.from_dict(filename_info["validity_information"])
    metadata.last_update = current_time

    if metadata.download_information:
        metadata.download_information.file_path = file_path
        metadata.download_information.page_count = page_count
        metadata.download_information.download_date = current_time
    else:
        metadata.download_information = GuidelineDownloadInformation(
            url=url,
            file_path=file_path,
            page_count=page_count,
            download_date=current_time
        )

    document = metadata.as_dict()
    existing = guideline_collection.find_one({"awmf_register_number": metadata.awmf_register_number})
    if existing:
        update_fields = {k: v for k, v in document.items() if existing.get(k) != v and v is not None}
        if update_fields:
            guideline_collection.update_one({"_id": existing["_id"]}, {"$set": update_fields})
            # logger.info(f"Updated document for {metadata.awmf_register_number}.")
        else:
            pass
            # logger.info(f"No changes detected for {metadata.awmf_register_number}.")
    else:
        result = guideline_collection.insert_one(document)
        # logger.info(f"Stored new document with id {result.inserted_id}.")

    return metadata

def run_guideline_downloader(pdf_output_folder, text_output_folder, file, guideline_collection):
    logger.info(f"Downloading pdfs listed in {file} ...")
    if not os.path.exists(file):
        raise FileNotFoundError(f"File {file} does not exist.")

    with open(file, 'r', encoding='utf-8') as json_file:
        metadata_entries = json.load(json_file)
        metadata_objects = [GuidelineMetadata.from_dict(entry) for entry in metadata_entries]

    updated_metadata = []
    failed = []

    logger.progress("Processing PDFs [PROGRESS]: ", 0, len(metadata_objects))
    for i, meta in enumerate(metadata_objects):
        updated = store_document(guideline_collection, meta, pdf_output_folder, text_output_folder)
        if updated:
            updated_metadata.append(updated)
        else:
            failed.append(meta.download_information.url if meta.download_information else "UNKNOWN")
        logger.progress("Processing PDFs [PROGRESS]", i + 1, len(metadata_objects))

    for url in failed:
        logger.error(f"Failed to process {url}")

    with open(file, "w", encoding="utf-8") as json_file:
        json.dump([m.as_dict() for m in updated_metadata], json_file, ensure_ascii=False, indent=2)

    return updated_metadata
