#!../.venv/bin/python

import os
import langcodes
from functional import seq

class Converter:
    src_lang_key = "en"

    def __init__(self, src_lang: str):
       src_lang_key = src_lang

    def _open_csv(self, path: str):
        with open(path, 'r') as f:
            return (path, [lines.strip() for lines in f.readlines()])

    def _get_langcode(self, filename: str, default: str):
        try:
            return langcodes.find(filename).language
        except:
            print("Could not find code for " + filename)
            return default

    def _cols_by_lang(self, path_rows: tuple):
        (path, rows) = path_rows
        src_lang_terms = seq(rows).map(lambda cols: cols[0])
        tgt_lang_terms = seq(rows).map(lambda cols: cols[1])
        filename = os.path.basename(path)
        tgt_lang_key = self._get_langcode(filename, filename)
        return {self.src_lang_key: src_lang_terms,
                tgt_lang_key: tgt_lang_terms}


    def convert(self, output_file: str, *input_files: str):
        file_contents = (seq(*input_files)
                        .map(self._open_csv)
                        .map(lambda path_lines: (path_lines[0], [line.split(",", 1) for line in path_lines[1]]))
                        .map(self._cols_by_lang))

        print(file_contents)
        # glossaries = reduce(lambda glossary, row: glossary.append(row[0], row[1]), file_contents, dict())
