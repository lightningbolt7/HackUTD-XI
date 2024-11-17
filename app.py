from flask import Flask, request, jsonify
import pandas as pd
import os
from flask_cors import CORS
import joblib
import csv
import pandas as pd

app = Flask(__name__)

CORS(app)


UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


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

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        df = pd.read_csv(file_path)

        df_cleaned = df.fillna(method='ffill')
        df_cleaned = df_cleaned.fillna(method='bfill')


        df_cleaned.to_csv('token.csv', index=False)


        try:

            model = joblib.load("random_forest_hydrate_model.pkl")
            scaler = joblib.load("scaler.pkl")


            data = pd.read_csv('token.csv')


            data['Timestamp'] = pd.to_datetime(data['Time'])
            data['Hour'] = data['Timestamp'].dt.hour
            data['Day'] = data['Timestamp'].dt.day
            data['Month'] = data['Timestamp'].dt.month
            data['Minute'] = data['Timestamp'].dt.minute


            feature_columns = [
                'Hour', 'Day', 'Month', 'Minute',
                'Inj Gas Meter Volume Instantaneous',
                'Inj Gas Meter Volume Setpoint',
                'Inj Gas Valve Percent Open'
            ]
            input_features = data[feature_columns]


            input_scaled = scaler.transform(input_features)


            predicted_likelihood = model.predict(input_scaled)


            data['Predicted Likelihood of Hydrate'] = predicted_likelihood


            output_csv_path = "final_prediction.csv"
            output_columns = ['Time', 'Predicted Likelihood of Hydrate']
            data[output_columns].to_csv(output_csv_path, index=False)


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


    with open('final_prediction.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)


        for row in csv_reader:

            if isinstance(row, dict):
                time = row.get('Time')
                likelihood_str = row.get('Predicted Likelihood of Hydrate')

                try:

                    likelihood = float(likelihood_str)
                except ValueError:

                    continue


                if likelihood > 75:
                    status = "highly likely"
                elif likelihood > 50:
                    status = "likely"
                else:
                    status = "unlikely"


                result.append({
                    'time': time,
                    'likelihood': likelihood,
                    'status': status
                })
            else:
                print("Row is not a dictionary:", row)


    return jsonify(result)


@app.route('/get_highly_likely_alerts', methods=['GET'])
def get_highly_likely_alerts():
    result = []


    with open('final_prediction.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)


        for row in csv_reader:

            if isinstance(row, dict):
                time = row.get('Time')
                likelihood_str = row.get('Predicted Likelihood of Hydrate')

                try:

                    likelihood = float(likelihood_str)
                except ValueError:

                    continue


                if likelihood > 75:
                    status = "highly likely"
                else:
                    continue

                result.append({
                    'time': time,
                    'likelihood': likelihood,
                    'status': status
                })


    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, port=5502)
