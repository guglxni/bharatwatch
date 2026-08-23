#!/usr/bin/env python3
import subprocess, time, re, sys, json, os
from pathlib import Path

fixtures = Path.home() / 'scrape-verse' / 'bharatwatch' / 'tests' / 'fixtures' / 'public-sites'
bharatwatch = Path.home() / 'scrape-verse' / 'bharatwatch'

print('Step 1: Starting fixture server on port 8765')
server = subprocess.Popen(
    ['python3', 'server.py', '8765'],
    cwd=fixtures,
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
)
time.sleep(3)
if server.poll() is not None:
    print('Server died immediately:', server.stdout.read())
    sys.exit(1)
print('Server running, PID:', server.pid)

# Verify local server works
print('Step 2: Verifying local fixture server')
local = subprocess.run(['curl', '-s', 'http://127.0.0.1:8765/naukri/'], capture_output=True, text=True, timeout=10)
if local.returncode != 0 or len(local.stdout) < 100:
    print('Local server not working:', local.returncode, len(local.stdout))
    server.kill()
    sys.exit(1)
print('Local server OK, len:', len(local.stdout))

print('Step 3: Starting cloudflared tunnel')
tunnel = subprocess.Popen(
    ['cloudflared', 'tunnel', '--url', 'http://127.0.0.1:8765'],
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
)

tunnel_url = None
for _ in range(60):
    line = tunnel.stdout.readline()
    if line:
        print('[tunnel]', line.strip())
        m = re.search(r'(https://[a-zA-Z0-9-]+\.trycloudflare\.com)', line)
        if m:
            tunnel_url = m.group(1)
    if tunnel_url:
        break

if not tunnel_url:
    print('Failed to get tunnel URL')
    server.kill()
    tunnel.kill()
    sys.exit(1)

print('Tunnel URL:', tunnel_url)
print('Note: local curl may not resolve tunnel hostname, but Bright Data should be able to reach it.')
time.sleep(3)  # Give tunnel a moment to register

print('Step 4: Creating NaukriAlert collector via Bright Data')
create_cmd = [
    'npx', '@brightdata/cli', 'scraper', 'create',
    f'{tunnel_url}/naukri/',
    'Extract all rows from the table with id notices. Return a flat JSON array with fields: title, department, notification_date, last_application_date, exam_date, number_of_vacancies, qualification_required, and official_link. Do not navigate any links.'
]
create = subprocess.Popen(
    create_cmd,
    cwd=bharatwatch,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)
collector_id = None
output_lines = []
for _ in range(600):  # 10 minutes
    line = create.stdout.readline()
    if line:
        output_lines.append(line.strip())
        print('[create]', line.strip())
        m = re.search(r'Template created: (c_[a-zA-Z0-9]+)', line)
        if m:
            collector_id = m.group(1)
    if create.poll() is not None and collector_id:
        break
    if create.poll() is not None and not collector_id:
        print('Create process ended without collector ID')
        break
    time.sleep(1)

if not collector_id:
    print('Failed to create collector. Full output:')
    print('\n'.join(output_lines))
    server.kill()
    tunnel.kill()
    sys.exit(1)

print('Collector ID:', collector_id)

print('Step 5: Running collector')
run_cmd = [
    'npx', '@brightdata/cli', 'scraper', 'run',
    collector_id,
    f'{tunnel_url}/naukri/',
    '--pretty'
]
run = subprocess.run(run_cmd, cwd=bharatwatch, capture_output=True, text=True, timeout=180)
print('[run stdout]', run.stdout[-2000:])
print('[run stderr]', run.stderr[-1000:])
print('Run exit code:', run.returncode)

result_path = Path('/tmp/naukri-orchestrated-result.json')
try:
    data = json.loads(run.stdout)
    result_path.write_text(json.dumps(data, indent=2))
    print('Saved parsed result, item count:', len(data) if isinstance(data, list) else 'not list')
except Exception as e:
    result_path.write_text(run.stdout)
    print('Could not parse result as JSON:', e)

print('Step 6: Cleanup')
server.kill()
tunnel.kill()
create.kill()

if run.returncode == 0 and isinstance(json.loads(run.stdout) if run.stdout else [], list) and len(json.loads(run.stdout) if run.stdout else []) > 0:
    print('SUCCESS')
    print('COLLECTOR_ID=' + collector_id)
else:
    print('FAILED')
    sys.exit(1)
