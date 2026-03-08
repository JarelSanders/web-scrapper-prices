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

    # loop through all <li> elements in the category list
    for li in category_ul.find_all("li"):
        a_tag = li.find("a")
        relative_url = a_tag["href"]
        full_url = urljoin(base_url, relative_url.strip())
        category_urls.append(full_url)
        li_elements = category_ul.find_all("li")

    # print(category_ul)

    # print category URLs
    for url in category_urls:
        current_page_url = url
        print(url)

        # loop through all pages in the current category until there is no next page
        while current_page_url is not None:
            r = requests.get(current_page_url)
            # set encoding to UTF-8 to prevent weird characters like 'Â'
            r.encoding = 'utf-8'
            # parse the HTML content of the page
            soup = BeautifulSoup(r.text, 'html.parser')

            # scrape books on this page
            book_find = soup.find_all('article', class_='product_pod')

            # iterating through the articles_find method to print each book name, price and availability
            for article in book_find:

                # convert star rating word into a numeric value
                book_rating = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}[
                    article.find('p', class_='star-rating')['class'][1]]

                # find the <h3> inside the article
                h3_tag = article.find('h3')

                # Find the <a> tag inside the <h3>
                a_tag = h3_tag.find('a')

                # print(book_name)
                # print(book_price)
                # print(book_availability)
                # print(book_name, book_price, book_availability)
                # print()

                # book title, price, avilability and rating
                book_name = a_tag['title']
                book_price = article.find('p', class_='price_color').text
                book_availability = article.find(
                    'p', class_='instock availability').text.strip()
                # book_rating = article.find('i', class_='icon-star')

                # add the book info to the books list
                books.append({
                    "book_name": book_name,
                    "book_price": book_price,
                    "book_availability": book_availability,
                    "book_Star_rating": book_rating
                })
            # check if a next page exists on the current page
            next_li = soup.find('li', class_='next')
            if next_li:
                # get the relative URL from the <a> tag inside the <li class="next">
                next_page_relative = next_li.find('a')['href']
                # buildfull URL for the next page
                current_page_url = urljoin(
                    current_page_url, next_page_relative)
            else:

                current_page_url = None
# prints the list of books
print(books)

# convert the list of book dictionaries into a DataFrame
df = pd.DataFrame(books)

# convert the cleaned string values to float so they can be used in ML models
df['book_price'] = df['book_price'].str.replace(
    '£', '').str.strip().astype(float)

# save all books to CSV
df.to_excel("output.xlsx", index=False)
