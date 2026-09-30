import streamlit as st
from app.chat.chat_service import send_message
from app.services.conversation_service import load_conversation


def render_chat():

    conversation_id = (
        st.session_state.get(
            "conversation_id"
        )
    )

    if conversation_id is None:

        st.info(
            "Selecciona una conversación "
            "o crea una nueva."
        )

        return

    conversation, messages = load_conversation(
        conversation_id
    )

    for message in messages:

        with st.chat_message(message.role):
            st.markdown(message.content)

    prompt = st.chat_input(
        "Escribe un mensaje..."
    )

    if prompt:

        api_key = st.session_state.get(
            "groq_api_key"
        )

        model = st.session_state.get(
            "selected_model"
        )

        if not api_key:

            st.warning(
                "Configura una API Key de Groq "
                "en el panel lateral."
            )

            return

        if not model:

            st.warning(
                "Selecciona un modelo de Groq "
                "en el panel lateral."
            )

            return

        send_message(
            conversation_id,
            prompt,
            api_key,
            model
        )

        st.rerun()