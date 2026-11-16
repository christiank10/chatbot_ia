import streamlit as st
from groq import Groq

# Configuração da página e visual cyberpunk
st.set_page_config(page_title="Assistente IA - Cyberpunk", page_icon="⚡")

# Inicializar cliente Groq utilizando os Secrets do Streamlit
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"Erro ao carregar a chave da API da Groq nos Secrets: {e}")
    client = None

st.title("⚡ Assistente IA")
st.caption("Desenvolvido por Christian Luiz")

# Histórico de mensagens na sessão
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá, Amigo(a)! 🦇 Por onde é que começamos hoje? Como posso ajudar?"}
    ]

# Exibir mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada do utilizador
if prompt := st.chat_input("Digite sua mensagem para a IA..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gerar resposta com a Groq
    with st.chat_message("assistant"):
        if client:
            try:
                # Formatar histórico para a API da Groq
                formatted_messages = [
                    {"role": m["role"], "content": m["content"]} 
                    for m in st.session_state.messages
                ]
                
                chat_completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",  # Modelo rápido, leve e garantido na Groq
                messages=formatted_messages,
                temperature=0.7,
                max_tokens=1024,
)
                response = chat_completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Ocorreu um erro ao gerar a resposta: {e}")
        else:
            st.error("Cliente Groq não configurado corretamente.")