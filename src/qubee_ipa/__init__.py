"""Qubee-IPA-Converter: Oromo Qubee to IPA Conversion Library.

Developed by Feda Negesse
Speech and Text Computing Group
Department of Linguistics and Philology
Addis Ababa University
"""

from .core import qubee_to_ipa, convert_file, create_dictionary_from_corpus
from .rules import check_word_quality, flag_misspelled_word

__version__ = "0.1.0"
__author__ = "Feda Negesse"
__email__ = "feda.negesse@aau.edu.et"
__affiliation__ = "Speech and Text Computing Group, Department of Linguistics and Philology, Addis Ababa University"

__all__ = [
    "qubee_to_ipa",
    "convert_file",
    "create_dictionary_from_corpus",
    "check_word_quality",
    "flag_misspelled_word",
]
