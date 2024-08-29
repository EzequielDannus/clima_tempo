import requests
import sqlite3
from pyramid.view import view_config
from googletrans import Translator

def get_db_connection():
    conn = sqlite3.connect('weather_data.db')
    conn.row_factory = sqlite3.Row  
    return conn

def incrementar_contagem_cidade(cidade):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT contagem FROM contagem_pesquisa WHERE cidade = ?", (cidade,))
        result = cursor.fetchone()
        if result:
            nova_contagem = result['contagem'] + 1
            cursor.execute("UPDATE contagem_pesquisa SET contagem = ? WHERE cidade = ?", (nova_contagem, cidade))
        else:
            cursor.execute("INSERT INTO contagem_pesquisa (cidade, contagem) VALUES (?, 1)", (cidade,))
        conn.commit()


def translate_text_googletrans(text, target_lang='pt'):
    translator = Translator()
    try:
        translation = translator.translate(text, dest=target_lang)
        return translation.text
    except AttributeError as e:
        # Tratar o erro específico de AttributeError
        print(f"Erro ao traduzir o texto: {e}")
        return f"Erro na tradução: {text}"
    except Exception as e:
        # Tratar qualquer outra exceção que possa ocorrer
        print(f"Ocorreu um erro inesperado: {e}")
        return f"Erro na tradução: {text}"


def get_contagem_cidades():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT cidade, contagem FROM contagem_pesquisa ORDER BY contagem DESC")
        return cursor.fetchall()

@view_config(route_name="home", renderer='templates/home.jinja2')
def home(request):
    # Obter contagem de pesquisas para cada cidade
    contagens = get_contagem_cidades()
    return {'contagens': contagens}

@view_config(route_name='weather', renderer='templates/home.jinja2')
def weather(request):
    city = request.params.get('city', 'New York')
    api_key = 'd8d31293bee740761c9ba933823c09ea'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'


    try:
        response = requests.get(url)
        data = response.json()
        descricao = data['weather'][0]['description']
        descricao_traduzida = translate_text_googletrans(descricao)
        
        velocidade_vento = data['wind']['speed']
        velocidade_ventokm = velocidade_vento*3.6

        weather_data = {
            'temperature': data['main']['temp'],
            'description': descricao_traduzida,
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': velocidade_ventokm,
        }
        
        # Atualizar contagem de pesquisa para a cidade
        incrementar_contagem_cidade(city)
        
        contagens = get_contagem_cidades()
        
        return {'weather_data': weather_data, 'contagens':contagens }
    except requests.exceptions.RequestException as e:
        return {'error': "Erro ao acessar o serviço de clima."}

