import streamlit as st
from groq import Groq

st.set_page_config(page_title="Assistente IA - Cyberpunk", page_icon="⚡")

# Inicializar cliente Groq
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
    
    # Descobrir automaticamente um modelo Llama disponível na tua conta
    models_response = client.models.list()
    available_models = [m.id for m in models_response.data]
    
    # Procura por um modelo Llama ou usa o primeiro disponível
    model_name = next((m for m in available_models if 'llama' in m), available_models[0] if available_models else 'llama-3.1-8b-instant')
except Exception as e:
    st.error(f"Erro ao conectar com a Groq. Verifique a chave nos Secrets: {e}")
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
                    model=model_name,  # Usa o modelo detetado automaticamente
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