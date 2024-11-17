from flask import Flask, request, jsonify
import pandas as pd
import os
from flask_cors import CORS
import joblib
import csv
import pandas as pd

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Ensure the uploads directory exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set allowed file types
ALLOWED_EXTENSIONS = {'csv'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return 'Welcome to the Pipeline Monitor!'


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pipeline_file' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'})

    file = request.files['pipeline_file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'})

    if file and allowed_file(file.filename):
        # Save the file to the server
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Process the CSV file
        df = pd.read_csv(file_path)

        # Clean the data (e.g., forward fill missing values)
        df_cleaned = df.fillna(method='ffill')
        df_cleaned = df_cleaned.fillna(method='bfill')

        # Save the cleaned CSV data to 'token.csv'
        df_cleaned.to_csv('token.csv', index=False)

        # Call the prediction logic
        try:
            # Load the saved Random Forest model and scaler
            model = joblib.load("random_forest_hydrate_model.pkl")
            scaler = joblib.load("scaler.pkl")  # Load the saved scaler

            # Read the cleaned Token.csv file
            data = pd.read_csv('token.csv')

            # Extract and preprocess the timestamp column
            data['Timestamp'] = pd.to_datetime(data['Time'])  # Convert to datetime
            data['Hour'] = data['Timestamp'].dt.hour
            data['Day'] = data['Timestamp'].dt.day
            data['Month'] = data['Timestamp'].dt.month
            data['Minute'] = data['Timestamp'].dt.minute

            # Select the relevant features for prediction
            feature_columns = [
                'Hour', 'Day', 'Month', 'Minute',
                'Inj Gas Meter Volume Instantaneous',
                'Inj Gas Meter Volume Setpoint',
                'Inj Gas Valve Percent Open'
            ]
            input_features = data[feature_columns]

            # Normalize the input features using the saved scaler
            input_scaled = scaler.transform(input_features)

            # Predict the likelihood of hydrate for each row
            predicted_likelihood = model.predict(input_scaled)

            # Add the predictions to the dataframe
            data['Predicted Likelihood of Hydrate'] = predicted_likelihood

            # Save the results to a new CSV file
            output_csv_path = "final_prediction.csv"
            output_columns = ['Time', 'Predicted Likelihood of Hydrate']
            data[output_columns].to_csv(output_csv_path, index=False)

            # Optionally return the predictions or file name
            response_data = data[output_columns].to_dict(orient='records')
            return jsonify({
                'success': True,
                'message': 'Predictions completed and saved.',
                'predictions': response_data,
                'output_file': output_csv_path
            })

        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    return jsonify({'success': False, 'message': 'Invalid file format'})


@app.route('/endpoint', methods=['GET'])
def convert_file():
    result = []

    # Open the CSV file and read its contents
    with open('final_prediction.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)  # This ensures that each row is a dictionary

        # Iterate through the rows in the CSV file
        for row in csv_reader:
            # Check if row is a dictionary and contains the expected keys
            if isinstance(row, dict):
                time = row.get('Time')  # Access dictionary key using 'get'
                likelihood_str = row.get('Predicted Likelihood of Hydrate')

                try:
                    # Convert the likelihood to float
                    likelihood = float(likelihood_str)
                except ValueError:
                    # Handle potential errors in conversion (e.g., empty or malformed fields)
                    continue  # Skip this row if conversion fails

                # Determine status based on likelihood
                if likelihood > 75:
                    status = "highly likely"
                elif likelihood > 50:
                    status = "likely"
                else:
                    status = "unlikely"

                # Append the entry to the result list
                result.append({
                    'time': time,
                    'likelihood': likelihood,
                    'status': status
                })
            else:
                print("Row is not a dictionary:", row)  # This helps debug if rows are not dictionaries

    # Return the results as a JSON response
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, port=5502)
