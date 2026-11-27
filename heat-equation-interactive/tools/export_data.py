#!/usr/bin/env python3
"""Export the split Chapter 11 registration files as a conventional JSON dataset."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read_dataset():
    folder = ROOT / 'docs/assets/data/chapter-11'
    template = (ROOT / 'src/template.html').read_text(encoding='utf-8')
    paths = re.findall(r'<script src="(assets/data/chapter-11/[^\"]+)"></script>', template)
    result = None
    for rel in paths:
        raw = (ROOT / 'docs' / rel).read_text(encoding='utf-8').strip()
        key, payload = raw.split(' = ', 1)
        value = json.loads(payload.removesuffix(';'))
        if key == 'window.chapter11Data':
            if result is not None: raise ValueError('Repeated initialization')
            result = value
        elif key.startswith('window.chapter11Data.original['):
            result['original'][json.loads(key[len('window.chapter11Data.original['):-1])] = value
        elif key.startswith('window.chapter11Data['):
            result[json.loads(key[len('window.chapter11Data['):-1])] = value
        else:
            raise ValueError(f'Unexpected dataset assignment in {rel}')
    if result is None: raise ValueError('Missing dataset')
    return result

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('output', type=Path, nargs='?', default=Path('numerical_investigations_v3_3.json'))
    args=p.parse_args()
    args.output.write_text(json.dumps(read_dataset(),separators=(',',':'),ensure_ascii=False),encoding='utf-8')
    print(f'Exported {args.output}')
