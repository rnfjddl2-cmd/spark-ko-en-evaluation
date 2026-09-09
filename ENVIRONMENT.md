# Pinned artifacts and actual environment

- Windows x86_64, Python 3.12.14, standard library urllib client.
- CPU Intel Core i5-12400F, 6 physical cores / 12 threads; installed RAM 32 GiB.
- GPU NVIDIA GeForce RTX 3060 Ti, runtime-reported 8024 MiB VRAM. Vulkan backend; 29/29 model layers offloaded. No cloud GPU or paid endpoint.
- llama.cpp release **b10828**, build commit **3ad1ba733**, version **0.4.0-dev**, built with Clang 20.1.8.
- Runtime archive: https://github.com/ggml-org/llama.cpp/releases/download/b10828/llama-b10828-bin-win-vulkan-x64.zip
- Runtime ZIP SHA256: `c8e8252564713b26ca55902fe1e3dd24d0dd5b8009726f96b773a9f3533d8ec7`.
- Official model repository: `XHToken/Spark-X2.5-1.7B-GGUF`.
- Exact revision: `23e1fcac55e7dd71e4c12a23723cc228ba0e5e85`.
- Filename: `Spark-X2.5-1.7B-Q4_K_M.gguf`, 1,107,457,856 bytes, Q4_K_M (mixed q4_K/q6_K/f32 tensors).
- Model SHA256: `902bde2522394954ac17821b3e5fd0df02defbc6944f122253f2580acf0503f4`.
- Pinned download: https://huggingface.co/XHToken/Spark-X2.5-1.7B-GGUF/resolve/23e1fcac55e7dd71e4c12a23723cc228ba0e5e85/Spark-X2.5-1.7B-Q4_K_M.gguf

The public pinned artifact was downloaded by HTTPS without authentication. No Hugging Face CLI login was performed because the user has no account yet. The event's stated CLI sign-in step and eligibility need resolution before claiming a conforming entry; this report does not imply that an unauthenticated download satisfied every administrative step. No model weight is uploaded here.

Actual server command from workspace root (loopback endpoint only):

```powershell
work/spark-runtime/bin/llama-server.exe -m work/spark-runtime/Spark-X2.5-1.7B-Q4_K_M.gguf --host 127.0.0.1 --port 8770 -c 4096 -np 1 -ngl 99 --alias spark-study --reasoning on --reasoning-format deepseek --jinja --cors-origins localhost -lv 4
```

For the exploratory off run, that process was stopped and the identical command was started with `--reasoning off`. Both logs are published as runtime-thinking-on.log and runtime-thinking-off.log. These server processes were stopped after their runs to release GPU memory. The path shown is a portable workspace-relative artifact path, not a user's private cache.

Actual client commands (Python executable location omitted to protect local username; Python version above):

```powershell
python outputs/spark-evaluation/study.py freeze
python -m unittest discover -s outputs/spark-evaluation -v
python outputs/spark-evaluation/study.py run --limit-seconds 1800
python outputs/spark-evaluation/study.py score
# Server restarted with --reasoning off; post-hoc plan recorded first.
python outputs/spark-evaluation/study.py run --thinking off --limit-seconds 600
python outputs/spark-evaluation/study.py score --thinking off
python -m unittest discover -s outputs/spark-evaluation -v
python outputs/spark-evaluation/build_report.py
```

Raw responses contain exact UTC start timestamps, each request's prompt/parameters, all returned reasoning and content, token counts, latency, finish reason and runtime fingerprint. There is no self-consistency, tool-use or chosen-best output. The 60-minute initial work cap and 10-minute exploratory execution cap were used to constrain this opportunity; pauses between chat turns are not paid work. Additional service charges: US$0. Electricity and sunk subscription/hardware costs were not measured or attributed as new purchases.

Published server logs decode as UTF-8 with invalid byte sequences represented as literal backslash-x escapes. This affects truncated tokenizer metadata previews; original local logs are retained. Raw inference JSON responses are unchanged.
