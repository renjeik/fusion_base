from flask import Flask, request, jsonify
from flask_caching import Cache
import asyncio
import httpx
from bs4 import BeautifulSoup

config = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache"
}
app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)

base_url = "http://books.toscrape.com/"


async def search_books(query, category_url, client):
    # Task 2: Search Functionality & Task 3: Results Structuring and Output
    response = await client.get(category_url)
    soup = BeautifulSoup(response.content, "html.parser")
    matched_books = []

    for book in soup.find_all("article", {"class": "product_pod"}):
        title = book.h3.a["title"]
        price = book.find("p", {"class": "price_color"}
                          ).text.replace("\u00a3", "") + " Euros"

        if query.lower() in title.lower():
            matched_books.append({
                "matching_indicator": "Match",
                "title": title,
                "price": price
            })
        else:
            matched_books.append({
                "matching_indicator": "No match",
                "title": title,
                "price": price
            })

    return matched_books


@app.route("/search/", methods=["GET"])
@cache.cached(timeout=300, query_string=True)
def search():
    # Task 1: Web Scraping and Data Extraction & Task 4: API Development
    # Bonus Task 5: Caching Strategy
    query = request.args.get("query")
    # print(query)

    async def search_async():
        async with httpx.AsyncClient() as client:
            response = await client.get(base_url)
            soup = BeautifulSoup(response.content, "html.parser")
            categories = soup.find("div", {"class": "side_categories"}).find(
                "ul").find("li").find("ul").find_all("a")
            matched_category = []

            for category in categories:
                category_url = base_url + category["href"]
                matched_category.append(
                    search_books(query, category_url, client))

            matched_books_by_category = await asyncio.gather(*matched_category)
            results = []

            for category_name, category_books in zip(categories, matched_books_by_category):
                category_results = []

                for book in category_books:
                    # print(book)
                    if book["matching_indicator"] == "Match":
                        category_results.append({
                            "category": category_name.text.strip(),
                            "title": book["title"],
                            "price": book["price"]
                        })
                if category_results:
                    results.extend(category_results)

            return results

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    matched_books = loop.run_until_complete(search_async())

    return jsonify(matched_books)


if __name__ == "__main__":
    app.run()
