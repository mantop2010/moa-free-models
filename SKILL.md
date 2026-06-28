---
name: moa-free-models
description: "Mixture of Agents with FREE models from OpenCode Zen — setup, model selection, common pitfalls"
version: 3.2.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [moa, mixture-of-agents, free, opencode-zen, opencode-free-models]
    homepage: https://opencode.ai
---

# MoA Free Models

Mixture of Agents using **free-tier models** from OpenCode Zen. All models cost **$0**.

## 📦 Installation

```bash
# 1. تأكد إن عندك Node.js
node --version

# 2. احصل على API Key من https://opencode.ai/auth
#    وخزنها في .env:
echo "OPENCODE_ZEN_API_KEY=*** ~/.hermes/.env

# 3. فعّل OpenCode Zen provider
hermes config set model.provider opencode-zen

# 4. لو عايز ترجع لـ OpenRouter بعدين:
# hermes config set model.provider openrouter
```

## ✅ Working Free Models

| Model | Speed | Role |
|-------|-------|------|
| `deepseek-v4-flash-free` | 1.5s | **Aggregator** — best synthesis quality |
| `nemotron-3-ultra-free` | 0.8s | Reference — fast analysis |
| `north-mini-code-free` | 0.8s | Reference — coding tasks |
| `mimo-v2.5-free` | 1.4s | Reference — conversational |
| `big-pickle` | 2.6s | Reference — general purpose |

## ❌ Failed Models (Do NOT use)

- `qwen3.6-plus-free` — 401 Unauthorized
- `minimax-m3-free` — 401 Unauthorized

## 🚀 Usage

```python
from tools.mixture_of_agents_tool_free import mixture_of_agents_tool
import asyncio

result = await mixture_of_agents_tool(
    user_prompt="Your complex question here"
)
```

## 🧪 Test It

```bash
hermes chat -q "استخدم MoA عشان تحل المسألة دي: ما هو جذر 144 التربيعي؟"
```

## 🔧 Troubleshooting

### ⚠️ httpx crashes on Windows
استخدم `requests` بدل `httpx` — httpx بيعمل crash على Windows بالـ error `[Errno 2] No such file or directory`.

### ⚠️ Empty content from models
بعض الموديلات بترد في `reasoning` أو `reasoning_content` مش `content`:
```python
message = result["choices"][0]["message"]
content = message.get("content", "") or message.get("reasoning", "") or message.get("reasoning_content", "")
```

### ⚠️ API Key not loading
```bash
source ~/.hermes/.env
echo $OPENCODE_ZEN_API_KEY
```

### ⚠️ Timeout with 5 models
لو الـ 5 موديلات أبطأ من المتوقع، قلّل العدد أو استخدم `MIN_SUCCESSFUL_REFERENCES = 1`.

## 📁 Files

| File | Purpose |
|------|---------|
| `tools/mixture_of_agents_tool_free.py` | Main MoA implementation (portable) |
| `references/model-test-results.md` | Test results detail |
| `references/portable-setup.md` | Cross-platform setup for sharing |
| `references/SETUP.md` | Quick start guide |
| `references/github-publishing.md` | How to publish on GitHub for friends |
| `scripts/install.sh` | One-click installer |

## 📤 Sharing with Friends

To share this skill with others, the friend needs:
1. **API Key** from https://opencode.ai/auth (free)
2. **GitHub** repo or direct file transfer

Full guide: `references/github-publishing.md`

## 📜 License

MIT — use freely, share with anyone!
