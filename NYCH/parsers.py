import re

def parse_provider_html(html: str) -> list:
    """
    Parse provider HTML to extract location data embedded in JavaScript objects.

    Args:
        html (str): The HTML content as a string.

    Returns:
        list: A list of dictionaries, each representing a location with extracted key-value pairs.
    """
    # Regular expression to match JavaScript location definitions
    location_pattern = re.compile(
        r"var location = \{\};\s*(.*?)mapLoactionData\.push\(location\);", re.DOTALL
    )

    # Regular expression to extract individual key-value pairs from the JavaScript object
    key_value_pattern = re.compile(r"location\.(\w+)='(.*?)';")

    # Find all location blocks in the HTML
    location_blocks = location_pattern.findall(html)

    locations = []

    for block in location_blocks:
        location_data = {}

        # Extract key-value pairs defined as location.<key>='<value>';
        for match in key_value_pattern.findall(block):
            key, value = match
            location_data[key] = value

        # Additional key-value pairs not explicitly captured by the first regex
        additional_info_pattern = re.compile(r"(\w+)=['\"](.*?)['\"];?")
        for match in additional_info_pattern.findall(block):
            key, value = match
            if key not in location_data:  # Avoid overwriting existing keys
                location_data[key] = value

        # Add the extracted data to the locations list
        locations.append(location_data)

    return locations
