import streamlit as st

from app.persistence.database import Base, engine

from app.models.conversation import Conversation
from app.models.message import Message


Base.metadata.create_all(engine)

from app.ui.chat import render_chat
from app.ui.sidebar import render_sidebar


st.set_page_config(
    page_title="Agente de Especificaciones",
    page_icon="📋",
    layout="wide"
)

st.title("Agente de Especificaciones")

render_sidebar()
render_chat()