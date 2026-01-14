from __future__ import annotations

from pathlib import Path
import re

from obsidiantools.api import Vault

ROOT = Path('guide-to-earendor')
SITE_PREFIX = '/anremithrl-s-guide-to-earendor'

vault = Vault(str(ROOT)).connect()

# Map: (source_path, target_name) -> target_path
resolution: dict[tuple[Path, str], Path] = {}

for link in vault.links:
    src = Path(link.source.path)
    tgt = Path(link.target.path)
    resolution[(src, link.target.name)] = tgt

WIKILINK = re.compile(r'\[\[([^|\]]+)(?:\|([^\]]+))?\]\]')

def rewrite(md: Path) -> None:
    content = md.read_text(encoding='utf-8')

    def replace(match: re.Match[str]) -> str:
        target = match.group(1)
        label = match.group(2) or target

        key = (md, target)
        if key not in resolution:
            return label  # inert fallback

        tgt = resolution[key].relative_to(ROOT).with_suffix('')
        return f'[{label}]({SITE_PREFIX}/{tgt.as_posix()}/)'

    new = WIKILINK.sub(replace, content)
    if new != content:
        md.write_text(new, encoding='utf-8')

for md in ROOT.rglob('*.md'):
    rewrite(md)

