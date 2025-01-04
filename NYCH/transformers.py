import logging

def build_availability_string(age_dict: dict) -> str:
    """
    Construct a formatted string representing available age ranges.

    Args:
        age_dict (dict): A dictionary with age range keys and boolean values.

    Returns:
        str: A formatted string listing available age ranges, separated by '|~|'.
    """
    age_brackets = [
        ("AGE_RANGE_INFANTS", "0-12 Months (Infant)"),
        ("AGE_RANGE_1_YEAR", "1 year"),
        ("AGE_RANGE_2_YEARS", "2 years"),
        ("AGE_RANGE_3_YEARS", "3 years"),
        ("AGE_RANGE_4_YEARS", "4 years"),
        ("AGE_RANGE_5_YEARS", "5 years"),
        ("AGE_RANGE_SCHOOL", "School-age"),
    ]

    # Build a list of age ranges that are available
    result = [label for key, label in age_brackets if age_dict.get(key, False)]

    # Join the list with the '|~|' separator
    return "|~|".join(result)


def normalize_program_type(program_type: str) -> str:
    """
    Normalize program type to fit the CSV schema.

    Args:
        program_type (str): The raw program type string.

    Returns:
        str: The normalized program type or None if the input is invalid.
    """
    if not program_type:  # Safeguard for None or empty values
        return None
    if "Infants" in program_type or "Toddlers" in program_type:
        return "Child Care Center"
    return program_type


def validate_float(value: str) -> float:
    """
    Validate and convert a string value to a float.

    Args:
        value (str): The value to convert.

    Returns:
        float: The converted float value, or None if conversion fails.
    """
    try:
        return float(value.strip()) if value.strip() else None
    except ValueError:
        logging.warning(f"Failed to convert value to float: {value}")
        return None


def transform_record(record: dict) -> dict:
    """
    Transform a raw record into a structured format for CSV export.

    Args:
        record (dict): The input record with raw data.

    Returns:
        dict: A transformed record matching the desired structure.
    """
    # Build the age range string using the age range dictionary
    age_range_str = build_availability_string(record.get("age_range", {}))

    # Transform the record into the desired schema
    transformed = {
        "PROGRAM_NAME": record.get("centerName", ""),  # Default to empty string if missing
        "ADDRESS_CITY": "New York",  # Hardcoded as it's specific to NYC
        "ADDRESS_COUNTRY": "United States",  # Hardcoded
        "ADDRESS_BOUROUGH": None,  # Placeholder for potential data
        "ADDRESS_COUNTY": "",  # Default to empty string
        "ADDRESS_LATITUDE": validate_float(record.get("lat", "")),
        "ADDRESS_LONGITUDE": validate_float(record.get("lon", "")),
        "ADDRESS_STATE": "New York",  # Hardcoded
        "ADDRESS_STREET": record.get("address", ""),
        "ADDRESS_ZIPCODE": record.get("zipCode", ""),
        "AGE_RANGE": age_range_str,
        **record.get("age_range", {}),  # Unpack age range values into the record
        "GEN_PHONE_1": record.get("phone", ""),
        "GEN_PROGRAM_SETTING": normalize_program_type(record.get("programType")),
        "GEN_WEBSITE": None,  # Placeholder for website data
    }

    return transformed
