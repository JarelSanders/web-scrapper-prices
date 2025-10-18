# import os
from bs4 import BeautifulSoup
import requests
import pandas as pd

# url os website to scrape
url = 'https://books.toscrape.com/index.html'

# send GET request to site
r = requests.get(url)

if r.status_code == 200:
    # displays url
    print(url)

    # print('Status code', r.status_code)
    print()

    # parse HTML
    soup = BeautifulSoup(r.text, 'html.parser')
    # soup = BeautifulSoup(r.content, 'html5lib')
    # print(soup)

    # find all <a> tags
    myFind = soup.find_all('a', title=True)
    # print(myFind)

    # Extract all book titles from the 'title' attribute
    book_titles = [book['title'] for book in myFind]
    # print(book_titles)

    # print()
    # create an empty pandas dataframe
    df = pd.DataFrame()
    # df['Book'] = None
    # # df['Price'] = None
    # df['In_Stock'] = None

    # Find all price elements by class
    find_price = soup.find_all('p', class_='price_color')

    # Extract price text from each element
    book_price = [price.text for price in find_price]
    # print(book_price)

    # Find all availability elements
    find_available = soup.find_all('p', class_='instock availability')

    # Clean and extract availability text
    book_availability = [avail.text.strip() for avail in find_available]

    # print(book_availability)

    # Add book titles to DataFrame
    df['Book'] = book_titles

    # Add book price to DataFrame
    df['Price'] = book_price

    # Add book availability to DataFrame
    df['In_Stock'] = book_availability

    # prints updated dataframe
    print(df)

    # exports dataframe to EXCEL
    df.to_excel('output.xlsx')


else:
    # prints message is request is not found
    print('NotFound')
