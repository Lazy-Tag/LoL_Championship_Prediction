"""Real local Git repositories test publishing scope, retry and conflict refusal."""
import contextlib,io,json,subprocess,sys,tempfile
from pathlib import Path
import publish_live_git as pub

def run(*args,cwd=None):
    return subprocess.check_output(args,cwd=cwd,text=True,stderr=subprocess.STDOUT).strip()

def main():
    with tempfile.TemporaryDirectory() as temp:
        root=Path(temp)/'repo';remote=Path(temp)/'remote.git'
        run('git','init','--bare',str(remote));run('git','init','-b','main',str(root))
        def git(*args):return run('git',*args,cwd=root)
        git('config','user.name','Test');git('config','user.email','test@example.invalid');git('remote','add','origin',str(remote))
        (root/'baseline').write_text('base');git('add','baseline');git('commit','-m','baseline');git('push','-u','origin','main')
        pub.ROOT=root;pub.REMOTE=str(remote);pub.STATE=root/'.local/state.json'
        (root/'.venv/bin').mkdir(parents=True);(root/'.venv/bin/python').symlink_to(sys.executable)
        (root/'scripts').mkdir()
        for script in ('verify.py','verify_publication.py','verify_live_s16.py'):(root/'scripts'/script).write_text('pass\n')
        latest=dict(snapshot='2026-10-25T015840Z',report='reports/s16/live/2026-10-25.md')
        for name in pub.publication_paths(latest):
            p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('{}\n' if p.suffix=='.json' else 'public\n')
        (root/'results/live_s16/latest.json').write_text(json.dumps(latest))
        (root/'private.txt').write_text('unrelated');git('add','private.txt')
        try:pub.publish_latest()
        except RuntimeError as e:assert 'staged' in str(e)
        else:raise AssertionError('Existing staged file accepted')
        assert git('diff','--cached','--name-only')=='private.txt';git('reset','--','private.txt')
        actual=pub.git
        def fail_push(*args):
            if args[0]=='push':raise RuntimeError('simulated offline push')
            return actual(*args)
        pub.git=fail_push
        try:pub.publish_latest()
        except RuntimeError as e:assert 'offline' in str(e)
        else:raise AssertionError('Push failure not surfaced')
        sha=git('rev-parse','HEAD');assert not json.loads(pub.STATE.read_text())['pushed']
        pub.git=actual;pub.publish_latest();assert git('rev-parse','HEAD')==sha==git('rev-parse','origin/main')
        assert json.loads(pub.STATE.read_text())['pushed'] and not git('ls-files','private.txt')
        pub.publish_latest();assert git('rev-parse','HEAD')==sha
        # A fresh publication may not push an unrelated local commit.
        pub.STATE.unlink();(root/'other').write_text('other');git('add','other');git('commit','-m','unrelated')
        try:pub.publish_latest()
        except RuntimeError as e:assert 'not this automatic' in str(e)
        else:raise AssertionError('Unrelated commit pushed')
    print('PASS exact publication paths, staged-change protection, real Git commit/push, failed-push retry, no duplicate commits, unrelated outgoing commit refusal')

if __name__=='__main__':main()
