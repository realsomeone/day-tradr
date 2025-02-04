from api import *
from config import *
from algorithms import *
from colorama import Fore
import sys
import time

def main():
    open = False
    trading = ['AMZN', 'AAPL', 'TSLA']
    stocks = dict()
    for sym in trading:
        prices = get_old_prices(sym)
        if prices == 'no data':
            stocks[sym] = [[], None, 0]
        else:
            stocks[sym] = [prices, None, 0]
    while True:
        market = get_clock()
        if not oneminleft(market):
            for sym in stocks:
                stocks[sym][0].append(get_price(sym))
            if market['is_open']:
                open = True
                for sym in stocks:
                    consensus = buyorsell(sym, stocks)
                    if consensus == 1 and (stocks[sym][1] != 1 and stocks[sym][1] != -1):
                        stocks[sym][2] = get_price(sym)
                        buy(sym, 5)
                        stocks[sym][1] = 1
                    elif (consensus == -1 and stocks[sym][1] is not None) or get_price(sym) <= stocks[sym][2] * 0.97:
                        sell(sym, stocks[sym][2])
                        stocks[sym][1] = -1
                    else:
                        if stocks[sym][1] == 1:
                            print(Fore.CYAN + sym + Fore.RESET, end=' ')
                        elif stocks[sym][1] == -1:
                            print(Fore.RED + sym + Fore.RESET, end=' ')
                        else:
                            print(Fore.YELLOW + sym + Fore.RESET, end=' ')
                print()
            else: 
                if not open: 
                    print(Fore.RED + "Market is closed. WAITING..." + Fore.RESET)
                else:
                    print(Fore.CYAN + "Market closed for today. Finished up.")
                    print(Fore.GREEN + "Cash: $" + get_cash() + Fore.RESET)
                    sys.exit()
        time.sleep(60*5)
        
if __name__ == "__main__":
    main()