# Official CLI acquisition check — 2026-09-11

This is acquisition evidence, not an additional inference run, human review, or contest submission.

- Official `huggingface_hub` package: **1.31.0**, installed from PyPI into an isolated workspace dependency directory.
- Python: **3.12.14**, Windows x86_64.
- Invocation used the package's registered console entry point (`huggingface_hub.cli.hf:main`), with the following CLI arguments:

```text
hf download XHToken/Spark-X2.5-1.7B-GGUF Spark-X2.5-1.7B-Q4_K_M.gguf --revision 23e1fcac55e7dd71e4c12a23723cc228ba0e5e85 --local-dir work/spark-runtime --format agent
```

The command exited **0** and returned the existing local artifact path. The private absolute workspace prefix is omitted here. Implicit token use and telemetry were disabled. The command warned that the request was unauthenticated.

The CLI-generated download metadata recorded:

```text
revision: 23e1fcac55e7dd71e4c12a23723cc228ba0e5e85
etag: 902bde2522394954ac17821b3e5fd0df02defbc6944f122253f2580acf0503f4
```

A separate local SHA-256 calculation returned the same digest:

```text
902bde2522394954ac17821b3e5fd0df02defbc6944f122253f2580acf0503f4
```

This matches the artifact recorded before the original 48 completions. The check reused the existing file; no new model execution or changed score is claimed.

`hf auth whoami` reported not logged in. The proposed browser OAuth grant was declined and no CLI account authorization was completed. The event's `hf auth login` instruction remains an administrative requirement pending organizer clarification; a successful public download alone is not assumed to satisfy it.

References: [official CLI documentation](https://huggingface.co/docs/huggingface_hub/guides/cli), [event requirements](https://github.com/XHToken/Spark-X2.5/issues/9), [pinned public artifact](https://huggingface.co/XHToken/Spark-X2.5-1.7B-GGUF/resolve/23e1fcac55e7dd71e4c12a23723cc228ba0e5e85/Spark-X2.5-1.7B-Q4_K_M.gguf).
