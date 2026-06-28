import os
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
def car_predict_placeholder():
    """
    Automotive Pathway Blueprint
    Aborting to a simple layout confirmation text for now. Your friends will 
    re-map this link directly to 'car_entry.html' once they start coding.
    """
    return "<h3>Automotive Form Vector Standby</h3><p>The frontend interface is operational. Ready for your friends to inject the 10 mechanical indicator fields.</p><br><a href='/'>&larr; Return to Main App</a>"

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