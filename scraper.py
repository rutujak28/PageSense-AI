import requests
from bs4 import BeautifulSoup

def get_page_text(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)

    return text


if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Artificial_intelligence"

    text = get_page_text(url)

    print(text[:1000])