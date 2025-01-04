from scrapers import scrape_provider_ids, scrape_html_from_url
from parsers import (
    parse_profile_html,
    parse_program_name,
    parse_site_address,
    parse_total_capacity,
    parse_location_html,
    parse_availability,
)
from transformers import build_profile_records, build_availability_string, transform_record
import logging
import os
import json
import petl as etl


# Configure logging for the application
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def save_to_json(file_path: str, data: dict):
    """
    Save data to a JSON file.

    Args:
        file_path (str): The path to the JSON file.
        data (dict): The data to save.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4)


def main():
    """
    Main function to orchestrate the scraping, parsing, and transforming of OCFS data.
    """
    # Configure the counties and program types to scrape
    counties = ["Manhattan", "Bronx", "Brooklyn", "Queens", "Staten Island"]
    program_types = ["Family Day Care", "Group Family Day Care", "School-Age Child Care"]

    # Scrape provider IDs for specified counties and program types
    for county in counties:
        for program_type in program_types:
            logging.info(f"Scraping data for {county}, {program_type}...")
            scrape_provider_ids(county, program_type)

    # Load provider IDs from CSV
    provider_ids = list(etl.fromcsv("OCFS/raw_data/provider_ids.csv").values("provider_id"))
    total_ids = len(provider_ids)

    logging.info(f"Starting scraping process for {total_ids} provider IDs.")
    for index, provider_id in enumerate(provider_ids, start=1):  # Limiting to first 5 IDs for testing
        try:
            logging.info(f"Scraping profile for provider ID {provider_id} ({index}/{total_ids})")

            # Scrape profile data
            profile_url = f"https://hs.ocfs.ny.gov/DCFS/Profile/Index/{provider_id}"
            profile_html = scrape_html_from_url(profile_url)
            if profile_html:
                profile_data = parse_profile_html(profile_html)
                profile_data["program_name"] = parse_program_name(profile_html)
                profile_data["address"] = parse_site_address(profile_html)
                profile_data["total_capacity"] = parse_total_capacity(profile_html)
                profile_data["raw_html"] = profile_html
                save_to_json(f"OCFS/raw_data/profiles/profile_{provider_id}.json", profile_data)
                logging.info(f"Saved profile data for provider ID {provider_id}.")

            # Scrape location data
            location_url = f"https://hs.ocfs.ny.gov/DCFS/Map/Index/{provider_id}"
            location_html = scrape_html_from_url(location_url)
            if location_html:
                location_data = parse_location_html(location_html)
                if location_data:
                    location_data["raw_html"] = location_html
                    save_to_json(f"OCFS/raw_data/locations/location_{provider_id}.json", location_data)
                    logging.info(f"Saved location data for provider ID {provider_id}.")
        except Exception as e:
            logging.error(f"An error occurred for provider ID {provider_id}: {e}")

    # Build profile records from scraped profiles and locations
    profiles_from_files = build_profile_records(
        profiles_folder="OCFS/raw_data/profiles/", locations_folder="OCFS/raw_data/locations/"
    )

    # Load additional county data from provider IDs CSV
    county_data = {r["provider_id"]: r for r in etl.fromcsv("OCFS/raw_data/provider_ids.csv").dicts()}

    # Process raw profiles
    raw_profiles = (
        etl.fromdicts(profiles_from_files)
        .addfield("lat", lambda rec: rec["location_data"].get("latitude", "") if rec.get("location_data") else "")
        .addfield("long", lambda rec: rec["location_data"].get("longitude", "") if rec.get("location_data") else "")
        .addfield("age_ranges", lambda rec: parse_availability(rec["total_capacity"]))
        .addfield("age_range_string", lambda rec: build_availability_string(rec["age_ranges"]))
        .addfield("county_info", lambda rec: county_data.get(rec["record_id"], ""))
        .cutout("raw_html", "location_data")  # Remove unnecessary fields
    )

    # Transform raw profiles to match the desired structure and save to CSV
    transformed_records = (
        etl.fromdicts([transform_record(r) for r in raw_profiles.dicts()])
        .tocsv("OCFS/result_data/OCFS_result_data.csv")
    )

    logging.info("Data transformation and export completed successfully.")


if __name__ == "__main__":
    main()
