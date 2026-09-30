import os
import streamlit as st
from dotenv import load_dotenv

from app.services.conversation_service import (
    new_conversation,
    list_conversations,
    remove_conversation,
    auto_generate_missing_titles
)

load_dotenv()


def init_api_keys():
    """Inicializa la lista de API Keys con la clave por defecto del archivo .env si existe."""
    if "api_keys" not in st.session_state:
        env_key = os.getenv("GROQ_API_KEY", "")
        st.session_state.api_keys = {}
        if env_key:
            st.session_state.api_keys["Default (.env)"] = env_key
        else:
            st.session_state.api_keys["Key 1"] = ""

    if "active_api_key_name" not in st.session_state:
        if "Default (.env)" in st.session_state.api_keys:
            st.session_state.active_api_key_name = "Default (.env)"
        elif st.session_state.api_keys:
            st.session_state.active_api_key_name = list(st.session_state.api_keys.keys())[0]


def render_sidebar():

    init_api_keys()

    with st.sidebar:
        # Estilos CSS personalizados para una interfaz estética y organizada
        st.markdown(
            """
            <style>
            .sidebar-header {
                display: flex;
                align-items: center;
                gap: 10px;
                padding: 5px 0px;
            }
            .sidebar-title {
                font-size: 1.25rem;
                font-weight: 700;
                color: var(--text-color);
                margin: 0;
            }
            .section-badge {
                display: inline-block;
                padding: 3px 10px;
                border-radius: 12px;
                font-size: 0.78rem;
                font-weight: 600;
                margin-bottom: 10px;
                background-color: rgba(99, 102, 241, 0.15);
                color: #6366f1;
            }
            .stButton > button {
                border-radius: 8px;
                transition: all 0.2s ease-in-out;
                background-color: #1e3a5f;
                color: white;
                border: 1px solid #2e5a87;
            }
            .stButton > button[kind="primary"]:hover {
                background-color: #264a73;
                color: white;
                border: 1px solid #264a73
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Encabezado principal
        st.markdown(
            """
            <div class="sidebar-header">
                <span style="font-size: 1.6rem;">📋</span>
                <span class="sidebar-title">Specs Agent</span>
            </div>
            <p style="font-size: 0.82rem; color: gray; margin-top: -5px; margin-bottom: 15px;">
                Asistente Inteligente de Especificaciones
            </p>
            """,
            unsafe_allow_html=True
        )

        # Botón de acción: Nueva conversación
        if st.button(
            "➕ Nueva conversación",
            use_container_width=True,
            type="primary"
        ):
            conversation = new_conversation()
            st.session_state.conversation_id = conversation.id
            st.rerun()

        st.markdown("---")

        # Sección 1: Configuración del modelo y API Keys
        st.markdown('<span class="section-badge">⚙️ CONFIGURACIÓN LLM</span>', unsafe_allow_html=True)
        
        # Selección de API Key activa
        key_names = list(st.session_state.api_keys.keys())
        if not key_names:
            st.session_state.api_keys["Default (.env)"] = os.getenv("GROQ_API_KEY", "")
            key_names = list(st.session_state.api_keys.keys())

        current_name = st.session_state.get("active_api_key_name", key_names[0])
        if current_name not in key_names:
            current_name = key_names[0]
            st.session_state.active_api_key_name = current_name

        selected_key_name = st.selectbox(
            "API Key Seleccionada",
            options=key_names,
            index=key_names.index(current_name),
            key="selected_key_name_widget"
        )
        st.session_state.active_api_key_name = selected_key_name

        active_api_key = st.session_state.api_keys.get(selected_key_name, "")

        if active_api_key:
            st.caption(f"🟢 **Estado:** API Key activa ({selected_key_name})")
        else:
            st.caption("🔴 **Estado:** Sin API Key configurada")

        # Opción clara para gestionar API Keys (Agregar / Eliminar)
        with st.expander("🔑 Gestor de API Keys", expanded=False):
            st.markdown("##### Añadir nueva API Key")
            new_key_label = st.text_input("Nombre o Etiqueta", placeholder="Ej. Key Secundaria", key="new_key_label_input")
            new_key_val = st.text_input("Valor de la API Key", type="password", placeholder="gsk_...", key="new_key_val_input")
            
            if st.button("💾 Guardar API Key", use_container_width=True):
                if new_key_val.strip():
                    label = new_key_label.strip() if new_key_label.strip() else f"Key {len(st.session_state.api_keys)+1}"
                    st.session_state.api_keys[label] = new_key_val.strip()
                    st.session_state.active_api_key_name = label
                    st.success(f"API Key '{label}' añadida.")
                    st.rerun()
                else:
                    st.warning("Ingresa una clave válida.")

            if len(st.session_state.api_keys) > 0:
                st.markdown("---")
                st.markdown("##### Eliminar API Key")
                key_to_delete = st.selectbox("Seleccionar key a eliminar", options=list(st.session_state.api_keys.keys()), key="key_to_delete_select")
                if st.button("🗑️ Eliminar API Key", use_container_width=True):
                    if len(st.session_state.api_keys) <= 1:
                        st.warning("Debes conservar al menos una API Key.")
                    else:
                        del st.session_state.api_keys[key_to_delete]
                        st.session_state.active_api_key_name = list(st.session_state.api_keys.keys())[0]
                        st.success(f"API Key '{key_to_delete}' eliminada.")
                        st.rerun()

        # Selección de Modelo de Groq
        model = st.selectbox(
            "Modelo de Lenguaje (Groq)",
            options=[
                "openai/gpt-oss-120b",
                "openai/gpt-oss-safeguard-20b",
                "openai/gpt-oss-20b",
                "whisper-large-v3",
                "whisper-large-v3-turbo",
                "meta-llama/llama-prompt-guard-2-22m",
                "meta-llama/llama-prompt-guard-2-86m",
                "canopylabs/orpheus-arabic-saudi",
                "canopylabs/orpheus-v1-english",
                "qwen/qwen3.8-27b",
            ],
            key="selected_model",
            help="Selecciona el modelo de Groq a utilizar."
        )

        st.markdown("---")

        # Sección 2: Historial de Conversaciones
        st.markdown('<span class="section-badge">💬 HISTORIAL DE CONVERSACIONES</span>', unsafe_allow_html=True)

        # Generar títulos automáticamente para conversaciones anteriores si hay API key activa y modelo
        if active_api_key and model:
            try:
                auto_generate_missing_titles(active_api_key, model)
            except Exception:
                pass

        conversations = list_conversations()
        current_conv_id = st.session_state.get("conversation_id")

        if not conversations:
            st.info("No hay conversaciones anteriores.")
        else:
            for conv in conversations:
                is_active = (conv.id == current_conv_id)
                icon = "▶" if is_active else "💬"
                display_title = f"{icon} {conv.title}"

                col_btn, col_del = st.columns([0.82, 0.18])
                with col_btn:
                    if st.button(
                        display_title,
                        key=f"conversation_{conv.id}",
                        use_container_width=True,
                        help=conv.title
                    ):
                        st.session_state.conversation_id = conv.id
                        st.rerun()
                with col_del:
                    if st.button(
                        "🗑️",
                        key=f"delete_conv_{conv.id}",
                        help="Borrar conversación",
                        use_container_width=True
                    ):
                        remove_conversation(conv.id)
                        if st.session_state.get("conversation_id") == conv.id:
                            st.session_state.conversation_id = None
                        st.rerun()

        # Guardar en session state para retrocompatibilidad
        st.session_state.groq_api_key = active_api_key

        return {
            "api_key": active_api_key,
            "model": model
        }