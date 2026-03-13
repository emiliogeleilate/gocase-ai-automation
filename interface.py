import streamlit as st
import json
from app import analisar_feedback

# Configuração visual da página
st.set_page_config(page_title="Gocase AI Triagem", page_icon="🚀")

st.title("🛡️ Gocase AI - Triagem Inteligente")
st.markdown("---")
st.write("Esta ferramenta utiliza IA Generativa para processar e categorizar feedbacks de clientes do **Gogroup**.")

# Campo de entrada
feedback_input = st.text_area(
    "Digite ou cole o feedback do cliente aqui:", 
    placeholder="Ex: Minha capinha personalizada chegou com a estampa errada...",
    height=150
)

if st.button("Analisar Processo"):
    if feedback_input:
        with st.spinner('IA analisando o processo e gerando insights...'):
            resultado_bruto = analisar_feedback(feedback_input)
            
            st.subheader("📊 Resultado da Análise")
            
            # Tenta exibir como JSON formatado, se falhar exibe o texto puro
            try:
                # Limpeza básica para garantir que o texto seja JSON puro
                json_clean = resultado_bruto.replace('```json', '').replace('```', '').strip()
                st.json(json.loads(json_clean))
            except:
                st.code(resultado_bruto, language='text')
                
            st.success("Análise concluída com sucesso!")
    else:
        st.warning("Por favor, insira um feedback para análise.")

st.sidebar.info("Projeto Laboratorial - Candidatura Estágio Gocase")