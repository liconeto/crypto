from datetime import datetime
from string import digits
from time import sleep
from dateutil import parser
from django.shortcuts import render
import json
from requests import Request, Session
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import locale
from . import viewsChart


# Create your views here.


def cotacao(request):
    # Cotação do Dolar na API Economia Awesomeapi
    urlmoeda = "https://economia.awesomeapi.com.br/last/USD-BRL"
    acesso = requests.get(urlmoeda)
    cotacao = acesso.json()
    valorBRL = float(cotacao["USDBRL"]["bid"])

    return valorBRL


def moedabrl(valor):
    valor = valor
    locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
    valor = locale.currency(valor, grouping=True, symbol=None)

    return valor


def moedausd(valor):
    valor = valor
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
    valor = locale.currency(valor, grouping=True, symbol=None)

    return valor


def whale(request):

    valorBRL = cotacao(request)

    # Usando a APi do Whale Alert Free limita a 10 consultas por minuto
    url = "https://api.whale-alert.io/v1/transactions?"

    # key by access to API Whale Alert
    api_key = "api_key=uLG0Lf6MKq6yWZ8pOAQEPpoOSinzxGWm"

    whalealert = requests.get(url + api_key)
    alerts = whalealert.json()

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
                "amount": moedausd(blockchain["amount"]),
                "amount_usd": moedausd(blockchain["amount_usd"]),
                "amount_brl": moedabrl(blockchain["amount_usd"] * valorBRL),
            }
        )

    return render(
        request,
        "whale.html",
        {
            "alerts": alerts,
            "transactions": transactions,
            "valorBRL": valorBRL,
        },
    )


def index(request):

    valorBRL = cotacao(request)

    global junta
    junta = []

    for i in range(1):
        num = i + 1
        url = (
            "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=200&page="
            + str(num)
            + "&sparkline=true&price_change_percentage=1h%2C24h%2C7d%2C30%2C"
        )
        coingecko = requests.get(url)
        coinsgecko = coingecko.json()

        # coins = coinsgecko["data"]

        coins = []
        for i in coinsgecko:
            coins.append(
                {
                    "id": i["id"],
                    "name": i["name"],
                    "market_cap_rank": i["market_cap_rank"],
                    "image": i["image"],
                    "symbol": i["symbol"],
                    "current_price": i["current_price"],
                    "price_br": moedabrl(i["current_price"] * valorBRL),
                    "price_change_percentage_1h_in_currency": i[
                        "price_change_percentage_1h_in_currency"
                    ],
                    "price_change_percentage_24h_in_currency": i[
                        "price_change_percentage_24h_in_currency"
                    ],
                    "price_change_percentage_7d_in_currency": i[
                        "price_change_percentage_7d_in_currency"
                    ],
                    "sparkline_in_7d": i["sparkline_in_7d"],
                }
            )
        junta += coins

    return render(
        request,
        "index.html",
        {"valorBRL": valorBRL, "coinsgecko": coinsgecko, "coins": junta},
    )


def gecko(request):

    valorBRL = cotacao(request)

    # Documentação API coingecko
    # https://www.coingecko.com/en/api/documentation

    # Doumentação com todas criptos listadas na coingecko
    # https://docs.google.com/spreadsheets/d/1wTTuxXt8n9q7C4NDXqQpI3wpKu1_5bGVmP9Xz0XGSyU/edit#gid=0

    list_coins = "https://api.coingecko.com/api/v3/search/trending"
    list_response = requests.get(list_coins)
    trend_coins = list_response.json()

    coins = []
    for i in trend_coins["coins"]:
        coins.append(
            {
                "id": i["item"]["id"],
                "coin_id": i["item"]["coin_id"],
                "name": i["item"]["name"],
                "symbol": i["item"]["symbol"],
                "market_cap_rank": i["item"]["market_cap_rank"],
                "thumb": i["item"]["thumb"],
                "small": i["item"]["small"],
                "large": i["item"]["large"],
                "slug": i["item"]["slug"],
                "price_btc": i["item"]["price_btc"],
                "score": int(i["item"]["score"]) + 1,
            }
        )

    # Endpoint para moeda espeficifica
    # https://api.coingecko.com/api/v3/coins/dogecoin

    # Endpoint com 7 criptos mais negociadas nas ultimas 24 horas
    # https://api.coingecko.com/api/v3/search/trending

    trend_coins = list_response.json()
    return render(
        request,
        "gecko.html",
        {"valorBRL": valorBRL, "coins": coins, "trend_coins": trend_coins},
    )


def gcoin(request, id):

    valorBRL = cotacao(request)

    url = "https://api.coingecko.com/api/v3/coins/"
    id = str.lower(id)
    coin_request = requests.get(url + id)
    coin_json = coin_request.json()

    print(type(id))
    print(url + id)

    return render(
        request,
        "gcoin.html",
        {"cripto": coin_json, "valorBRL": valorBRL},
    )


def geraChart(request, sparkline):

    spark = sparkline

    return render(
        request,
        "geraChart.html",
        {"sparkline": spark},
    )
