import logging
from bs4 import BeautifulSoup
import re


def parse_profile_html(html: str) -> dict:
    """
    Parse the HTML content of a provider's profile to extract key-value pairs.

    Args:
        html (str): The HTML content as a string.

    Returns:
        dict: A dictionary containing the extracted profile data.
    """
    soup = BeautifulSoup(html, 'html.parser')
    data = {}

    # Find all <td> elements and process their <b> children
    td_elements = soup.find_all('td')
    for td in td_elements:
        b_tag = td.find('b')
        if b_tag:
            key = b_tag.get_text(strip=True).replace(":", "")
            value = b_tag.next_sibling.strip() if b_tag.next_sibling else None
            if value:
                data[key] = value

    return data


def parse_location_html(html: str) -> dict:
    """
    Extract latitude, longitude, and address information from the HTML content.

    Args:
        html (str): The HTML content as a string.

    Returns:
        dict: A dictionary containing 'latitude', 'longitude', and 'address' if found, otherwise None.
    """
    soup = BeautifulSoup(html, 'html.parser')
    result = {}

    # Extract latitude and longitude from JavaScript variables
    script_tags = soup.find_all('script', type="text/javascript")
    for script in script_tags:
        if script.string and 'var lat' in script.string:
            lat_match = re.search(r'var lat = "([-+]?[0-9]*\.?[0-9]+)"', script.string)
            lng_match = re.search(r'var lng = "([-+]?[0-9]*\.?[0-9]+)"', script.string)
            if lat_match and lng_match:
                result['latitude'] = float(lat_match.group(1))
                result['longitude'] = float(lng_match.group(1))
                break

    # Extract address from the page
    address_div = soup.find('div', {'id': 'facilityaddress'})
    if address_div:
        address = address_div.find('span')
        if address:
            result['address'] = address.get_text(strip=True)

    return result if 'latitude' in result and 'longitude' in result else None


def parse_site_address(html: str) -> str:
    """
    Extract the site address from the HTML content.

    Args:
        html (str): The HTML content as a string.

    Returns:
        str: The extracted site address, or None if not found.
    """
    soup = BeautifulSoup(html, 'html.parser')

    # Find the "Site Address" span and extract the text
    address_span = soup.find('span', text=lambda t: t and 'Site Address:' in t)
    if address_span:
        address_text = address_span.find_next('span').text.strip()
        return address_text

    return None


def parse_total_capacity(html: str) -> str:
    """
    Extract the total capacity from the provided HTML content.

    Args:
        html (str): The HTML content as a string.

    Returns:
        str: The extracted total capacity, or None if not found.
    """
    soup = BeautifulSoup(html, 'html.parser')

    # Find the "Total Capacity" label and get the text after it
    capacity_label = soup.find('u', text=lambda t: t and 'Total Capacity:' in t)
    if capacity_label:
        capacity_text = capacity_label.find_next('td').text.strip()
        return capacity_text

    return None


def parse_program_name(html: str) -> str:
    """
    Extract the program name from the HTML content.

    Args:
        html (str): The HTML content as a string.

    Returns:
        str: The extracted program name, or None if not found.
    """
    soup = BeautifulSoup(html, 'html.parser')

    # Look for the h3 tag containing "Program Name"
    h3_tags = soup.find_all('h3')
    for h3 in h3_tags:
        if 'Program Name:' in h3.text:
            program_name = h3.text.split('Program Name: ')[-1].split('\n')[0].strip()
            return program_name

    return None


def parse_availability(string: str) -> dict:
    """
    Parse availability information from a given string to determine supported age ranges.

    Args:
        string (str): A string containing availability information.

    Returns:
        dict: A dictionary with age ranges as keys and boolean or specific values as needed.
    """
    age_ranges = {
        'AGE_INFANT_MINIMUM': None,
        'AGE_RANGE_1_YEAR': False,
        'AGE_RANGE_2_YEARS': False,
        'AGE_RANGE_3_YEARS': False,
        'AGE_RANGE_4_YEARS': False,
        'AGE_RANGE_5_YEARS': False,
        'AGE_RANGE_INFANTS': False,
        'AGE_RANGE_SCHOOL': False
    }

    if not string or not isinstance(string, str):
        return age_ranges  # Return defaults for empty or invalid input

    # Check specific patterns in the string
    if "ages 6 weeks to 12 years" in string or "6 weeks" in string:
        for key in age_ranges:
            if key != 'AGE_INFANT_MINIMUM':  # Exclude setting this here
                age_ranges[key] = True
        age_ranges['AGE_INFANT_MINIMUM'] = "6 weeks"

    if "School-Aged Children" in string:
        age_ranges['AGE_RANGE_SCHOOL'] = True

    if "Preschoolers" in string:
        age_ranges['AGE_RANGE_3_YEARS'] = True
        age_ranges['AGE_RANGE_4_YEARS'] = True
        age_ranges['AGE_RANGE_5_YEARS'] = True

    # Handle additional school-aged children
    if "additional school-aged children" in string:
        age_ranges['AGE_RANGE_SCHOOL'] = True

    return age_ranges
