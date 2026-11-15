import streamlit as st
import google.generativeai as genai
import base64
import os

# Configuração da página
st.set_page_config(page_title="Chatbot IA - CL", page_icon="🤖", layout="centered")

# Função para converter imagens em base64 de forma segura
def get_image_base64(path):
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""

logo_path = "assets/images/logo.JPG"
fundo_path = "assets/images/img_fundo.JPG"

logo_base64 = get_image_base64(logo_path)
fundo_base64 = get_image_base64(fundo_path)

# Carregar o CSS externo
try:
    with open("assets/css/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception as e:
    st.error(f"Erro ao carregar o style.css: {e}")

# Aplicar a imagem de fundo expandida de ponta a ponta
st.markdown(
    """
    <style>
    /* Fundo Cyberpunk Leve (Gradiente Escuro sem imagens pesadas ou fixed) */
    .stApp {
        background: linear-gradient(135deg, #030308 0%, #0c0c1d 50%, #05050a 100%) !important;
        color: #e0e0e0;
        background-attachment: scroll !important;
    }

    /* Ocultar elementos padrão desnecessários para limpar a interface mobile */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Mensagens do Chat com Glassmorphism Otimizado */
    .stChatMessage {
        background: rgba(15, 15, 25, 0.9) !important;
        border: 1px solid rgba(0, 243, 255, 0.25) !important;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        margin-bottom: 10px;
    }

    /* Ajustes para a barra de input fluida e estável no telemóvel */
    .stChatInputContainer {
        background-color: rgba(10, 10, 20, 0.95) !important;
        border-top: 1px solid rgba(0, 243, 255, 0.2) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Cabeçalho com colunas para alinhar o logótipo de boas-vindas e o título com perfeição
col1, col2 = st.columns([1, 6], vertical_alignment="center")

with col1:
    if logo_base64:
        st.markdown(f"""
            <img src="data:image/jpeg;base64,{logo_base64}" style="width: 75px; height: 75px; border-radius: 50%; object-fit: cover; border: 2px solid #0dcaf0; box-shadow: 0 0 20px rgba(13, 202, 240, 0.7);">
        """, unsafe_allow_html=True)
    else:
        st.markdown("🤖")

with col2:
    st.markdown("""
        <h1 style="margin: 0; font-size: 1.9rem; font-weight: 700; color: #ffffff; text-shadow: 0 0 12px rgba(13, 202, 240, 0.5);">Assistente IA</h1>
        <p style="margin: 0; color: #93c5fd; font-size: 0.95rem; letter-spacing: 0.5px;">Desenvolvido por Christian Luiz</p>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border-color: rgba(13, 202, 240, 0.4); margin-top: 15px; margin-bottom: 25px;'>", unsafe_allow_html=True)

# Configuração segura da Chave de API (tenta ler dos Secrets do Streamlit ou usa fallback local)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    API_KEY = "CHAVE_API_AQUI"

try:
    genai.configure(api_key=API_KEY)
    # Tenta carregar o gemini-1.5-flash de forma direta
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception:
    try:
        # Alternativa caso a biblioteca exija a tag latest
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
    except Exception as e:
        st.error(f"Erro ao configurar a API: {e}")
        model = None

# Histórico de mensagens com saudação inicial automática
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá, Amigo(a)! 🚀 Por onde é que começamos hoje? Como posso ajudar?"}
    ]

# Exibir histórico de mensagens (minimalista, sem ícones laterais)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada do utilizador
if prompt := st.chat_input("Digite sua mensagem para a IA..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Resposta da IA
    with st.chat_message("assistant"):
        with st.spinner("A pensar..."):
            try:
                if model:
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                else:
                    st.error("Modelo não inicializado corretamente.")
            except Exception as e:
                st.error(f"Ocorreu um erro ao gerar a resposta: {e}")