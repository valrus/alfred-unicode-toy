from collections import defaultdict, Counter
from string import punctuation
import io
import re
import sys
import unicodedata


COLLECTIONS = [
    "FULLWIDTH",
    "MATHEMATICAL BOLD",
    "MATHEMATICAL ITALIC",
    "MATHEMATICAL BOLD ITALIC",
    "MATHEMATICAL SCRIPT",
    "MATHEMATICAL BOLD SCRIPT",
    "MATHEMATICAL FRAKTUR",
    "MATHEMATICAL DOUBLE-STRUCK",
    "MATHEMATICAL BOLD FRAKTUR",
    "MATHEMATICAL SANS-SERIF",
    "MATHEMATICAL SANS-SERIF BOLD",
    "MATHEMATICAL SANS-SERIF ITALIC",
    "MATHEMATICAL SANS-SERIF BOLD ITALIC",
    "MATHEMATICAL MONOSPACE",
    "GREEK",
    "MATHEMATICAL BOLD",
    "MATHEMATICAL ITALIC",
    "MATHEMATICAL BOLD ITALIC",
    "MATHEMATICAL SANS-SERIF BOLD",
    "MATHEMATICAL SANS-SERIF BOLD ITALIC",
    "CYRILLIC",
]


def to_unistr(code_points):
    return ''.join([chr(int(code_point, 16)) for code_point in code_points.split()])


def extract_latin_letter(char):
    if len(char) > 1:
        return None

    latin_letter_match = re.search('LATIN (SMALL|CAPITAL) LETTER [a-zA-Z]', unicodedata.name(char))
    if latin_letter_match:
        return unicodedata.lookup(latin_letter_match.group(0))
    else:
        return None


def load_confusables(confusables_file):
    confusables = defaultdict(set)
    for line in io.open(confusables_file, encoding='utf-8-sig'):
        line = line.strip()
        if line.startswith('#') or not line:
            continue
        parts = line.split(';')
        target = to_unistr(parts[1])
        try:
            target.encode('ascii')
        except UnicodeEncodeError:
            modified_latin_letter = extract_latin_letter(target)
            if modified_latin_letter:
                confusables[modified_latin_letter].add(target)
            continue
        else:
            if len(target) > 1:
                target = target.translate({p: None for p in punctuation})
            if len(target) > 1:
                continue
        confusables[target].add(to_unistr(parts[0]))
    return confusables


def accumulate_from(iterable):
    accumulator = []
    for i in iterable:
        accumulator.append(i)
        yield accumulator


def collect_confusables(confusables):
    possible_set_names = Counter()
    for target, alternates in confusables.items():
        for alternate in alternates:
            alternate_name_words = unicodedata.name(alternate).split()
            possible_set_names.update([ ' '.join(phrase) for phrase in accumulate_from(alternate_name_words) ])
    return { name: count for name, count in possible_set_names.items() if count > 26 }


def main():
    confusables = load_confusables('confusables.txt')
    print(collect_confusables(confusables))


if __name__ == '__main__':
    sys.exit(main())
