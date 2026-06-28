# MoA Free Models — Test Results

## Individual Model Tests

| Model | Status | Speed | Response |
|-------|--------|-------|----------|
| deepseek-v4-flash-free | ✅ Working | 1.5-2.0s | "four" |
| nemotron-3-ultra-free | ✅ Working | 0.8-12.6s | "Four" |
| north-mini-code-free | ✅ Working | 0.8-6.9s | "four" |
| mimo-v2.5-free | ✅ Working | 1.4-3.1s | "Four" |
| big-pickle | ✅ Working | 2.6s | "4" |

## Full Pipeline Tests

| Test | Prompt | Result | Time |
|------|--------|--------|------|
| Simple | "What is 2+2?" | "2 + 2 equals 4." | ~4-15s |
| Simple | "What is 5+3?" | "5 plus 3 equals 8." | ~4-15s |
| Simple | "Square root of 144?" | "The square root of 144 is 12." | ~10-30s |
| Complex | "Python prime function" | Full code with comments (3462 chars) | ~10-30s |

## Failed Models

| Model | Error |
|-------|-------|
| qwen3.6-plus-free | 401 Unauthorized |
| minimax-m3-free | 401 Unauthorized |

## Platform

- **OS:** Windows 10 (git-bash)
- **Python:** 3.11.8
- **HTTP library:** requests (httpx fails on Windows)
- **API:** OpenCode Zen v1 (https://opencode.ai/zen/v1)

## Notes
- Models using deepseek internally return content in `reasoning` field
- Aggregator temperature: 0.4 (focused synthesis)
- Reference temperature: 0.6 (balanced creativity)
- Min successful references: 1 (tolerates 4 failures)
