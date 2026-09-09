# Spark-X2.5 bilingual quantity evaluation — frozen plan

Prepared 2026-09-10 for possible HER Hack-Astron #6 entry. This is not an entry, award or receipt. International payout eligibility is awaiting organizer clarification. The sole human entrant must review the completed work before submission. AI assistance in design, implementation, orchestration and writing will be disclosed.

Budget: US$0 extra spending; at most 60 minutes for preparation and initial execution. Stop on persistent runtime failure; do not buy cloud compute. Publication requires Hugging Face login and human review. Do not repeat external inquiries while awaiting a reply.

Question: Does the same small local model preserve exact quantitative answers when an original English word problem is rendered in Korean, including Korean large-number units?

Design fixed before viewing evaluation outputs: 12 independently specified problems, each in English and Korean, 24 calls total. Six families each with two numerical variants: percentage discounts, net sale proceeds, package ceiling, tiered charges, weighted mixtures and event timing. Ground truths are computed with exact Fraction arithmetic and independently checked with hand examples. Every item and output is retained. No item selection based on model performance. Synthetic units and people; not financial advice or real transactions.

One completion per prompt. Greedy decoding (temperature 0, seed 20260910), max_tokens 1536, thinking on, same token ceiling for both languages. Request a short derivation plus `FINAL: <number>` in the specified unit. Exact rational comparison of the final marker; missing/malformed/conflicting markers are incorrect. No last-number fallback. Report final accuracy separately from reasoning inspection and truncation. Paired results are descriptive only: this tiny constructed set is not MGSM, random population sampling, or evidence of broad language proficiency. Korean tokenization may increase budget pressure.

Model: official XHToken/Spark-X2.5-1.7B-GGUF, revision 23e1fcac55e7dd71e4c12a23723cc228ba0e5e85, Q4_K_M. Quantization differs from original BF16. Runtime: official llama.cpp b10828 Windows Vulkan build; record actual device offload and version. Retain SHA256, requests, full JSON responses and timing. Model weights stay local and are never published.

All original scripts, prompts and report text will be MIT licensed. No third-party contestant code, dataset or outputs are reused.

## Exploratory addition, declared before its outputs

After inspecting the complete thinking-on baseline (10/24 strict correct, 8 length stops), run exactly one thinking-off ablation on ALL the same 24 frozen prompts. This is a post-hoc diagnostic, not a preregistered confirmatory result. Restart the same server with `--reasoning off`; set request enable_thinking=false. Keep weights, seed, greedy decoding, 1536-token ceiling and scoring unchanged. Preserve baseline raw.jsonl and put new outputs in raw-thinking-off.jsonl. No selective reruns or new prompts. Report missing final markers separately from wrong numeric answers. Budget for this addition: 10 minutes; no paid compute.
