#!/usr/bin/env python3
"""Install and update Atlas without a persistent checkout or external packages."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tarfile
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import zipfile

REPOSITORY = 'DevelopingMedo/atlas'
STATE = '.atlas-install.json'
PAYLOAD = 'skills/atlas/assets/package.zip'
BEGIN = '<!-- atlas:begin -->\n'
END = '<!-- atlas:end -->'
SKILL = 'skills/atlas/'
REQUIRED = ['AGENTS.md', 'SUBAGENTS.md', 'LICENSE', 'atlas.json.example',
            'commands/atlas.md', 'commands/setup-atlas.md', SKILL + 'SKILL.md',
            SKILL + 'scripts/atlas.py', SKILL + 'references/model-setup.md']
ROLES = ['Analyze', 'Auto', 'Build', 'Develop', 'Orchestrate', 'Plan', 'Review', 'Run']
GUIDES = ['ARTIFACTS', 'MCP', 'PLANNING', 'REPOSITORIES']
REQUIRED += ['agents/' + name + '.md' for name in ROLES]
REQUIRED += ['guide/' + name + '.md' for name in GUIDES]


class AtlasError(Exception):
    pass


def digest(data):
    return hashlib.sha256(data).hexdigest() if data is not None else None


def safe_path(name):
    path = PurePosixPath(name)
    if not name or path.is_absolute() or '..' in path.parts or '\\' in name or ':' in name:
        raise AtlasError('Unsafe package path: ' + name)
    return path


def target_path(root, name):
    safe_path(name)
    path = root / name
    for parent in [path, *path.parents]:
        if parent == root.parent:
            break
        if parent.is_symlink():
            raise AtlasError('Symlink at installation path: ' + str(parent))
    return path


def read_optional(path):
    if path.exists() and not path.is_file():
        raise AtlasError('Expected a file: ' + str(path))
    return path.read_bytes() if path.exists() else None


def request(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Atlas-Installer',
                                             'Accept': 'application/vnd.github+json'})
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read(8 * 1024 * 1024 + 1)
        if len(data) > 8 * 1024 * 1024:
            raise AtlasError('Package exceeds 8 MiB.')
        return data
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        raise AtlasError('GitHub request failed (HTTP %s).' % error.code) from error
    except OSError as error:
        raise AtlasError('Download failed: ' + str(error)) from error


def resolve_ref(ref):
    if not ref or ref.startswith('-') or re.search(r'[\s~^:?*\[\\]', ref):
        raise AtlasError('Expected a branch or version, for example opencode or v1.0.0.')
    matches = []
    for kind in ('heads', 'tags'):
        data = request('https://api.github.com/repos/%s/git/ref/%s/%s' %
                       (REPOSITORY, kind, urllib.parse.quote(ref, safe='')))
        if data is not None:
            obj = json.loads(data)['object']
            for _ in range(5):
                if obj['type'] != 'tag':
                    break
                tag = request('https://api.github.com/repos/%s/git/tags/%s' % (REPOSITORY, obj['sha']))
                obj = json.loads(tag)['object']
            if obj['type'] != 'commit' or not re.fullmatch(r'[0-9a-f]{40}', obj['sha']):
                raise AtlasError('Source does not identify a commit.')
            matches.append(obj['sha'])
    if len(matches) != 1:
        raise AtlasError('Unknown or ambiguous branch/version: ' + ref)
    return matches[0]


def collect_files(read):
    files = {}
    for name in REQUIRED:
        data = read(name)
        if data is None:
            raise AtlasError('Incomplete Atlas source; missing ' + name)
        files[name if name != 'LICENSE' else SKILL + 'LICENSE'] = data
    return files


def local_package(source, ref):
    source = Path(source).resolve()
    revision = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    files = collect_files(lambda name: read_optional(target_path(source, name)))
    return {'ref': ref, 'commit': revision, 'files': files}


def download_package(ref):
    revision = resolve_ref(ref)
    data = request('https://api.github.com/repos/%s/tarball/%s' % (REPOSITORY, revision))
    if data is None:
        raise AtlasError('Source archive is unavailable.')
    files = {}
    with tarfile.open(fileobj=io.BytesIO(data), mode='r:gz') as archive:
        for member in archive.getmembers():
            parts = PurePosixPath(member.name).parts
            if len(parts) < 2:
                continue
            name = '/'.join(parts[1:])
            if name not in REQUIRED:
                continue
            safe_path(name)
            if not member.isfile() or member.size > 1024 * 1024 or name in files:
                raise AtlasError('Invalid archive member: ' + name)
            files[name] = archive.extractfile(member).read()
    return {'ref': ref, 'commit': revision, 'files': collect_files(files.get)}


def encode_package(package):
    manifest = {'format': 1, 'ref': package['ref'], 'commit': package['commit'],
                'files': {name: digest(data) for name, data in sorted(package['files'].items())}}
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(package['files'].items()):
            archive.writestr(zipfile.ZipInfo(name), data)
        archive.writestr(zipfile.ZipInfo('manifest.json'), json.dumps(manifest, indent=2) + '\n')
    return stream.getvalue()


def decode_package(data):
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        if len(set(archive.namelist())) != len(archive.namelist()):
            raise AtlasError('Duplicate package entries.')
        if sum(info.file_size for info in archive.infolist()) > 8 * 1024 * 1024:
            raise AtlasError('Expanded package exceeds 8 MiB.')
        manifest = json.loads(archive.read('manifest.json'))
        if manifest.get('format') != 1 or not re.fullmatch(r'[0-9a-f]{40}', manifest['commit']):
            raise AtlasError('Unsupported package manifest.')
        files = {}
        allowed = {name if name != 'LICENSE' else SKILL + 'LICENSE' for name in REQUIRED}
        if set(manifest['files']) != allowed or set(archive.namelist()) != allowed | {'manifest.json'}:
            raise AtlasError('Unexpected package contents.')
        for name, expected in manifest['files'].items():
            safe_path(name)
            data = archive.read(name)
            if digest(data) != expected:
                raise AtlasError('Checksum mismatch: ' + name)
            files[name] = data
    return {'ref': manifest['ref'], 'commit': manifest['commit'], 'files': files}


def jsonc_tokens(text):
    pattern = r'\s+|//[^\r\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|[{}\[\]:,]|[^\s{}\[\]:,]+'
    tokens = [(m.group(), m.start(), m.end()) for m in re.finditer(pattern, text)
              if not m.group().isspace() and not m.group().startswith(('//', '/*'))]
    cleaned = ' '.join(token for i, (token, _, _) in enumerate(tokens)
                      if not (token == ',' and i + 1 < len(tokens) and tokens[i + 1][0] in (']', '}')))
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise AtlasError('Duplicate JSON key: ' + key)
            result[key] = value
        return result
    try:
        value = json.loads(cleaned, object_pairs_hook=unique)
    except ValueError as error:
        raise AtlasError('Invalid OpenCode JSON/JSONC; correct it before installing.') from error
    if not isinstance(value, dict):
        raise AtlasError('OpenCode configuration must be an object.')
    return value, tokens


def add_instruction(data):
    text = data.decode('utf-8') if data else '{}\n'
    value, tokens = jsonc_tokens(text)
    instruction = '.opencode/AGENTS.md'
    if 'instructions' in value:
        if not isinstance(value['instructions'], list) or not all(isinstance(v, str) for v in value['instructions']):
            raise AtlasError('OpenCode instructions must be an array of strings.')
        if instruction in value['instructions']:
            return text.encode()
        depth = 0
        start = None
        for i, (token, _, _) in enumerate(tokens):
            if token == '"instructions"' and depth == 1:
                start = i + 2
                break
            if token in ('{', '['):
                depth += 1
            elif token in ('}', ']'):
                depth -= 1
        if start is None or tokens[start][0] != '[':
            raise AtlasError('Cannot locate instructions safely.')
        end = start + 1
        while tokens[end][0] != ']':
            end += 1
        previous = tokens[end - 1][0]
        addition = (',' if previous not in ('[', ',') else '') + '\n    ' + json.dumps(instruction) + '\n  '
        position = tokens[end][1]
    else:
        previous = tokens[-2][0]
        addition = (',' if previous not in ('{', ',') else '') + '\n  "instructions": [' + json.dumps(instruction) + ']\n'
        position = tokens[-1][1]
    result = text[:position] + addition + text[position:]
    jsonc_tokens(result)
    return result.encode()


def rule_parts(data):
    text = data.decode('utf-8') if data is not None else ''
    if BEGIN.strip() not in text and END not in text:
        return text, None, ''
    if text.count(BEGIN) != 1 or text.count(END) != 1:
        raise AtlasError('Modified Atlas rule markers in AGENTS.md.')
    before, remaining = text.split(BEGIN)
    body, after = remaining.split(END)
    return before, body.encode(), after


def plan_install(root, package, phase, state):
    originals = dict(package['files'])
    if phase == 'bootstrap':
        originals = {name: data for name, data in originals.items()
                     if name.startswith(SKILL) or name == 'commands/atlas.md'}
    originals[PAYLOAD] = encode_package(package)
    old = state.get('files', {})
    allowed = {name if name != 'LICENSE' else SKILL + 'LICENSE' for name in REQUIRED} | {PAYLOAD}
    if not isinstance(old, dict) or not set(old) <= allowed:
        raise AtlasError('Unexpected paths in installation state.')
    changes, snapshot, conflicts = {}, {}, []
    for name in sorted(set(old) | set(originals)):
        current = read_optional(target_path(root, name))
        snapshot[name] = current
        incoming = originals.get(name)
        if name == 'AGENTS.md':
            before, local, after = rule_parts(current)
            # Adopt an identical manual Atlas installation without duplicating its rules.
            if local is None and current == incoming:
                local, before, after = current, '', ''
            elif local is None and current and '# Atlas: Wegweiser' in before:
                conflicts.append(name)
                continue
            if digest(local) not in (old.get(name), digest(incoming)) and digest(incoming) != old.get(name):
                conflicts.append(name)
                continue
            if local != incoming and digest(incoming) == old.get(name):
                continue
            prefix = before + ('\n\n' if before and not before.endswith('\n\n') else '')
            desired = (prefix + BEGIN + incoming.decode() + END + after).encode() if incoming else (before + after).encode()
        else:
            if current != incoming and digest(current) != old.get(name):
                if digest(incoming) != old.get(name):
                    conflicts.append(name)
                continue
            desired = incoming
        if current != desired:
            changes[name] = desired
    if conflicts:
        raise AtlasError('Local changes or name collisions; nothing written:\n' + '\n'.join(conflicts))
    return originals, changes, snapshot


def apply_transaction(root, changes, snapshot):
    for name, expected in snapshot.items():
        if read_optional(target_path(root, name)) != expected:
            raise AtlasError('File changed during planning; nothing written: ' + name)
    changed = []
    try:
        for name, data in changes.items():
            path = target_path(root, name)
            path.parent.mkdir(parents=True, exist_ok=True)
            changed.append(name)
            if data is None:
                path.unlink(missing_ok=True)
            else:
                with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
                    temporary = Path(handle.name)
                    handle.write(data)
                try:
                    os.replace(temporary, path)
                finally:
                    temporary.unlink(missing_ok=True)
        for name, data in changes.items():
            if read_optional(target_path(root, name)) != data:
                raise AtlasError('Verification failed: ' + name)
    except (OSError, AtlasError):
        for name in reversed(changed):
            path = root / name
            original = snapshot[name]
            if original is None:
                path.unlink(missing_ok=True)
            else:
                path.write_bytes(original)
        raise


def install(root, package, phase, project=False, dry_run=False):
    root = Path(root).absolute()
    state_data = read_optional(target_path(root, STATE))
    state = json.loads(state_data) if state_data else {}
    if state and state.get('format') != 1:
        raise AtlasError('Unsupported installation state.')
    if state.get('phase') == 'installed':
        phase = 'installed'
    originals, changes, snapshot = plan_install(root, package, phase, state)
    if phase == 'installed':
        if project:
            config = 'opencode.jsonc' if (root / 'opencode.jsonc').exists() else 'opencode.json'
            snapshot[config] = read_optional(target_path(root, config))
            updated = add_instruction(snapshot[config])
            if updated != snapshot[config]:
                changes[config] = updated
        try:
            tracked = subprocess.run(['git', '-C', str(root.parent if project else root), 'ls-files', '--error-unmatch',
                                      str(root / 'atlas.json')], capture_output=True).returncode == 0
        except FileNotFoundError:
            tracked = False
        if tracked:
            raise AtlasError('atlas.json is already tracked; remove it from Git tracking before installing.')
    snapshot['.gitignore'] = read_optional(target_path(root, '.gitignore'))
    ignore = snapshot['.gitignore'] or b''
    entries = ['/atlas.json', '/.atlas-install.json', '/skills/atlas/assets/package.zip']
    missing = [entry for entry in entries if entry not in ignore.decode().splitlines()]
    if missing:
        changes['.gitignore'] = ignore + (b'\n' if ignore and not ignore.endswith(b'\n') else b'') + ('\n'.join(missing) + '\n').encode()
    next_state = {'format': 1, 'phase': phase, 'project': project,
                  'ref': package['ref'], 'commit': package['commit'],
                  'files': {name: digest(data) for name, data in sorted(originals.items())}}
    snapshot[STATE] = state_data
    encoded = (json.dumps(next_state, indent=2) + '\n').encode()
    if encoded != state_data:
        changes[STATE] = encoded
    print(json.dumps({'target': str(root), 'source': package['ref'], 'commit': package['commit'],
                      'phase': phase, 'dry_run': dry_run, 'changes': sorted(changes)}, indent=2))
    if not dry_run:
        apply_transaction(root, changes, snapshot)
    return next_state


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['bootstrap', 'install', 'update', 'package'])
    parser.add_argument('branchOrVersion', nargs='?')
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument('--project', type=Path, metavar='PROJECT')
    scope.add_argument('--global', dest='global_scope', action='store_true')
    scope.add_argument('--target', type=Path, help='Explicit OpenCode configuration directory')
    parser.add_argument('--ref', help='Source for bootstrap/install; defaults to opencode')
    parser.add_argument('--source', type=Path, help='Build/test from a local Atlas source checkout')
    parser.add_argument('--output', type=Path, help='Output directory for package')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args(argv)
    if args.action == 'update' and (not args.branchOrVersion or args.ref):
        parser.error('update requires branchOrVersion: atlas.py update opencode')
    if args.action != 'update' and args.branchOrVersion:
        parser.error('branchOrVersion is only used by update; use --ref for other actions')
    if args.action == 'package':
        if not args.source or not args.output:
            parser.error('package requires --source and --output')
        package = local_package(args.source, args.ref or 'opencode')
        payload = encode_package(package)
        args.output.mkdir(parents=True, exist_ok=True)
        (args.output / 'atlas-package.zip').write_bytes(payload)
        (args.output / 'atlas.py').write_bytes(package['files'][SKILL + 'scripts/atlas.py'])
        with zipfile.ZipFile(args.output / 'atlas-skill.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
            for name, data in package['files'].items():
                if name.startswith(SKILL):
                    archive.writestr('atlas/' + name[len(SKILL):], data)
            archive.writestr('atlas/assets/package.zip', payload)
        print('Built atlas-skill.zip, atlas-package.zip and atlas.py in ' + str(args.output))
        return
    if args.project:
        root = args.project.expanduser().absolute() / '.opencode'
    elif args.target:
        root = args.target.expanduser().absolute()
    elif args.global_scope:
        root = Path(os.environ.get('OPENCODE_CONFIG_DIR', Path.home() / '.config/opencode')).expanduser()
    else:
        parser.error('Choose --project PROJECT, --global or --target CONFIG_DIRECTORY')
    project = bool(args.project)
    state_data = read_optional(target_path(root, STATE))
    if state_data:
        project = json.loads(state_data).get('project', project)
    if args.action == 'update' and not state_data:
        raise AtlasError('No managed Atlas installation at ' + str(root))
    ref = args.branchOrVersion or args.ref or 'opencode'
    cached = root / PAYLOAD
    # A bundled skill can install offline, and keeps setup on its downloaded revision.
    bundled = Path(__file__).resolve().parent.parent / 'assets/package.zip'
    if args.source:
        package = local_package(args.source, ref)
    elif args.action == 'install' and not args.ref and (cached.is_file() or bundled.is_file()):
        package = decode_package((cached if cached.is_file() else bundled).read_bytes())
    else:
        package = download_package(ref)
    install(root, package, 'bootstrap' if args.action == 'bootstrap' else 'installed', project, args.dry_run)


if __name__ == '__main__':
    try:
        main()
    except (AtlasError, OSError, ValueError, KeyError, zipfile.BadZipFile, tarfile.TarError) as error:
        print('Atlas: ' + str(error), file=sys.stderr)
        sys.exit(1)
