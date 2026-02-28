# import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
from urllib.parse import urljoin

# url website to scrape
base_url = 'https://books.toscrape.com/'

# send GET request to site
r = requests.get(base_url)
books = []


if r.status_code == 200:

    # prevents encoding artifacts like 'Â' appearing in scraped text
    r.encoding = 'utf-8'

    # parse HTML
    soup = BeautifulSoup(r.text, 'html.parser')

    book_find = soup.find_all('article', class_='product_pod')

    # get the outer <ul> with class 'nav nav-list'
    nav_list = soup.find("ul", class_="nav nav-list")

    # finds the nested <ul> inside the first <li>
    category_ul = nav_list.find("ul")

    # get category links
    category_urls = []
    for li in category_ul.find_all("li"):
        a_tag = li.find("a")
        relative_url = a_tag["href"]
        full_url = urljoin(base_url, relative_url.strip())
        category_urls.append(full_url)

    # print category URLs
    for url in category_urls:
        print(url)

        # iterating through the articles_find method to print each book name, price and availability
        for article in book_find:
            # Find the <h3> inside the article
            h3_tag = article.find('h3')

            # Find the <a> tag inside the <h3>
            a_tag = h3_tag.find('a')


            book_name = a_tag['title']
            book_price = article.find('p', class_='price_color').text
            book_availability = article.find(
                'p', class_='instock availability').text.strip()
            

            # print(book_name)
            # print(book_price)
            # print(book_availability)
            # print(book_name, book_price, book_availability)
            # print()
            

            # stores the information into a dictionary so i can add it into a list
            book_info = {
                "book_name": book_name,
                "book_price": book_price,
                "book_availability": book_availability,
            }
            

            books.append(book_info)
# prints the list of books
print(books)

# Convert the list of book dictionaries into a DataFrame
df = pd.DataFrame(books)

# convert the cleaned string values to float so they can be used in ML models
df['book_price'] = df['book_price'].str.replace(
    '£', '').str.strip().astype(float)

# save all books to CSV
df.to_excel("output.xlsx", index=False)


