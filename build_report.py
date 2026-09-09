"""Build auditable descriptive tables from the preserved outputs; no inference."""
import csv
import hashlib
import json
from pathlib import Path
from statistics import median
import study

root=Path(__file__).resolve().parent
prompts=json.loads((root/'prompts.json').read_text(encoding='utf-8'))
summary=[]
details=[]
traces=['# Complete model traces for representative cases', '', 'These are outputs of the evaluated Spark model, not evaluator-written reconstructions. All 48 outputs remain in the two raw JSONL files.', '']
chosen={'discount1-ko','pack1-ko','net1-ko','tier2-ko','time1-en','mix1-en'}
for thinking, suffix in [(True,''),(False,'-thinking-off')]:
    study.score(thinking)
    rows=[json.loads(x) for x in (root/f'raw{suffix}.jsonl').read_text(encoding='utf-8').splitlines()]
    scores=json.loads((root/f'scores{suffix}.json').read_text(encoding='utf-8'))
    assert len(rows)==24 and [x['id'] for x in rows]==[x['id'] for x in prompts]
    for row,prompt,s in zip(rows,prompts,scores['results']):
        assert row['request']['messages'][0]['content']==prompt['prompt']
        assert row['request']['chat_template_kwargs']['enable_thinking']==thinking
        assert row['request']['seed']==20260910 and row['request']['max_tokens']==1536
        assert not s['operational_error']
        m=row['response']['choices'][0]['message']
        if not thinking:
            assert not m.get('reasoning_content')
        category='correct' if s['correct'] else 'truncated' if s['finish_reason']=='length' else 'format_failure' if s['parsed'] is None else 'wrong_number'
        details.append({'mode':'on' if thinking else 'off','id':s['id'],'expected':s['expected'],'parsed':s['parsed'],'category':category,'elapsed_seconds':s['elapsed_seconds'],'completion_tokens':row['response']['usage']['completion_tokens']})
        if s['id'] in chosen:
            traces.extend([f"## Thinking {'on' if thinking else 'off'} — {s['id']}", '', f"Expected: {s['expected']}; primary category: {category}", '', 'Prompt:', '```text', prompt['prompt'], '```', '', 'Complete reasoning field:', '```text',m.get('reasoning_content') or '(empty)', '```', '', 'Complete content field:', '```text', m.get('content') or '(empty)', '```', ''])
    ds=[d for d in details if d['mode']==('on' if thinking else 'off')]
    summary.append({'mode':'on' if thinking else 'off','n':24,'correct':scores['correct'],'en_correct':scores['by_language']['en']['correct'],'ko_correct':scores['by_language']['ko']['correct'], **{k:sum(d['category']==k for d in ds) for k in ['truncated','format_failure','wrong_number']},'total_seconds':round(sum(d['elapsed_seconds'] for d in ds),3),'median_seconds':round(median(d['elapsed_seconds'] for d in ds),3),'completion_tokens':sum(d['completion_tokens'] for d in ds)})
(root/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
with (root/'per-item.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(details[0]));w.writeheader();w.writerows(details)
(root/'TRACES.md').write_text('\n'.join(traces)+'\n',encoding='utf-8')
table=['# Results generated from all raw outputs','','Primary metric requires an exact unique `FINAL:` marker, a valid number, and the correct rational value. Format failures and truncation count as incorrect.','','| Mode | EN /12 | KO /12 | Correct /24 | Truncated | Format failure | Wrong valid number | Median seconds | Total seconds | Completion tokens |','|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
for s in summary:
    table.append('| '+' | '.join(str(s[k]) for k in ['mode','en_correct','ko_correct','correct','truncated','format_failure','wrong_number','median_seconds','total_seconds','completion_tokens'])+' |')
table.extend(['','## Every item','','| Mode | Item | Expected | Parsed | Primary category |','|---|---|---:|---:|---|'])
table.extend('| '+' | '.join(str(d[k]) for k in ['mode','id','expected','parsed','category'])+' |' for d in details)
(root/'RESULTS.md').write_text('\n'.join(table)+'\n',encoding='utf-8')
manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.iterdir()) if p.is_file() and p.name!='SHA256SUMS.json'}
(root/'SHA256SUMS.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary,indent=2))
