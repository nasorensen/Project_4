
# Project 4 Home Sales
 - Nicolette Sorensen
 - Deborah Kisch
 - Janice Guallpa
 - Kelley Blue
 - Jennifer Robison

## Project Overview
Project 4 pulls together skills learned throughout the Data Analytics Bootcamp to create a Real estate map and prediction model. An interactive map shows real estate sales in the target area. A web interface allows users to input the number of bedrooms, bathrooms, and size of house and lot. An html-based interface is connected to a machine-learning model. The model uses Random Forest to predict the optimal sale price for the house. 

## Data Source
 - Used API for realtor.com to call for single family homes in/around St. Paul, MM.
 - Used Pandas to pull desired data: list price, list date, sold price, sold date, bedrooms, baths, square footage, lot square footage, address and coordinates.
 - Formatted dataframe and save as a .csv file.

## Create Predictive Model
 - Connected to rapidapi.com and queried twin cities area MN Real Estate sales for single-family homes.  
 - The areas queried in are based on zip codes in St. Paul and the surrounding areas including Roseviile, North Oaks, Shoreview, Hugo, White Bear Lake, Arden Hills, Gem Lake, New Brighton, Little Canada, Maplewood, West St. Paul, Falcon Heights, Mounds View, Lauderdale, Mendota Heights and North St. Paul. 
 - Due to API calls limitaions, the data goes back to sale date of December 2024 and includes about 1300 entries. 

## Map  
 - Kelley

## Predicting Home Sales and Market Duration in Saint Paul
Analyzing home sale data in Saint Paul, Minnesota to:
1. Developed and compared various regression models to find the best-performing solution to predict the sale price and estimate how long a house stays on the market.
2. Predict the sale price of a house based on features like square footage, number of beds/baths, and lot size and created a model for integration in to a site.
### 1. Model_Selction.ipynb in Model_Selection Folder
Compare multiple machine learning models to predict sold_price and days_on_market.
Steps Taken:
 - Upload st_paul_sold_properties.csv performed data processing and data clean-up.
 - Cleaned and engineered features (computed days_on_market).
 - Explored data using correlation heatmaps.
 - Tested 8 regression models (e.g. Random Forest, Gradient Boosting, Ridge, Lasso).
 - Evaluated performance using MAE and R2.
Results
 - Random Forest gave the best result for both sold price and days on market. Followed close by Gradient Boosting.
 - Predicting sale price was more accurate than days_on_market (R2 for DOM was low).
### 2. Price_Sold_Regression.ipynb in Model_Selection Folder
Optimize a single model (Gradient Boosting Regressor) to reliably predict sold price.
 - Added new features like beds_baths_ratio and lot_to_sqft_ratio.
 - Created a machine learning pipeline with preprocessing steps.
 - Perfomed hyperparameter tuning using GridSearchCV.
 - Final model saved to disk as sold_price_model.pkl.
Results
Achieved R2 of 0.828 on the test set with slight overfitting of R2 training vs test.
 - 
 - Jennifer: 
 - A model was developed to predict the number of days on market based on the user input. 
 - The model used XGBoost, a type of decision tree machine learning model commonly used in real estate.
 - Many attemps were made to optimize this model, however, results peaked at 71% R2 accuracy. 
 - Ultimately, the group decided not to include this model in the final project due to the low accuracy.
 - 

## Create Folium map 
 - Upload CSV and create Folium map to show recently sold homes that match a users input (beds, bath, square footage)

## Build Webpage
 - Build an intereactive user face
 - User can put in features from their property and it will reference the model to make a prediction for what their home will sell for
 -   

## Flask Web Interface
 - Deborah

## HTML Tying it all together
 - Nicolette
