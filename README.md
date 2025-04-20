# CSC-325: Machine Learning Final Project
#### Developed by Huy Nguyen, Anh Le 

## Overview
This project collects, processes, and visualizes Chicago crime data. It consists of two main parts:
- **Data Crawling:** The `scrape.py` script uses Selenium with ChromeDriver to navigate to the Chicago crime dashboard, interact with UI elements (like the three-dots and export buttons), and download the dataset.
- **Data Preprocessing & Visualization:** The `preprocess.ipynb` Jupyter Notebook reads and cleans the crawled data, then creates various visualizations (e.g., bar plots, heatmaps, trend analyses) to showcase crime patterns over the years.

## Project Structure
```
├── scrape.py                 # Data crawling script
├── preprocess.ipynb          # Notebook for data cleaning and visualization
├── datasets/                 # Folder for downloaded datasets
├── Resources and Demo/       # Demo assets including plots, videos, and project pipeline PDF
│   ├── assault_plot.png
│   ├── Crawled Data Example.png
│   ├── crime_type_plot.png
│   ├── Data Crawling Demo.mov
│   ├── heatmap_monthly_2020_to_2024.png
│   ├── monthly_crime_trend_with_linear_line.png
│   ├── motor_vehicle_plot.png
│   ├── plot_location_description.png
│   ├── Project Pipeline.pdf
│   └── yearly_plot.png
└── README.md                 # This file
```

## Setup

### Prerequisites
- Python 3.x
- Google Chrome browser
- pip package manager

### Dependencies
Install the required packages via pip:
```
pip install selenium webdriver-manager pandas numpy matplotlib seaborn pydeck
```
The project uses `webdriver-manager` to handle ChromeDriver automatically.

## Usage

### 1. Running the Data Crawler
Run the `scrape.py` script to start the crawling process:
   ```
   python scrape.py
   ```

### 2. Processing and Visualizing Data
1. Open the `preprocess.ipynb` notebook in Jupyter or VS Code.
2. Execute the notebook cells sequentially:
   - The notebook reads the crawled data from `./datasets/crawled_data.csv`.
   - Processes and cleans the data.
   - Generates various visualizations (e.g., crime type distributions, yearly trends, monthly trends, heatmaps).
   - Aggregates geographic data by using Pydeck based on logitude and latitude in Chicago, rounded to the 3rd decimal.

    ### Pydeck Map Details
    - **Interactive Features:** Hovering over a column displays tooltips with the crime count and location.
    - **View State:** The map is centered on Chicago (latitude 41.8781, longitude -87.6298) with a zoom level of 10 for a city-level view.


### 3. Crime rate prediction using KNN, Random Forest, Naive Bayes, and XGBoost
#### ---> WIP (Work In Progress)

## Demonstration Resources
The folder `Resources and Demo` contains visual aids and supporting materials:
- **Images:** Visualizations such as `assault_plot.png`, `crime_type_plot.png`, `yearly_plot.png`, etc.
- **Video:** `Data Crawling Demo.mov` demonstrates the data crawling process.
- **Documentation:** `Project Pipeline.pdf` outlines the project workflow and methodology.



