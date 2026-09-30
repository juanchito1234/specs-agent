from app.agent.agent import process_message, generate_title

from app.persistence.message_repository import (
    create_message,
    get_messages
)

from app.persistence.conversation_repository import (
    get_conversation,
    update_conversation_title
)


def send_message(
    conversation_id,
    user_message,
    api_key,
    model
):

    # Check if conversation needs title update
    conversation = get_conversation(conversation_id)
    if conversation and conversation.title == "Nueva conversación":
        new_title = generate_title(user_message, api_key, model)
        if new_title:
            update_conversation_title(conversation_id, new_title)

    create_message(
        conversation_id,
        "user",
        user_message
    )

    messages = get_messages(
        conversation_id
    )

    history = [
        {
            "role": message.role,
            "content": message.content
        }
        for message in messages
    ]

    response = process_message(
        history,
        api_key,
        model
    )

    create_message(
        conversation_id,
        "assistant",
        response
    )

    return response