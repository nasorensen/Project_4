# Project-4-Home-Sales
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
 - Janice:
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
