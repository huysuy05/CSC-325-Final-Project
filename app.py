from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder
import os

app = Flask(__name__)

# Load models
def load_model(model_name):
    # Map form model names to directory names
    model_dir_map = {
        'Logistic_Regression': 'Logistic_Regression',
        'KNN': 'KNN',
        'Decision_Tree': 'Decision_Tree',
        'Random_Forest': 'Random_Forest',
        'XGBoost': 'XGBoost'
    }
    
    # Map form model names to file names
    model_file_map = {
        'Logistic_Regression': 'logisticregression.bin',
        'KNN': 'knnclassifier.bin',
        'Decision_Tree': 'decisiontreeclassifier.bin',
        'Random_Forest': 'randomforestclassifier.bin',
        'XGBoost': 'xgboostclassifier.bin'
    }
    
    if model_name not in model_dir_map:
        print(f"Error: Unknown model name: {model_name}")
        return None
        
    model_path = f"models/{model_dir_map[model_name]}/{model_file_map[model_name]}"
    print(f"Looking for model at: {model_path}")
    
    if os.path.exists(model_path):
        print(f"Found model at: {model_path}")
        return joblib.load(model_path)
    
    print(f"Model not found at: {model_path}")
    return None

# Load data for preprocessing
data = pd.read_csv("datasets/cleaned_crime_data.csv")

# Create label encoders for categorical variables
le_primary_type = LabelEncoder()
le_district = LabelEncoder()
le_ward = LabelEncoder()
le_community_area = LabelEncoder()

# Create a mapping dictionary for generalized_loc
generalized_loc_mapping = {
    'Airport': 0,
    'Commercial': 1,
    'Institutional': 2,
    'Other': 3,
    'Public Transportation': 4,
    'Residential': 5,
    'Street/Outdoor': 6,
    'Vehicle': 7
}
primary_type_mapping = {'CRIMINAL DAMAGE': 5, 'THEFT': 22, 'SEX OFFENSE': 20, 'ROBBERY': 19, 'MOTOR VEHICLE THEFT': 14, 'BURGLARY': 3, 'BATTERY': 2, 'HOMICIDE': 9, 
                        'CRIMINAL SEXUAL ASSAULT': 6, 'OFFENSE INVOLVING CHILDREN': 16, 'WEAPONS VIOLATION': 23, 'DECEPTIVE PRACTICE': 8, 'STALKING': 21, 'CRIMINAL TRESPASS': 7, 
                        'ASSAULT': 1, 'PROSTITUTION': 17, 'NARCOTICS': 15, 'KIDNAPPING': 13, 'ARSON': 0, 'INTERFERENCE WITH PUBLIC OFFICER': 11, 'PUBLIC PEACE VIOLATION': 18,
                            'INTIMIDATION': 12, 'HUMAN TRAFFICKING': 10, 'CRIM SEXUAL ASSAULT': 4}

# Get unique values for dropdowns before encoding
districts = sorted(data['District'].dropna().unique().tolist())
community_areas = sorted(data['Community Area'].dropna().unique().tolist())

# Fit label encoders
data["Primary Type"] = le_primary_type.fit_transform(data["Primary Type"])
data["District"] = le_district.fit_transform(data["District"])
data["Community Area"] = le_community_area.fit_transform(data["Community Area"])
data["Generalized Location"] = data["generalized_loc"].map(generalized_loc_mapping)

@app.route('/')
def home():
    return render_template('index.html', 
                         districts=districts,
                         community_areas=community_areas)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        print("\n=== Starting Prediction Process ===")
        
        # Print all form data received
        print("\n=== Form Data Received ===")
        print("Raw form data:", request.form)
        print("Form keys:", request.form.keys())
        
        # Get form data
        district = float(request.form['District'])
        community_area = float(request.form['Community Area'])
        domestic = int(request.form['domestic'])
        month = int(request.form['Month'])
        year = int(request.form['Year'])
        generalized_loc = request.form['generalized_loc']
        arrest = int(request.form['arrest'])
        location_crime_count = int(request.form['location_crime_count'])
        primary_type_count = int(request.form['primary_type_count'])
        
        print("\n=== Processed Form Data ===")
        print(f"District: {district}")
        print(f"Community Area: {community_area}")
        print(f"Domestic: {domestic}")
        print(f"Month: {month}")
        print(f"Year: {year}")
        print(f"Generalized Location: {generalized_loc}")
        print(f"Arrest: {arrest}")
        print(f"Location Crime Count: {location_crime_count}")
        print(f"Primary Type Count: {primary_type_count}")
        
        # Create feature array with all relevant features in the correct order
        features = np.array([[
            year,
            district,
            generalized_loc_mapping[generalized_loc],
            community_area,
            month,
            arrest,
            domestic,
            location_crime_count,
            primary_type_count
        ]])
        
        print("\n*** Features Array ***")
        print("Features shape:", features.shape)
        print("Features:", features)
        
        # Get selected model
        model_name = request.form['model']
        print(f"\n*** Loading Model: {model_name} ***")
        model = load_model(model_name)
        
        if model is None:
            print("Error: Model not found!")
            return jsonify({'error': 'Model not found'})
        
        print("Model loaded successfully")
        
        # Make prediction
        print("\n*** Making Prediction ***")
        prediction = model.predict(features)[0]
        print("Raw prediction:", prediction)
        
        # Get the predicted crime type name
        predicted_crime_type = le_primary_type.inverse_transform([prediction])[0]
        print("Transformed prediction:", predicted_crime_type)
        
        # Prepare response with more detailed information
        response = {
            'prediction': predicted_crime_type,
            'details': {
                'location': f'District {district}, Area {community_area}',
                'time': f'{month}/{year}',
                'domestic': 'Yes' if domestic == 1 else 'No',
                'arrest': 'Yes' if arrest == 1 else 'No',
                'generalized_loc': generalized_loc,
                'location_crime_count': location_crime_count,
                'primary_type_count': primary_type_count
            }
        }
        
        print("\n*** Final Response ***")
        print("Response:", response)
        print("========================\n")
        
        return jsonify(response)
        
    except Exception as e:
        print(f"\n*** Error in prediction ***")
        print(f"Error type: {type(e)}")
        print(f"Error message: {str(e)}")
        print("========================\n")
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(port=5000) 