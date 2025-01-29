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
    print(Fore.CYAN + f"Low Average: {lowavg}\t High Average: {highavg}" + Fore.RESET)
    if lowavg == 0 or highavg == 0: return 0
    if highavg < lowavg:
        consensus = 1
    elif highavg > highavg:
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
        stocks[sym] = [get_old_prices(sym), None]
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
                        buy(sym, 5)
                    elif consensus == -1 and stocks[sym][1] is not None:
                        sell(sym)
                    else:
                        print(Fore.YELLOW + "Waiting on " + sym + Fore.RESET)
            else: 
                if not open: 
                    print(Fore.RED + "Market is closed. WAITING..." + Fore.RESET)
                else:
                    print(Fore.CYAN + "Market closed for today. Finished up.")
                    print(Fore.GREEN + "Cash: $" + get_cash() + Fore.RESET)
                    sys.exit()
        else: 
            print("1 minute left in the market. Selling...")
            for sym in stocks:
                sell(sym)
        print(Fore.YELLOW + "Sleeping for 1 minute..." + Fore.RESET)
        time.sleep(60)
        
if __name__ == "__main__":
    main()