from scraper import get_page_text
from ai_engine import ask_gemini

url = "https://en.wikipedia.org/wiki/Artificial_intelligence"

content = get_page_text(url)

answer = ask_gemini(
    content,
    "What is artificial intelligence?"
)

print(answer)