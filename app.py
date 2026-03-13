import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Busca a chave (prioriza Secrets do Streamlit, depois .env)
API_KEY = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("Chave API não encontrada!")
    st.stop()

genai.configure(api_key=API_KEY)

def analisar_feedback(texto):
    # Usando a biblioteca estável (google-generativeai)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Atue como um Analista de CX da Gocase. 
    Retorne um JSON para este feedback: "{texto}"
    Campos: sentimento, urgencia (1-10), categoria, resumo_critico, sugestao_resposta.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f'{{"erro": "{str(e)}"}}'