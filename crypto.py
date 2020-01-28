import requests
from globals import favorite_crypto_pairs


def prettify(change):
    if float(change) < 0:
        return "🔻%.2f" % float(change)
    elif float(change) == 0:
        return "↔️%.2f" % float(change)
    else:
        return "🔼%.2f" % float(change)


def query(base, target):

    # Building a url from base and target currency symbols
    # It must look like this: https://api.cryptonator.com/api/ticker/btc-eth

    url = 'https://api.cryptonator.com/api/ticker/{}-{}'.format(
        base.lower(), target.lower())
    try:
        response = requests.get(url).json()
        price = response['ticker']['price']
        change = response['ticker']['change']
    except KeyError:
        return "Wrong pair {}/{}! \n" \
               "Full list of symbols is here: https://coinmarketcap.com/all/views/all/\n" \
               "".format(base, target)
    else:
        return "{}/{}\nPrice: {} {}\n" \
               "Change: {} {}\n\n".format(
            base, target, int(float(price)),
            target, prettify(change), target)


# Iterate over your favorite crypto pairs
def check_favorites():
    result = ""
    for pair in favorite_crypto_pairs:
        base, target = pair.split('/')
        result += query(base, target)
    return result
