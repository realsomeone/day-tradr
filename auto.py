import trader 
import datetime
import api
import os

def main():
    time = api.get_clock()
    today = datetime.datetime.now().isoformat().split('T')[0]
    stockday = time['next_open'].split('T')[0]
    if today == stockday:
        trader.main()
    else:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    