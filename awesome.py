'''
将预定义好的宏输出到 `notations/notations.sty`, `typora.json` 和 `anki.tex`。
'''

from string import ascii_letters
import json
from yaml import load, SafeLoader
from typing import Dict
from abc import ABC, abstractmethod
from os.path import exists
from os import makedirs
from copy import deepcopy

class Writer:
    def __init__(self, path: str, data: Dict):
        self.path = path
        self.data = data

    def __call__(self):
        with open(self.path, 'w') as f:
            self.output(f)

    @abstractmethod
    def output(self, f): pass

class LaTeXWriter(Writer):
    header = r"""\ProvidesPackage{awesome}
\RequirePackage{amsmath}
"""

    def output(self, f):
        f.write(self.header)
        for key, value in self.data.items():
            argc = value.count('#')
            argcpart = f'[{argc}]' if argc else ''
            f.write(f'\\providecommand{{\\key}}{argcpart}{{value}}\n')
            f.write(f'\\renewcommand{{\\key}}{argcpart}{{value}}\n')

class TyporaWriter(Writer):
    def output(self, f):
        def listize(value):
            argc = value.count('#')
            if argc: return [value, argc]
            else: return value
        data = {key: listize(value) for key, value in self.data.items()}
        json.dump(data, f)

class AnkiWriter(Writer):
    def output(self, f):
        for k, v in self.data.items():
            f.write('\def{%s}{%s}\n' % (k, v))

def preprocessor(raw: Dict):
    GREEK_LETTER: Dict[str, str] = raw['greek_letter']
    VAR: List[str] = raw['greek_letter_var']
    PREFIX = raw['prefix']
    data = raw['base']
    for letter in ascii_letters:
        data[f'{PREFIX["latin_boldsymbol"]}{letter}'] = f'\\boldsymbol {letter}'
        data[f'{PREFIX["latin_mathsf"]}{letter}'] = f'\\mathsf {letter}'
    for name, letter in GREEK_LETTER.items():
        data[f'{PREFIX["greek_"]}{letter}'] = f'\\{name}'
        data[f'{PREFIX["greek_boldsymbol"]}{letter}'] = f'\\boldsymbol \\{name}'
        data[f'{PREFIX["greek_mathsf"]}{letter}'] = f'\\mathsf \\{name}'
    for name in VAR:
        letter = GREEK_LETTER[name]
        data[f'{PREFIX["greek_"]}{letter}'] = f'\\var{name}'
        data[f'{PREFIX["greek_boldsymbol"]}{letter}'] = f'\\boldsymbol \\var{name}'
        data[f'{PREFIX["greek_mathsf"]}{letter}'] = f'\\mathsf \\var{name}'
    return data

with open('awesome.yaml') as f:
    AWESOME = preprocessor(load(f, Loader=SafeLoader))

if not exists('awesome'): makedirs('awesome')
LaTeXWriter('awesome/awesome.sty', AWESOME)()
TyporaWriter('typora.json', AWESOME)()
AnkiWriter('anki.tex', AWESOME)()
