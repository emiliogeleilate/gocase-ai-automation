import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Carrega variáveis locais do .env (se existir)
load_dotenv()

# 2. Configuração da Chave API (Busca no Streamlit Secrets ou .env)
API_KEY = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("Erro: A chave GEMINI_API_KEY não foi configurada nos Secrets do Streamlit.")
    st.stop()

# Configura a biblioteca com a chave
genai.configure(api_key=API_KEY)

def analisar_feedback(texto):
    """
    Usa a biblioteca google-generativeai para analisar o feedback.
    """
    # Usamos o nome técnico completo para evitar erro 404
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    
    prompt = f"""
    Atue como um Analista de CX (Customer Experience) sênior da Gocase.
    Analise o feedback do cliente abaixo e retorne estritamente um objeto JSON puro, sem formatação markdown.
    
    Feedback: "{texto}"
    
    Campos necessários no JSON:
    - sentimento: (Positivo, Neutro ou Negativo)
    - urgencia: (Número de 1 a 10)
    - categoria: (Logística, Produto, Atendimento ou Financeiro)
    - resumo_critico: (Máximo 10 palavras)
    - sugestao_resposta: (Frase curta e empática no tom da Gocase)
    """
    
    try:
        response = model.generate_content(prompt)
        # Limpa possíveis marcações de markdown (```json ...) caso a IA envie
        resultado_limpo = response.text.replace('```json', '').replace('```', '').strip()
        return resultado_limpo
    except Exception as e:
        return f'{{"erro": "{str(e)}"}}'

# Teste rápido se rodar o arquivo diretamente
if __name__ == "__main__":
    print(analisar_feedback("Teste de conexão"))