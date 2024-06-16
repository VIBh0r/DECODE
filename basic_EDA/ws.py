import pandas as pd
from bs4 import BeautifulSoup

with open('ws2016R6.html', 'r') as f:
    lines = f.read()

soup = BeautifulSoup(lines, 'html.parser')
table = soup.find('table')

table_rows = table.find_all('tr')

headings = [th.get_text() for th in table_rows[0].find_all('th')]

data = []
for row in table_rows[1:]:
    row_data = [td.get_text().strip() for td in row.find_all('td')]
    data.append(row_data)

df = pd.DataFrame(data, columns=headings)
df.to_excel('web_scrapped_josaa(2016)R6.xlsx', index=False)


