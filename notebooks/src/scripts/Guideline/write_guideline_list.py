import json
import re
import shutil
import subprocess
import time
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from general.data_model.guideline_metadata import GuidelineMetadata, GuidelineDownloadInformation
from general.helper.logging import logger

def extract_guideline_metadata(driver, url) -> Optional[GuidelineMetadata]:
    try:
        # Navigate to the URL
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        # find the PDF URL
        download_element = wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Download')]"))
        )
        pdf_link = download_element.get_attribute('href')
        logger.note("Extracted link: %s", pdf_link)

        # find the contributing organization (primary / leading and other)
        def find_contained_organization_labels(col_label_text):
            # Helper: Wait until the label has a non-empty textContent
            def wait_for_text_content(label, timeout=10):
                wait.until(
                    lambda d: d.execute_script("return arguments[0].textContent.trim().length > 0;", label)
                )

            row_element = wait.until(
                EC.presence_of_element_located((
                    By.XPATH,
                    f"//ion-row[ion-col[1][contains(text(), '{col_label_text}')]]"
                ))
            )
            org_col = row_element.find_elements(By.XPATH, "./ion-col")[1]
            organisation_labels = org_col.find_elements(By.XPATH, ".//ion-label")
            organizations = []
            for label in organisation_labels:
                try:
                    wait_for_text_content(label)
                    text = label.get_attribute("textContent").strip()
                    if text:
                        organizations.append(text)
                except Exception as e:
                    logger.warning(f"Label unreadable for '{col_label_text}': {e}")

            return organizations
        leading_organizations, other_contributing_organizations = [], []
        try:
            leading_organizations += find_contained_organization_labels("Federführende Fachgesellschaft")
        except Exception as e:
            logger.warning(f"Could not extract leading organizations: {e}")
        # logger.note("Extracted the following leading organizations: %s", leading_organizations)
        try:
            other_contributing_organizations += find_contained_organization_labels("AWMF-Fachgesellschaft")
        except Exception as e:
            logger.warning(f"Could not extract other contributing AWMF organizations: {e}")
        try:
            other_contributing_organizations += find_contained_organization_labels("weiterer Fachgesellschaften")
        except Exception as e:
            logger.warning(f"Could not extract other contributing external organizations: {e}")
        # logger.note("Extracted the following other contributing organizations: %s", other_contributing_organizations)

        # find the keywords
        keywords = []
        def find_keywords(col_label_text="Schlüsselwörter"):
            row_element = wait.until(
                EC.presence_of_element_located((
                    By.XPATH,
                    f"//ion-row[ion-col[1][contains(text(), '{col_label_text}')]]"
                ))
            )
            content_col = row_element.find_elements(By.XPATH, "./ion-col")[1]
            wait.until(
                lambda d: d.execute_script("return arguments[0].textContent.trim().length > 0;", content_col)
            )
            full_text = content_col.get_attribute("textContent").strip()

            keywords = [kw.strip() for kw in full_text.split(",") if kw.strip()]
            return keywords
        try:
            keywords += find_keywords()
        except Exception as e:
            logger.warning(f"Could not extract keywords")
            # logger.warning(e)
        # logger.note("Extracted the following keywords: %s", keywords)

        return GuidelineMetadata(
            download_information=GuidelineDownloadInformation(url=pdf_link),
            leading_publishing_organizations=leading_organizations,
            other_contributing_organizations=other_contributing_organizations,
            keywords=keywords
        )

    except Exception as e:
        logger.error(f"An error occurred in extract_pdf_link for {url}: %s", e)
        return None


def find_guideline_sides(driver, url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 30)

        try:
            expected_text = WebDriverWait(driver, 10).until(
                lambda d: (t := d.find_element(By.XPATH, "//*[contains(text(), 'Treffer')]")).text.strip() or None
            )
            logger.info(f"Found Treffer text: '{expected_text}'")

            # Use regex to extract the first number in the text
            match = re.search(r"\d+", expected_text)
            if match:
                expected_number_guidelines = int(match.group())
            else:
                logger.error("Could not extract number of guidelines from Treffer text.")
                raise ValueError("Need to find guidelines")

        except Exception as e:
            logger.error("An error occurred in find_guideline_sides")
            raise e

        guideline_links = set()  # Use a set to avoid duplicates

        def scroll():
            element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,"#menu_content_container > app-tabs > ion-tabs > div > ion-router-outlet > app-suche > ion-content"))
            )
            # Access the shadow DOM to retrieve the scrollable element
            scrollable_element = driver.execute_script(
                "return arguments[0].shadowRoot.querySelector('main.inner-scroll.scroll-y');", element)

            prev_scroll_top = driver.execute_script("return arguments[0].scrollTop;", scrollable_element)
            driver.execute_script("arguments[0].scrollTop += 5000;", scrollable_element)
            time.sleep(2)  # Give time for new content to load
            new_scroll_top = driver.execute_script("return arguments[0].scrollTop;", scrollable_element)
            return new_scroll_top > prev_scroll_top

        # Scroll several times until no more new content is loaded.
        scroll_counter = 5
        while scroll_counter > 0:
            logger.note("Scrolling...")
            did_reveal_new_content = scroll()
            if not did_reveal_new_content:
                scroll_counter -= 1
            else:
                scroll_counter = 5  # Reset counter if new content is revealed

        # Get all the guideline side links using the provided XPath condition
        link_elements = driver.find_elements(By.XPATH, "//a[text() = @title]")
        for link_element in link_elements:
            guideline_side_link = link_element.get_attribute('href')
            guideline_links.add(guideline_side_link)  # Avoid duplicates

        logger.info("Expected: %d, Retrieved: %d", expected_number_guidelines, len(guideline_links))
        return list(guideline_links)

    except Exception as e:
        logger.error("An error occurred in find_guideline_sides: %s", e)
        return []

def setup():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    def ensure_chromedriver_installed():
        if shutil.which("chromedriver") is None:
            print("Installing chromedriver...")
            subprocess.run(["apt", "update"], check=True)
            subprocess.run(["apt", "install", "-y", "chromium-driver"], check=True)

    ensure_chromedriver_installed()
    webdriver_service = Service("/usr/bin/chromedriver")

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    logger.success("Chromedriver initialized")
    return driver

def close(driver):
    driver.quit()
    logger.success("Chromdriver canceled")

def run_guideline_finding(output_file, search_url):
    driver = setup()
    collected_metadata = []
    logger.info("Getting guideline page links from search")

    try:
        guideline_sides = find_guideline_sides(driver, search_url)

        count_added_links = 0
        logger.progress("Extracting pdf links [PROGRESS]: ", 0, len(guideline_sides))
        for i, guideline_side in enumerate(guideline_sides):
            metadata = extract_guideline_metadata(driver, guideline_side)
            if metadata:
                collected_metadata.append(metadata)
                count_added_links += 1
            logger.progress("Extracting pdf links [PROGRESS]", i + 1, len(guideline_sides))
    finally:
        close(driver)

    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump([g.as_dict() for g in collected_metadata], json_file, ensure_ascii=False, indent=2)

    logger.success(f"Wrote {count_added_links} pdf links to {output_file}")
    return collected_metadata
