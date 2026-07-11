"""Quality control rules for Oromo orthography."""

import re
from typing import Tuple, List


def flag_misspelled_word(word: str) -> Tuple[bool, List[str]]:
    """
    Check if a word violates Oromo orthographic rules.

    Based on the Oromo Qubee-IPA mapping table.

    Rules:
    1. No geminate at start: bb, tt, dd, kk, gg, mm, nn, rr, ff, ss, yy, ww, ll, jj, vv, zz
    2. No geminate at end: bb, tt, dd, kk, gg, mm, nn, rr, ff, ss, yy, ww, ll, jj, vv, zz
    3. No more than 2 consecutive vowels
    4. No more than 2 consecutive consonants
    5. No invalid vowel sequences (ae, au, etc.)
    6. No glottal stop at start

    Args:
        word: Oromo word in Qubee orthography

    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    word = word.lower().strip()
    issues = []

    # GEMINATES: doubled single consonants (NOT digraphs)
    geminate_patterns = ['bb', 'tt', 'dd', 'kk', 'gg', 'mm', 'nn', 'rr', 'ff', 'ss', 'yy', 'ww', 'll', 'jj', 'vv', 'zz']

    # Rule 1: No geminate at start
    for g in geminate_patterns:
        if word.startswith(g):
            issues.append("starts with geminate")
            break

    # Rule 2: No geminate at end
    for g in geminate_patterns:
        if word.endswith(g):
            issues.append("ends with geminate")
            break

    # Rule 3: No more than 2 consecutive vowels
    if re.search(r'[aeiou]{3,}', word):
        issues.append("has more than 2 consecutive vowels")

    # Rule 4: No more than 2 consecutive consonants
    if re.search(r'([b-df-hj-np-tv-z])\1{2,}', word):
        issues.append("has more than 2 consecutive consonants")

    # Rule 5: No invalid vowel sequences
    valid_long_vowels = ['aa', 'ee', 'ii', 'oo', 'uu']
    invalid_sequences = ['ae', 'ao', 'au', 'ea', 'eo', 'eu', 'ia', 'ie', 'io', 'oa', 'oe', 'oi', 'ua', 'ue', 'ui']

    if re.search(r'[aeiou][aeiou]', word):
        vowel_pairs = re.findall(r'[aeiou]{2}', word)
        for pair in vowel_pairs:
            if pair not in valid_long_vowels:
                issues.append(f"has invalid vowel sequence '{pair}'")
                break

    for seq in invalid_sequences:
        if seq in word:
            issues.append(f"has invalid vowel sequence '{seq}'")
            break

    # Rule 6: No glottal stop at start
    if word.startswith("'"):
        issues.append("starts with glottal stop")

    is_valid = len(issues) == 0
    return is_valid, issues


def check_word_quality(word: str) -> Tuple[bool, List[str]]:
    """
    Comprehensive word quality check with additional validation.

    Args:
        word: Word to check

    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    word = word.strip().lower()

    if not word:
        return False, ["empty word"]

    if not re.match(r'^[a-z\']+$', word):
        return False, ["contains non-Oromo characters"]

    return flag_misspelled_word(word)
