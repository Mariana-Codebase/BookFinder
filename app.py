import os
from urllib.parse import quote

import mysql.connector
import requests
import wikipediaapi
from dotenv import load_dotenv
from flask import Flask, render_template, request

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Simple i18n dictionary for UI strings
TRANSLATIONS = {
    'es': {
        'app_title': 'LibroFinder - Resúmenes desde Wikipedia',
        'tagline': 'Descubre resúmenes de tus libros favoritos',
        'search_placeholder': 'Busca el resumen por título',
        'search_button': 'Buscar',
        'results_for': 'Resultados para',
        'found': 'encontrados',
        'summary': 'Resumen',
        'view_on_wikipedia': 'Ver en Wikipedia',
        'no_results': 'No se encontraron libros que coincidan con',
        'try_another': 'Intenta con otro término de búsqueda',
        'isbn': 'ISBN',
        'footer': 'LibroFinder © 2025 - Mariana Sinisterra',
        'lang_es': 'Español',
        'lang_en': 'English',
    },
    'en': {
        'app_title': 'BookFinder - Summaries from Wikipedia',
        'tagline': 'Discover summaries of your favorite books',
        'search_placeholder': 'Search summary by title',
        'search_button': 'Search',
        'results_for': 'Results for',
        'found': 'found',
        'summary': 'Summary',
        'view_on_wikipedia': 'View on Wikipedia',
        'no_results': 'No books found matching',
        'try_another': 'Try another search term',
        'isbn': 'ISBN',
        'footer': 'BookFinder © 2025 - Mariana Sinisterra',
        'lang_es': 'Español',
        'lang_en': 'English',
    },
}

# Database configuration
db_config = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS')
}

# Configure Wikipedia client
wiki_wiki = wikipediaapi.Wikipedia(
    language='es',
    user_agent='BookFinderApp/1.0 (example@example.com)',
    extract_format=wikipediaapi.ExtractFormat.WIKI
)

def get_wikipedia_summary(title):
    """Return a short summary for a title using Spanish Wikipedia."""
    try:
        # Clean the title for better search results
        clean_title = title.split('(')[0].strip().replace(':', '')

        # Try the exact title first
        page = wiki_wiki.page(clean_title)

        if not page.exists():
            # Fall back to the Wikipedia search API
            search_url = f"https://es.wikipedia.org/w/api.php?action=query&list=search&srsearch={quote(clean_title)}&format=json"
            response = requests.get(search_url)
            data = response.json()

            if data['query']['search']:
                # Use the first search result
                page_title = data['query']['search'][0]['title']
                page = wiki_wiki.page(page_title)

        if page.exists():
            # Limit the summary to 500 characters
            summary = page.summary[0:500]
            return summary + "..." if len(page.summary) > 500 else summary

        return f"Buscar '{clean_title}' en Wikipedia para más información"
    except Exception as e:
        print(f"Wikipedia error: {e}")
        return "Summary temporarily unavailable"

@app.route('/')
def index():
    """Render the home page."""
    lang = request.args.get('lang', 'es').lower()
    if lang not in TRANSLATIONS:
        lang = 'es'

    def t(key):
        return TRANSLATIONS[lang].get(key, key)

    return render_template('index.html', lang=lang, t=t)

@app.route('/buscar', methods=['POST'])
def buscar():
    """Search books in MySQL and enrich results with Wikipedia summaries."""
    titulo = request.form.get('titulo', '')
    lang = request.form.get('lang', request.args.get('lang', 'es')).lower()
    if lang not in TRANSLATIONS:
        lang = 'es'

    def t(key):
        return TRANSLATIONS[lang].get(key, key)

    conn = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM libro WHERE nombre LIKE %s", (f"%{titulo}%",))
        libros = cursor.fetchall()

        for libro in libros:
            # Add Wikipedia summary and URL for each book
            libro['resumen'] = get_wikipedia_summary(libro['nombre'])
            libro['wikipedia_url'] = f"https://es.wikipedia.org/wiki/{libro['nombre'].replace(' ', '_').replace('/', '%2F')}"

        return render_template('index.html',
                           libros=libros,
                           titulo_buscado=titulo,
                           lang=lang,
                           t=t)
    except Exception as e:
        return render_template('index.html', error=str(e), lang=lang, t=t)
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    # Default dev server
    app.run(debug=True, port=5000)