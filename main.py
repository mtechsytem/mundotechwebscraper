
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def obter_cotacao():
    try:
        r = requests.get('https://economia.awesomeapi.com.br/last/USD-BRL')
        return float(r.json()['USDBRL']['bid'])
    except:
        return 5.0

def coletar_produtos(url_base):
    produtos = []
    cotacao = obter_cotacao()
    for pagina in range(1, 6):
        url = f"{url_base}?pagina={pagina}"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        itens = soup.select('.product-container')
        if not itens:
            break
        for item in itens:
            nome = item.select_one('.name')
            preco = item.select_one('.price')
            img = item.select_one('img')
            if nome and preco and img:
                preco_valor = float(preco.text.replace('U$', '').replace('.', '').replace(',', '.').strip())
                produtos.append({
                    "nome": nome.text.strip(),
                    "preco_dolar": preco_valor,
                    "preco_real": round(preco_valor * cotacao, 2),
                    "imagem": "https://bestshop.com.py" + img.get('data-src', img.get('src'))
                })
    return produtos

@app.get("/iphones")
def iphones():
    return coletar_produtos("https://bestshop.com.py/departamentos/iphone/swap")

@app.get("/xiaomi")
def xiaomi():
    return coletar_produtos("https://bestshop.com.py/departamentos/smartphonesetablets/xiaomi")
