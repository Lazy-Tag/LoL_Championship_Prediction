"""Run each historical event 14,000,605 times, independently seeded by year.

These are simulations of the documented implemented rules, including explicit
approximations for old tiebreaks/draws. They are not exact official-rule replays.
"""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import time

R = Path(__file__).resolve().parents[1]
SAMPLES = 14_000_605

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    build = R / '.local/build'
    build.mkdir(parents=True, exist_ok=True)
    output = R / 'results/event_replay'
    output.mkdir(parents=True, exist_ok=True)
    logs = R / '.local/event_replay_logs'
    logs.mkdir(parents=True, exist_ok=True)
    source = R / 'scripts/event_simulation.cpp'
    binary = build / 'event_simulation'
    compiler = shlex.split(os.environ.get('CXX', 'clang++'))
    clt = Path('/Library/Developer/CommandLineTools/usr/bin/clang++')
    if 'CXX' not in os.environ and clt.exists():
        compiler = [str(clt), '-isysroot', '/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk']
    subprocess.run([*compiler, '-O3', '-std=c++17', str(source), '-o', str(binary)], check=True)
    configs = json.loads((R / 'data/event_replay/configs.json').read_text())
    assert len(configs) == 23 and all(c['season'] >= 4 for c in configs)
    started = time.time()
    def run(c):
        assert c['year'] == c['seed'] == c['season'] + 2010
        assert c['samples'] == SAMPLES
        assert not c['latest_training_date'] or c['latest_training_date'] < c['start_date']
        inp = R / f"data/event_replay/{c['id']}.txt"
        assert int(inp.read_text().split()[0]) == c['year']
        meta = dict(event_id=c['id'], input_sha256=sha(inp), engine_sha256=sha(source),
                    half_life_days=90, rule_status='implemented-format scenario; historical tiebreak and draw approximations remain')
        target = output / f"{c['id']}.json"
        if target.exists():
            old = json.loads(target.read_text())
            if all(old.get(k) == v for k, v in meta.items()) and old['samples'] == SAMPLES and old['seed'] == c['year']:
                return c['id'], 'reused verified matching result'
        tmp = target.with_suffix('.json.tmp')
        print(f"START {c['id']} seed={c['year']} samples={SAMPLES:,}", flush=True)
        with inp.open('rb') as stdin, tmp.open('wb') as stdout, (logs / f"{c['id']}.log").open('wb') as stderr:
            subprocess.run([str(binary), str(SAMPLES)], stdin=stdin, stdout=stdout, stderr=stderr, check=True)
        result = json.loads(tmp.read_text())
        assert result['samples'] == SAMPLES and result['seed'] == c['year']
        assert len(result['counts']) == len(c['teams'])
        assert all(sum(v[2] for v in bands) == SAMPLES for bands in result['counts'])
        assert sum(v[2] for bands in result['counts'] for v in bands if v[:2] == [1, 1]) == SAMPLES
        result.update(meta)
        tmp.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        tmp.replace(target)
        return c['id'], f"complete in {result['seconds']:.1f}s; complex ties={result['complex_tie_scenarios']:,}; waivers={result['draw_waivers']}"
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(run, c) for c in configs]
        for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
            name, status = future.result()
            print(f"[{i}/{len(configs)}] {name}: {status}", flush=True)
    print(f'COMPLETE {len(configs)} events x {SAMPLES:,} = {len(configs)*SAMPLES:,} simulations, {time.time()-started:.1f}s wall time', flush=True)

if __name__ == '__main__':
    main()
