from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
from lxml import etree

#send request to get the content of the website
# 爬取数据
url = "https://www.hko.gov.hk/tide/KCTtextPH2024_uc.htm"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# find the tide table
table = soup.find('table')
data = []

# Iterate through table rows遍历表格行
for row in table.find_all('tr'):
    cols = row.find_all('td')
    if len(cols) > 0:
        month = cols[0].text.strip()
        day = cols[1].text.strip()
        if month == "01" and day == "01":  # Only get data for January 1
            for i in range(3, len(cols)):  # Start from the 4th column for tide height data
                if i < 26:  # the first 24 hours
                    time = f"{i - 2:02d}:00"  # Generate time (hour)
                    date = "2024-01-01"
                    height = float(cols[i].text.strip())  # Tide height
                    data.append((f"{date} {time}", height))
                else:  # the last hour (24:00)
                    time = "00:00"
                    date = "2024-01-02"
                    height = float(cols[i].text.strip())  # Tide height
                    data.append((f"{date} {time}", height))

# Convert to DataFrame
df = pd.DataFrame(data, columns=['Datetime', 'Height'])
df['Datetime'] = pd.to_datetime(df['Datetime'])

# ensure no duplicate time data
df = df.drop_duplicates(subset=['Datetime'])
print(df)

# Visualize line chart
plt.figure(figsize=(10, 5))
plt.plot(df['Datetime'], df['Height'], marker='o', linestyle='-', linewidth=2, color='blue')
plt.title('Tide Data on January 1, 2024')
plt.xlabel('Time')
plt.ylabel('Tide Height (m)')
plt.xticks(rotation=45)
plt.grid(True)  # Add grid lines
plt.tight_layout()
plt.show()