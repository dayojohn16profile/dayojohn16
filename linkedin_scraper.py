import requests
from bs4 import BeautifulSoup

def google_scrape(query):
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")

    results = []
    for g in soup.select("div.g"):
        title = g.select_one("h3")
        link = g.select_one("a")
        if title and link:
            results.append({
                "title": title.text,
                "url": link["href"]
            })
    return results

print(google_scrape("marketing manager siargao linkedin"))
