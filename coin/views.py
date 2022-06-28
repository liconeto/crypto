from datetime import datetime
from dateutil import parser
from django.shortcuts import render
import json
from requests import Request, Session
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import locale

# Create your views here.


def index(request):

    # Api de teste.
    url = "https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

    # Api de produção.
    # url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

    parameters = {"start": "1", "limit": "5000", "convert": "USD"}
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": "b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c",
        # Key de produção
        # "X-CMC_PRO_API_KEY": "73224774-775b-4677-8eca-0eb4e2a07f17",
    }

    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)
    data = json.loads(response.text)

    hoje = datetime.strftime(parser.parse(data["status"]["timestamp"]), "%d/%m/%Y")

    # Cotação do Dolar na API economia awesomeapi
    urlmoeda = "https://economia.awesomeapi.com.br/last/USD-BRL"
    acesso = requests.get(urlmoeda)
    cotacao = acesso.json()
    valorBRL = float(cotacao["USDBRL"]["bid"])

    coin = []
    for content in data["data"]:

        coin.append(
            {
                "rank": content["cmc_rank"],
                "name": content["name"],
                "symbol": content["symbol"],
                "quote": locale.format("%.04f", content["quote"]["USD"]["price"]),
                "quotebr": locale.format(
                    "%.04f", content["quote"]["USD"]["price"] * valorBRL
                ),
            }
        )

    return render(
        request,
        "index.html",
        {
            "data": data,
            "cotacao": cotacao,
            "valorBRL": valorBRL,
            "coin": coin,
            "hoje": hoje,
        },
    )


def whale(request):
    # GET https://api.whale-alert.io/v1/status?api_key=your-api-key-here
    # url = "https://api.whale-alert.io/v1/status?"

    # GET https://api.whale-alert.io/v1/transactions?api_key=your-api-key-here&min_value=10000&start=1550237797&cursor=2bc7e46-2bc7e46-5c66c0a7
    url = "https://api.whale-alert.io/v1/transactions?"

    # key by access to API Whale Alert
    api_key = "api_key=uLG0Lf6MKq6yWZ8pOAQEPpoOSinzxGWm"

    whalealert = requests.get(url + api_key)
    alerts = whalealert.json()

    # Cotação do Dolar na API economia awesomeapi
    urlmoeda = "https://economia.awesomeapi.com.br/last/USD-BRL"
    acesso = requests.get(urlmoeda)
    cotacao = acesso.json()
    valorBRL = float(cotacao["USDBRL"]["bid"])

    transactions = []
    for blockchain in alerts["transactions"]:
        transactions.append(
            {
                "name": blockchain["blockchain"],
                "symbol": blockchain["symbol"],
                "id": blockchain["id"],
                "type": blockchain["transaction_type"],
                "hash": blockchain["hash"],
                "from": blockchain["from"],
                "to": blockchain["to"],
                "time": datetime.strftime(
                    datetime.fromtimestamp(
                        blockchain["timestamp"],
                        tz=None,
                    ),
                    "%d/%m/%Y %H:%M:%S",
                ),
                "amount": locale.format("%.02f", blockchain["amount"]),
                "amount_usd": locale.format("%.02f", blockchain["amount_usd"]),
                "amount_brl": locale.format(
                    "%.02f", blockchain["amount_usd"] * valorBRL
                ),
            }
        )

    return render(
        request,
        "whale.html",
        {
            "alerts": alerts,
            "transactions": transactions,
            "cotacao": cotacao,
            "valorBRL": valorBRL,
        },
    )


def lore(request):

    # url= https://api.coinlore.net/api/tickers/?start=100&limit=100

    url = "https://api.coinlore.net/api/tickers/?start=0&limit=100"
    coinlore = requests.get(url)
    coinslore = coinlore.json()

    coins = coinslore["data"]

    # Cotação do Dolar na API economia awesomeapi
    urlmoeda = "https://economia.awesomeapi.com.br/last/USD-BRL"
    acesso = requests.get(urlmoeda)
    cotacao = acesso.json()
    valorBRL = float(cotacao["USDBRL"]["bid"])

    coin = []
    for content in coinslore["data"]:

        coin.append(
            {
                "rank": content["rank"],
                "name": content["name"],
                "symbol": content["symbol"],
                "price_usd": round(float(content["price_usd"]), 4),
                "price_br": round((float(content["price_usd"]) * valorBRL), 4),
                "percent_change_1h": round(float(content["percent_change_1h"]), 4),
                "percent_change_24h": round(float(content["percent_change_24h"]), 4),
                "logo": "https://cryptoicons.org/api/color/"
                + content["symbol"].lower()
                + "/16",
            }
        )

    return render(
        request, "coinlore.html", {"coin": coin, "valorbrl": valorBRL, "coins": coins}
    )
