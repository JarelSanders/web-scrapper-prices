# Book Price Web Scraper

A Python web scraping project that collects book information from *Books to Scrape* and exports the data for analysis.

The scraper extracts key details for each book and organizes them into a structured dataset using Pandas.

## Data Collected

* Book titles
* Prices
* Ratings
* Stock availability

## Features

* Scrapes multiple book categories
* Handles pagination across category pages
* Converts rating classes into numeric values
* Stores results in a Pandas DataFrame
* Exports the dataset to Excel for further analysis

## Technologies Used

* Python
* BeautifulSoup
* Requests
* Pandas

## Output

The script generates a structured dataset containing all scraped books and saves the results to an Excel file.

## Future Improvements

* Add additional data fields from book detail pages
* Improve data cleaning and validation
* Add visualization or analysis of the collected dataset
