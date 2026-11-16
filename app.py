import streamlit as st
from groq import Groq

st.set_page_config(page_title="Assistente IA - Cyberpunk", page_icon="⚡")

# Inicializar cliente Groq e selecionar um modelo de chat válido
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
    
    # Listar modelos e excluir modelos de embedding, guard ou áudio
    models_response = client.models.list()
    valid_models = [
        m.id for m in models_response.data 
        if not any(x in m.id for x in ['embed', 'whisper', 'guard', 'tool'])
    ]
    
    # Prioriza um modelo Llama de chat ou usa uma alternativa padrão segura
    model_name = next((m for m in valid_models if 'llama' in m), 'llama-3.1-8b-instant')
except Exception as e:
    client = None
    model_name = "llama-3.1-8b-instant"

st.title("⚡ Assistente IA")
st.caption("Desenvolvido por Christian Luiz")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá, Amigo(a)! 🦇 Por onde é que começamos hoje? Como posso ajudar?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Digite sua mensagem para a IA..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if client:
            try:
                formatted_messages = [
                    {"role": m["role"], "content": m["content"]} 
                    for m in st.session_state.messages
                ]
                
                chat_completion = client.chat.completions.create(
                    model=model_name,
                    messages=formatted_messages,
                    temperature=0.7,
                    max_tokens=512,
                )
                response = chat_completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Ocorreu um erro ao gerar a resposta: {e}")
        else:
            st.error("Cliente Groq não configurado corretamente.")