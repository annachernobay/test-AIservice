PRICING_CONFIG = {
    "gpt-4o-mini": {
        "prompt_price_per_1m": 0.15,
        "completion_price_per_1m": 0.60,
    },
    "gpt-4o": {
        "prompt_price_per_1m": 2.50,
        "completion_price_per_1m": 10.00,
    },
}


def calculate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    if model not in PRICING_CONFIG:
        raise ValueError(f"Модель '{model}' не підтримується для розрахунку вартості.")

    config = PRICING_CONFIG[model]
    
    prompt_cost = (prompt_tokens / 1_000_000) * config["prompt_price_per_1m"]
    completion_cost = (completion_tokens / 1_000_000) * config["completion_price_per_1m"]
    
    return round(prompt_cost + completion_cost, 6)