from ..settings import alpacaApiClient

def GetAlpacaStockPriceByStockSymbol(stockSymbol):
    account = alpacaApiClient.get_account()
    c = alpacaApiClient.get_last_quote(stockSymbol)
    stock = alpacaApiClient.get_last_trade(stockSymbol)
    return stock.price