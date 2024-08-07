import requests
import sqlite3
from pyramid.view import view_config

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('weather_data.db')
c = conn.cursor()

# Criar as tabelas para armazenar dados do clima e contagem de pesquisas
c.execute('''
CREATE TABLE IF NOT EXISTS clima (
    id INTEGER PRIMARY KEY,
    cidade TEXT NOT NULL,
    temperatura REAL,
    descricao TEXT,
    umidade INTEGER,
    pressao INTEGER,
    velocidade_vento REAL,
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS contagem_pesquisa (
    cidade TEXT PRIMARY KEY,
    contagem INTEGER DEFAULT 0
)
''')
conn.commit()

def incrementar_contagem_cidade(cursor, cidade):
    cursor.execute("SELECT contagem FROM contagem_pesquisa WHERE cidade = ?", (cidade,))
    result = cursor.fetchone()
    if result:
        nova_contagem = result[0] + 1
        cursor.execute("UPDATE contagem_pesquisa SET contagem = ? WHERE cidade = ?", (nova_contagem, cidade))
    else:
        cursor.execute("INSERT INTO contagem_pesquisa (cidade, contagem) VALUES (?, 1)", (cidade,))
    cursor.connection.commit()

@view_config(route_name="home", renderer='templates/home.jinja2')
def home(request):
    return {}

@view_config(route_name='weather', renderer='templates/home.jinja2')
def weather(request):
    city = request.params.get('city')
    api_key = 'd8d31293bee740761c9ba933823c09ea'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

    try:
        response = requests.get(url)
        data = response.json()
        weather_data = {
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed'],
        }
        
        # Inserir dados do clima no banco de dados
        c.execute('''
        INSERT INTO clima (cidade, temperatura, descricao, umidade, pressao, velocidade_vento)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (city, weather_data['temperature'], weather_data['description'],
              weather_data['humidity'], weather_data['pressure'], weather_data['wind_speed']))
        
        # Incrementar a contagem de pesquisas para a cidade
        incrementar_contagem_cidade(c, city)
        
        conn.commit()
        
        return {'weather_data': weather_data}
    except Exception as e:
        # Fechar conexão no banco de dados em caso de erro
        conn.close()
        return {'error': "Cidade não encontrada, ou digitada incorretamente"}

# Função para consultar a quantidade de pesquisas por cidade
def consultar_contagem_cidades():
    c.execute("SELECT cidade, contagem FROM contagem_pesquisa")
    return c.fetchall()

# Fechar conexão no banco de dados quando não estiver mais sendo usada
conn.close()
