import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega localmente, mas no Streamlit ele usará os Secrets
load_dotenv()

# Captura a chave do painel do Streamlit
API_KEY = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("ERRO: Configure a chave GEMINI_API_KEY nos Secrets do Streamlit.")
    st.stop()

# Configuração da API
genai.configure(api_key=API_KEY)

def analisar_feedback(texto):
    # 'gemini-1.5-flash' é a melhor versão: rápida, gratuita e estável
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Atue como um Analista de CX da Gocase. 
    Analise o feedback abaixo e retorne APENAS um objeto JSON puro.
    Feedback: "{texto}"
    Campos: sentimento, urgencia (1-10), categoria, resumo_critico, sugestao_resposta.
    """
    
    try:
        response = model.generate_content(prompt)
        # Limpa o texto caso a IA mande blocos de código markdown
        resultado = response.text.replace('```json', '').replace('```', '').strip()
        return resultado
    except Exception as e:
        # Se der erro 404, o código vai te avisar aqui
        return f'{{"erro": "{str(e)}"}}'