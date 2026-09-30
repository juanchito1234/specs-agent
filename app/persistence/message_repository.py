from app.models.message import Message
from app.persistence.database import get_db


def create_message(
    conversation_id,
    role,
    content
):

    db = get_db()

    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    db.close()

    return message


def get_messages(conversation_id):

    db = get_db()

    messages = (
        db.query(Message)
        .filter(
            Message.conversation_id == conversation_id
        )
        .order_by(Message.created_at.asc())
        .all()
    )

    db.close()

    return messages