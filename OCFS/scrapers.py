import os
import csv
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# NOTE - This must be set to the machine this is running on; parameterize in production for flexibility
chromedriver_path = "/usr/local/bin/chromedriver"

def scrape_provider_ids(county: str, program_type: str):
    """
    Scrape provider IDs from the OCFS website based on the given county and program type.

    Parameters:
        county (str): The county or borough name to filter by.
        program_type (str): The program type to filter by.

    Returns:
        None: Writes scraped data to a CSV file.

    Creates or appends to a CSV file 'provider_ids.csv' with columns:
        - county
        - program_type
        - provider_id
    """
    # Set up the ChromeDriver
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # CSV file path
    csv_file = "OCFS/raw_data/provider_ids.csv"

    try:
        # Navigate to the website
        url = "https://hs.ocfs.ny.gov/dcfs"
        logging.info(f"Navigating to {url}")
        driver.get(url)

        # Allow the page to load
        time.sleep(3)

        # Select the County/Borough from the dropdown
        county_dropdown = Select(driver.find_element(By.ID, "ddlCounty"))
        county_dropdown.select_by_visible_text(county)
        logging.info(f"Selected county: {county}")

        # Select the Program Type from the dropdown
        program_type_dropdown = Select(driver.find_element(By.ID, "ddlProgramType"))
        program_type_dropdown.select_by_visible_text(program_type)
        logging.info(f"Selected program type: {program_type}")

        # Set the results per page to 500
        results_per_page_dropdown = Select(driver.find_element(By.ID, "Paging_PageSize"))
        results_per_page_dropdown.select_by_visible_text("500")
        logging.info("Set results per page to 500")

        # Click the "Find Day Care" button
        find_day_care_button = driver.find_element(By.ID, "btnSubmit")
        find_day_care_button.click()
        logging.info("Clicked 'Find Day Care' button")

        # Pause to allow results to load
        time.sleep(5)

        # Initialize list to store provider data
        provider_data = []

        # Loop through paginated results
        while True:
            time.sleep(3)  # Allow time for page load
            rows = driver.find_elements(By.XPATH, "//td[contains(., 'License/Registration ID:')]")
            for row in rows:
                text = row.text
                if "License/Registration ID:" in text:
                    provider_id = text.split("License/Registration ID:")[1].split("\n")[0].strip()
                    provider_data.append((county, program_type, provider_id))
                    logging.info(f"Extracted provider ID: {provider_id}")

            # Try navigating to the next page, if available
            try:
                next_page = driver.find_element(By.LINK_TEXT, "Next Page")
                next_page.click()
                logging.info("Navigated to the next page")
                time.sleep(5)  # Allow new page to load
            except Exception:
                logging.info("No more pages to process.")
                break

        # Write data to the CSV
        file_exists = os.path.isfile(csv_file)
        with open(csv_file, "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(["county", "program_type", "provider_id"])
            writer.writerows(provider_data)

        logging.info(f"Appended {len(provider_data)} records to '{csv_file}'.")

    finally:
        # Clean up resources
        driver.quit()
        logging.info("Browser closed")

def scrape_html_from_url(url: str) -> str:
    """
    Fetch the HTML content of a given URL using Selenium.

    Parameters:
        url (str): The URL to fetch HTML content from.

    Returns:
        str: The HTML content of the page, or None if an error occurs.
    """
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        logging.info(f"Navigating to URL: {url}")
        driver.get(url)
        time.sleep(3)  # Wait for the page to load
        html_content = driver.page_source
        logging.info("Successfully fetched HTML content.")
        return html_content
    except Exception as e:
        logging.error(f"An error occurred while fetching HTML: {e}")
        return None
    finally:
        driver.quit()
        logging.info("Browser closed")
