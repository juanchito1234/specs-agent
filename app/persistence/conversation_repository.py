from app.models.conversation import Conversation
from app.persistence.database import get_db


def create_conversation(title="Nueva conversación"):

    db = get_db()

    conversation = Conversation(
        title=title
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    db.close()

    return conversation


def get_conversations():

    db = get_db()

    conversations = (
        db.query(Conversation)
        .order_by(Conversation.updated_at.desc())
        .all()
    )

    db.close()

    return conversations


def get_conversation(conversation_id):

    db = get_db()

    conversation = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id)
        .first()
    )

    db.close()

    return conversation


def update_conversation_title(conversation_id, title):

    db = get_db()

    conversation = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id)
        .first()
    )

    if conversation:
        conversation.title = title
        db.commit()
        db.refresh(conversation)

    db.close()

    return conversation


def delete_conversation(conversation_id):

    db = get_db()

    conversation = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id)
        .first()
    )

    if conversation:
        db.delete(conversation)
        db.commit()

    db.close()
