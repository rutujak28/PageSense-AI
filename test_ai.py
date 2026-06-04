from scraper import get_page_text
from ai_engine import ask_gemini

url = "https://en.wikipedia.org/wiki/Artificial_intelligence"

content = get_page_text(url)

index, chunks = create_vector_store(
    content
)

answer = ask_gemini(
    question,
    index,
    chunks
)

print(answer)