import os
from openai import OpenAI
import json

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

PROMPT_SISTEMA_ESTRATEGISTA = """
Você é um Diretor de Experiência do Cliente em um banco.

Você recebeu uma lista de reclamações já analisadas e estruturadas em formato JSON.

Sua tarefa é:

1. Escrever um breve relatório executivo em português contendo:
   - Um resumo geral dos problemas encontrados.
   - A identificação da tendência mais preocupante (o problema que mais se repete ou o mais grave).
   - Uma recomendação de ação prioritária para a diretoria.

2. Para cada reclamação individual, escreva uma solução direta, clara e amigável, **direcionada ao cliente que fez a reclamação**, explicando o que ele pode fazer para resolver ou contornar o problema. A solução deve ser escrita de forma acessível, evitando termos técnicos ou internos da empresa.

3. Apresente cada reclamação com o link correspondente no início, seguido do problema e da solução, fundamental que seja no formato abaixo:
- **reclamação:** <link da reclamação>  
- **Problema:** <descrição do problema>  
- **Solução:** <solução direcionada ao cliente>

Seja direto e objetivo em todo o relatório, focando em insights acionáveis e úteis para os clientes e para a diretoria.
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
