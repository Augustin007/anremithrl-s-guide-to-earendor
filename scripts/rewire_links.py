from __future__ import annotations

import re
from pathlib import Path

ROOT = Path('guide-to-earendor')

SITE_PREFIX = '/anremithrl-s-guide-to-earendor'

WIKILINK = re.compile(r'\[\[([^|\]]+)(?:\|([^\]]+))?\]\]')

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'[^a-z0-9\-]', '', text)
    return text

def replace(match: re.Match[str]) -> str:
    target = match.group(1)
    label = match.group(2) or target
    slug = slugify(target)
    return f'[{label}]({SITE_PREFIX}/{slug}/)'

for md in ROOT.rglob('*.md'):
    content = md.read_text(encoding='utf-8')
    new = WIKILINK.sub(replace, content)
    if new != content:
        md.write_text(new, encoding='utf-8')

