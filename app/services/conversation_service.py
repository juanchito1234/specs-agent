from app.persistence.conversation_repository import (
    create_conversation,
    get_conversations,
    get_conversation,
    update_conversation_title,
    delete_conversation
)

from app.persistence.message_repository import (
    get_messages
)

from app.agent.agent import generate_title


def new_conversation():

    return create_conversation()


def list_conversations():

    return get_conversations()


def load_conversation(conversation_id):

    conversation = get_conversation(
        conversation_id
    )

    messages = get_messages(
        conversation_id
    )

    return conversation, messages


def update_title(conversation_id, title):

    return update_conversation_title(conversation_id, title)


def auto_generate_missing_titles(api_key, model):
    """
    Recorre las conversaciones que aún tienen el título por defecto 'Nueva conversación'
    y, si ya tienen mensajes del usuario, genera un título automático con el agente.
    """
    if not api_key or not model:
        return

    conversations = get_conversations()

    for conv in conversations:
        if conv.title == "Nueva conversación":
            messages = get_messages(conv.id)
            user_messages = [m for m in messages if m.role == "user"]
            if user_messages:
                first_query = user_messages[0].content
                new_title = generate_title(first_query, api_key, model)
                if new_title and new_title != "Nueva conversación":
                    update_conversation_title(conv.id, new_title)


def remove_conversation(conversation_id):

    delete_conversation(conversation_id)
