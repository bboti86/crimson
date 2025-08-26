# Import necessary modules from Flask and standard Python libraries
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

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
    If the file doesn't exist, it creates it with an empty list.
    This function handles file I/O and JSON deserialization.
    """
    db_path = get_database_path(app)
    # Check if the database file exists
    if not os.path.exists(db_path):
        # If not, create the 'data' directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        # Create the file with an empty list of periods
        with open(db_path, 'w') as f:
            json.dump([], f)
        return []
    # If the file exists, open it and load the JSON data
    with open(db_path, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # If the file is empty or corrupted, return an empty list
            return []

def write_data(data):
    """
    Writes the given data to the JSON database file.
    This function handles file I/O and JSON serialization.
    It's used to save new periods or update the list after a deletion.
    """
    db_path = get_database_path(app)
    # Open the database file in write mode and dump the data into it
    # The 'indent=4' argument makes the JSON file more readable
    with open(db_path, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/api/periods', methods=['GET'])
def get_periods():
    """
    API endpoint to retrieve all period entries.
    Handles GET requests to /api/periods.
    It reads the data from the database and returns it as a JSON response.
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
    The new entry is added to the database.
    """
    # Get the JSON data from the request body
    new_period = request.json
    # Read the existing data from the database
    periods = read_data()
    # Append the new period entry to the list
    periods.append(new_period)
    # Write the updated list back to the database
    write_data(periods)
    # Return a success message
    return jsonify({'message': 'Period added successfully'}), 201

@app.route('/api/periods/<start_date>', methods=['DELETE'])
def delete_period(start_date):
    """
    API endpoint to delete a period entry.
    Handles DELETE requests to /api/periods/<start_date>.
    The <start_date> is used to identify the entry to be deleted.
    """
    # Read the existing data from the database
    periods = read_data()
    # Create a new list that excludes the period with the matching start_date
    updated_periods = [p for p in periods if p.get('start_date') != start_date]

    # Check if any period was actually deleted
    if len(updated_periods) < len(periods):
        # If so, write the updated list back to the database
        write_data(updated_periods)
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
