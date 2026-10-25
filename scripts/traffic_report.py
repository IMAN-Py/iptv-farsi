#!/usr/bin/env python3
"""Save GitHub traffic snapshots locally; never commit credentials or visitor data."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo', default='IMAN-Py/open-tv-atlas')
parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parents[1] / '.local-metrics')
args = parser.parse_args()
gh = shutil.which('gh') or '/opt/homebrew/bin/gh'

def get(endpoint):
    result = subprocess.run([gh, 'api', endpoint], check=True, capture_output=True, text=True)
    return json.loads(result.stdout)

now = datetime.now(timezone.utc)
base = 'repos/' + args.repo
report = {'captured_at': now.isoformat(), 'repository': args.repo,
          'repository_metrics': {key: value for key, value in get(base).items()
                                 if key in ('stargazers_count', 'forks_count', 'subscribers_count', 'open_issues_count')},
          'views': get(base + '/traffic/views'), 'clones': get(base + '/traffic/clones'),
          'referrers': get(base + '/traffic/popular/referrers'),
          'popular_pages': get(base + '/traffic/popular/paths')}
args.output.mkdir(parents=True, exist_ok=True)
path = args.output / (now.strftime('%Y-%m-%dT%H%M%SZ') + '.json')
path.write_text(json.dumps(report, indent=2) + '\n')
summary = (f'# Open TV Atlas traffic\n\nCaptured: {now.isoformat()}\n\n'
           f'- Stars: {report["repository_metrics"]["stargazers_count"]}\n'
           f'- Forks: {report["repository_metrics"]["forks_count"]}\n'
           f'- GitHub views in the reported 14-day window: {report["views"]["count"]}\n'
           f'- Unique visitors in that window: {report["views"]["uniques"]}\n'
           f'- Clones in that window: {report["clones"]["count"]}\n\n'
           'These are GitHub repository metrics, not website sessions or TV viewers. '
           'Rolling windows overlap; do not add totals across snapshots. Referrers can lag by a day.\n')
(args.output / 'latest.md').write_text(summary)
print(summary)
print(f'Snapshot saved to {path}')
