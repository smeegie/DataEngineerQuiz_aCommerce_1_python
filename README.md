# data-engineer-quiz-easy
This project contains the prompts, data, and starter code for the Graduate/Associate Data Engineer quiz.

## Task
Browse through the following fake on-line bookstore: http://books.toscrape.com/. This website is meant for toying with scraping.

The goal of the task is to create an end-to-end flow that scrapes the website for data on books, and then transform the scraped data so that the final CSV file contains only books that have at least a four-star rating and Price (incl. tax) under £20. A skeleton code base has been provided for you to extend. Feel free to refactor the code in any way you see fit.

The first step is to scrape the website, collecting data on all available books and storing it as a JSON file first. This will be the Scraper's job (src/scraper.py). For each book, we want the following info:

 - UPC
 - Product Type
 - Price (excl. tax)
 - Price (incl. tax)
 - Tax
 - Availability
 - Number of reviews
 - Description
 - Rating
 - Title
 
Below is a sample record from the JSON file if the Scraper is implemented correctly:
```
{
	"UPC": "a897fe39b1053632",
	"Product Type": "Books",
	"Price (excl. tax)": "Â£51.77",
	"Price (incl. tax)": "Â£51.77",
	"Tax": "Â£0.00",
	"Availability": "In stock (22 available)",
	"Number of reviews": "0",
	"Description": "It's hard to imagine a world without A Light in the Attic.",
	"Rating": "Three",
	"Title": "A Light in the Attic"
}
```

The second step is to process the JSON file containing scraped data, filter it so that only books that have at least a four-star rating and Price (incl. tax) under £20 are included, and convert it to CSV format. This will be the Transformer's job (src/transformer.py).

The two steps should be encapsulated by a single framework (src/framework.py), and the framework should be executed in main.py. The following command will be executed to test your code:
```
$ python main.py
```
NOTE: Make sure to update requirements.txt accordingly with any additional libraries as we will setup a virtual environment based on it prior to testing your code.

## Evaluation
You will be evaluated on both code accuracy and code quality.

## Hints
1. The website has a total of 50 pages that you will have to loop through to get all book links. You can set it to 1 first when you develop your code.
2. You can create additional helper methods in the child class to help with scraping.

## Bonus
Design the Transformer so that it can handle an arbitrarily large JSON file that won't fit in memory.
