import streamlit as st
import base64
from groq import Groq

# Configuração da página
st.set_page_config(page_title="Assistente IA - Cyberpunk", page_icon="🦇", layout="centered")

# Função com Cache para conversão rápida de imagens (evita bloqueios no servidor)
@st.cache_data
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

# Função para injetar o fundo
def set_background(image_file):
    encoded = get_base64_image(image_file)
    if encoded:
        css = f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(10, 10, 15, 0.88), rgba(10, 10, 15, 0.88)), url("data:image/jpeg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

set_background("assets/images/img_fundo.JPG")

# Carregar o estilo CSS
try:
    with open("assets/css/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# Inicializar cliente Groq
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception as e:
    client = None

logo_base64 = get_base64_image("assets/images/logo.JPG")

# Cabeçalho
header_col1, header_col2 = st.columns([0.15, 0.85], gap="small")

with header_col1:
    if logo_base64:
        st.markdown(f"""
            <div class="d-flex align-items-center justify-content-center pt-1">
                <img src="data:image/jpeg;base64,{logo_base64}" style="width: 65px; height: 65px; border-radius: 50%; border: 2px solid #00f0ff; box-shadow: 0 0 15px rgba(0, 240, 255, 0.8), inset 0 0 10px rgba(0, 240, 255, 0.4); object-fit: cover;">
            </div>
        """, unsafe_allow_html=True)

with header_col2:
    st.markdown("""
        <div class="pt-1">
            <h1 class="m-0 fs-2 fw-bold text-white">Assistente IA</h1>
            <p class="m-0 text-secondary" style="font-size: 0.9rem;">Desenvolvido por Christian Luiz</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<hr class='my-4 border-secondary opacity-25'>", unsafe_allow_html=True)

# Histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá, Amigo(a)! Por onde é que começamos hoje? Como posso ajudar?"}
    ]

for message in st.session_state.messages:
    avatar_path = "assets/images/logo.JPG" if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=avatar_path):
        st.markdown(message["content"])

# Entrada do utilizador
if prompt := st.chat_input("Digite sua mensagem para a IA..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="assets/images/logo.JPG"):
        with st.spinner("Processando resposta..."):
            if client:
                try:
                    formatted_messages = [
                        {"role": m["role"], "content": m["content"]} 
                        for m in st.session_state.messages
                    ]
                    
                    # Chamada direta e ultra-rápida (elimina o loop de timeout 1ST)
                    chat_completion = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=formatted_messages,
                        temperature=0.7,
                        max_tokens=512,
                    )
                    response = chat_completion.choices[0].message.content
                    
                    if response:
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    else:
                        st.error("Erro: Resposta vazia da API.")
                except Exception as e:
                    st.error(f"Ocorreu um erro ao processar o pedido: {e}")
            else:
                st.error("Cliente Groq não configurado corretamente nos Secrets.")