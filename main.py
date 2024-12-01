"""This script serves as a skeleton template for synchronous AgentQL scripts."""

import logging

import agentql
from agentql.ext.playwright.sync_api import Page
from playwright.sync_api import sync_playwright
import polars as pl
# Set up logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Set the URL to the desired website
URL = "https://webscraper.io/test-sites/e-commerce/allinone"


def main():
    with sync_playwright() as p, p.chromium.launch(headless=False) as browser:
        # Create a new page in the browser and wrap it to get access to the AgentQL's querying API
        page = agentql.wrap(browser.new_page())

        # Navigate to the desired URL
        page.goto(URL)

        response = get_response(page)
        
        # Use products as a key as that is what we set as the key in our AgentQLquery
        data = response['products']

        # Write the data to an Excel file. We are using Excel because we need to support nested data
        write_response_to_xlsx(data, "output.xlsx")

def get_response(page: Page):
    query = """
{
    products[] {
        product_name,
        product_price,
        product_description
    }
}
    """

    return page.query_data(query)

def write_response_to_xlsx(data, filename:str = "output.xlsx"):
    df = pl.DataFrame(data)
    df.write_excel(filename)

if __name__ == "__main__":
    main()
