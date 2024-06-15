import os
import time
import requests
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json

# Calea unde dorești să salvezi paginile descărcate
SAVE_PATH = 'downloaded_pages/'

# Creează directorul dacă nu există
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)

# URL-ul de la care să descărcăm fișierul feed.txt
FEED_URL = 'https://openphish.com/feed.txt'

# Descarcă fișierul feed.txt cu antete pentru a evita blocarea
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
response = requests.get(FEED_URL, headers=headers)

stop_scraping = False

def check_for_interrupt():
    global stop_scraping
    while True:
        user_input = input("Type 'stop' to stop the script:\n")
        if user_input.lower() == 'stop':
            stop_scraping = True
            break

if response.status_code == 200:
    # Extrage URL-urile din răspunsul text primit
    urls = response.text.splitlines()

    # Configurează opțiuni pentru Chrome
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # rulează Chrome în mod headless
    driver = webdriver.Chrome(options=chrome_options)

    data = []

    # Creează un thread pentru a asculta întreruperea de la tastatură
    interrupt_thread = threading.Thread(target=check_for_interrupt)
    interrupt_thread.start()

    try:
        # Parcurge fiecare URL și descarcă conținutul paginii
        for url in urls:
            if stop_scraping:
                print("Stopping script as requested by user...")
                break

            try:
                # Curăță URL-ul (elimină spații albe și linii noi)
                url = url.strip()

                # Navighează la link
                driver.get(url)
                page_source = driver.page_source

                # Parsează conținutul paginii cu BeautifulSoup
                soup = BeautifulSoup(page_source, 'html.parser')

                # Extrage caracteristicile relevante
                page_data = {
                    'url': url,
                    'title': soup.title.string if soup.title else '',
                    'meta_description': '',
                    'meta_keywords': '',
                    'text_content': soup.get_text(),
                    'content_length': len(soup.get_text()),
                    'num_forms': len(soup.find_all('form')),
                    'num_external_links': len([link for link in soup.find_all('a', href=True) if not link['href'].startswith('#') and not link['href'].startswith('/')])
                }

                # Extrage meta taguri (description și keywords)
                for meta in soup.find_all('meta'):
                    if 'name' in meta.attrs:
                        if meta.attrs['name'].lower() == 'description':
                            page_data['meta_description'] = meta.attrs['content']
                        elif meta.attrs['name'].lower() == 'keywords':
                            page_data['meta_keywords'] = meta.attrs['content']

                # Salvează datele în listă
                data.append(page_data)

                # Opțional: salvează și conținutul paginii ca fișier HTML pentru referințe ulterioare
                file_name = SAVE_PATH + url.split('/')[-1] + '.html'
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(page_source)

            except Exception as e:
                print(f"An error occurred with URL {url}: {e}")

            # Așteaptă 2 secunde între request-uri pentru a nu suprasolicita serverele
            time.sleep(2)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Închide browserul când scriptul s-a terminat
        driver.quit()

        # Salvează datele extrase într-un fișier JSON
        with open('phishing_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print("Data saved. Exiting...")

else:
    print("Failed to download feed.txt. Status Code:", response.status_code)

