import logging
import sys
import copy
import petl as etl
from scrapers import scrape_provider_html
from parsers import parse_provider_html
from transformers import transform_record


def main():
    """
    Main function to orchestrate scraping, parsing, and transforming provider data
    for child care services in New York City.
    """
    url = "https://a816-healthpsi.nyc.gov/ChildCare/search"
    age_ranges = [
        "Child Care - Infants/Toddlers",
        "Child Care - Pre School",
        "School Based Child Care",
    ]

    # Mapping age ranges to structured dictionaries for downstream use
    age_range_map = {
        "Child Care - Infants/Toddlers": {
            "AGE_INFANT_MINIMUM": None,
            "AGE_RANGE_1_YEAR": True,
            "AGE_RANGE_2_YEARS": False,
            "AGE_RANGE_3_YEARS": False,
            "AGE_RANGE_4_YEARS": False,
            "AGE_RANGE_5_YEARS": False,
            "AGE_RANGE_INFANTS": True,
            "AGE_RANGE_SCHOOL": False,
        },
        "Child Care - Pre School": {
            "AGE_INFANT_MINIMUM": None,
            "AGE_RANGE_1_YEAR": False,
            "AGE_RANGE_2_YEARS": True,
            "AGE_RANGE_3_YEARS": True,
            "AGE_RANGE_4_YEARS": True,
            "AGE_RANGE_5_YEARS": True,
            "AGE_RANGE_INFANTS": False,
            "AGE_RANGE_SCHOOL": False,
        },
        "School Based Child Care": {
            "AGE_INFANT_MINIMUM": None,
            "AGE_RANGE_1_YEAR": False,
            "AGE_RANGE_2_YEARS": False,
            "AGE_RANGE_3_YEARS": False,
            "AGE_RANGE_4_YEARS": False,
            "AGE_RANGE_5_YEARS": False,
            "AGE_RANGE_INFANTS": False,
            "AGE_RANGE_SCHOOL": True,
        },
    }

    provider_results = []

    # Scrape and parse data for each age range
    for age_range in age_ranges:
        result = scrape_provider_html(url, age_range)
        if result["status_code"] != 200:
            logging.warning(f"Skipping age range {age_range} due to failed fetch.")
            continue

        # Parse provider data from HTML
        providers = parse_provider_html(result["raw_html"])

        # Build a table with additional age range information
        table = (
            etl.fromdicts(providers)
            .addfield("age_range", age_range_map[age_range])
        )

        # Append the parsed table to the results list
        provider_results.append(table)

    # Process and save the results
    if provider_results:
        # Concatenate all provider tables
        all_providers = etl.cat(*provider_results)

        # Save raw provider data to CSV
        raw_providers = copy.deepcopy(all_providers)
        try:
            raw_providers.tocsv("NYCH/raw_data/raw_providers.csv")
            logging.info("All raw provider data saved to raw_providers.csv")
        except Exception as e:
            logging.error(f"Failed to save raw provider data to CSV: {e}")

        # Transform and save the provider data
        try:
            transformed_providers = [transform_record(rec) for rec in all_providers.dicts()]
            etl.fromdicts(transformed_providers).tocsv("NYCH/result_data/NYCH_result_data.csv")
            logging.info("Successfully transformed and saved provider records.")
        except Exception as e:
            logging.error(f"Failed to save transformed provider data to CSV: {e}")
    else:
        logging.warning("No provider data to process and save.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.critical(f"Unhandled exception: {e}")
        sys.exit(1)
