
# Child Care Scraping and Transformation Toolkit

This repository provides a toolkit for scraping, parsing, and transforming data related to child care providers in New York City and New York State. The two main modules, `NYCH` (for New York City Health) and `OCFS` (for New York State Office of Children and Family Services), are designed to scrape web-based provider data, process it, and output transformed CSV files for analysis.

## Table of Contents
- [Summary](#summary)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [Running the Scrapers](#running-the-scrapers)
  - [Running `NYCH/main.py`](#running-nychmainpy)
  - [Running `OCFS/main.py`](#running-ocfsmainpy)
- [Design and Organization Patterns](#design-and-organization-patterns)

---

## Summary

This application automates the process of extracting, parsing, and transforming child care provider data. The data is scraped from two different sources:
1. **NYCH**: Focuses on scraping and processing provider data from New York City Health's child care database.
2. **OCFS**: Targets New York State's Office of Children and Family Services provider database.

Both modules are organized around a modular architecture:
- **Scrapers**: Handle the web scraping tasks using Selenium or `requests`.
- **Parsers**: Extract relevant data from HTML content using regular expressions or libraries like BeautifulSoup.
- **Transformers**: Process raw parsed data into structured formats, ready for analysis.

The outputs are saved in CSV files, facilitating downstream analytics or integration into other systems.

---

## Repository Structure

The repository is structured as follows:

```
NYCH/
    raw_data/        # Contains raw scraped data in JSON or CSV format
    result_data/     # Contains transformed data in CSV format
    scrapers.py      # Scraping logic for NYCH
    parsers.py       # HTML parsing logic for NYCH
    transformers.py  # Data transformation logic for NYCH
    main.py          # Main script to orchestrate scraping and processing for NYCH

OCFS/
    raw_data/        # Contains raw scraped data in JSON or CSV format
    result_data/     # Contains transformed data in CSV format
    scrapers.py      # Scraping logic for OCFS
    parsers.py       # HTML parsing logic for OCFS
    transformers.py  # Data transformation logic for OCFS
    main.py          # Main script to orchestrate scraping and processing for OCFS

final_cleanup.ipynb  # Optional notebook for post-processing the data
nyc_zip_to_county.json # Helper JSON file for NYC zip-to-county mapping
requirements.txt     # Python dependencies
LICENSE              # License for the repository
README.md            # This documentation
```

---

## Installation

### Prerequisites
1. **Python**: Ensure you have Python 3.8+ installed on your system.
2. **Chromedriver**: If you plan to run Selenium-based scrapers (used in `OCFS`), ensure `chromedriver` is installed and available in your PATH. Installation instructions can be found [here](https://chromedriver.chromium.org/downloads).

### Setup

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Verify installation:
   ```bash
   python --version
   pip list
   ```

---

## Running the Scrapers

### Running `NYCH/main.py`


1. Run the main script:
   ```bash
   python NYCH/main.py
   ```

2. Outputs:
   - Raw scraped data will be saved in `NYCH/raw_data/` (e.g., `raw_providers.csv`).
   - Transformed data will be saved in `NYCH/result_data/` (e.g., `NYCH_result_data.csv`).

3. Note: If you encounter network or connection issues, check your internet connection and ensure the URL is accessible.

---

### Running `OCFS/main.py`

1. Run the main script:
   ```bash
   python OCFS/main.py
   ```

2. Outputs:
   - Raw scraped data will be saved in `OCFS/raw_data/` (e.g., `provider_ids.csv`).
   - Transformed data will be saved in `OCFS/result_data/` (e.g., `OCFS_result_data.csv`).

3. Note: Ensure `chromedriver` is installed and accessible. Update the `chromedriver_path` in `OCFS/scrapers.py` if necessary.

---

## Design and Organization Patterns

### Modular Design
Both `NYCH` and `OCFS` follow a modular design with clearly separated responsibilities:
1. **Scrapers**: Handle data fetching using HTTP requests or Selenium.
2. **Parsers**: Extract meaningful data from raw HTML content using regex or BeautifulSoup.
3. **Transformers**: Normalize and transform the parsed data into structured CSV-ready formats.

### Consistent File Structure
The file structure for both `NYCH` and `OCFS` mirrors each other:
- `raw_data/` and `result_data/` folders store raw and processed data, respectively.
- Each module (`scrapers.py`, `parsers.py`, `transformers.py`) corresponds to a specific stage of the data pipeline.
- `main.py` orchestrates the full process, tying the scraper, parser, and transformer together.

### Shared Practices
- **Logging**: Both modules use Python's `logging` library for consistent and informative logging.
- **Error Handling**: Exceptions during scraping or processing are caught and logged, ensuring the scripts can continue running.
- **Extensibility**: New scraping targets or transformations can be easily added by extending the respective modules.

### Differences Between NYCH and OCFS
- **Scraping Methodology**:
  - `NYCH` relies on HTTP POST requests to fetch data.
  - `OCFS` uses Selenium to interact with a web interface and navigate pages.
- **Parsing**:
  - `NYCH` parses JavaScript-embedded data in HTML.
  - `OCFS` parses structured table data and dropdown menus.
- **Transformation**:
  - Both modules share similar transformation logic but adapt to the differences in their input data structure.

---

Feel free to customize or expand the scripts as needed for your use case!

---
