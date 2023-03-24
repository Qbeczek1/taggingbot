import requests
from bs4 import BeautifulSoup
import csv

def extract_text(soup):
    paragraphs = soup.find_all('p')
    text = ' '.join([para.get_text() for para in paragraphs])
    return text

def categorize_text(text):
    categories = {
        'seo tech': ['seo', 'search engine optimization', 'on-page', 'technical seo', 'technical'],
        'linkbuilding': ['seo', 'search engine optimization', 'link building', 'backlinks', 'inbound links', 'outbound links', 'off-page'],
        'case study': ['seo', 'search engine optimization', 'case study', 'analysis', 'research', 'study', 'success story'],
        'content': ['seo', 'search engine optimization', 'content marketing', 'blogging', 'copywriting', 'content strategy', 'content creation'],
        'guide': ['seo', 'search engine optimization', 'documentation', 'guide', 'manual', 'tutorial', 'how-to']
    }

    matched_category = None
    max_matches = 0

    for category, keywords in categories.items():
        matches = sum([1 for keyword in keywords if keyword.lower() in text.lower()])
        if matches > max_matches:
            max_matches = matches
            matched_category = category

    return matched_category

def fetch_and_categorize(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            text = extract_text(soup)
            category = categorize_text(text)
            return category
        else:
            print(f"Nie udało się pobrać strony {url}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Wystąpił problem podczas analizy {url}: {e}")
        return None

with open('urls.txt', 'r') as file:
    urls = [line.strip() for line in file.readlines()]

results = []
for url in urls:
    category = fetch_and_categorize(url)
    results.append((url, category))

with open('wyniki.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['URL', 'Kategoria'])
    for result in results:
        writer.writerow(result)
