from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import psycopg2
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Database connection parameters
db_params = {
    'dbname': 'PFE',
    'user': 'postgres',
    'password': 'admin'
}

# Connect to the PostgreSQL database
def connect_to_db():
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        cursor.execute("SET search_path TO PFE")
        return conn, cursor
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return None, None

# Load data from the database
def load_data_from_db(conn, cursor):
    try:
        current_year = datetime.now().year
        previous_year = current_year - 1
        sql_query = f"""
                    SELECT annee_id, v_eng
                    FROM fact_suivi_engagement_bud
                    WHERE annee_id::int <= {previous_year}
                    """
        cursor.execute(sql_query)
        data = cursor.fetchall()
        return data
    except psycopg2.Error as e:
        print("Error fetching data from the database:", e)
        return None

# Preprocess data
def preprocess_data(data):
    df = pd.DataFrame(data, columns=['annee_id', 'V_ENG'])
    sum_by_year = df.groupby('annee_id')['V_ENG'].sum()
    total_engagement_by_year = pd.DataFrame(sum_by_year).reset_index()
    total_engagement_by_year['V_ENG'] /= 1e6  # Convert to millions
    return total_engagement_by_year

# Train models
def train_models(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    linear_model = LinearRegression()
    linear_model.fit(X_train, y_train)
    linear_accuracy = linear_model.score(X_test, y_test)

    degree = 2
    poly_features = PolynomialFeatures(degree=degree)
    X_poly_train = poly_features.fit_transform(X_train)
    X_poly_test = poly_features.transform(X_test)
    
    poly_model = LinearRegression()
    poly_model.fit(X_poly_train, y_train)
    poly_accuracy = poly_model.score(X_poly_test, y_test)

    forest_model = RandomForestRegressor(random_state=42)
    forest_model.fit(X_train, y_train)
    forest_accuracy = forest_model.score(X_test, y_test)

    return linear_model, linear_accuracy, poly_model, poly_accuracy, forest_model, forest_accuracy, poly_features

conn, cursor = connect_to_db()
if conn and cursor:
    data = load_data_from_db(conn, cursor)
    conn.close()

    if data:
        total_engagement_by_year = preprocess_data(data)
        X = total_engagement_by_year[['annee_id']]
        y = total_engagement_by_year['V_ENG']

        linear_model, linear_accuracy, poly_model, poly_accuracy, forest_model, forest_accuracy, poly_features = train_models(X, y)

@app.route('/', methods=['GET'])
def index():
    return "Welcome to the prediction service!"

@app.route('/predict_future', methods=['GET'])
def predict_future():
    if data:
        future_year = np.array([[datetime.now().year + 1]])
        best_model = max(linear_accuracy, poly_accuracy, forest_accuracy)
        if best_model == linear_accuracy:
            future_prediction = linear_model.predict(future_year)
        elif best_model == poly_accuracy:
            future_prediction = poly_model.predict(poly_features.transform(future_year))
        else:
            future_prediction = forest_model.predict(future_year)

        return jsonify({'future_prediction': future_prediction[0]})
    else:
        return jsonify({'message': 'No data available for prediction'})

if __name__ == '__main__':
    app.run(debug=True)
