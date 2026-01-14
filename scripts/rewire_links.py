from __future__ import annotations

import re
from pathlib import Path

import obsidiantools.api as otools
import os
from typing import Final


def find(filename: str) -> str:
    cwd: Final[str] = os.getcwd()

    for root, _, files in os.walk(cwd):
        if filename in files:
            absolute_path: str = os.path.join(root, filename)
            relative_path: str = os.path.relpath(absolute_path, cwd)
            return relative_path
    return filename

#    raise FileNotFoundError(f'File not found: {filename}')

ROOT = Path('guide-to-earendor')
SITE_PREFIX = '/anremithrl-s-guide-to-earendor'

vault = otools.Vault(ROOT).connect().gather()

# Build a map: note slug -> full relative path (as Path)
note_map: dict[str, Path] = {}
for raw_path in vault.md_file_index:
    # Ensure it's a Path object
    path = Path(find(raw_path)[18:-3])
    # Create a slug path relative to the vault root
    rel = path#.relative_to(ROOT).with_suffix('')
    slug = rel.as_posix()
    note_map[slug] = rel

# Regex for wiki-style links
WIKILINK = re.compile(r'\[\[([^|\]]+)(?:\|([^\]]+))?\]\]')

def resolve(target: str) -> str:
    """
    Resolve a wiki link target to a root-relative mkdocs URL.
    """
    # Normalize (lowercase and replace spaces with hyphens)
    key = target.strip().lower().replace(' ', '-')
    for slug in note_map:
        # Exact match on slug ending segment
        if slug.endswith('/' + key) or slug == key:
            return f'{SITE_PREFIX}/{slug}/'
    # Fallback: link to target slug at root
    return f'{SITE_PREFIX}/{key}/'

def rewrite_file(md: Path) -> None:
    text = md.read_text(encoding='utf-8')

    def repl(match):
        name = match.group(1)
        label = match.group(2) or name
        url = resolve(name)
        return f'[{label}]({url})'

    new_text = WIKILINK.sub(repl, text)
    if new_text != text:
        md.write_text(new_text, encoding='utf-8')

# Rewrite every markdown file
for md_file in ROOT.rglob('*.md'):
    rewrite_file(md_file)

