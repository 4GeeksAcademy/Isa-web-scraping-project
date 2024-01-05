import requests
import pandas as pd
import time
from bs4 import BeautifulSoup


#url="https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
url="https://es.wikipedia.org/wiki/Leucocito"
#https://es.wikipedia.org/wiki/Leucocito 
#(tabla de tipos de leucocitos y gráfica de la relación del diámetro y porcentaje aproximado de adultos#
response= requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

#tabla de tipos de leucocitos
tabla_tipos = soup.find_all("table", class_="wikitable")

#Vamos a transformarlo en un df
data = []

for table in tabla_tipos:
    rows = table.find_all('tr')
    header = [header.text.strip() for header in rows[0].find_all('th')]
    
    for row in rows[1:]:
        values = [value.text.strip() for value in row.find_all('td')]
        data.append(dict(zip(header, values)))

df = pd.DataFrame(data)

#Vamos a hacer un gráfico del diámetro por el % de adultos
import matplotlib.pyplot as plt

#1º Vamos a obtener los números de la columna Diametro [4]
df['Diametro min']= df.iloc[:,4].str.extract('(\d+(\.\d+)?)', expand=True)[0]

#2º Lo mismo de la columna de % para poder convertirlo en número
df['%']= df.iloc[:,3].str.extract('(\d+(\.\d+)?)', expand=True)[0]
print(df['Diametro min'],df['%'])

a=df['Diametro min']
b=df['%']
#Las transformamos en números
df['%']=[float(valor) for valor in b]
df['Diametro min']=[float(valor) for valor in a]

#Hacemos un gráfico de puntos

plt.scatter(df['Diametro min'],df['%'])
plt.xlabel('Diametro')
plt.ylabel('% de adultos')
plt.show()