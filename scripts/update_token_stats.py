#!/usr/bin/env python3
import json, re, datetime, pathlib
sessions_path = pathlib.Path('/home/tim/.openclaw/agents/main/sessions/sessions.json')
out_path = pathlib.Path('/home/tim/.openclaw/workspace/projects/nursing-shift-copilot/token-stats.json')

input_tokens = output_tokens = tool_calls = 0
cost_gbp = 0.0
source = 'openclaw-sessions-json'

try:
    data = json.loads(sessions_path.read_text())
    sess = data.get('agent:main:main', {})
    input_tokens = int(sess.get('inputTokens') or 0)
    output_tokens = int(sess.get('outputTokens') or 0)
    sf = sess.get('sessionFile')
    if sf and pathlib.Path(sf).exists():
        txt = pathlib.Path(sf).read_text(errors='ignore')
        tool_calls = len(re.findall(r'"recipient_name"\s*:\s*"functions\.[^"]+"', txt))
except Exception:
    source = 'openclaw-sessions-json-error'

payload = {
    'source': source,
    'updatedAt': datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z',
    'inputTokens': input_tokens,
    'outputTokens': output_tokens,
    'toolCalls': tool_calls,
    'costGbp': cost_gbp
}
out_path.write_text(json.dumps(payload, indent=2) + '\n')
print('updated', out_path)
