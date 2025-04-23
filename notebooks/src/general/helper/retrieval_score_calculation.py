# general/helper/retrieval_score_calculation.py

import copy
import re
from typing import List, Tuple

from general.data_model.question_dataset import ExpectedAnswer
from general.data_model.system_interactions import RetrievalEntry
from general.helper.logging import logger


def normalize(text: str) -> str:
    norm = re.sub(r'[\s\-•]+', ' ', text.strip())
    return norm

def longest_common_substring(s1: str, s2: str) -> Tuple[str, str]:
    """
    Finds the longest common substring between s1 and s2.

    Returns:
        - the longest common substring
        - start index in s1
        - end index in s1
        - start index in s2
        - end index in s2
    """
    m, n = len(s1), len(s2)
    lcs_in_s1, lcs_in_s2 = None, None
    max_len = -1

    for i in range(m):
        for j in range(n):
            if s1[i] == s2[j]:
                current_s1, current_s2, k_i, k_j = s1[i], s2[j], 1, 1
                while True:
                    if i+k_i >= m or j+k_j >= n:
                        break
                    if s1[i+k_i] != s2[j+k_j]:
                        if s1[i+k_i] == ' ':
                            current_s1 += s1[i+k_i]
                            k_i += 1
                            continue
                        if s2[j+k_j] == ' ':
                            current_s2 += s2[j+k_j]
                            k_j += 1
                            continue
                        break
                    else:
                        current_s1 += s1[i+k_i]
                        current_s2 += s2[j+k_j]
                        k_i += 1
                        k_j += 1
                if len(current_s1) > max_len:
                    lcs_in_s1, lcs_in_s2, max_len = current_s1, current_s2, len(current_s1)

    logger.debug(
        f"Longest substring between \n -> {s1} \nand \n -> {s2}\n= '{lcs_in_s1}'\n"
    )

    return lcs_in_s1, lcs_in_s2

def find_and_remove_substring(s1: str, s2: str, removal_s1: str, removal_s2: str) -> Tuple[bool, str, str]:
    if (s1.find(removal_s1) == -1) or (s2.find(removal_s2) == -1):
        return False, s1, s2
    else:
        s1 = s1.replace(removal_s1, '')
        s2 = s2.replace(removal_s2, '')
        return True, s1, s2

def create_retrieval_scores(
        expected_retrieval: List[ExpectedAnswer],
        actual_retrieval: List[RetrievalEntry]
):
    logger.info("Starting retrieval evaluation with number of expected entries [{len(expected_retrieval)}] and number of actual entries [{len(actual_retrieval)}] ...")
    logger.debug(f"Expected entries: {[(er.guideline.awmf_register_number, er.text) for er in expected_retrieval]}")
    logger.debug(f"Retrieved entries: {[(ar.guideline.awmf_register_number, ar.text) for ar in actual_retrieval]}")

    normalized_expected_retrieval, normalized_actual_retrieval = copy.deepcopy(expected_retrieval), copy.deepcopy(actual_retrieval)

    for er in normalized_expected_retrieval:
        er.text = normalize(er.text)

    for ar in normalized_actual_retrieval:
        ar.text = normalize(ar.text)

    original_lengths_expected = [len(er.text) for er in normalized_expected_retrieval]
    original_lengths_actual = [len(ar.text) for ar in normalized_actual_retrieval]
    partial_tp_expected = [0] * len(normalized_expected_retrieval)
    partial_fn_expected = [0] * len(normalized_expected_retrieval)
    partial_tp_actual = [0] * len(normalized_actual_retrieval)
    partial_fp_actual = [0] * len(normalized_actual_retrieval)

    substrings = []
    for i_er, er in enumerate(normalized_expected_retrieval):
        for i_ar, ar in enumerate(normalized_actual_retrieval):
            if er.guideline.awmf_register_number != ar.guideline.awmf_register_number:
                continue
            lcs_er, lcs_ar = longest_common_substring(er.text, ar.text)
            if lcs_er is not None:
                substrings.append({
                    "er_index": i_er,
                    "ar_index": i_ar,
                    "er_lcs": lcs_er,
                    "ar_lcs": lcs_ar,
                })

    for sub in sorted(substrings, key=lambda x: len(x['er_lcs']), reverse=True):
        i_er, i_ar, lcs_er, lcs_ar = sub["er_index"], sub["ar_index"], sub["er_lcs"], sub["ar_lcs"]
        logger.info(f"For expected[{i_er}], actual[{i_ar}] -> substring: '{lcs_er}' of length {len(lcs_er)}")

        found, normalized_expected_retrieval[i_er].text, normalized_actual_retrieval[i_ar].text = find_and_remove_substring(normalized_expected_retrieval[i_er].text, normalized_actual_retrieval[i_ar].text, lcs_er, lcs_ar)
        if found:
            partial_tp_expected_value = len(lcs_er) / original_lengths_expected[i_er]
            partial_tp_actual_value = len(lcs_ar) / original_lengths_actual[i_ar]
            partial_tp_expected[i_er] += partial_tp_expected_value
            partial_tp_actual[i_ar] += partial_tp_actual_value

            logger.info(f" - Partial TP for expected: {len(lcs_er)} / {original_lengths_expected[i_er]} = {partial_tp_expected_value} --> Now at value {partial_tp_expected[i_er]} for the expected entry")
            logger.info(f" - Partial TP for retrieved: {len(lcs_ar)} / {original_lengths_actual[i_ar]} = {partial_tp_actual_value} --> Now at value {partial_tp_actual[i_ar]} for the retrieved entry")
        else:
            logger.info(f" - Skipped")

    for i_er, er in enumerate(normalized_expected_retrieval):
        if len(er.text) > 0:
            partial_fn_expected[i_er] = len(er.text) / original_lengths_expected[i_er]
            logger.info(f"[Expected {i_er}]  partial TP: {partial_tp_expected[i_er]:.2f}; partial FN {partial_fn_expected[i_er]:.2f} (should be {(1-partial_tp_expected[i_er]):.2f})")
    for i_ar, ar in enumerate(normalized_actual_retrieval):
        if len(ar.text) > 0:
            partial_fp_actual[i_ar] = len(ar.text) / original_lengths_actual[i_ar]
            logger.info(f"[Actual   {i_ar}]  partial TP: {partial_tp_actual[i_ar]:.2f}; partial FP {partial_fp_actual[i_ar]:.2f} (should be {(1-partial_tp_actual[i_ar]):.2f})")

    tp_retrieval = sum(partial_tp_actual)
    tp_expectation = sum(partial_tp_expected)
    fp = sum(partial_fp_actual)
    fn = sum(partial_fn_expected)

    precision = tp_retrieval / (tp_retrieval + fp) if tp_retrieval + fp > 0 else 0.0
    recall = tp_expectation / (tp_expectation + fn) if tp_expectation + fn > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0.0
    logger.info(
        f"""Summed results:
        [Expected ] TP: {tp_expectation:.2f}, FN: {fn:.2f}, max possible: {len(partial_tp_expected)}
        [Actual   ] TP: {tp_retrieval:.2f}, FP: {fp:.2f}, max possible: {len(partial_tp_actual)}
        [Return   ] Precision: {precision}, Recall: {recall}, F1: {f1}
        """
    )
    return precision, recall, f1