# 📋 Specs Agent

**Specs Agent** es un asistente inteligente conversacional especializado en ingeniería de requisitos de software. Su objetivo principal es transformar solicitudes vagas e informales en **Especificaciones de Software (SPECs)** explícitas, verificables y aprobables bajo la norma **ISO/IEC/IEEE 29148:2018** y la metodología **BDD (Given-When-Then)**.

## 🚀 Características Principales

* **Interacción Guiada por Preguntas**: Para evitar suposiciones o invenciones de negocio, el agente realiza aclaraciones de manera concisa (una sola pregunta por turno).
* **Especificaciones Estructuradas de 17 Secciones**: Al resolver todas las ambigüedades, genera un documento SPEC completo (v1.0) con requisitos funcionales, no funcionales, reglas de negocio, flujos y criterios de aceptación.
* **Interfaz de Usuario Estética y Organizada**: Desarrollada en **Streamlit** con paneles organizados por secciones visuales.
* **Gestor de Múltiples API Keys (Groq)**: Detecta automáticamente la clave `.env` como clave por defecto y permite agregar o eliminar claves adicionales en tiempo de ejecución.
* **Títulos Generados por IA**: El mismo agente genera títulos cortos y descriptivos para cada conversación basados en la primera consulta del usuario.
* **Persistencia Integrada**: Almacenamiento local mediante **SQLAlchemy** y **SQLite** con capacidad de crear y eliminar conversaciones del historial.

---

## 🛠️ Requisitos Previos

* **Python 3.10+** instalado en el sistema.
* Una cuenta y **API Key de Groq** ([https://console.groq.com](https://console.groq.com)).

---

## ⚙️ Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/juanchito1234/specs-agent.git
cd specs-agent
```

### 2. Crear y activar un entorno virtual

* **Windows (PowerShell)**:
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\activate
  ```

* **Linux / macOS**:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto con tu clave API de Groq:

```env
GROQ_API_KEY=gsk_tu_api_key_aqui
```

---

## 🏃‍♂️ Ejecución de la Aplicación

Para iniciar la aplicación web en Streamlit, ejecuta el siguiente comando:

```bash
streamlit run main.py
```

La aplicación se abrirá automáticamente en tu navegador predeterminado en `http://localhost:8501`.

---

## 📁 Estructura del Proyecto

```text
specs-agent/
│
├── app/
│   ├── agent/             # Prompt del sistema y lógica del agente de especificaciones
│   ├── chat/              # Servicio de mensajería del chat
│   ├── llm/               # Cliente y llamadas a la API de Groq
│   ├── models/            # Modelos ORM de SQLAlchemy (Conversation, Message)
│   ├── persistence/       # Repositorios y conexión a la base de datos SQLite
│   ├── services/          # Lógica de negocio y servicios de conversación
│   └── ui/                # Componentes de la interfaz en Streamlit (Chat y Sidebar)
│
├── data/                  # Almacenamiento local de la base de datos SQLite
├── main.py                # Punto de entrada de la aplicación Streamlit
├── requirements.txt       # Dependencias del proyecto
├── .env                   # Archivo de variables de entorno (no incluir en git)
└── README.md              # Documentación del proyecto
```
