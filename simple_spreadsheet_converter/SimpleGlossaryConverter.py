#!/usr/bin/env python3
"""`simple_spreadsheet_converter is a module which` converts a simple
collection of bilingual CSV glossaries into a consolidated TBX-Basic
file."""

import os
import re
import langcodes
from functional import seq
from .TBXBasicWriter import TBXBasicWriter


class SimpleGlossaryConverter:

    """`SimpleGlossaryConverter` class for converting multiple bilingual CSV
    glossaries into a single TBX-Basic file.

    Input assumptions:
    - It is assumed that each CSV uses the same source language in column 1.
    - The language code for the source language is passed to the constructor.
      - If the language is given (e.g., "English"), an attempt at auto-finding
        the appropriate IETF language code will be made.
      - If an IETF language code is given, it will be used as-is.
    - Language codes for target languages are taken from the CSV file names:

        ("Spanish.csv" -> "sp")

    """

    def __init__(self, src_lang: str):
        self.src_lang_key = (src_lang if langcodes.tag_is_valid(src_lang)
                             else self.get_langcode(src_lang, src_lang))

    def _get_rows_from_csv(self, path: str):
        with open(path, 'r', encoding='utf-8') as f:
            return (path, [lines.strip() for lines in f.readlines()])

    def _split_to_cols(self, path_rows: tuple):
        return (path_rows[0], [row.split(",", 1) for row in path_rows[1]])

    def _cols_by_lang(self, path_rows: tuple):
        (path, rows) = path_rows
        filename = os.path.basename(path)
        tgt_lang_key = self.get_langcode(filename, filename)
        return (seq(rows)
                .map(lambda cols: {cols[0]: cols[1]})
                .reduce(lambda agg, entry: agg.update(entry) or agg,
                        {"_tgt": tgt_lang_key}))

    def _consolidate_glossary(self, agg: dict, sub_gloss: dict):
        tgt = sub_gloss["_tgt"]
        sub_gloss.pop("_tgt")
        for (src_term, tgt_term) in sub_gloss.items():
            agg.update({src_term: [*agg.get(src_term, []), (tgt, tgt_term)]})
        return agg

    def get_langcode(self, lang_candidate: str, default: str):
        """Attempt to get a language code from a language candidate. If it
        fails it returns the value of `default`.
        """
        result = langcodes.find(lang_candidate)

        if result is None:
            print("Could not find code for " + lang_candidate)
            return default

        lang = result.language
        rmatch = re.search(r'\((\w+?)\)', lang_candidate)
        rgroups = rmatch.groups() if rmatch else None
        if rgroups is None:
            print("Could not find region name for " + lang_candidate)
            return lang

        region = rgroups[0]
        return lang + '-' + region

    def convert(self, output_file: str, *input_files: str):
        """Convert one or more bilingual CSV glossaries to TBX-Basic."""
        contents_by_src = (seq(*input_files)
                           .map(self._get_rows_from_csv)
                           .map(self._split_to_cols)
                           .map(self._cols_by_lang)
                           .reduce(self._consolidate_glossary, {}))

        flattend_contents = (seq(contents_by_src.items())
                             .map(lambda kvp: [(self.src_lang_key, kvp[0]), *kvp[1]]))

        tbx_writer = TBXBasicWriter(self.src_lang_key,
                                    flattend_contents,
                                    [os.path.basename(f) for f in input_files])
        tbx_writer.write(output_file)
