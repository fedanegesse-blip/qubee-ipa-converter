"""Command-line interface for qubee-ipa-converter."""

import argparse
from .core import convert_file, create_dictionary_from_corpus


def main():
    parser = argparse.ArgumentParser(
        description="Convert Oromo Qubee orthography to IPA phonemes",
        epilog="Example: qubee-to-ipa words.txt --output lexicon.txt"
    )
    
    parser.add_argument(
        "input",
        help="Input file (word list) or corpus directory"
    )
    parser.add_argument(
        "-o", "--output",
        default="lexicon.txt",
        help="Output dictionary file (default: lexicon.txt)"
    )
    parser.add_argument(
        "--corpus",
        action="store_true",
        help="Input is a corpus directory with .lab files"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Skip flagged (misspelled) words"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print debugging information"
    )
    
    args = parser.parse_args()
    
    if args.corpus:
        stats = create_dictionary_from_corpus(
            args.input,
            args.output,
            strict=args.strict,
            debug=args.debug
        )
    else:
        stats = convert_file(
            args.input,
            args.output,
            strict=args.strict,
            debug=args.debug
        )
    
    print(f"\n✅ Dictionary created!")
    print(f"   Valid entries: {stats['valid']}")
    print(f"   Flagged entries: {stats['flagged']}")
    print(f"   Total entries: {stats['total']}")
    print(f"   Output file: {stats['output_file']}")


if __name__ == "__main__":
    main()
