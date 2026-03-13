import os
from google import genai
from dotenv import load_dotenv

# 1. Carrega as variáveis de ambiente do arquivo .env (para teste local)
load_dotenv()

# 2. Busca a chave de forma segura
# No Streamlit Cloud, ele buscará automaticamente nos "Secrets"
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("ERRO: A variável GEMINI_API_KEY não foi encontrada. Verifique as configurações.")

# 3. Inicializa o cliente do Gemini
client = genai.Client(api_key=API_KEY)

def analisar_feedback(texto):
    """
    Envia o feedback para o modelo Gemini e retorna
    uma análise estruturada em formato JSON.
    """
    
    # Prompt de sistema para garantir que a IA se comporte como um Analista da Gocase
    prompt = f"""
    Atue como um Analista de CX (Customer Experience) sênior da Gocase.
    Analise o feedback do cliente abaixo e retorne estritamente um objeto JSON.
    
    Feedback: "{texto}"
    
    Campos necessários no JSON:
    - sentimento: (Positivo, Neutro ou Negativo)
    - urgencia: (Número de 1 a 10, onde 10 é crítico como erro de entrega ou produto trocado)
    - categoria: (Logística, Produto, Atendimento ou Financeiro)
    - resumo_critico: (Máximo 10 palavras)
    - sugestao_resposta: (Uma frase curta, empática e no tom de voz da Gocase)
    """
    
    try:
        # Ajustado para gemini-1.5-flash para maior estabilidade de cota
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        
        # Retorna o texto gerado pela IA (que deve ser o JSON)
        return response.text
        
    except Exception as e:
        # Tratamento para erro de limite de cota (429) ou erro de rede
        error_msg = str(e)
        if "429" in error_msg:
            return '{"erro": "Limite de requisições (Quota) atingido. Tente novamente em 60 segundos."}'
        return f'{{"erro": "Ocorreu um erro na análise: {error_msg}"}}'

# Bloco para testar o script individualmente via terminal
if __name__ == "__main__":
    test_feedback = "Meu pedido #12345 está atrasado há 5 dias e ninguém me responde no chat!"
    print("Iniciando análise de teste...")
    resultado = analisar_feedback(test_feedback)
    print(resultado)