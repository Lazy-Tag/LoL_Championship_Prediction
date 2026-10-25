"""Publish only the latest validated daily forecast; retry non-force pushes.

Never include unrelated work or pre-existing staged changes. Refuse unrelated
outgoing commits; a failed automatic push is recognized by an exact trailer
and its path allowlist. No tokens, raw responses, or machine settings are added.
"""
import json,os,re,subprocess,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
STATE=ROOT/'.local/live_s16/git_publish.json'
REMOTE='git@github.com:Lazy-Tag/LoL_Championship_Prediction.git'
# launchd has a minimal PATH; Apple's git shim may require unavailable Xcode.
GIT=next((p for p in ('/opt/homebrew/bin/git','/usr/local/bin/git','/Library/Developer/CommandLineTools/usr/bin/git') if Path(p).is_file()),None) or shutil.which('git') or 'git'

def git(*args):
    env={**os.environ,'GIT_TERMINAL_PROMPT':'0','GIT_SSH_COMMAND':'ssh -o BatchMode=yes -o ConnectTimeout=20'}
    return subprocess.check_output([GIT,*args],cwd=ROOT,env=env,text=True,stderr=subprocess.STDOUT,timeout=180).strip()

def publication_paths(latest):
    stamp=latest['snapshot'];report=latest['report']
    assert re.fullmatch(r'2026-\d{2}-\d{2}T\d{6}Z',stamp)
    assert re.fullmatch(r'reports/s16/live/2026-\d{2}-\d{2}\.md',report)
    return [report,'reports/s16/live/README.md','results/live_s16/latest.json','results/live_s16/observed_events.json',
            *[f'results/live_s16/{stamp}/{name}' for name in ('forecast.json','simulation.json','input.txt')]]

def validate_outgoing(commits,latest,paths):
    if not commits:return
    if len(commits)!=1:raise RuntimeError('Unrelated outgoing commits: leave them for manual review')
    sha=commits[0];message=git('show','-s','--format=%B',sha)
    if f'Auto-Live-Snapshot: {latest["snapshot"]}' not in message.splitlines():
        raise RuntimeError('Outgoing commit is not this automatic forecast publication')
    changed=set(git('diff-tree','--no-commit-id','--name-only','-r',sha).splitlines())
    if not changed or not changed<=set(paths):raise RuntimeError('Outgoing commit contains unrelated files')

def publish_latest():
    pointer=ROOT/'results/live_s16/latest.json'
    if not pointer.exists():return
    latest=json.loads(pointer.read_text());paths=publication_paths(latest)
    state=json.loads(STATE.read_text()) if STATE.exists() else {}
    if state.get('snapshot')==latest['snapshot'] and state.get('pushed'):
        return
    if git('branch','--show-current')!='main' or git('remote','get-url','origin')!=REMOTE:
        raise RuntimeError('Unexpected branch or origin; automatic publication stopped')
    if git('diff','--cached','--name-only'):
        raise RuntimeError('Existing staged changes: automatic publication leaves index untouched')
    git('fetch','origin','main')
    outgoing=git('rev-list','origin/main..HEAD').splitlines()
    validate_outgoing(outgoing,latest,paths)
    if git('rev-list','HEAD..origin/main'):
        raise RuntimeError('Remote has new commits: do not auto-merge or force-push')
    # A previous validated commit only needs its push retried. New local files
    # are not swept into that retry.
    if not outgoing:
        for script in ('verify.py','verify_publication.py','verify_live_s16.py'):
            subprocess.run([str(ROOT/'.venv/bin/python'),str(ROOT/'scripts'/script)],cwd=ROOT,check=True,timeout=180)
        for name in paths:
            p=ROOT/name
            if not p.is_file() or p.is_symlink():raise RuntimeError('Missing or unsafe publication path: '+name)
            text=p.read_text()
            if re.search(r'/Users/|BEGIN .*PRIVATE KEY|github_pat_|ghp_[A-Za-z0-9]{20,}',text):
                raise RuntimeError('Private data pattern in publication: '+name)
        git('add','--',*paths)
        if git('diff','--cached','--name-only'):
            git('diff','--cached','--check')
            day=Path(latest['report']).stem
            git('commit','--only','-m',f'Update S16 live forecast for {day}',
                '-m',f'Auto-Live-Snapshot: {latest["snapshot"]}','--',*paths)
    sha=git('rev-parse','HEAD')
    STATE.parent.mkdir(parents=True,exist_ok=True)
    STATE.write_text(json.dumps(dict(snapshot=latest['snapshot'],commit=sha,pushed=False),indent=2)+'\n')
    print(git('push','origin','HEAD:main'),flush=True)
    if git('rev-parse','origin/main')!=sha:raise RuntimeError('Remote tracking tip does not match published commit')
    STATE.write_text(json.dumps(dict(snapshot=latest['snapshot'],commit=sha,pushed=True),indent=2)+'\n')
    print('Published daily forecast to GitHub: '+sha,flush=True)

if __name__=='__main__':publish_latest()
