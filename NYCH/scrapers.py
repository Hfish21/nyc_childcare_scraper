import logging
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def scrape_provider_html(url: str, age_range: str) -> dict:
    """
    Fetch provider HTML by sending a POST request with specified headers and data.

    Args:
        url (str): The URL to which the POST request will be sent.
        age_range (str): The age range filter to include in the POST data.

    Returns:
        dict: A dictionary containing:
            - 'status_code' (int): The HTTP status code of the response.
            - 'age_range' (str): The requested age range.
            - 'raw_html' (str): The HTML content of the response, or an empty string on failure.
    """
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "a816-healthpsi.nyc.gov",
        "Origin": "https://a816-healthpsi.nyc.gov",
        "Referer": "https://a816-healthpsi.nyc.gov/ChildCare/search",
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        ),
        "Cookie": (
            "JSESSIONID=A5A804C8563BC128387C041D6F652464; "
            "__RequestVerificationToken_L05ZtO1FRA2=Sb_MTZ8lSXZyIT_YtK0g5viLhXgoOfeH3jaYQqw48tsZQlGazfB60ip_"
            "XBvYrrlmWdVFc_ea44pn3qHFnHBFdqN4m5n4pKQ1B2q"
        ),
    }

    data = {
        "searchBean.linkPK": "0",
        "searchBean.pageoffset": "0",
        "searchBean.getNewResult": "true",
        "searchBean.progTypeValues": age_range,
        "searchBean.search1": "1",
        "toggle-cols": "co-1",
        "toggle-cols": "co-2",
        "toggle-cols": "co-3",
        "toggle-cols": "co-4",
        "toggle-cols": "co-5",
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        logging.info(f"Successfully fetched data for age range: {age_range}")
        return {
            "status_code": response.status_code,
            "age_range": age_range,
            "raw_html": response.text,
        }
    except requests.RequestException as e:
        logging.error(f"Failed to fetch data for age range: {age_range} - {e}")
        return {
            "status_code": None,
            "age_range": age_range,
            "raw_html": "",
        }
