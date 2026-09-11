# When a correct calculation never becomes an answer

An original paired Korean/English quantitative case study of **Spark-X2.5-1.7B Q4_K_M**, with a post-hoc thinking-off comparison. 24 fixed prompts per mode, 48 real local completions, no selected reruns. Prepared for possible HER Hack-Astron #6 participation.

**Status: research artifacts published; payout eligibility confirmed by the organizer on September 11; human reproduction/review and CLI-authentication clarification pending. This repository is not a formal contest entry, award or payment claim.** Codex designed the cases, implemented the scripts, operated model inference, inspected outputs and wrote this report on the account owner's authorization. The human account owner has not yet reviewed or reproduced the completed experiment. We do not claim that these AI-operated runs were personally performed by the human entrant. AI assistance will be disclosed in any eventual submission. See [official CLI acquisition verification](CLI-ACQUISITION.md) for the subsequently verified pinned artifact.

## Result

| Mode | English strict correct | Korean strict correct | Total strict correct | Length stops | Format failures | Wrong valid number |
|---|---:|---:|---:|---:|---:|---:|
| Thinking on, baseline | 7/12 | 3/12 | 10/24 | 8/24 | 4/24 | 2/24 |
| Thinking off, exploratory | 5/12 | 2/12 | 7/24 | 0/24 | 5/24 | 12/24 |

Disabling thinking eliminated length stops in this run but did **not** improve the predeclared strict answer metric. It also produced more parseable wrong numbers. This small experiment does not establish broad language capability or which mode is generally better.

See [all per-item results](RESULTS.md), [machine-readable scores](summary.json), [complete selected traces](TRACES.md), and the complete [thinking-on](raw.jsonl) / [thinking-off](raw-thinking-off.jsonl) API responses. Failed cases were retained.

## Method fixed before baseline output

Twelve original problems, each rendered in English and Korean, span discounts, percentage fee bases, whole-pack rounding, tiered charges, weighted concentration, and event intervals. Each family has two numerical variants. Korean money prompts use large-number units such as `3만 7000`; English uses `37000`. Ground truths use Python `Fraction` and independent hand-calculated checks. All 24 items form one constructed diagnostic set: no training split, exclusions, dataset sampling or public benchmark claim. Original creation is not proof of absence from model training.

The [plan](PLAN.md) and [24 prompts](prompts.json) were frozen before inference. Frozen UTF-8 prompt content SHA256: `b2977bd22fa5e02f20b5865ef0f94f7c8b56a08958892dae2769f3219d61ab4a`. On Windows the file's physical CRLF byte hash may differ; SHA256SUMS.json records physical published bytes. Baseline began 2026-09-09 16:27 UTC. The thinking-off comparison was declared **after** examining baseline outputs and before its own execution; it is exploratory. It changes the server thinking setting and request template flag, retaining every prompt and the same generation ceiling.

Each mode uses one greedy completion per prompt, temperature 0, seed 20260910, max_tokens 1536 including reasoning, no tools, no majority vote or pass@k. The runtime reports default top_p 0.95, top_k 0 and min_p 0.05; temperature zero selects greedy decoding. Context 4096, one slot, GPU offload 99 requested / 29 layers actually offloaded. Requests set cache_prompt=false; runtime logs still show shared-prefix processing, so timing is not a cache-free benchmark.

Primary score: the **last nonempty line must be a unique, case-sensitive `FINAL: <number>`**, with no units/Markdown or conflicting marker lines. Exact rational equality accepts equivalent integers, decimals or fractions. No last-number fallback. Missing, malformed and truncated answers count as incorrect, not omitted. This measures combined numeric and instruction-format success, not pure arithmetic accuracy. `RESULTS.md` separates operational failures, truncation, format and wrong numeric answers. All 48 requests completed without transport errors.

## Reasoning and delivery failures

- **discount1-ko, thinking on:** the model interprets 37000 correctly and initially obtains 29150. During checking it incorrectly subtracts 2000 from 31450 as 30450, delivering 30150. This is an arithmetic regression, not evidence that Korean large-number notation was misread.
- **pack1-ko, thinking on:** 111 required stickers means 14 whole packs. The model finds 13.875 but chooses 13 packs (104 stickers), returning 80600 without the marker. The numeric answer is wrong as well as malformed.
- **net1-ko, thinking on:** the reasoning correctly subtracts the fee and shipping, and the content is the correct bare number 73990. It fails the strict format metric only. net2-ko and tier1-ko similarly deliver correct bare numbers. Thus three of the four baseline format failures carry the right number; they are not arithmetic failures.
- **tier2-ko, thinking on:** the reasoning first overcharges, then repairs the interpretation to 5200 + 6 × 900 = 10600, but continues and hits the token ceiling without final content. Correct intermediate arithmetic is not a delivered answer.
- **time1-en, thinking on:** reasoning identifies seven intervals and a 130-second result but repeatedly debates formatting and truncates. The thinking-off answer finishes, but counts eight intervals and returns 147. Faster completion does not guarantee correctness.
- **mix1-en:** both modes use the correct salt mass 36 + 42 = 78 and total mass 300, giving 26%. Complete traces are included alongside failures. We did not establish a delivered-correct / mathematically-invalid trace in these inspected examples; we do not invent one to fill a category.

Thinking-off format failures include two lowercase `Final:` wrong answers, two correct values followed by Korean units, and time2-ko's bold `FINAL: 123` following an echoed prompt. The last three contain visibly correct terminal values but still fail the original parser. These are qualitative annotations, not a replacement score or silently relaxed metric.

## Reproduce

Python 3.12.14 standard library only; no API key or paid compute was used. Exact model and runtime downloads and commands are in [ENVIRONMENT.md](ENVIRONMENT.md). Model weights are **not** in this repository.

To re-score existing evidence (no model download or inference):

```sh
python -m unittest discover -s . -p test_study.py -v
python build_report.py
```

To reproduce inference, use a fresh directory containing the scripts and prompts but no `raw*.jsonl`. Start the pinned server with thinking on, then:

```sh
python study.py run --thinking on --limit-seconds 1800
```

Stop that server and restart the same command with `--reasoning off`, then:

```sh
python study.py run --thinking off --limit-seconds 600
python build_report.py
```

Existing raw outputs are never overwritten or silently retried. The full server logs record runtime behavior and default samplers. Five scoring/ground-truth tests passed; the report builder additionally checks exact item order, all 48 prompts, seeds, budgets, thinking flags, absence of transport errors and empty reasoning fields in off mode.

## Limits and practical use

This is a small diagnostic, not MGSM, a leaderboard submission, a random sample or a reliable estimate of Korean/English performance. Translations and instructions were AI-assisted and have not been reviewed by a human bilingual evaluator. Language, numeric notation, prompt phrasing and tokenization are confounded. The wording about requested units versus omitting units on the final line may encourage formatting rumination; no causal isolation was attempted. No confidence interval, significance test, winner probability or expected income is claimed.

Q4_K_M differs from original BF16. No full-precision, other-model or larger-budget comparison was run. Greedy results can vary across hardware/runtime versions; first requests include initialization/warm-up and other desktop load is uncontrolled. Treat timing as this run's resource record, not throughput rankings. Useful follow-up work would separate token-budget and formatting effects with a new predeclared design; it was not performed here.

All new code, prompts and report text: MIT. The underlying model is Apache-2.0; its weights remain on the official host. No contestant work was reused.

Sources: [official model](https://huggingface.co/XHToken/Spark-X2.5-1.7B), [official GGUF source](https://huggingface.co/XHToken/Spark-X2.5-1.7B-GGUF), [challenge](https://github.com/XHToken/Spark-X2.5/issues/9), [organizer AI and human-accountability clarification](https://github.com/XHToken/Spark-X2.5/issues/9#issuecomment-5578566842).
