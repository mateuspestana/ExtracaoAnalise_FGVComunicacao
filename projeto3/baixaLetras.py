"""
Script para extrair letras de músicas do site Letras.mus.br

Este script utiliza Selenium para automatizar a navegação no site e BeautifulSoup
para extrair informações das páginas. Ele busca por um artista específico,
coleta uma lista de músicas e extrai as letras, visualizações e informações
de composição de cada música.

Autor: Matheus C. Pestana
"""

# Imports para automação web com Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Imports para gerenciamento automático de drivers
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

# Imports para manipulação de dados e parsing HTML
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm  # Para barra de progresso
import requests
from datetime import datetime

# Input do usuário
input_user = input("Digite o nome do artista a ser pesquisado: ")

# =============================================================================
# CONFIGURAÇÃO DO NAVEGADOR
# =============================================================================

# Configuração das opções do Chrome
chrome_options = ChromeOptions()
chrome_options.add_argument("--start-maximized")  # Abre a janela maximizada
# Não mostrar o navegador
# chrome_options.add_argument("--headless")

# O WebDriver Manager baixa e configura o driver automaticamente
print('Abrindo o driver...')
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# =============================================================================
# NAVEGAÇÃO E BUSCA NO SITE
# =============================================================================

print('Acessando o site...')
driver.get("https://www.letras.mus.br")
print('Site acessado... Esperando 3 segundos...')
time.sleep(3)

# Localiza o campo de busca na página
print('Buscando campo de busca...')
buscar = driver.find_element(By.CLASS_NAME, "searchBar-input")
time.sleep(1)

# Digita o nome do artista a ser pesquisado
buscar.send_keys(input_user)
time.sleep(1)

# Navega pelos resultados e seleciona o primeiro
print(f'Digitando "{input_user}" e pressionando Enter...')
time.sleep(1)
buscar.send_keys(Keys.ARROW_DOWN)  # Seleciona o primeiro resultado
time.sleep(1)
buscar.send_keys(Keys.ENTER)  # Confirma a seleção

print(f'URL atual após busca: {driver.current_url}')
time.sleep(3)  # Aguarda o carregamento da página de resultados

# Obtém o HTML da página de resultados
source = driver.page_source
soup = BeautifulSoup(source, "lxml")

# =============================================================================
# EXTRAÇÃO DA LISTA DE MÚSICAS
# =============================================================================

# Localiza a área que contém a lista de músicas
songs_area = soup.find('div', {'class': 'cnt-list--alp'})

# Extrai todos os elementos de música da lista
songs = songs_area.find_all('li', {'class': 'songList-table-row'})

# Lista para armazenar informações das músicas
songs_list = []

# Itera sobre cada música encontrada e extrai as informações básicas
for song in songs:
    song_url = song.get('data-shareurl')      # URL da página da música
    song_title = song.get('data-name')        # Título da música
    song_artist = song.get('data-artist')     # Nome do artista
    
    # Adiciona as informações à lista
    songs_list.append({
        'url': song_url,
        'title': song_title,
        'artist': song_artist
    })

# =============================================================================
# CONFIGURAÇÃO E FUNÇÃO PARA EXTRAÇÃO DE LETRAS
# =============================================================================

# Cria uma sessão HTTP para reutilizar conexões
session = requests.Session()

def get_lyrics(song_url):
    """
    Extrai informações detalhadas de uma música específica.
    
    Args:
        song_url (str): URL da página da música no Letras.mus.br
        
    Returns:
        tuple: (lyrics, views, composition) - letra, visualizações e info de composição
    """
    # Faz requisição HTTP para a página da música
    response = session.get(song_url)
    soup = BeautifulSoup(response.content, "lxml")
    
    # Extrai a letra da música
    lyrics = soup.find('div', {'class': 'lyric-original'}).get_text(strip=False)
    
    # Extrai o número de visualizações
    views = soup.find('div', {'class': 'head-info-exib'}).find('b').get_text(strip=True)
    
    # Extrai informações de composição
    composition = soup.find('div', {'class': 'lyric-info-composition'}).get_text(strip=True)
    # Remove texto padrão desnecessário
    composition = composition.replace('Essa informação está errada? Nos avise.', '')
    
    return lyrics, views, composition

# =============================================================================
# EXTRAÇÃO DAS LETRAS E INFORMAÇÕES DETALHADAS
# =============================================================================

try:
    # Itera sobre cada música com barra de progresso
    for song in tqdm(songs_list, desc="Extraindo letras"):
        # Extrai informações detalhadas da música
        lyrics, views, composition = get_lyrics(song['url'])
        
        # Adiciona as informações extraídas ao dicionário da música
        song['lyrics'] = lyrics
        song['views'] = views
        song['composition'] = composition
        
except Exception as e:
    print(f"Erro ao obter letras da música {song['title']}: {e}")
    time.sleep(1)

# =============================================================================
# SALVAMENTO DOS DADOS
# =============================================================================

# Converte a lista de dicionários em DataFrame do pandas
df = pd.DataFrame(songs_list)
df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Salva os dados em arquivo CSV
df.to_csv('songs.csv', index=False)
print(f"Dados salvos em 'songs.csv' com {len(songs_list)} músicas")

# Aguarda antes de fechar o navegador
time.sleep(10)

# =============================================================================
# FINALIZAÇÃO
# =============================================================================

# Fecha o navegador
driver.quit()
print("Script finalizado com sucesso!")