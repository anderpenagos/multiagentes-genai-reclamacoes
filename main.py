
import argparse
from agente_coletor_web import coletar_reclamacoes_reais
from agente_analista import analisar_reclamacao
from agente_estrategista import gerar_relatorio_estrategico
import json

def main():
    parser = argparse.ArgumentParser(
        description="Protótipo Multiagentes GenAI para Análise de Reclamações"
    )
    parser.add_argument(
        "--empresa", "-e",
        help="Nome da empresa no ReclameAqui (ex: itau, nubank)"
    )
    parser.add_argument(
        "--limite", "-l",
        type=int,
        default=5,
        help="Número de reclamações a coletar (padrão: 5)"
    )
    args = parser.parse_args()


    if not args.empresa:
        args.empresa = input("Digite o nome da empresa (ex: itau): ").strip()

    print(f"\nAnalisando reclamações de '{args.empresa}' (limite={args.limite})…\n")


    caminho_json = coletar_reclamacoes_reais(args.empresa, args.limite)
    if not caminho_json:
        print("Falha na coleta. Verifique o nome da empresa ou sua conexão.")
        return


    with open(caminho_json, encoding="utf-8") as f:
        reclamacoes = json.load(f)


    analises = []
    for rec in reclamacoes:
        analise = analisar_reclamacao(rec["texto"])
        analise["link"] = rec.get("link", "")
        analise["id_reclamacao"] = rec["id"]
        analises.append(analise)


    relatorio = gerar_relatorio_estrategico(analises)
    print(">> Relatório Executivo:\n")
    print(relatorio)

if __name__ == "__main__":
    main()
