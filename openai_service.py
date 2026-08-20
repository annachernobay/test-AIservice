def generate_response(model: str, messages: list):

    last_user_msg = messages[-1]["content"] if messages else ""

    mock_reply = f"[MOCK RESPONSE] Відповідь на запит: '{last_user_msg}'"

    prompt_tokens = len(last_user_msg.split()) + 5
    completion_tokens = len(mock_reply.split())

    return mock_reply, prompt_tokens, completion_tokens