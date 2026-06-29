import os
import pickle
import numpy as np

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
def house_predict_placeholder():
    """
    Real Estate Pathway Blueprint
    Aborting to a simple layout confirmation text for now. Your friends will 
    re-map this link directly to 'house_entry.html' once they start coding.
    """
    return "<h3>Real Estate Form Vector Standby</h3><p>The frontend interface is operational. Ready for your friends to inject the 20-dimensional input fields.</p><br><a href='/'>&larr; Return to Main App</a>"

@app.route('/predict/car', methods=['GET'])
def car_page():
    return render_template('car.html')
@app.route('/predict/car/result', methods=['POST'])
def car_result():
    import numpy as np

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

    features = np.array([[
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
    ]])

    try:
        prediction = car_model.predict(features)[0]
    except Exception:
        return render_template('cresult.html', prediction=None, error='Model error during prediction.')

    return render_template("cresult.html", prediction=round(prediction, 2), error=None)


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