# 🤖 MoA Free Models — Mixture of Agents with FREE AI Models

## 📋 Overview
Use **5 different AI models** together to solve complex problems — **completely FREE**.

No API costs. No subscriptions. Just smart collaboration between models.

## 🚀 Quick Start

### 1. Get a Free API Key
- Go to [https://opencode.ai/auth](https://opencode.ai/auth)
- Sign up for a free account
- Copy your API key

### 2. Install the Skill
```bash
hermes skills install moa-free-models
```

### 3. Set Your API Key
```bash
echo "OPENCODE_ZEN_API_KEY=your_k...n### 4. Enable Provider
```bash
hermes config set model.provider opencode-zen
```

### 5. Restart & Use
```bash
/reset
hermes chat -q "solve this complex problem using MoA: ..."
```

## 🧠 Architecture
```
User Question → 5 Free Models (parallel) → Aggregator → Final Answer
```

## ✅ Requirements
- Node.js 18+
- Hermes Agent v0.17+
- Internet connection

## 📜 License
MIT — Use freely, share with anyone!
