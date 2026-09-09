"""Original paired word problems and transparent exact scoring (MIT)."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import time
import urllib.request

ROOT = Path(__file__).resolve().parent

def cases():
    rows = []
    def add(key, family, answer, derivation, en, ko):
        for lang, text in [('en', en), ('ko', ko)]:
            instruction = ('Show a short calculation. End with exactly one line FINAL: <number>, in the unit requested. Use an integer, decimal, or fraction and no unit on that final line.' if lang == 'en' else '짧게 계산 과정을 쓰세요. 마지막에는 FINAL: <숫자> 형식의 줄을 정확히 한 번 쓰세요. 답은 문제에서 요구한 단위로 쓰고, 마지막 줄에는 정수·소수·분수만 쓰고 단위는 붙이지 마세요.')
            rows.append(dict(id=f'{key}-{lang}', pair=key, family=family, language=lang, expected=str(answer), derivation=derivation, prompt=text+'\n\n'+instruction))
    for k, price, discount, coupon in [(1, 37000, 15, 2300), (2, 46000, 12, 1700)]:
        answer=Fraction(price)*(100-discount)/100-coupon
        add(f'discount{k}', 'discount_order', answer, f'{price}*(100-{discount})/100-{coupon}={answer}',
            f'A fictional shop sells a kit for {price} won. First it discounts that price by {discount}%, then subtracts a {coupon}-won coupon. What is the final price in won?',
            f'가상의 가게에서 키트 가격은 {price//10000}만 {price%10000}원입니다. 먼저 이 가격에서 {discount}%를 할인하고, 그다음 {coupon}원 쿠폰을 뺍니다. 최종 가격은 몇 원인가요?')
    for k, gross, rate, shipping in [(1, 83000, 7, 3200), (2, 67000, 9, 2800)]:
        answer=Fraction(gross)*(100-rate)/100-shipping
        add(f'net{k}', 'fee_base', answer, f'{gross}-{gross}*{rate}/100-{shipping}={answer}',
            f'In a fictional sale, the buyer pays {gross} won. A platform takes {rate}% of that buyer payment. The seller also pays {shipping} won shipping. After both costs, how many won remain?',
            f'가상의 거래에서 구매자는 {gross//10000}만 {gross%10000}원을 냅니다. 플랫폼은 구매자가 낸 금액의 {rate}%를 수수료로 가져갑니다. 판매자는 배송비 {shipping}원도 냅니다. 두 비용을 뺀 나머지는 몇 원인가요?')
    for k, people, per, pack, price in [(1, 37, 3, 8, 6200), (2, 29, 4, 9, 5700)]:
        packs=(people*per+pack-1)//pack
        answer=Fraction(packs*price)
        add(f'pack{k}', 'integer_ceiling', answer, f'ceil({people}*{per}/{pack})={packs}; {packs}*{price}={answer}',
            f'{people} people each need {per} stickers. Stickers are sold only in whole packs of {pack}, costing {price} won per pack. What is the minimum total cost in won?',
            f'{people}명에게 각각 스티커 {per}개가 필요합니다. 스티커는 {pack}개들이 한 팩 단위로만 판매하며, 한 팩 가격은 {price}원입니다. 필요한 최소 총비용은 몇 원인가요?')
    for k, hours, basehours, base, extra in [(1, 7, 2, 4500, 1200), (2, 9, 3, 5200, 900)]:
        answer=Fraction(base+(hours-basehours)*extra)
        add(f'tier{k}', 'tier_boundary', answer, f'{base}+({hours}-{basehours})*{extra}={answer}',
            f'A locker rental costs a total of {base} won for the first {basehours} hours, then {extra} won for each additional hour. It is rented for exactly {hours} hours. What is the total charge in won?',
            f'보관함 대여료는 처음 {basehours}시간 전체에 대해 {base}원이고, 그 이후에는 한 시간마다 {extra}원씩 추가됩니다. 정확히 {hours}시간 빌리면 총요금은 몇 원인가요?')
    for k,a,b,p,q in [(1,180,120,20,35),(2,150,250,12,28)]:
        answer=Fraction(a*p+b*q,a+b)
        add(f'mix{k}', 'weighted_percentage', answer, f'({a}*{p}+{b}*{q})/({a}+{b})={answer}',
            f'Mix {a} grams of a {p}%-by-mass salt solution with {b} grams of a {q}%-by-mass salt solution. No mass is lost. What is the resulting salt percentage (give the percentage number, not a fraction of one)?',
            f'질량 기준 농도 {p}%인 소금물 {a}그램과 농도 {q}%인 소금물 {b}그램을 섞습니다. 질량 손실은 없습니다. 섞은 소금물의 농도는 몇 %인가요? (1에 대한 비율이 아니라 백분율의 숫자를 답하세요.)')
    for k,n,interval,pause_after,pause in [(1,8,17,4,11),(2,9,13,5,19)]:
        answer=Fraction((n-1)*interval+pause)
        add(f'time{k}', 'interval_count', answer, f'({n}-1)*{interval}+{pause}={answer}',
            f'A machine stamps its first card at time zero. It stamps {n} cards in total, with {interval} seconds between consecutive cards. Immediately after card {pause_after}, it adds a one-time pause of {pause} seconds before resuming the usual interval. How many seconds elapse from the first stamp to the last?',
            f'기계는 0초에 첫 카드를 찍습니다. 총 {n}장의 카드를 찍으며, 연속된 두 카드를 찍는 사이의 시간은 {interval}초입니다. {pause_after}번째 카드를 찍은 직후에 한 번만 {pause}초를 추가로 쉬고, 그 뒤 평소 간격으로 작업합니다. 첫 카드부터 마지막 카드까지 몇 초가 걸리나요?')
    return rows

NUMBER = r'[+-]?(?:\d+(?:\.\d+)?|\.\d+)(?:/[+-]?\d+)?'

def extract(text):
    # Require a unique complete final marker as the final nonempty line.
    lines = [x.strip() for x in text.splitlines() if x.strip()]
    markers = [x for x in lines if 'FINAL:' in x]
    if len(markers)!=1 or markers[0]!=lines[-1]:
        return None
    m=re.fullmatch(r'FINAL:\s*('+NUMBER+r')', markers[0])
    if not m:
        return None
    try:
        return Fraction(m.group(1))
    except (ValueError, ZeroDivisionError):
        return None

def freeze():
    out=ROOT/'prompts.json'
    data=json.dumps(cases(),ensure_ascii=False,indent=2)+'\n'
    if out.exists() and out.read_text(encoding='utf-8')!=data:
        raise RuntimeError('Refusing to replace frozen inputs')
    out.write_text(data,encoding='utf-8')
    print(f'Frozen {len(cases())} prompts; sha256={hashlib.sha256(data.encode()).hexdigest()}')

def run(url,limit,thinking=True):
    items=json.loads((ROOT/'prompts.json').read_text(encoding='utf-8'))
    out=ROOT/('raw.jsonl' if thinking else 'raw-thinking-off.jsonl')
    if out.exists():
        raise RuntimeError('Raw run exists; refusing to overwrite or silently retry')
    started=time.monotonic()
    with out.open('x',encoding='utf-8') as fh:
        for item in items:
            if time.monotonic()-started>limit:
                print('Time budget reached; remaining prompts unattempted',flush=True)
                break
            payload={'model':'spark-study','messages':[{'role':'user','content':item['prompt']}], 'temperature':0,'seed':20260910,'max_tokens':1536,'stream':False,'chat_template_kwargs':{'enable_thinking':thinking},'cache_prompt':False}
            before=time.monotonic()
            record={'id':item['id'],'request':payload,'started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
            try:
                req=urllib.request.Request(url+'/v1/chat/completions',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
                with urllib.request.urlopen(req,timeout=180) as response:
                    record['response']=json.load(response)
            except Exception as exc:
                record['error_type']=type(exc).__name__
                record['error']='Request failed; no response is claimed. See local diagnostic log.'
            record['elapsed_seconds']=round(time.monotonic()-before,3)
            fh.write(json.dumps(record,ensure_ascii=False)+'\n'); fh.flush()
            print(f"{item['id']}: {'error' if 'error' in record else record['response']['choices'][0]['finish_reason']} ({record['elapsed_seconds']}s)",flush=True)
            if 'error' in record:
                break

def score(thinking=True):
    items={x['id']:x for x in json.loads((ROOT/'prompts.json').read_text(encoding='utf-8'))}
    results=[]
    for line in (ROOT/('raw.jsonl' if thinking else 'raw-thinking-off.jsonl')).read_text(encoding='utf-8').splitlines():
        row=json.loads(line); item=items[row['id']]
        choice=row.get('response',{}).get('choices',[{}])[0]
        content=choice.get('message',{}).get('content') or ''
        value=extract(content)
        results.append({k:item[k] for k in ['id','pair','family','language','expected']} | {'parsed':None if value is None else str(value),'correct':value==Fraction(item['expected']),'finish_reason':choice.get('finish_reason'),'elapsed_seconds':row['elapsed_seconds'],'operational_error':'error' in row})
    if len({r['id'] for r in results})!=len(results):
        raise RuntimeError('Duplicate raw item IDs')
    summary={'planned':len(items),'attempted':len(results),'unattempted':len(items)-len(results),'correct':sum(r['correct'] for r in results),'by_language':{lang:{'attempted':sum(r['language']==lang for r in results),'correct':sum(r['language']==lang and r['correct'] for r in results),'truncated':sum(r['language']==lang and r['finish_reason']=='length' for r in results)} for lang in ['en','ko']},'results':results}
    (ROOT/('scores.json' if thinking else 'scores-thinking-off.json')).write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k!='results'},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('action',choices=['freeze','run','score']); p.add_argument('--url',default='http://127.0.0.1:8770'); p.add_argument('--limit-seconds',type=int,default=1800); p.add_argument('--thinking',choices=['on','off'],default='on'); args=p.parse_args()
    if args.action=='freeze': freeze()
    elif args.action=='run': run(args.url,args.limit_seconds,args.thinking=='on')
    else: score(args.thinking=='on')
