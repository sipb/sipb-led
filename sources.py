# sources.py: Pull messages from various sources

import urllib.request, urllib.error, urllib.parse


def getBTCmessage():
    # Gets the current price of Bitcoin from BitcoinAverage.com
    # Don't call this more than once a minute -- it will make BitcoinAverage.com sad if we overload their servers.
    btc_api_url = "https://api.bitcoinaverage.com/ticker/USD/24h_avg"
    try:
        data = urllib.request.urlopen(btc_api_url).read()
        return "1 BTC = $" + data
    except:
        return "Bitcoin price unavailable."
