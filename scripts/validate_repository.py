"""Validate this repository without importing tools or accessing user data."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def validate(root=ROOT):
    failures = []
    folders = sorted((root / 'skills').iterdir())
    for folder in folders:
        if not folder.is_dir():
            continue
        path = folder / 'SKILL.md'
        if not path.is_file():
            failures.append(f'{folder.name}: missing SKILL.md')
            continue
        text = path.read_text(encoding='utf-8')
        match = re.match(r'^---\nname: ([a-z0-9]+(?:-[a-z0-9]+)*)\ndescription: (.+)\n---\n', text)
        if not match or match.group(1) != folder.name:
            failures.append(f'{folder.name}: invalid name/frontmatter')
        if match and not 20 <= len(match.group(2)) <= 1024:
            failures.append(f'{folder.name}: description must be useful and bounded')
        if len(text.splitlines()) > 220 or '[TODO:' in text:
            failures.append(f'{folder.name}: unfinished or excessively long')
        interface = folder / 'agents' / 'openai.yaml'
        if not interface.exists():
            failures.append(f'{folder.name}: missing interface metadata')
        else:
            interface_text = interface.read_text(encoding='utf-8')
            for field in ('display_name', 'short_description', 'default_prompt'):
                found = re.search(rf'^  {field}: (".*")$', interface_text, re.M)
                if not found:
                    failures.append(f'{folder.name}: missing quoted {field}')
                    continue
                try:
                    value = json.loads(found.group(1))
                except ValueError:
                    failures.append(f'{folder.name}: invalid string in {field}')
                    continue
                if field == 'short_description' and not 25 <= len(value) <= 64:
                    failures.append(f'{folder.name}: short_description outside 25-64 characters')
                if field == 'default_prompt' and f'${folder.name}' not in value:
                    failures.append(f'{folder.name}: prompt does not invoke this skill')
        for relative in re.findall(r'`((?:scripts|references|assets)/[^`]+)`', text):
            if not (folder / relative).is_file():
                failures.append(f'{folder.name}: unresolved resource {relative}')
    for path in root.rglob('*'):
        if not path.is_file() or '.git' in path.parts or '__pycache__' in path.parts:
            continue
        if path.suffix.lower() in {'.wav', '.mp4', '.pdf', '.sqlite', '.jsonl'} or path.name.startswith('.env'):
            failures.append(f'{path.relative_to(root)}: private/binary artifact not allowed')
            continue
        text = path.read_text(encoding='utf-8')
        # Construct patterns from pieces so the checker does not flag itself.
        patterns = [r'\b' + 'sk' + r'-[A-Za-z0-9_-]{16,}', r'\b' + 'gh[pousr]' + r'_[A-Za-z0-9_]{16,}', 'github' + r'_pat_[A-Za-z0-9_]{16,}', 'C:' + r'[\\/]Users[\\/][^\s`]+']
        if any(re.search(pattern, text) for pattern in patterns):
            failures.append(f'{path.relative_to(root)}: potential secret or personal path')
    return failures


if __name__ == '__main__':
    issues = validate()
    print(json.dumps({'skills': len(list((ROOT / 'skills').glob('*/SKILL.md'))), 'errors': issues}, ensure_ascii=False, indent=2))
    sys.exit(bool(issues))
