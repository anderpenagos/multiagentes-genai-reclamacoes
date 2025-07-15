import os
from openai import OpenAI
import json
# No terminal antes de executar
# Windows: set OPENAI_API_KEY=sua_chave_aqui
# Mac/Linux: export OPENAI_API_KEY=sua_chave_aqui
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

PROMPT_SISTEMA_ANALISTA = """
Você é um especialista em análise de reclamações de clientes do setor financeiro.
Sua tarefa é receber o texto de uma reclamação e extrair as seguintes informações em um formato JSON ESTRITO:
1.  "produto": O produto financeiro principal da reclamação (ex: "Cartão de Crédito", "Conta Corrente", "PIX", "Aplicativo", "Empréstimo").
2.  "motivo_reclamacao": Uma categoria curta e direta para o problema (ex: "Cobrança Indevida", "Falha no Aplicativo", "Fraude / Cartão Clonado", "Mau Atendimento", "Problema em Transação").
3.  "sentimento": O sentimento do cliente ("Positivo", "Neutro", "Negativo").
4.  "resumo_tecnico": Um resumo de uma frase do que aconteceu.
5.  "sugestao_area": A área interna do banco que deveria tratar o caso (ex: "Tecnologia/App", "Cartões", "Segurança/Fraudes", "Contas", "Atendimento").

Responda APENAS com o objeto JSON, sem nenhum texto adicional.
"""

def analisar_reclamacao(texto_reclamacao: str) -> dict:

    print(f"\nAgente Analista: Analisando reclamação...")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o", 
            messages=[
                {"role": "system", "content": PROMPT_SISTEMA_ANALISTA},
                {"role": "user", "content": texto_reclamacao}
            ],
            temperature=0,
            response_format={"type": "json_object"} 
        )
        resultado_json = response.choices[0].message.content
        print("Agente Analista: Análise concluída.")
        return json.loads(resultado_json)
    except Exception as e:
        print(f"Agente Analista: Erro ao contatar a API da OpenAI - {e}")
        return {"erro": str(e)}
