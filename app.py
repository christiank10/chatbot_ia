import streamlit as st
from groq import Groq

st.set_page_config(page_title="Assistente IA - Cyberpunk", page_icon="⚡")

# Inicializar cliente Groq
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception as e:
    client = None

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
                
                # Lista de modelos oficiais da Groq para testar por ordem de prioridade
                candidate_models = [
                    "llama-3.3-70b-versatile",
                    "llama-3.1-8b-instant",
                    "llama3-70b-8192",
                    "llama3-8b-8192"
                ]
                
                response = None
                success = False
                
                # Testa os modelos um a um até encontrar um compatível com a chave
                for m_name in candidate_models:
                    try:
                        chat_completion = client.chat.completions.create(
                            model=m_name,
                            messages=formatted_messages,
                            temperature=0.7,
                            max_tokens=512,
                        )
                        response = chat_completion.choices[0].message.content
                        success = True
                        break
                    except Exception:
                        continue
                
                if success and response:
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    st.error("Erro: Nenhum modelo da Groq respondeu. Confirma se a tua GROQ_API_KEY está correta nos Secrets.")
            except Exception as e:
                st.error(f"Ocorreu um erro ao gerar a resposta: {e}")
        else:
            st.error("Cliente Groq não configurado corretamente.")