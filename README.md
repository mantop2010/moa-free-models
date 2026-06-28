# 🤖 MoA Free Models

<div align="center">

### Mixture of Agents with **FREE** AI Models

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/mantop2010/moa-free-models.svg)](https://github.com/mantop2010/moa-free-models/stargazers)

**Use 5 different AI models together to solve complex problems — completely FREE!**

</div>

---

## 🧠 What is MoA?

**Mixture of Agents (MoA)** is a technique that uses **multiple AI models simultaneously** to solve complex problems. Instead of relying on one model, it:
1. Sends your question to **5 different models in parallel**
2. Collects all 5 responses
3. Uses an **Aggregator model** to synthesize the best answer

**Result:** More accurate, diverse, and reliable answers — at **zero cost!**

---

## ✨ Features

- ✅ **5 FREE models** working together
- ✅ **Zero cost** — all models are from OpenCode Zen free tier
- ✅ **Parallel processing** — fast execution
- ✅ **Smart aggregation** — diverse perspectives, one answer
- ✅ **Cross-platform** — Windows, macOS, Linux
- ✅ **Easy to install** — one command setup

---

## 🚀 Quick Start

### 1. Install via Hermes

```bash
# Add the skill source
hermes skills tap add https://github.com/mantop2010/moa-free-models

# Install the skill
hermes skills install moa-free-models
```

### 2. Get a Free API Key

1. Go to **[OpenCode Zen](https://opencode.ai/auth)**
2. Sign up for a free account
3. Copy your API key

### 3. Configure

```bash
# Add your API key
echo "OPENCODE_ZEN_API_KEY=your_api_key_here" >> ~/.hermes/.env

# Set the provider
hermes config set model.provider opencode-zen
```

### 4. Use It!

```bash
# In chat mode, just say:
"use MoA to solve this problem: ..."

# Or from CLI:
hermes chat -q "استخدم MoA عشان تحل المسألة دي: ما هو جذر 144 التربيعي؟"
```

---

## 🤖 Models Used

| # | Model | Source | Role | Speed |
|---|-------|--------|------|-------|
| 1 | `deepseek-v4-flash-free` | DeepSeek | 🧠 **Aggregator** | 1.5s |
| 2 | `nemotron-3-ultra-free` | NVIDIA | ⚡ Fast analysis | 0.8s |
| 3 | `north-mini-code-free` | North | 💻 Coding | 0.8s |
| 4 | `mimo-v2.5-free` | Xiaomi | 💬 Conversational | 1.4s |
| 5 | `big-pickle` | DeepSeek | 🎯 General purpose | 2.6s |

**All models cost $0!** 🆓

---

## 🏗️ Architecture

```
Your Question
    ↓
┌─────────────────────────────────────────────┐
│         5 Reference Models (parallel)        │
│                                             │
│  🧠 deepseek     ⚡ nemotron     💻 north   │
│  💬 mimo         🎯 big-pickle              │
└─────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────┐
│         Aggregator (deepseek-v4)            │
│    Synthesizes all 5 into one answer         │
└─────────────────────────────────────────────┘
                     ↓
            Final Response 🎯
```

---

## 🧪 Test Results

| Test | Input | Output | Time |
|------|-------|--------|------|
| ✅ Simple | "What is 2+2?" | "2 + 2 equals 4" | ~5s |
| ✅ Simple | "Square root of 144?" | "The square root of 144 is 12" | ~10s |
| ✅ Complex | "Write Python prime function" | Full code with comments (3462 chars) | ~15s |

---

## ⚠️ Troubleshooting

### httpx crashes on Windows
```python
# Use requests instead
import requests  # ✅ Works
# import httpx  # ❌ Fails on Windows
```

### Empty content from models
Some models return content in the `reasoning` field, not `content`:
```python
message = result["choices"][0]["message"]
content = message.get("content", "") or message.get("reasoning", "") or message.get("reasoning_content", "")
```

### API Key not found
```bash
source ~/.hermes/.env
echo $OPENCODE_ZEN_API_KEY
```

---

## 📁 Repository Structure

```
moa-free-models/
├── SKILL.md (v3.2.1)                          # Main skill documentation
├── README.md                         # This file
├── tools/
│   └── mixture_of_agents_tool_free.py  # Core MoA implementation
├── references/
│   ├── SETUP.md                      # Setup instructions
│   └── model-test-results.md         # Detailed test results
└── scripts/
    └── install.sh                    # Installation script
```

---

## 🛠️ Requirements

- **Hermes Agent** v0.17+
- **Python** 3.8+
- **Internet connection**
- **OpenCode Zen** API key (free)

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Karim Gamal** (@mantop2010)

---

## ⭐ Support

If you find this useful, **star the repo** ⭐ and share it with friends!

[![GitHub stars](https://img.shields.io/github/stars/mantop2010/moa-free-models.svg?style=social)](https://github.com/mantop2010/moa-free-models)
