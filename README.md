# Commodity Price Volatility & Social Sentiment Correlation

This project explores the relationship between high-frequency commodity price movements (e.g., oil, gold, silver) and social-media sentiment (e.g., Reddit post volume and tone). By aligning price volatility with sentiment trends, you can uncover whether online chatter can act as an early indicator for short-term commodity moves.

## Table of Contents

- [Project Structure](#project-structure)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Workflow](#workflow)
- [Data Extraction](#data-extraction)
- [Database Setup](#database-setup)
- [Exploratory Data Analysis](#exploratory-data-analysis)
- [Tableau Analysis](#tableau-analysis)
- [Output Data](#output-data)

## Project Structure

```
Commodity-Price-Volatility-Social-Sentiment-Correlation-using-Tabelau/
├── analysis/ # Exploratory data analysis scripts
│ └── exploratory_data_analysis.py
├── data_ingestion/ # Data extraction scripts
│ ├── fetch_prices.py
│ └── fetch_reddit.py
├── etl/ # Data loading utilities
│ └── load_to_mysql.py
├── exports/ # Raw & processed CSV exports
│ ├── staging_prices.csv
│ ├── staging_reddit.csv
│ ├── prices.csv
│ ├── sentiment.csv
│ └── daily_metrics.csv
├── outputs/ # Generated EDA figures
│ ├── Figure_1.png
│ ├── Figure_2.png
│ ├── Figure_3.png
│ ├── Figure_4.png
│ └── Figure_5.png
├── scripts/ # Utility scripts
│ └── export_sql_data.py
├── sql/ # Database schema & transformation SQL
│ ├── database_creation.sql
│ ├── staging_tables.sql
│ ├── schema.sql
│ ├── daily_metrics.sql
│ └── final_tables.sql
├── tableau/ # Tableau workbook
│ └── Commodity_and_Sentiment_Analysis.twbx
├── LICENSE # License file
├── README.md # Project documentation
└── requirements.txt # Python dependencies

```

## Features

- **Live price fetch** using `yfinance` for symbols like `CL=F`, `GC=F`, `SI=F` at hourly granularity.
- **Reddit sentiment** via PRAW and VADER/TextBlob for subreddits such as `r/WallStreetBets`, `r/Gold`, `r/Silver`.
- **Upsert** into MySQL tables for prices and sentiment metrics.
- **Metrics export** to CSV for rolling volatility, correlation, and returns.
- **Interactive Tableau dashboard** packaged in `tableau/Commodity_and_Sentiment_Analysis.twbx`.

## Prerequisites

- Python 3.8+ installed  
- MySQL server (v5.7+ or v8.0+)  
- Tableau Desktop (to open `.twbx` workbook)  

## Installation

1. Clone this repository:  
   ```bash
   git clone https://github.com/Anaghar27/Commodity-Price-Volatility-Social-Sentiment-Correlation-using-Tabelau.git
   cd Commodity-Price-Volatility-Social-Sentiment-Correlation-using-Tabelau
   ```
2. Install Python dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Obtaining Reddit API Credentials
- Navigate to your Reddit app preferences at https://www.reddit.com/prefs/apps.
- Click Create App or Create Another App.
- Select script for the application type.
- Provide a name (e.g., commodity-sentiment-app).
- Enter a redirect URI (e.g., http://localhost:8080).
- Submit and note your Client ID (displayed under the app name) and Client Secret.

2. Copy the below to `.env` file and fill in the credentials:  
   ```ini
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=commodity
   DB_USER=root
   DB_PASSWORD=yourpassword

   REDDIT_CLIENT_ID=abc123
   REDDIT_CLIENT_SECRET=def456
   REDDIT_USER_AGENT=your_app_name
   ```
3. Ensure MySQL user has privileges to create databases and tables.

## Workflow

Follow these steps in order:

1. **Run SQL setups** to create database & staging tables:
   ```bash
   mysql -u root -p < sql/database_creation.sql
   mysql -u root -p < sql/staging_tables.sql
   mysql -u root -p < sql/final_tables.sql

   OR 
   Just run the below command:

   mysql -u root -p < sql/schema.sql
   ```
2. **Extract data** from source APIs:
   ```bash
   python data_injestion/fetch_prices.py
   python data_injestion/fetch_reddit.py
   ```
3. **Load into MySQL**:
   ```bash
   python etl/load_to_mysql.py
   ```
4. **Run EDA** (exploratory_data_analysis.py):
   ```bash
   python analysis/exploratory_data_analysis.py
   ```
   This script generates and saves the following visuals under `reports/EDA/` and prints two-line summaries for each:
   - **Correlation Heatmap**: shows Pearson correlations between 24h volatility, average sentiment, and post count.
   - **Daily Averages for CL=F, GC=F, SI=F**: overlays volatility vs. sentiment trends for each commodity.
   - **Hourly Returns Distribution**: histograms of price returns to inspect distribution and outliers.
5. **Save the data to csv** by running the py file which will save all the csv files in the exports\ folder
   ```bash
   python scripts/export_sql_data.py
   ```
6. **Open Tableau dashboard** for further analysis and storytelling:
   ```bash
   open tableau/Commodity_and_Sentiment_Analysis.twbx
   ```

## Data Extraction

- **fetch_prices.py**: pulls OHLCV data from Yahoo Finance into `staging_prices.csv`.
- **fetch_reddit.py**: retrieves hourly Reddit post counts & sentiment into `staging_reddit.csv`.

## Database Setup
1. **Create databases**: Firstly the database and the tables must be created.
   ```bash
   mysql -u root -p < sql/schema.sql
   ```
1. **Staging Tables**: load the tables with data:
   ```bash
   python src/load_to_mysql.py --staging prices staging_prices.csv
   python src/load_to_mysql.py --staging reddit staging_reddit.csv
   ```
2. **Final Tables**: transform & upsert:
   ```bash
   mysql -u root -p < sql/final_tables.sql
   ```
3. **Export Metrics**:
   ```bash
   python src/export_sql_data.py --tables prices sentiment daily_metrics
   ```

## Exploratory Data Analysis

After running `exploratory_data_analysis.py`, the following outputs are shown which is saved locally in outputs\ folder where:

- **Correlation Heatmap** (`Figure_1.png`): highlights low correlation (~0.008) between volatility and sentiment, moderate correlation (~0.12) between volatility and post count.
- **CL=F Daily Averages** (`Figure_2.png`): shows sentiment spikes often follow volatility peaks, suggesting lagged sentiment response.
- **GC=F Daily Averages** (`Figure_3.png`): illustrates gold’s high volatility peaks with relatively stable, low sentiment levels.
- **SI=F Daily Averages** (`Figure_4.png`): indicates silver sentiment can lead volatility swings, e.g., sentiment drop on May 23 precedes higher volatility.
- **Hourly Returns Distribution** (`Figure_5.png`): reveals returns are tightly clustered around zero with occasional outliers, confirming price stability with rare spikes.

## Tableau Analysis

Open the provided `.twbx` to explore:

- **Small multiples**: overlay price & sentiment timelines for each commodity.
- **Bubble chart**: maps day-over-day volatility vs. sentiment change, bubble size = post count.
- **Story sheet**: annotated narrative hypothesizing Reddit’s role in short-term commodity moves.

## Output Data

- `data/prices.csv`: Hourly OHLCV series  
- `data/sentiment.csv`: Hourly post counts & sentiment  
- `data/daily_metrics.csv`: Rolling volatility & correlation metrics  
