from api import *
from config import *
from colorama import Fore
import sys
import time

def get_avg_val(data, amnt):
    try:
        return sum(data[-amnt:]) / amnt
    except:
        return 0 # not enough data gathered

def buyorsell(sym, stocks):
    lowavg = round(get_avg_val(stocks[sym][0], LOAVG) * 100)
    highavg = round(get_avg_val(stocks[sym][0], HIAVG) * 100)
    # print(Fore.CYAN + f"Low Average: {lowavg}\t High Average: {highavg}" + Fore.RESET)
    if lowavg == 0 or highavg == 0: return 0
    if highavg < lowavg:
        consensus = 1
    elif highavg > lowavg:
        consensus = -1
    else:
        return 0
    if stocks[sym][1] != consensus: return consensus
    return 0

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
                    if consensus == 1 and stocks[sym][1] != 1:
                        stocks[sym][2] = get_price(sym)
                        buy(sym, 5)
                        stocks[sym][1] = 1
                    elif consensus == -1 and stocks[sym][1] is not None:
                        sell(sym)
                        stocks[sym][1] = -1
                    else:
                        if stocks[sym][1] == 1:
                            print(Fore.CYAN + sym + Fore.RESET, end=' ')
                        else:
                            print(Fore.YELLOW + sym + Fore.RESET, end=' ')
            else: 
                if not open: 
                    print(Fore.RED + "Market is closed. WAITING..." + Fore.RESET)
                else:
                    print(Fore.CYAN + "Market closed for today. Finished up.")
                    print(Fore.GREEN + "Cash: $" + get_cash() + Fore.RESET)
                    sys.exit()
        print()
        time.sleep(60*5)
        
if __name__ == "__main__":
    main()