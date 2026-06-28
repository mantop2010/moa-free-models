#!/usr/bin/env python3
"""
Mixture-of-Agents Tool Module (Portable — works on any system)

Uses FREE models from OpenCode Zen for cost-free multi-model reasoning.
To use: set OPENCODE_ZEN_API_KEY in your .env file.

Based on: "Mixture-of-Agents Enhances Large Language Model Capabilities"
by Junlin Wang et al. (arXiv:2406.04692v1)
"""

import json
import logging
import os
import asyncio
import datetime
from typing import Dict, Any, List, Optional
import requests
from tools.debug_helpers import DebugSession

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════
# CONFIGURATION — Edit these to customize
# ═══════════════════════════════════════════════════

# FREE models from OpenCode Zen
REFERENCE_MODELS = [
    "deepseek-v4-flash-free",      # DeepSeek - excellent for reasoning ✅
    "nemotron-3-ultra-free",       # NVIDIA Nemotron - strong analysis ✅
    "north-mini-code-free",        # North - good for coding ✅
    "mimo-v2.5-free",              # Xiaomi MiMo - conversational ✅
    "big-pickle",                  # DeepSeek - general purpose ✅
]

AGGREGATOR_MODEL = "deepseek-v4-flash-free"

# API Configuration
OPENCODE_ZEN_API_BASE = "https://opencode.ai/zen/v1"
OPENCODE_ZEN_API_KEY_ENV = "OPENCODE_ZEN_API_KEY"

# Temperature settings
REFERENCE_TEMPERATURE = 0.6
AGGREGATOR_TEMPERATURE = 0.4
MIN_SUCCESSFUL_REFERENCES = 1

# System prompt for the aggregator
AGGREGATOR_SYSTEM_PROMPT = """You have been provided with a set of responses from various open-source models to the latest user query. Your task is to synthesize these responses into a single, high-quality response. It is crucial to critically evaluate the information provided in these responses, recognizing that some of it may be biased or incorrect. Your response should not simply replicate the given answers but should offer a refined, accurate, and comprehensive reply to the instruction. Ensure your response is well-structured, coherent, and adheres to the highest standards of accuracy and reliability.

Responses from models:"""

_debug = DebugSession("moa_tools_free", env_var="MOA_TOOLS_FREE_DEBUG")


# ═══════════════════════════════════════════════════
# API KEY LOADING — Works across all systems
# ═══════════════════════════════════════════════════

def _load_api_key():
    """Load API key from environment or .env file (cross-platform)."""
    # 1. Try environment variable
    api_key = os.getenv(OPENCODE_ZEN_API_KEY_ENV)
    if api_key:
        return api_key

    # 2. Try common .env locations
    home = os.path.expanduser("~")
    env_paths = [
        os.path.join(home, ".hermes", ".env"),
        os.path.join(home, ".env"),
        ".env",
    ]
    for env_path in env_paths:
        try:
            with open(env_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith(f"{OPENCODE_ZEN_API_KEY_ENV}=") and not line.startswith("#"):
                        return line.split("=", 1)[1]
        except:
            continue

    return None


# ═══════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════

def _construct_aggregator_prompt(system_prompt: str, responses: List[str]) -> str:
    response_text = "\n".join([f"{i+1}. {response}" for i, response in enumerate(responses)])
    return f"{system_prompt}\n\n{response_text}"


def _extract_content(result: dict) -> str:
    """Extract content from response handling all field names (cross-model)."""
    message = result.get("choices", [{}])[0].get("message", {})
    return message.get("content", "") or message.get("reasoning", "") or message.get("reasoning_content", "")


# ═══════════════════════════════════════════════════
# REFERENCE MODELS (parallel execution)
# ═══════════════════════════════════════════════════

async def _run_reference_model_safe(
    model: str,
    user_prompt: str,
    temperature: float = REFERENCE_TEMPERATURE,
    max_tokens: int = 32000,
    max_retries: int = 6
) -> tuple[str, str, bool]:
    for attempt in range(max_retries):
        try:
            logger.info("Querying %s (attempt %s/%s)", model, attempt + 1, max_retries)

            api_key = _load_api_key()
            if not api_key:
                raise ValueError(f"{OPENCODE_ZEN_API_KEY_ENV} not set")

            response = requests.post(
                f"{OPENCODE_ZEN_API_BASE}/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": user_prompt}],
                    "max_tokens": max_tokens,
                    "temperature": temperature
                },
                timeout=120.0
            )
            response.raise_for_status()
            content = _extract_content(response.json())

            if not content:
                logger.warning("%s empty (attempt %s/%s), retrying", model, attempt + 1, max_retries)
                if attempt < max_retries - 1:
                    await asyncio.sleep(min(2 ** (attempt + 1), 60))
                    continue

            logger.info("%s responded (%s chars)", model, len(content))
            return model, content, True

        except Exception as e:
            error_str = str(e)
            logger.warning("%s error (attempt %s): %s", model, attempt + 1, error_str)

            if attempt < max_retries - 1:
                wait = min(2 ** (attempt + 1), 60)
                await asyncio.sleep(wait)
            else:
                return model, f"{model} failed: {error_str}", False


# ═══════════════════════════════════════════════════
# AGGREGATOR MODEL
# ═══════════════════════════════════════════════════

async def _run_aggregator_model(
    system_prompt: str, user_prompt: str,
    temperature: float = AGGREGATOR_TEMPERATURE, max_tokens: int = None
) -> str:
    logger.info("Running aggregator: %s", AGGREGATOR_MODEL)
    api_key = _load_api_key()
    if not api_key:
        raise ValueError(f"{OPENCODE_ZEN_API_KEY_ENV} not set")

    payload = {
        "model": AGGREGATOR_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": temperature
    }
    if max_tokens:
        payload["max_tokens"] = max_tokens

    resp = requests.post(
        f"{OPENCODE_ZEN_API_BASE}/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json=payload, timeout=120.0
    )
    resp.raise_for_status()
    content = _extract_content(resp.json())

    if not content:
        logger.warning("Aggregator empty, retrying once")
        resp = requests.post(
            f"{OPENCODE_ZEN_API_BASE}/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json=payload, timeout=120.0
        )
        resp.raise_for_status()
        content = _extract_content(resp.json())

    return content


# ═══════════════════════════════════════════════════
# MAIN TOOL
# ═══════════════════════════════════════════════════

async def mixture_of_agents_tool(
    user_prompt: str,
    reference_models: Optional[List[str]] = None,
    aggregator_model: Optional[str] = None
) -> str:
    """
    Process a complex query using Mixture-of-Agents with FREE models.

    Args:
        user_prompt: The complex query to solve
        reference_models: Custom reference models (defaults to REFERENCE_MODELS)
        aggregator_model: Custom aggregator (defaults to AGGREGATOR_MODEL)

    Returns:
        JSON string with {success, response, models_used, processing_time}
    """
    start = datetime.datetime.now()

    try:
        if not _load_api_key():
            raise ValueError(f"{OPENCODE_ZEN_API_KEY_ENV} not set")

        ref_models = reference_models or REFERENCE_MODELS
        agg_model = aggregator_model or AGGREGATOR_MODEL

        logger.info("MoA starting with %d free models", len(ref_models))

        # Layer 1: Parallel reference models
        results = await asyncio.gather(*[
            _run_reference_model_safe(m, user_prompt) for m in ref_models
        ])

        successes = [c for _, c, s in results if s]
        failed = [m for m, _, s in results if not s]

        if len(successes) < MIN_SUCCESSFUL_REFERENCES:
            raise ValueError(
                f"Need {MIN_SUCCESSFUL_REFERENCES} successful models, got {len(successes)}"
            )

        # Layer 2: Aggregate
        agg_prompt = _construct_aggregator_prompt(AGGREGATOR_SYSTEM_PROMPT, successes)
        final = await _run_aggregator_model(agg_prompt, user_prompt)

        elapsed = (datetime.datetime.now() - start).total_seconds()

        return json.dumps({
            "success": True,
            "response": final,
            "models_used": {
                "reference_models": ref_models,
                "aggregator_model": agg_model
            },
            "processing_time": elapsed
        }, indent=2, ensure_ascii=False)

    except Exception as e:
        logger.error("MoA failed: %s", e)
        return json.dumps({
            "success": False,
            "response": "MoA processing failed.",
            "error": str(e)
        }, indent=2, ensure_ascii=False)


def check_moa_requirements() -> bool:
    """Check if API key is configured."""
    return bool(_load_api_key())


def get_moa_configuration() -> Dict[str, Any]:
    """Get current MoA configuration."""
    return {
        "reference_models": REFERENCE_MODELS,
        "aggregator_model": AGGREGATOR_MODEL,
        "total_reference_models": len(REFERENCE_MODELS),
        "cost": "FREE (all models from OpenCode Zen free tier)"
    }


if __name__ == "__main__":
    print("🤖 MoA Free Models — Portable Edition")
    print(f"✅ API Key: {'available' if check_moa_requirements() else 'MISSING'}")
    print(f"📋 Models: {len(REFERENCE_MODELS)} free reference + 1 aggregator")
