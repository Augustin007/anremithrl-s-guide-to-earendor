from pathlib import Path
import re
import obsidiantools.api as otools

ROOT = Path('guide-to-earendor')
SITE_PREFIX = '/anremithrl-s-guide-to-earendor'

vault = otools.Vault(ROOT).connect().gather()

WIKILINK = re.compile(r'\[\[([^|\]]+)(?:\|([^\]]+))?\]\]')

# Build a mapping from file path to its slugified output directory
note_map = {}
for path, data in vault.md_file_index.items():  # note: md_file_index maps Path->metadata
    slug = path.relative_to(ROOT).with_suffix('')
    note_map[path] = slug.as_posix()

def resolve_link(source_path: Path, target_name: str) -> str:
    """
    Given a source file and the name of a link in its text,
    use the vault's graph to resolve to a target path (if it exists).
    """
    # Look up the actual target file directly if possible
    # vault.md_file_index keys are full Paths
    for path in vault.md_file_index:
        if path.stem.lower() == target_name.lower():
            return f'{SITE_PREFIX}/{note_map[path]}/'
    # Fallback: render the label as inert
    return f'{SITE_PREFIX}/{target_name.lower()}/'

def rewrite_file(md: Path) -> None:
    text = md.read_text(encoding='utf-8')
    def repl(m):
        label = m.group(2) or m.group(1)
        url = resolve_link(md, m.group(1))
        return f'[{label}]({url})'
    new_text = WIKILINK.sub(repl, text)
    if new_text != text:
        md.write_text(new_text, encoding='utf-8')

for md_file in ROOT.rglob('*.md'):
    rewrite_file(md_file)

