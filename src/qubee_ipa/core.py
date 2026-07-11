"""Core conversion logic for Oromo Qubee to IPA."""

import re
import os
from collections import OrderedDict
from typing import Tuple, List, Dict

from .rules import check_word_quality

# ============================================
# OROMO QUBEE TO IPA MAPPING
# ============================================

GRAPHEME_TO_IPA = OrderedDict([
    # Geminated digraphs (must come first for proper processing)
    ('nyn', 'ɲː'), ('nny', 'ɲː'),
    ('shsh', 'ʃː'), ('ssh', 'ʃː'),
    ('chch', 'tʃː'), ('cch', 'tʃː'),
    ('dhdh', 'ɗː'), ('ddh', 'ɗː'),
    ('phph', 'pʼː'), ('pph', 'pʼː'),
    # Consonants - Digraphs
    ('ny', 'ɲ'), ('sh', 'ʃ'), ('ch', 'tʃ'), ('dh', 'ɗ'), ('ph', 'pʼ'),
    # Geminated consonants
    ('xx', 'tʼː'), ('qq', 'kʼː'), ('cc', 'tʃʼː'),
    ('bb', 'bː'), ('tt', 'tː'), ('dd', 'dː'), ('kk', 'kː'), ('gg', 'gː'),
    ('mm', 'mː'), ('nn', 'nː'), ('rr', 'rː'), ('ff', 'fː'), ('ss', 'sː'),
    ('yy', 'jː'), ('ww', 'wː'), ('ll', 'lː'), ('jj', 'dʒː'), ('vv', 'vː'), ('zz', 'zː'),
    # Single consonants
    ('b', 'b'), ('t', 't'), ('d', 'd'), ('k', 'k'), ('g', 'g'),
    ("'", 'ʔ'),
    ('m', 'm'), ('n', 'n'), ('r', 'r'), ('f', 'f'), ('s', 's'),
    ('y', 'j'), ('w', 'w'), ('l', 'l'), ('j', 'dʒ'), ('h', 'h'),
    ('v', 'v'), ('z', 'z'),
    # Ejectives
    ('c', 'tʃʼ'), ('x', 'tʼ'), ('q', 'kʼ'),
    # Long vowels
    ('aa', 'aː'), ('ee', 'eː'), ('ii', 'iː'), ('oo', 'oː'), ('uu', 'uː'),
    # Short vowels
    ('a', 'a'), ('e', 'e'), ('i', 'i'), ('o', 'o'), ('u', 'u'),
])


def qubee_to_ipa(word: str, strict: bool = False, debug: bool = False) -> Tuple[str, bool, List[str]]:
    """
    Convert an Oromo Qubee word to its IPA phoneme sequence.

    Args:
        word: Oromo word in Qubee orthography
        strict: If True, skip words with quality issues
        debug: If True, print debugging information

    Returns:
        Tuple of (ipa_string, is_valid, issues_list)
    """
    word = word.strip().lower()
    if not word:
        return "", False, ["empty word"]

    # Check quality first
    is_valid, issues = check_word_quality(word)

    if strict and not is_valid:
        return "", False, issues

    phonemes = []
    i = 0
    length = len(word)

    while i < length:
        matched = False
        sorted_keys = sorted(GRAPHEME_TO_IPA.keys(), key=len, reverse=True)

        for grapheme in sorted_keys:
            if word[i:i + len(grapheme)] == grapheme:
                phonemes.append(GRAPHEME_TO_IPA[grapheme])
                i += len(grapheme)
                matched = True
                break

        if not matched:
            char = word[i]
            if debug:
                print(f"Warning: Unknown character '{char}' in word '{word}' at position {i}")
            phonemes.append('?')
            i += 1

    return ' '.join(phonemes), is_valid, issues


def convert_file(wordlist_path: str, output_path: str, strict: bool = False, debug: bool = False) -> Dict:
    """
    Convert a word list file to a pronunciation dictionary.

    Args:
        wordlist_path: Path to file with one word per line
        output_path: Path to output dictionary file
        strict: If True, skip flagged words
        debug: If True, print debugging information

    Returns:
        Dictionary with statistics: {'valid': int, 'flagged': int, 'total': int}
    """
    valid_count = 0
    flagged_count = 0

    with open(output_path, 'w', encoding='utf-8') as f_out:
        f_out.write("# Oromo Pronunciation Dictionary\n")
        f_out.write("# Generated using qubee-ipa-converter\n")
        f_out.write("# Words flagged with '#' have potential issues\n\n")

        with open(wordlist_path, 'r', encoding='utf-8') as f_in:
            for line in f_in:
                word = line.strip()
                if not word:
                    continue

                ipa, is_valid, issues = qubee_to_ipa(word, strict=strict, debug=debug)

                if not is_valid and strict:
                    continue

                if not is_valid:
                    flagged_count += 1
                    issues_str = ", ".join(issues)
                    f_out.write(f"# {word}\t{ipa}  # FLAG: {issues_str}\n")
                    if debug:
                        print(f"FLAGGED: '{word}' - {issues_str}")
                else:
                    valid_count += 1
                    f_out.write(f"{word}\t{ipa}\n")

    return {
        'valid': valid_count,
        'flagged': flagged_count,
        'total': valid_count + flagged_count,
        'output_file': output_path
    }


def create_dictionary_from_corpus(corpus_dir: str, output_path: str, strict: bool = False, debug: bool = False) -> Dict:
    """
    Create a pronunciation dictionary from a corpus directory with .lab files.

    Args:
        corpus_dir: Path to corpus directory containing .lab files
        output_path: Path to output dictionary file
        strict: If True, skip flagged words
        debug: If True, print debugging information

    Returns:
        Dictionary with statistics
    """
    word_set = set()

    # Collect all words from .lab files
    for root, dirs, files in os.walk(corpus_dir):
        for file in files:
            if file.endswith('.lab'):
                lab_path = os.path.join(root, file)
                try:
                    with open(lab_path, 'r', encoding='utf-8') as f:
                        text = f.read().strip().lower()
                        words = re.findall(r"[a-z']+", text)
                        word_set.update(words)
                except Exception as e:
                    print(f"Error reading {lab_path}: {e}")

    print(f"Found {len(word_set)} unique words in corpus")

    # Write the dictionary
    valid_count = 0
    flagged_count = 0

    with open(output_path, 'w', encoding='utf-8') as f_out:
        f_out.write("# Oromo Pronunciation Dictionary\n")
        f_out.write(f"# Generated from corpus: {corpus_dir}\n")
        f_out.write("# Words flagged with '#' have potential issues\n\n")

        for word in sorted(word_set):
            ipa, is_valid, issues = qubee_to_ipa(word, strict=strict, debug=debug)

            if not is_valid and strict:
                continue

            if not is_valid:
                flagged_count += 1
                issues_str = ", ".join(issues)
                f_out.write(f"# {word}\t{ipa}  # FLAG: {issues_str}\n")
                if debug:
                    print(f"FLAGGED: '{word}' - {issues_str}")
            else:
                valid_count += 1
                f_out.write(f"{word}\t{ipa}\n")

    return {
        'valid': valid_count,
        'flagged': flagged_count,
        'total': valid_count + flagged_count,
        'output_file': output_path
    }
