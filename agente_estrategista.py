import os
from openai import OpenAI
import json

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

PROMPT_SISTEMA_ESTRATEGISTA = """
Você é um Diretor de Experiência do Cliente em um banco.
Você recebeu uma lista de reclamações já analisadas e estruturadas em formato JSON.
Sua tarefa é analisar o conjunto de dados e escrever um breve relatório executivo em português.

O relatório deve conter:
1.  Um resumo geral dos problemas encontrados.
2.  Identificação da tendência mais preocupante (o problema que mais se repete ou o mais grave).
3.  Uma recomendação de ação prioritária para a diretoria.

Seja direto e foque em insights acionáveis.
"""

def gerar_relatorio_estrategico(lista_de_analises: list) -> str:

    print("\nAgente Estrategista: Gerando relatório de insights...")
    

    dados_formatados = json.dumps(lista_de_analises, indent=2, ensure_ascii=False)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": PROMPT_SISTEMA_ESTRATEGISTA},
                {"role": "user", "content": f"Analise os seguintes dados de reclamações:\n{dados_formatados}"}
            ],
            temperature=0.7
        )
        relatorio = response.choices[0].message.content
        print("Agente Estrategista: Relatório gerado com sucesso.")
        return relatorio
    except Exception as e:
        print(f"Agente Estrategista: Erro ao contatar a API da OpenAI - {e}")
        return "Não foi possível gerar o relatório."
