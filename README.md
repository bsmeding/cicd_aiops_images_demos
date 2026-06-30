# AIOps CI/CD Demo Pipelines

Demo repository showing how to use the [`bsmeding/aiops_cicd_*`](https://hub.docker.com/r/bsmeding/aiops_cicd_ubuntu) Docker images in real CI/CD pipelines.

These images include LLM clients (OpenAI, Anthropic, LiteLLM), evaluation frameworks (DeepEval, Ragas), agent tooling (LangChain, LangGraph), and operational API libraries (pynautobot, pynetbox). They are built for testing AI-assisted network and infrastructure automation pipelines — not for running production agents.

Blog posts:
- [AIOps CI/CD images – bartsmeding.nl](https://bartsmeding.nl/docker/docker_container_aiops_cicd/)
- [AIOps CI/CD Docker Images for LLM, Agent, Prompt, and RAG Testing – netdevops.it](https://netdevops.it/blog/aiops-cicd-docker-images-for-llm-agent-prompt-and-rag-testing/)

Source images: [github.com/bsmeding/docker_containers_aiops_cicd](https://github.com/bsmeding/docker_containers_aiops_cicd)

---

## Repository layout

```
.github/workflows/
  weekly_demo.yml          # Weekly scheduled run of all demo jobs
  prompt_regression.yml    # PR/push: prompt contract tests
  structured_output.yml    # PR: structured output / JSON schema validation
  rag_evaluation.yml       # PR + manual: RAG quality evaluation
  llm_smoke.yml            # Manual only: live LLM smoke test

.gitlab-ci.yml             # GitLab CI equivalent (agent + replay stages)
Jenkinsfile                # Jenkins declarative pipeline

src/
  prompt_runner.py         # Thin LiteLLM wrapper used by tests
  toolbox.py               # Fake toolbox for agent tests

tests/
  conftest.py
  prompts/
    test_incident_router.py
  agents/
    test_nautobot_agent.py
  contracts/
    test_json_schemas.py
  rag/
    test_runbook_rag.py
  replay/
    test_incident_replay.py
  provider_smoke/
    test_llm_smoke.py

tools/
  llm_smoke.py             # Quick LiteLLM smoke check script
  validate_json_schemas.py # Stand-alone schema validator

schemas/
  incident_triage.json
  device_lookup.json

eval/
  run_ragas.py
  datasets/
    network_runbooks.jsonl

replay/
  run_replay.py
  check_regressions.py
  incidents/
    bgp_flap.jsonl
    interface_down.jsonl

rag/
  build_index.py

docs/runbooks/
  bgp_recovery.md
  interface_troubleshooting.md
```

---

## Secrets required

| Secret | Used by |
|---|---|
| `OPENAI_API_KEY` | prompt tests, RAG eval, LLM smoke |
| `ANTHROPIC_API_KEY` | LLM smoke (optional) |

Deterministic tests (contracts, replay, schema validation) run without any secrets.

---

## Running locally

```bash
docker run --rm -it \
  -v "$PWD:/work" \
  -w /work \
  -e OPENAI_API_KEY \
  -e ANTHROPIC_API_KEY \
  bsmeding/aiops_cicd_ubuntu:latest \
  bash

# Inside the container:
ruff check .
pytest tests/contracts tests/replay -vv
pytest tests/prompts -vv          # requires OPENAI_API_KEY
python eval/run_ragas.py --dataset eval/datasets/network_runbooks.jsonl
```

---

## Available image tags

| Image | Base |
|---|---|
| `bsmeding/aiops_cicd_ubuntu:latest` | Ubuntu 26.04 |
| `bsmeding/aiops_cicd_ubuntu2404:latest` | Ubuntu 24.04 |
| `bsmeding/aiops_cicd_ubuntu2604:latest` | Ubuntu 26.04 |
| `bsmeding/aiops_cicd_debian:latest` | Debian 13 |
| `bsmeding/aiops_cicd_rockylinux:latest` | Rocky Linux 9 |
| `bsmeding/aiops_cicd_alpine3:latest` | Alpine 3.23 |
