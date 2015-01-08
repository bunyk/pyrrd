from decimal import Decimal
 
import requests
from tabulate import tabulate
import json
 
 
def yahoo_finance_query(**params):
    ''' Return the text of the request to the Yahoo finance API
    s - ids of entities we wnant to receive. Every stock, index or currency has their own ID.
    If you want to get values of more than one ID, separate them with ","
    f - properties we ant to get. See
    https://code.google.com/p/yahoo-finance-managed/wiki/enumQuoteProperty
    '''
    return requests.get('http://download.finance.yahoo.com/d/quotes.csv', params=params).text
 
def get_exchange_rate(fixed_currency, variable_currency):
    ''' Return tuple of last trade, ask and bid prices for given currencies '''
    r = yahoo_finance_query(s=variable_currency + fixed_currency + '=X', f='l1a0b0')
    return tuple(map(Decimal, r.split(',')))

def get_wikipedia_edits():
    j = json.loads(requests.get(
        'https://uk.wikipedia.org/w/api.php',
        params={
            'action': 'query',
            'meta': 'siteinfo',
            'siprop': 'statistics',
            'continue': '',
            'format': 'json',
        }
    ).text)
    return int(j['query']['statistics']['edits'])


def table():
    print(tabulate(
        (
            ('RUB/' + currency, ) + get_exchange_rate('RUB', currency)
            for currency in ('EUR', 'USD', 'UAH')
        ),
        headers = ('Pair', 'Trade', 'Ask', 'Bid')
    ))
