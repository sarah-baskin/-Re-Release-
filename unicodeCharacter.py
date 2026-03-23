from requests import get
from bs4 import BeautifulSoup
from collections import defaultdict

def get_table_data(table):

    data = []
    for row in table.find_all("tr"):
        row_data = [cell.get_text(strip=True) for cell in row.find_all(["td", "th"])]
        data.append(row_data)

    data = data[1:]
    return data

def find_max_col(data):

    max_col = 0
    for datum in data:
        if int(datum[0]) > max_col:
            max_col = int(datum[0])
    return max_col

def find_max_row(data):

    max_row = 0
    for datum in data:
        if int(datum[2]) > max_row:
            max_row = int(datum[2])
    return max_row

def make_unicode_list(data, max_row, max_col):

    unicode_list = []
    for _ in range(0, max_row):
        unicode_list.append([' '] * max_col)

    for datum in data:
        uni = datum[1]
        unicode_list[int(datum[2])][int(datum[0])] = uni
    
    return unicode_list[::-1]


def unicode_grid(url):

    response = get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find("table")

    data = get_table_data(table)
    max_col = find_max_col(data)
    max_row = find_max_row(data)
    unicode_list = make_unicode_list(data, max_row + 1, max_col + 1)
    
    for line in unicode_list:
        line = "".join(line)
        print(line)

unicode_grid("https://docs.google.com/document/d/e/2PACX-1vRPzbNQcx5UriHSbZ-9vmsTow_R6RRe7eyAU60xIF9Dlz-vaHiHNO2TKgDi7jy4ZpTpNqM7EvEcfr_p/pub")

