import requests
import time
import pandas as pd
import sys

pd.options.mode.chained_assignment = None

headers = {'Accept-Language': 'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                         'Version/15.4 Safari/605.1.15'}

airplane_reg = ["HB-IHX", "HB-IHY", "HB-IHZ", "HB-IJU", "HB-IJV", "HB-IJW", "HB-JJK", "HB-JJL", "HB-JJM", "HB-JJN",
                "HB-JMD", "HB-JME", "HB-JMG"]
rename = ['DATE', 'FROM', 'TO', 'FLIGHT',
          'FLIGHT_TIME', 'STD', 'ATD', 'STA', 'STATUS']
df_definitive = pd.DataFrame(columns=rename)
list_dataframe = []

for i in range(len(airplane_reg)):
    URL = "https://www.flightradar24.com/data/aircraft/" + airplane_reg[i]
    plane = requests.get(URL, headers=headers)
    table_ = pd.read_html(plane.text)
    df = table_[0]
    df.drop(df.tail(1).index, inplace=True)
    df = df.drop(columns=['FLIGHTS HISTORY', 'FLIGHTS HISTORY.1', 'FLIGHTS HISTORY.10', 'FLIGHTS HISTORY.12',
                          'FLIGHTS HISTORY.13', 'FLIGHTS HISTORY.14', 'FLIGHTS HISTORY.15',
                          'FLIGHTS HISTORY.16', 'FLIGHTS HISTORY.17', 'FLIGHTS HISTORY.18',
                          'FLIGHTS HISTORY.19', 'Unnamed: 20', 'DATE', 'FROM',
                          'TO', 'FLIGHT', 'FLIGHT TIME', 'STD', 'ATD', 'STA',
                          'Unnamed: 29', 'STATUS', 'Unnamed: 31', 'Unnamed: 32'])

    df.columns = rename
    list_index = [airplane_reg[i]] * len(df.index)
    df_new = df.assign(AIRPLANE_NAME=list_index)
    df_new = df_new.set_index(['AIRPLANE_NAME'])
    list_dataframe.append(df_new)
    time.sleep(1)

df_definitive = pd.concat(list_dataframe, axis=0)


# DISPLAY DELAY FUNCTION

def print_delay(df_delay, column, msg, formatting=None):
    delay = str(df_delay[column].mean())
    if formatting is None:
        print(msg + delay)
    else:
        print(msg + formatting(delay))


def trim_time(delay):
    delay = delay.removeprefix('0 days ')
    time_array = delay.split(':')
    if int(time_array[0]) == 0:
        time_string = str(int(time_array[1])) + ' minutes'
    else:
        time_string = str(int(time_array[0])) + ' hours and ' + str(int(time_array[1])) + ' minutes'
    return time_string


def departure_delay():
    df_delay = df_definitive
    df_delay = df_delay[df_delay['ATD'] != '—']
    df_delay['STD_DT'] = pd.to_datetime(df_delay['STD'])
    df_delay['ATD_DT'] = pd.to_datetime(df_delay['ATD'])
    df_delay['DELAY_D'] = df_delay['ATD_DT'] - df_delay['STD_DT']
    df_delay = df_delay[df_delay['DELAY_D'] > pd.Timedelta(0)]
    print_delay(df_delay, 'DELAY_D', 'During last week, the average departure delay was ', trim_time)


def arrival_delay():
    df_delay = df_definitive
    df_delay['STA_DT'] = pd.to_datetime(df_delay['STA'])
    df_delay = df_delay[df_delay['STATUS'].str.startswith('Landed')]
    df_delay['STATUS'] = df_delay['STATUS'].apply(lambda row: row.removeprefix('Landed '))
    df_delay['STATUS_DT'] = pd.to_datetime(df_delay['STATUS'])
    df_delay['DELAY_A'] = df_delay['STATUS_DT'] - df_delay['STA_DT']
    df_delay = df_delay[df_delay['DELAY_A'] > pd.Timedelta(0)]
    print_delay(df_delay, 'DELAY_A', 'During last week, the average arrival delay was ', trim_time)


#START OF THE PROGRAM AND FUNCTION SELECTOR

print("Welcome to our data-analyzer of Edelweiss Air's flights!")
while True:
    print("What do you want to do?\n\nFunction 1: Display "
          "average delay during last week\nFunction 2: Find a connection betwee to places")
    a = input("Select a function (1-2) or enter 0 to end the program: ")
    if a == "0":
        print("Thank you for using our program, we hope to see you again!")
        break
    elif a == "1":
        departure_delay()
        arrival_delay()
    elif a == "2":
        def find_connection(departure, arrival):
            dep = df_definitive[df_definitive['FROM'].str.contains(departure)]
            arr = dep[dep['TO'].str.contains(arrival)]
            if dep.empty:
                return sys.exit(f'No flights from {departure}')
            elif arr.empty:
                return sys.exit(f'No flights to {arrival}')
            else:
                arr = arr.assign(INDEX = range(1, len(arr) + 1))
                arr = arr.set_index(['INDEX'])
                return arr

        print('''Please note that EdelSwiss is based in Zurich, therefore either the 
        departure or the arrival should be Zurich. Otherwise the function will
        print an error message.''')
        departure = input('Please insert a departure location: ')
        arrival = input ('Please insert an arrival location: ')
        connections = find_connection(departure, arrival)
        print(connections)
        information = int(input(f'''Select a fly you want to have more infromation about. 
        To select a flight insert the index number,
        in this case a number between 1 and {len(connections)}: '''))


        print(f'''These are the information about your flight: 
        {connections.iloc[information - 1]}''')

    else:
        print('You selected an invalid function, you must enter a number between 0 and 2!')
    print(" ")
    time.sleep(5)
