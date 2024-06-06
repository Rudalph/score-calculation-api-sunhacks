# from flask import Flask, request, jsonify
# import pandas as pd
# import joblib
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# # Load the trained model
# model = joblib.load('trained_model.pkl')
# model_columns = joblib.load('model_columns.pkl')

# @app.route('/', methods=['POST'])
# def index():
#     try:
#         data = request.get_json()
#         print("Received data:", data)

#         Age = int(data['Age'])
#         Gender = data['Gender']
#         Weight = float(data['Weight'])
#         Height = float(data['Height'])
#         Medical_Conditions = data['Medical_Conditions']
#         Medication = data['Medication']
#         Smoker = data['Smoker']
#         Alcohol_Consumption = data['Alcohol_Consumption']
#         Sleep_Duration = float(data['Sleep_Duration'])
#         Wakeups = int(data['Wakeups'])
#         Snoring = data['Snoring']
#         Heart_Rate = int(data['Heart_Rate'])
#         Blood_Oxygen_Level = float(data['Blood_Oxygen_Level'])
#         ECG = data['ECG']
#         Calories_Intake = float(data['Calories_Intake'])
#         Water_Intake = float(data['Water_Intake'])
#         Stress_Level = data['Stress_Level']
#         Mood = data['Mood']
#         Body_Fat_Percentage = float(data['Body_Fat_Percentage'])
#         Muscle_Mass = float(data['Muscle_Mass'])

#         user_data = pd.DataFrame([[Age, Gender, Weight, Height, Medical_Conditions, Medication, Smoker, Alcohol_Consumption, Sleep_Duration, Wakeups, Snoring, Heart_Rate, Blood_Oxygen_Level, ECG, Calories_Intake, Water_Intake, Stress_Level, Mood, Body_Fat_Percentage, Muscle_Mass]],
#                                  columns=['Age', 'Gender', 'Weight', 'Height', 'Medical_Conditions', 'Medication', 'Smoker', 'Alcohol_Consumption', 'Sleep_Duration', 'Wakeups', 'Snoring', 'Heart_Rate', 'Blood_Oxygen_Level', 'ECG', 'Calories_Intake', 'Water_Intake', 'Stress_Level', 'Mood', 'Body_Fat_Percentage', 'Muscle_Mass'])

#         # Perform one-hot encoding
#         user_data = pd.get_dummies(user_data)

#         # Ensure user_data has the same columns as the trained model data
#         missing_cols = set(model_columns) - set(user_data.columns)
#         for col in missing_cols:
#             user_data[col] = 0
#         user_data = user_data.reindex(columns=model_columns, fill_value=0)

#         # Make prediction
#         health_score = model.predict(user_data)

#         return jsonify({'health_score': health_score[0]})

#     except Exception as e:
#         print("Error:", e)
#         return jsonify({'error': 'An error occurred'}), 400

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)



from flask import Flask, request, jsonify
import pandas as pd
import joblib
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load the trained model
model = joblib.load('trained_model.pkl')
model_columns = joblib.load('model_columns.pkl')

@app.route('/', methods=['POST'])
def index():
    try:
        data = request.get_json()
        print("Received data:", data)

        # Helper function to safely convert data
        def safe_convert(data, data_type, default=0):
            try:
                return data_type(data) if data else default
            except ValueError:
                return default

        Age = safe_convert(data.get('Age'), int)
        Gender = data.get('Gender', 'Unknown')
        Weight = safe_convert(data.get('Weight'), float)
        Height = safe_convert(data.get('Height'), float)
        Medical_Conditions = data.get('Medical_Conditions', 'None')
        Medication = data.get('Medication', 'No')
        Smoker = data.get('Smoker', 'No')
        Alcohol_Consumption = data.get('Alcohol_Consumption', 'None')
        Sleep_Duration = safe_convert(data.get('Sleep_Duration'), float)
        Wakeups = safe_convert(data.get('Wakeups'), int)
        Snoring = data.get('Snoring', 'No')
        Heart_Rate = safe_convert(data.get('Heart_Rate'), int)
        Blood_Oxygen_Level = safe_convert(data.get('Blood_Oxygen_Level'), float)
        ECG = data.get('ECG', 'Normal')
        Calories_Intake = safe_convert(data.get('Calories_Intake'), float)
        Water_Intake = safe_convert(data.get('Water_Intake'), float)
        Stress_Level = data.get('Stress_Level', 'Low')
        Mood = data.get('Mood', 'Neutral')
        Body_Fat_Percentage = safe_convert(data.get('Body_Fat_Percentage'), float)
        Muscle_Mass = safe_convert(data.get('Muscle_Mass'), float)

        user_data = pd.DataFrame([[
            Age, Gender, Weight, Height, Medical_Conditions, Medication, Smoker, Alcohol_Consumption, Sleep_Duration, 
            Wakeups, Snoring, Heart_Rate, Blood_Oxygen_Level, ECG, Calories_Intake, Water_Intake, Stress_Level, 
            Mood, Body_Fat_Percentage, Muscle_Mass
        ]], columns=[
            'Age', 'Gender', 'Weight', 'Height', 'Medical_Conditions', 'Medication', 'Smoker', 'Alcohol_Consumption', 
            'Sleep_Duration', 'Wakeups', 'Snoring', 'Heart_Rate', 'Blood_Oxygen_Level', 'ECG', 'Calories_Intake', 
            'Water_Intake', 'Stress_Level', 'Mood', 'Body_Fat_Percentage', 'Muscle_Mass'
        ])

        # Perform one-hot encoding
        user_data = pd.get_dummies(user_data)

        # Ensure user_data has the same columns as the trained model data
        missing_cols = set(model_columns) - set(user_data.columns)
        for col in missing_cols:
            user_data[col] = 0
        user_data = user_data.reindex(columns=model_columns, fill_value=0)

        # Make prediction
        health_score = model.predict(user_data)

        return jsonify({'health_score': health_score[0]})

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
