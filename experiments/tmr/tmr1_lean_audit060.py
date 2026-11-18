#!/usr/bin/env python3
"""Fail-closed provenance/log checks. A log audit does not execute a Lean kernel."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

PIN = '16a5ce41304fcdaea4e0be7c132e1c361dc26da5'
ARTIFACT_SHA256 = '6b0a8993626d37614c7843d9c3dfd181a847591c684f425b7a470cc41fb43bf6'
THEOREMS = {'MainResults.ethIsFalse', 'MainResults.mainTheorem'}
STANDARD = {'propext', 'Classical.choice', 'Quot.sound'}
FILE_PINS = {
    'eth/MainResults.lean': '1c62a550fa1e4cbec65bb7112f92ad67589afddc',
    'eth/Solution.lean': '176892178e49792ae41368c13bb4973bae035b29',
    'eth/scripts/PrintAxioms.lean': 'cb31f549acbce8de837f111979acfdd9836c8411',
    'eth/lake-manifest.json': '296fefa9ac614013ab29708d71c1ae5dcbc39765',
    'eth/lean-toolchain': 'a8afa7d1b02d96f0671eba854a8dc4b416beb473',
    'eth/comparator.json': '85f16dc55e511335729e668917308b375f0f6036',
    '.github/scripts/comparator-check.sh': '0143ba15873eac3d3056ceee0f19471b82987a98',
}

def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)

def git(root: Path, *args: str) -> str:
    return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()

def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def source(root: Path) -> dict:
    require(git(root, 'rev-parse', 'HEAD') == PIN, 'wrong upstream commit')
    found = {}
    for name, expected in FILE_PINS.items():
        actual = blob((root / name).read_bytes())
        require(actual == expected, f'source mismatch: {name}')
        found[name] = actual
    return {'revision': PIN, 'files': found, 'kernel_executed_by_this_check': False}

def dependencies(root: Path) -> dict:
    project = root / 'eth'
    manifest = json.loads((project / 'lake-manifest.json').read_text())
    found = {}
    for package in manifest['packages']:
        require(package['type'] == 'git', 'unhandled dependency kind')
        path = project / manifest['packagesDir'] / package['name']
        actual = git(path, 'rev-parse', 'HEAD')
        require(actual == package['rev'], f'dependency mismatch: {package["name"]}')
        require(not git(path, 'status', '--porcelain', '--untracked-files=no'),
                f'modified tracked dependency files: {package["name"]}')
        found[package['name']] = actual
    return found

def axioms(text: str) -> dict:
    records = re.findall(r"'([^']+)'\s+depends on axioms:\s*\[([^\]]*)\]", text)
    require(len(records) == 2, 'expected exactly two printed axiom records')
    require({name for name, _ in records} == THEOREMS, 'wrong theorem names')
    result = {}
    for name, body in records:
        names = [v.strip() for v in body.split(',') if v.strip()]
        require(len(names) == 3 and set(names) == STANDARD,
                f'unexpected transitive axioms for {name}: {names}')
        result[name] = sorted(names)
    return {'reported_axioms': result, 'kernel_executed_by_this_check': False}

def comparator(text: str) -> dict:
    needed = ['nanoda kernel accepts the solution',
              'Lean default kernel accepts the solution', 'Your solution is okay!']
    lines = text.splitlines()
    for line in needed:
        require(lines.count(line) == 1, f'missing or duplicate acceptance line: {line}')
    require('from Challenge' in text and 'from Solution' in text, 'missing comparison exports')
    for name in THEOREMS:
        require(text.count(name) >= 2, f'missing target export: {name}')
    return {'reported_dual_kernel_acceptance': True, 'kernel_executed_by_this_check': False}

def artifact(path: Path) -> dict:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    require(digest == ARTIFACT_SHA256, 'upstream artifact SHA-256 mismatch')
    with zipfile.ZipFile(path) as z:
        expected = {'lake-build.log', 'comparator-logs/comparator.json',
                    'comparator-logs/comparator.log'}
        require(set(z.namelist()) == expected, 'unexpected artifact file set')
        files = {name: z.read(name) for name in sorted(expected)}
    config = json.loads(files['comparator-logs/comparator.json'])
    require(set(config['theorem_names']) == THEOREMS, 'wrong comparator targets')
    require(set(config['permitted_axioms']) == STANDARD, 'wrong permitted axioms')
    require(config['enable_nanoda'] is True, 'nanoda disabled')
    require(config['challenge_module'] == 'Challenge' and config['solution_module'] == 'Solution',
            'wrong comparator modules')
    acceptance = comparator(files['comparator-logs/comparator.log'].decode())
    return {'status': 'UPSTREAM_ARTIFACT_VERIFIED_NOT_INDEPENDENT_REBUILD',
            'artifact_id': 12707409821, 'upstream_run_id': 40442388505,
            'upstream_revision': PIN, 'sha256': digest,
            'file_bytes': {k: len(v) for k, v in files.items()},
            'file_sha256': {k: hashlib.sha256(v).hexdigest() for k, v in files.items()},
            'configuration': config, **acceptance}

def self_test() -> dict:
    good = "\n".join(f"'{name}' depends on axioms: [propext, Classical.choice, Quot.sound]"
                     for name in sorted(THEOREMS))
    axioms(good)
    bad = [good.replace('Quot.sound', 'sorryAx'), good.splitlines()[0], good + '\n' + good,
           good.replace('MainResults.mainTheorem', 'MainResults.someOtherTheorem'),
           good.replace('Quot.sound', 'Lean.ofReduceBool'),
           good.replace('Quot.sound', 'MyExtraAxiom')]
    rejected = 0
    for text in bad:
        try:
            axioms(text)
        except ValueError:
            rejected += 1
        else:
            raise AssertionError('negative axiom-log control accepted')
    return {'positive_axiom_log_controls': 1, 'negative_axiom_log_controls_rejected': rejected,
            'kernel_executed': False}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['source', 'dependencies', 'axioms', 'comparator', 'artifact', 'self-test'])
    parser.add_argument('path', type=Path, nargs='?')
    args = parser.parse_args()
    if args.mode == 'self-test':
        result = self_test()
    else:
        require(args.path is not None, 'path required')
        if args.mode in ('axioms', 'comparator'):
            result = globals()[args.mode](args.path.read_text(encoding='utf-8'))
        else:
            result = globals()[args.mode](args.path)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0

if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError, subprocess.SubprocessError, zipfile.BadZipFile) as exc:
        print(f'AUDIT FAILED: {exc}', file=sys.stderr)
        raise SystemExit(1)
