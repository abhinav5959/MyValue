import os
import pickle
import numpy as np
import pandas as pd

from flask import Flask, render_template, abort, request, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Initialize Supabase client
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    supabase = None
# Load model
car_model = pickle.load(open("models/car.pkl", "rb"))
house_model = pickle.load(open("models/house_price_model.pkl", "rb"))
@app.route('/')
def index():
    """
    Core Route Handler
    Renders your single-page application framework containing the
    floating navigation pod pod and your 4 chromodynamic viewports.
    """
    return render_template('index.html')

# Temporary placeholder development pathways for your friends' future prediction logic
@app.route('/predict/house', methods=['GET'])
def house_page():
    return render_template('house.html')

@app.route('/predict/house/result', methods=['POST'])
def house_result():
    try:
        # 1. Extract all 15 inputs from the house.html form fields
        bedrooms = int(request.form['number_of_bedrooms'])
        bathrooms = int(request.form['number_of_bathrooms'])
        living_area = float(request.form['living_area'])
        lot_area = float(request.form['lot_area'])
        floors = int(request.form['number_of_floors'])
        condition = int(request.form['condition_of_the_house'])
        grade = int(request.form['grade_of_the_house'])
        built_year = int(request.form['built_year'])
        schools = int(request.form['number_of_schools_nearby'])
        airport_dist = float(request.form['distance_from_the_airport'])

        # New inputs from the updated form:
        waterfront = int(request.form['waterfront'])
        views = int(request.form['number_of_views'])
        area_ex_basement = float(request.form['area_without_basement'])
        basement = float(request.form['basement_area'])
        renovation_year = int(request.form['renovation_year'])

    except (ValueError, KeyError) as e:
        return render_template('hresult.html', prediction=None, error='Invalid input: please enter valid numeric values.')

    # 2. Hardcoded behind-the-scenes engineering for spatial/renovation columns omitted from screen
    latitude = 47.5600      
    longitude = -122.2140   
    living_area_renov = living_area
    lot_area_renov = lot_area

    # 3. Construct your exact 19-feature vector matching your model sequence using pandas DataFrame
    # to preserve column/feature names and prevent sklearn version/feature warnings.
    features = pd.DataFrame([[
        bedrooms,          # 1. number of bedrooms
        bathrooms,         # 2. number of bathrooms
        living_area,       # 3. living area
        lot_area,          # 4. lot area
        floors,            # 5. number of floors
        waterfront,        # 6. waterfront present
        views,             # 7. number of views
        condition,         # 8. condition of the house
        grade,             # 9. grade of the house
        area_ex_basement,  # 10. Area of the house(excluding basement)
        basement,          # 11. Area of the basement
        built_year,        # 12. Built Year
        renovation_year,   # 13. Renovation Year
        latitude,          # 14. Lattitude
        longitude,         # 15. Longitude
        living_area_renov, # 16. living_area_renov
        lot_area_renov,    # 17. lot_area_renov
        schools,           # 18. Number of schools nearby
        airport_dist       # 19. Distance from the airport
    ]], columns=[
        'number of bedrooms', 'number of bathrooms', 'living area', 'lot area',
        'number of floors', 'waterfront present', 'number of views', 'condition of the house',
        'grade of the house', 'Area of the house(excluding basement)', 'Area of the basement',
        'Built Year', 'Renovation Year', 'Lattitude', 'Longitude',
        'living_area_renov', 'lot_area_renov', 'Number of schools nearby', 'Distance from the airport'
    ])

    try:
        # Prediction output is in USD. We convert it to INR (1 USD = 83 INR) and then to Lakhs (divide by 100,000)
        prediction_usd = house_model.predict(features)[0]
        prediction_inr_lakhs = (prediction_usd * 83.0) / 100000.0
    except Exception as e:
        return render_template('hresult.html', prediction=None, error='Model error during prediction.')

    return render_template("hresult.html", prediction=round(prediction_inr_lakhs, 2), error=None)

   

@app.route('/predict/car', methods=['GET'])
def car_page():
    return render_template('car.html')
@app.route('/predict/car/result', methods=['POST'])
def car_result():
    try:
        km_driven = int(request.form['km_driven'])
        fuel = int(request.form['fuel'])
        seller_type = int(request.form['seller_type'])
        transmission = int(request.form['transmission'])
        owner = int(request.form['owner'])
        mileage = float(request.form['mileage'])
        engine = int(request.form['engine'])
        max_power = float(request.form['max_power'])
        seats = int(request.form['seats'])
        car_age = int(request.form['car_age'])

    except (ValueError, KeyError) as e:
        return render_template('cresult.html', prediction=None, error='Invalid input: please enter valid numeric values.')

    # Using pandas DataFrame to preserve feature/column names for the scikit-learn model and prevent warnings
    features = pd.DataFrame([[
        km_driven,
        fuel,
        seller_type,
        transmission,
        owner,
        mileage,
        engine,
        max_power,
        seats,
        car_age
    ]], columns=['km_driven', 'fuel', 'seller_type', 'transmission', 'owner', 'mileage', 'engine', 'max_power', 'seats', 'car_age'])

    try:
        # Prediction output is in raw Rupees, we convert it to Lakhs (divide by 100,000) for a cleaner UI display
        prediction_raw = car_model.predict(features)[0]
        prediction_lakhs = prediction_raw / 100000.0
    except Exception as e:
        return render_template('cresult.html', prediction=None, error='Model error during prediction.')

    return render_template("cresult.html", prediction=round(prediction_lakhs, 2), error=None)


@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.json
    if not data or not data.get('name') or not data.get('email') or not data.get('message'):
        return jsonify({"error": "Missing required fields"}), 400
    
    if not supabase:
        return jsonify({"error": "Supabase not configured on the server"}), 500

    try:
        response = supabase.table('messages').insert({
            "name": data.get('name'),
            "email": data.get('email'),
            "message": data.get('message')
        }).execute()
        
        return jsonify({"success": True, "data": response.data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Set debug=True so that anytime you make a adjustment to your CSS or layout,
    # the server auto-reloads the changes immediately without manual restarts.
    app.run(debug=True)