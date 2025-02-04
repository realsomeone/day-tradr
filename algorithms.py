from config import *

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
    elif lowavg / highavg < 0.983:
        consensus = -1
    else:
        return 0
    if stocks[sym][1] != consensus: return consensus
    return 0