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

# ----------------------------------------------------------------------
# Build index: slug -> list of paths
# ----------------------------------------------------------------------

index: dict[str, list[Path]] = {}

for md in ROOT.rglob('*.md'):
    slug = slugify(md.stem)
    index.setdefault(slug, []).append(md)

# ----------------------------------------------------------------------
# Rewrite links
# ----------------------------------------------------------------------

def resolve(target: str, current: Path) -> str:
    slug = slugify(target)

    if slug not in index:
        # Leave unresolved links readable but inert
        return f'{SITE_PREFIX}/{slug}/'

    candidates = index[slug]

    # Prefer same directory or subdirectory
    for path in candidates:
        try:
            path.relative_to(current.parent)
            rel = path.relative_to(ROOT).with_suffix('')
            return f'{SITE_PREFIX}/{rel.as_posix()}/'
        except ValueError:
            continue

    # Fallback: first indexed occurrence
    rel = candidates[0].relative_to(ROOT).with_suffix('')
    return f'{SITE_PREFIX}/{rel.as_posix()}/'

def replace(match: re.Match[str], current: Path) -> str:
    target = match.group(1)
    label = match.group(2) or target
    url = resolve(target, current)
    return f'[{label}]({url})'

for md in ROOT.rglob('*.md'):
    content = md.read_text(encoding='utf-8')
    new = WIKILINK.sub(lambda m: replace(m, md), content)
    if new != content:
        md.write_text(new, encoding='utf-8')

