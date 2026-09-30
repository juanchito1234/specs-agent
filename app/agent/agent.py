from app.llm.client import generate_response
from app.agent.prompt import SYSTEM_PROMPT


def process_message(
    history,
    api_key,
    model
):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(history)

    return generate_response(
        api_key,
        model,
        messages,
        max_tokens=16384
    )


def generate_title(user_message, api_key, model):
    prompt = [
        {
            "role": "system",
            "content": (
                "Eres una IA encargada de resumir preguntas de usuarios en un título "
                "de conversación muy breve, conciso e informativo (entre 3 y 6 palabras). "
                "No uses comillas, ni símbolos innecesarios, ni prefijos como 'Título:'. "
                "Responde únicamente con el título en el mismo idioma de la pregunta."
            )
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

    try:
        title = generate_response(api_key, model, prompt, max_tokens=100)
        title = title.strip().strip('"').strip("'").strip('`')
        if len(title) > 60:
            title = title[:57] + "..."
        return title if title else user_message[:30]
    except Exception:
        return user_message[:30]

