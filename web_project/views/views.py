from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict
from web_project.models.stock import *
from django.http import HttpResponse
from django.template import loader
from web_project.models.forms import NewStockForm
from django.utils import timezone
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import DeleteView
from django.core.serializers.json import DjangoJSONEncoder
from web_project.models.alpaca import *
from decimal import *

import datetime
import pandas
import json
import pytz

SecondsBeforeRefreshStocks = 30

def index(request):
    if request.method == 'POST':
        addResult = addStock(request)
        return addResult
    else:
        getResult = getStocksToDisplay(request)
        return getResult

def getStocksToDisplay (request):
    stocksResult = getStocksFromDatabase()
    stocksList = []
    if stocksResult:
        for stock in stocksResult:
            stockTemp = getStockByStock(stock)
            stocksList.append(stockTemp)
    
    if not stocksList:
        stocksList = getDefaultStocks()

    context = {
        'stocksList': stocksList
    }

    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))

def getDefaultStocks():
    stocksList = [getStockByStockSymbol("AMD"), 
        getStockByStockSymbol("CERN"), 
        getStockByStockSymbol("FB"), 
        getStockByStockSymbol("GOOGL")]
    return stocksList

def getStockByStockSymbol (stockSymbol):
    stockPrice = GetAlpacaStockPriceByStockSymbol(stockSymbol)
    stock = Stock(stock_symbol = stockSymbol, 
        last_price = stockPrice, 
        last_checked = timezone.now(),
        change = 0) # Change being 0 should only persist for brand new stocks being added

    return stock

def getStockByStock (stock):
    stockResult = Stock.objects.get(stock_symbol = stock.stock_symbol)

    if stockResult and stockResult.last_checked <= timezone.now() - datetime.timedelta(seconds = SecondsBeforeRefreshStocks):
        stockFromApi = getStockByStockSymbol(stock.stock_symbol)
        stockChange = round(Decimal(stockFromApi.last_price), 2) - stock.last_price
        stock.last_checked = timezone.now()
        stock.last_price = stockFromApi.last_price
        
        if stockChange > 0 or stockChange < 0:
            stock.change = stockChange

        stock.save()

        return stock
    elif stockResult:
        return stockResult
    else:
        # Shouldn't ever reach here
        return

def addStock(request):
    form = NewStockForm(request.POST)
    if form.is_valid():
        saveStock(form.cleaned_data['new_stock'].upper())

    return getStocksToDisplay(request)

def saveStock (stockSymbol):
    doesStockExist = checkIfStockExistsInDatabase(stockSymbol)
    if doesStockExist:
        return
    try:
        stock = getStockByStockSymbol(stockSymbol)
        stock.save()
    except:
        return
    return

def checkIfStockExistsInDatabase (stockSymbol):
    try:
        stock = Stock.objects.get(stock_symbol = stockSymbol)
        return True
    except Stock.DoesNotExist:
        return False

def getStocksFromDatabase():
    stocksList = []
    stocks = Stock.objects.all().order_by('stock_symbol')
    for stock in stocks:
        stocksList.append(stock)
    return stocksList

class DeleteView(SuccessMessageMixin, DeleteView):
    model = Stock
    success_url = '/'
    success_message = "deleted..."

def delete(self, request, *args, **kwargs):
    self.object = self.get_object()
    name = self.object.name
    request.session['name'] = name  # name will be change according to your need
    message = request.session['name'] + ' deleted successfully'
    messages.success(self.request, message)
    b = super(DeleteView, self).delete(request, *args, **kwargs)
    response = redirect('index.html')
    return response