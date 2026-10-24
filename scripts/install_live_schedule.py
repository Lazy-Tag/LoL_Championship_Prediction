"""Install the requested local hourly checks, ending after 2026-11-01 Beijing.
The installed plist contains local absolute paths and is never published.
"""
import os
import plistlib
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
LABEL='com.lazytag.lol-worlds-2026'
def main():
    local=ROOT/'.local/live_s16';local.mkdir(parents=True,exist_ok=True)
    folder=Path.home()/'Library/LaunchAgents';folder.mkdir(parents=True,exist_ok=True)
    target=folder/(LABEL+'.plist')
    job={'Label':LABEL,'ProgramArguments':[str(ROOT/'.venv/bin/python'),str(ROOT/'scripts/update_live_s16.py'),'--fetch','--daily'],
         'WorkingDirectory':str(ROOT),'StartInterval':3600,'RunAtLoad':True,
         'StandardOutPath':str(local/'scheduled.stdout.log'),'StandardErrorPath':str(local/'scheduled.stderr.log'),
         'EnvironmentVariables':{'PYTHONUNBUFFERED':'1'},'ProcessType':'Background'}
    target.write_bytes(plistlib.dumps(job))
    domain=f'gui/{os.getuid()}'
    subprocess.run(['launchctl','bootout',domain+'/'+LABEL],capture_output=True)
    subprocess.run(['launchctl','bootstrap',domain,str(target)],check=True)
    subprocess.run(['launchctl','print',domain+'/'+LABEL],check=True)
if __name__=='__main__':main()
