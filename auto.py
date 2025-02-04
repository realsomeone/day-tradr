import trader 
import datetime
import api
import win32api

def main():
    time = api.get_clock()
    today = datetime.datetime.now().isoformat().split('T')[0]
    stockday = time['next_open'].split('T')[0]
    if today == stockday:
        trader.main()
    else:
        win32api.SetSystemPowerState(True, True)

if __name__ == '__main__':
    main()
