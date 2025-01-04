import os
import json
import logging


def build_profile_records(profiles_folder: str, locations_folder: str) -> list:
    """
    Build a list of profile records by combining profile JSON files with corresponding location JSON files.

    Args:
        profiles_folder (str): Path to the folder containing profile JSON files.
        locations_folder (str): Path to the folder containing location JSON files.

    Returns:
        list: A list of dictionaries representing combined profile and location data.
    """
    profiles = []

    # Iterate through all JSON files in the profiles folder
    for profile_file in os.listdir(profiles_folder):
        profile_path = os.path.join(profiles_folder, profile_file)

        if profile_file.endswith(".json"):  # Ensure it's a JSON file
            record_id = profile_file.replace("profile_", "").replace(".json", "")

            with open(profile_path, 'r', encoding='utf-8') as file:
                profile_record = json.load(file)  # Load JSON data
                profile_record['record_id'] = record_id  # Add the record ID

                # Check for a matching location file
                location_file = f"location_{record_id}.json"
                location_path = os.path.join(locations_folder, location_file)

                if os.path.exists(location_path):
                    with open(location_path, 'r', encoding='utf-8') as loc_file:
                        location_data = json.load(loc_file)  # Load location data
                else:
                    location_data = None  # No matching location data

                profile_record['location_data'] = location_data
                profiles.append(profile_record)  # Append combined data

    return profiles


def build_availability_string(age_dict: dict) -> str:
    """
    Convert an age dictionary into a formatted availability string.

    Args:
        age_dict (dict): Dictionary with age range keys and boolean values.

    Returns:
        str: A formatted string listing available age ranges, separated by '|~|'.
    """
    age_brackets = [
        ('AGE_RANGE_INFANTS', '0-12 Months (Infant)'),
        ('AGE_RANGE_1_YEAR', '1 year'),
        ('AGE_RANGE_2_YEARS', '2 years'),
        ('AGE_RANGE_3_YEARS', '3 years'),
        ('AGE_RANGE_4_YEARS', '4 years'),
        ('AGE_RANGE_5_YEARS', '5 years'),
        ('AGE_RANGE_SCHOOL', 'School-age')
    ]

    result = []

    # Check each age range and append its label if available
    for key, label in age_brackets:
        if age_dict.get(key, False):  # Default to False if key is missing
            result.append(label)

    return '|~|'.join(result)


def transform_record(record: dict) -> dict:
    """
    Transform a record dictionary to match the template CSV column structure.

    Args:
        record (dict): The input record with keys and values to map.

    Returns:
        dict: A transformed dictionary with keys matching the template columns.
    """
    county_info = record.get("county_info", {})

    transformed_record = {
        "PROGRAM_NAME": record.get("program_name", ""),
        "ADDRESS_CITY": county_info.get("county", "Unknown City"),
        "ADDRESS_COUNTRY": "United States",  # Hardcoded value
        "ADDRESS_BOUROUGH": record.get("School District", ""),
        "ADDRESS_COUNTY": county_info.get("county", ""),
        "ADDRESS_LATITUDE": record.get("lat", ""),
        "ADDRESS_LONGITUDE": record.get("long", ""),
        "ADDRESS_STATE": "New York",  # Hardcoded value
        "ADDRESS_STREET": record.get("address", "").split(",")[0] if record.get("address") else "",
        "ADDRESS_ZIPCODE": record.get("address", "").split(",")[-1].strip().replace('NY ', "") if record.get("address") else "",
        "AGE_RANGE": record.get("age_range_string", ""),
        "AGE_RANGE_1_YEAR": record.get("age_ranges", {}).get("AGE_RANGE_1_YEAR", False),
        "AGE_RANGE_2_YEARS": record.get("age_ranges", {}).get("AGE_RANGE_2_YEARS", False),
        "AGE_RANGE_3_YEARS": record.get("age_ranges", {}).get("AGE_RANGE_3_YEARS", False),
        "AGE_RANGE_4_YEARS": record.get("age_ranges", {}).get("AGE_RANGE_4_YEARS", False),
        "AGE_RANGE_5_YEARS": record.get("age_ranges", {}).get("AGE_RANGE_5_YEARS", False),
        "AGE_RANGE_INFANTS": record.get("age_ranges", {}).get("AGE_RANGE_INFANTS", False),
        "AGE_RANGE_SCHOOL": record.get("age_ranges", {}).get("AGE_RANGE_SCHOOL", False),
        "GEN_PHONE_1": record.get("Phone", ""),
        "GEN_PROGRAM_SETTING": record.get("Program Type", ""),
        "GEN_WEBSITE": f"https://hs.ocfs.ny.gov/DCFS/Profile/Index/{record['record_id']}"  # Constructed URL
    }

    return transformed_record
