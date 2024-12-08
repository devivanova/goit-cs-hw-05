import requests
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
import re


def fetch_text(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text


def map_words(text):
    words = re.findall(r'\b\w+\b', text.lower())
    return words


def reduce_word_counts(word_chunks):
    counter = Counter()
    for chunk in word_chunks:
        counter.update(chunk)
    return counter


def visualize_top_words(word_counts, top_n=10):
    most_common = word_counts.most_common(top_n)
    words, counts = zip(*most_common)

    plt.barh(words, counts, color='skyblue')
    plt.xlabel('Frequency')
    plt.ylabel('Words')
    plt.title('Top 10 Most Frequent Words')
    plt.gca().invert_yaxis()
    plt.show()


if __name__ == "__main__":
    url = "https://dou.ua/lenta/articles/kharkiv-tech-industry-2024/?from=recent"

    try:
        text = fetch_text(url)

        word_list = map_words(text)

        chunk_size = len(word_list) // 4 + 1
        chunks = [word_list[i:i + chunk_size]
                  for i in range(0, len(word_list), chunk_size)]

        with ThreadPoolExecutor() as executor:
            word_chunks = list(executor.map(Counter, chunks))

        word_counts = reduce_word_counts(word_chunks)

        visualize_top_words(word_counts)

    except requests.RequestException as e:
        print(f"Error fetching the text: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
