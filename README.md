# CSC-325: Machine Learning Final Project
#### Developed by Huy Nguyen, Anh Le 

## Overview
This project collects, processes, and visualizes Chicago crime data. It consists of three main parts:
- **Data Crawling:** The `scrape.py` script uses Selenium with ChromeDriver to navigate to the Chicago crime dashboard, interact with UI elements (like the three-dots and export buttons), and download the dataset.
- **Data Preprocessing:** The `crim_rate_preprocessing.ipynb` Jupyter Notebook reads and cleans the crawled data, performing necessary transformations and feature engineering.
- **Data Analysis & Visualization:** The `crime_rate_analysis.ipynb` Jupyter Notebook creates various visualizations (e.g., bar plots, heatmaps, trend analyses) to showcase crime patterns over the years.
- **Crime Rate Prediction:** The `pred.py` file for implementing all the machine learning models used for this project.

## Project Structure
```
├── scrape.py                 # Data crawling script
├── pred.py                   # Python file for predicting crime rate
├── crime_rate_preprocessing.ipynb  # Notebook for data cleaning and preprocessing
├── crime_rate_analysis.ipynb      # Notebook for data analysis and visualization
├── datasets/                 # Folder for datasets
│   ├── crawled_data.csv      # Raw crawled data
│   └── cleaned_crime_data.csv # Preprocessed data
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
└── README.md                
```

## Setup

### Prerequisites
- Python 3.x
- Google Chrome browser
- pip package manager

### Dependencies
### Installing Dependencies
Install all required packages using the requirements file:
```
pip install -r requirements.txt
```

## Usage

### 1. Running the Data Crawler
Run the `scrape.py` script to start the crawling process:
   ```
   python scrape.py
   ```

### 2. Data Preprocessing
1. Open the `crim_rate_preprocessing.ipynb` notebook in Jupyter or VS Code.
2. Execute the notebook cells sequentially:
   - The notebook reads the raw data from `./datasets/crawled_data.csv`
   - Performs data cleaning and preprocessing
   - Creates new features and aggregates data
   - Saves the cleaned data to `./datasets/cleaned_crime_data.csv`

### 3. Data Analysis and Visualization
1. Open the `crime_rate_analysis.ipynb` notebook in Jupyter or VS Code.
2. Execute the notebook cells sequentially:
   - The notebook reads the preprocessed data from `./datasets/cleaned_crime_data.csv`
   - Generates various visualizations:
     - Crime type distributions
     - Yearly and monthly trends
     - Location-based analysis
     - Geographic heatmaps using Pydeck

    ### Pydeck Map Details
    - **Interactive Features:** Hovering over a column displays tooltips with the crime count and location.
    - **View State:** The map is centered on Chicago (latitude 41.8781, longitude -87.6298) with a zoom level of 10 for a city-level view.

### 4. Crime Rate Prediction using KNN, Random Forest, Naive Bayes, and XGBoost
#### ---> WIP (Work In Progress)

## Demonstration Resources
The folder `Resources and Demo` contains visual aids and supporting materials:
- **Images:** Visualizations such as `assault_plot.png`, `crime_type_plot.png`, `yearly_plot.png`, etc.
- **Video:** `Data Crawling Demo.mov` demonstrates the data crawling process.
- **Documentation:** `Project Pipeline.pdf` outlines the project workflow and methodology.



