# Asynchronous PEP Parser🔍

## Project Description

**The Asynchronous PEP Parser is designed to automatically collect information about Python Enhancement Proposals (PEPs) from the official Python website (https://peps.python.org/).
The parser's main task is to gather data about all PEPs, including their number, title, and status, and to generate a summary report of statuses in CSV format.
The parser is implemented using the Scrapy framework and leverages asynchronous methods for efficient data extraction and processing.**

## Installation and Setup

1. **Clone the repository:**
    
    ```bash
    git clone git@github.com:closecodex/scrapy_parser_pep.git
    cd scrapy_parser_pep
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv\Scripts\activate
    ```

3. **Upgrade pip and install dependencies:**
   
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Run the parser:**

   ```bash
   scrapy crawl pep
   ```
   
## Results

1. **pep_DateTime.csv: Contains three columns: number, name, and status. This file lists all PEPs with detailed information about each.**

2. **status_summary_DateTime.csv: Contains two columns: Status and Count. The file summarizes all possible PEP statuses and the number of PEPs per status. The last row of the file shows the total number of documents (Total).**

## Additional Information

1. **Author: Mariia Osmolovskaia (closecodex@github.com)**

2. **Tech Stack: Python, Scrapy, CSV**
