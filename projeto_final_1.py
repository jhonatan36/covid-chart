from os import write
import requests as r
import datetime as dt
import csv
from PIL import Image
from IPython.display import display
from urllib.parse import quote

from requests.sessions import dispatch_hook

url = 'https://api.covid19api.com/dayone/country/brazil'
response = r.get(url)

raw_data = response.json()
final_data = []

for line in raw_data:
    final_data.append([line['Confirmed'], line['Deaths'], line['Recovered'], line['Active'], line['Date']])

final_data.insert(0,['Confirmados', 'Obitos', 'Recuperados', 'Ativos', 'Data'])

CONFIRMADOS = 0
OBITOS = 1
RECUPERADOS = 2
ATIVOS = 3
DATA = 4

for i in range(1, len(final_data)):
    final_data[i][DATA] = final_data[i][DATA][:10]

with open('brasil-covid-projeto.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(final_data)

for i in range(1, len(final_data)):
    final_data[i][DATA] = dt.datetime.strptime(final_data[i][DATA], "%Y-%m-%d")

def get_datasets(y, labels):
    if type(y[0]) == list:
        datasets = []
        for i in range(len(y)):
            datasets.append({
                'label': labels[i],
                'data': y[i]
            })
        return datasets
    else:
        return [
            {
                'label': labels[0],
                'data': y
            }
        ]

def set_title(title=''):
    if title != '':
        display = 'true'
    else:
        display = 'false'
    return {
        'title': title,
        'display': display
    }

def create_chart(x, y, labels, kind='bar', title=''):
    datasets = get_datasets(y, labels)
    options = set_title(title)

    chart = {
        'type': kind,
        'data': {
            'labels': x,
            'datasets': datasets
        },
        'options': options
    }

    return chart

def get_api_chart(chart):
    url_base = 'https://quickcharts.io/charts'
    resp = r.get(f'{url_base}?c={str(chart)}')
    return resp.content

def save_image(path, content):
    with open(path, 'wb') as image:
        image.write(content)

def display_image(path):
    img_pil = Image.open(path)
    display(img_pil)

def get_api_qrcode(link):
    text = quote(link) #parse de link para url
    url_base = 'https://quickchart.io/qr'
    resp = r.get(f'{url_base}?text={text}')
    return resp.content


y_data_1 = []
y_data_2 = []
y_data_3 = []
x = []

for obs in final_data[1::30]:
    y_data_1.append(obs[CONFIRMADOS])
    y_data_2.append(obs[RECUPERADOS])
    x.append(obs[DATA].strftime('%d/%m/%Y'))

labels = ['Confirmados', 'Recuperados']

#cria json de dados para gerar o grafico
chart = create_chart(x, [y_data_1, y_data_2], labels, title='Gráfico Covid (CONFIRMADOS, RECUPERADOS)')

#retorna grafico da api
chart_content = get_api_chart(chart)
print(chart_content)

#salva imagem no diretorio
#save_image('meu-primeio-grafico.png', chart_content)

#mostra imagem
#display_image('meu-primeiro-grafico.png')