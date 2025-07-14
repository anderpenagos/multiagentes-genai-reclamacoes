import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def coletar_reclamacoes_reais(nome_empresa: str, limite: int = 5) -> str:

    print(f"Agente de Coleta Web: iniciando busca por '{nome_empresa}' (limite={limite})...")
    url_lista = f"https://www.reclameaqui.com.br/empresa/{nome_empresa}/lista-reclamacoes/"

 
    options = Options()
    # Colocar o url de seu navegador baseado no chromium exemplo: C:\Program Files\Google\Chrome\Application\chrome.exe
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    #options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url_lista)

        try:
            WebDriverWait(driver, 7).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Aceitar']"))
            ).click()
            print("Banner de cookies aceito.")
            time.sleep(1)
        except TimeoutException:
            print("Banner de cookies não apareceu.")

    
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )

        reclamacoes = []
        vistos = set()

        for passo in range(4):
            driver.execute_script("window.scrollBy(0, window.innerHeight);")
            print(f"Scroll incremental passo {passo+1}/4 realizado.")
            time.sleep(2)

            elems = driver.find_elements(By.ID, "site_bp_lista_ler_reclamacao")
            print(f"Encontrados {len(elems)} reclamções neste passo.")
            for a in elems:
                href = a.get_attribute('href')
                if not href or href in vistos:
                    continue
                vistos.add(href)
                # extrai título dentro do <h4>
                try:
                    titulo = a.find_element(By.TAG_NAME, 'h4').text.strip()
                except Exception:
                    titulo = ''
                # extrai o <p> irmão logo após o <a>
                try:
                    texto_elem = a.find_element(By.XPATH, 'following-sibling::p')
                    texto = texto_elem.text.strip()
                except Exception:
                    texto = ''

                reclamacoes.append({
                    "id": len(reclamacoes) + 1,
                    "titulo": titulo,
                    "link": href,
                    "texto": texto
                })
                if len(reclamacoes) >= limite:
                    break
            if len(reclamacoes) >= limite:
                print("Limite de reclamações coletadas atingido.")
                break

        if not reclamacoes:
            raise RuntimeError("Nenhuma reclamação coletada — verifique o ID e o scroll.")


        arquivo = f"reclamacoes_{nome_empresa}.json"
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(reclamacoes, f, ensure_ascii=False, indent=2)
        print(f"Dados salvos em '{arquivo}'")
        return arquivo

    except Exception as e:
        print("Erro durante coleta:", e)
        try:
            driver.save_screenshot('erro_coleta.png')
            print("Screenshot de debug: erro_coleta.png")
        except:
            pass
        return None

    finally:
        driver.quit()
        print("Browser fechado." )



