# Import necessary modules from Flask and standard Python libraries
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime, timedelta

# Initialize the Flask application
app = Flask(__name__)
# Enable Cross-Origin Resource Sharing (CORS) to allow the frontend to communicate with this backend
CORS(app)

# Define the path for our JSON database file.
# It's placed in a 'data' subdirectory to keep the project organized.
DATABASE_FILE = os.path.join('data', 'database.json')

def get_database_path(app):
    """
    Constructs the absolute path to the database file.
    This function ensures that the path is correct regardless of where the app is run from.
    """
    return os.path.join(app.root_path, DATABASE_FILE)

def read_data():
    """
    Reads the period data from the JSON database file.
    If the file doesn't exist, it creates it with a default structure.
    This function handles file I/O and JSON deserialization.
    """
    db_path = get_database_path(app)
    # Check if the database file exists
    if not os.path.exists(db_path):
        # If not, create the 'data' directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        # Create the file with a default structure
        default_data = {'historical': [], 'estimated': []}
        with open(db_path, 'w') as f:
            json.dump(default_data, f)
        return default_data
    # If the file exists, open it and load the JSON data
    with open(db_path, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # If the file is empty or corrupted, return the default structure
            return {'historical': [], 'estimated': []}

def write_data(data):
    """
    Writes the given data to the JSON database file.
    This function handles file I/O and JSON serialization.
    """
    db_path = get_database_path(app)
    # Open the database file in write mode and dump the data into it
    # The 'indent=4' argument makes the JSON file more readable
    with open(db_path, 'w') as f:
        json.dump(data, f, indent=4)

def calculate_and_store_future_periods(periods_data):
    """
    Calculates future period dates for the next 3 years based on historical data.
    """
    historical_periods = sorted(periods_data['historical'], key=lambda p: datetime.strptime(p['start_date'], '%Y-%m-%d'))

    if len(historical_periods) < 2:
        periods_data['estimated'] = []
        return periods_data

    # Calculate average cycle length
    cycle_lengths = []
    for i in range(1, len(historical_periods)):
        start_date1 = datetime.strptime(historical_periods[i-1]['start_date'], '%Y-%m-%d')
        start_date2 = datetime.strptime(historical_periods[i]['start_date'], '%Y-%m-%d')
        cycle_lengths.append((start_date2 - start_date1).days)

    avg_cycle_length = sum(cycle_lengths) / len(cycle_lengths)

    # Calculate average period duration
    durations = []
    for p in historical_periods:
        start = datetime.strptime(p['start_date'], '%Y-%m-%d')
        end = datetime.strptime(p['end_date'], '%Y-%m-%d')
        durations.append((end - start).days + 1)
    avg_duration = sum(durations) / len(durations)

    # Estimate future periods for the next 3 years
    estimated_periods = []
    last_period = historical_periods[-1]
    last_start_date = datetime.strptime(last_period['start_date'], '%Y-%m-%d')

    current_date = last_start_date
    three_years_later = datetime.now() + timedelta(days=3*365)

    while True:
        next_start_date = current_date + timedelta(days=avg_cycle_length)
        if next_start_date > three_years_later:
            break
        next_end_date = next_start_date + timedelta(days=avg_duration - 1)
        estimated_periods.append({
            'start_date': next_start_date.strftime('%Y-%m-%d'),
            'end_date': next_end_date.strftime('%Y-%m-%d')
        })
        current_date = next_start_date

    periods_data['estimated'] = estimated_periods
    return periods_data

@app.route('/api/periods', methods=['GET'])
def get_periods():
    """
    API endpoint to retrieve all period entries (historical and estimated).
    Handles GET requests to /api/periods.
    """
    # Read the current data from our database
    periods = read_data()
    # Return the data as a JSON response
    return jsonify(periods)

@app.route('/api/periods', methods=['POST'])
def add_period():
    """
    API endpoint to add a new period entry.
    Handles POST requests to /api/periods.
    It expects a JSON payload with 'start_date' and 'end_date'.
    The new entry is added to the database, and future periods are recalculated.
    """
    # Get the JSON data from the request body
    new_period = request.json
    # Read the existing data from the database
    periods_data = read_data()
    # Append the new period entry to the historical list
    periods_data['historical'].append(new_period)
    # Recalculate and store future periods
    updated_data = calculate_and_store_future_periods(periods_data)
    # Write the updated data back to the database
    write_data(updated_data)
    # Return a success message
    return jsonify({'message': 'Period added successfully'}), 201

@app.route('/api/periods/<start_date>', methods=['DELETE'])
def delete_period(start_date):
    """
    API endpoint to delete a historical period entry.
    Handles DELETE requests to /api/periods/<start_date>.
    The <start_date> is used to identify the entry to be deleted.
    Future periods are recalculated after deletion.
    """
    # Read the existing data from the database
    periods_data = read_data()
    # Create a new list that excludes the period with the matching start_date
    updated_historical = [p for p in periods_data['historical'] if p.get('start_date') != start_date]

    # Check if any period was actually deleted
    if len(updated_historical) < len(periods_data['historical']):
        periods_data['historical'] = updated_historical
        # Recalculate and store future periods
        updated_data = calculate_and_store_future_periods(periods_data)
        # Write the updated data back to the database
        write_data(updated_data)
        # Return a success message
        return jsonify({'message': 'Period deleted successfully'})
    else:
        # If no period was found with the given start_date, return an error
        return jsonify({'message': 'Period not found'}), 404

# This block ensures that the Flask development server runs when the script is executed directly
if __name__ == '__main__':
    # The host '0.0.0.0' makes the server accessible from any IP address,
    # which is necessary for it to be reachable from other Docker containers.
    app.run(host='0.0.0.0', port=5000, debug=True)
