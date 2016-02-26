import csv
import urllib.request
from bs4 import BeautifulSoup
import datetime
import pytz

# A list of tickers we get the data for update as needed
# add new ones separated by commas inside the brackets to get all at once
tickers = ['MSFT', 'AMZN']

# get today's date so we know the end date for the website query
today_date = datetime.datetime.now(pytz.timezone('US/Eastern'))
year = str(today_date.year)
month = str(today_date.month)
day = str(today_date.day)

# headers to print to the csv later
headers = ['DATE', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME']

# scraping loop
for ticker in tickers:
    wsj_website = ("http://quotes.wsj.com/ajax/historicalprices/"
                   "7/{0}?MOD_VIEW=page&ticker={1}"
                   "&country=US&exchange=XNAS&instrumentType=STOCK"
                   "&num_rows=35037&range_days=35037&startDate="
                   "1%2F1%2F1920&endDate={2}%2F{3}%2F{4}"
                   ).format(ticker, ticker, month, day, year)
    soup = BeautifulSoup(urllib.request.urlopen(wsj_website).read(),
                         'lxml-xml')
    table = soup.find_all('table', attrs={'class': 'cr_dataTable'})[1]
    rows = []
    for row in table.find_all('tr'):
        rows.append([val.text for val in row.find_all('td')])
    with open("{0}.csv".format(ticker), 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(row for row in rows if row)
