import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import psycopg2
import numpy as np
from datetime import datetime


current_year = datetime.now().year
previous_year = current_year - 1


con = psycopg2.connect(dbname='PFE', user='postgres', password='admin')
cursor = con.cursor()

cursor.execute("SET search_path TO PFE")


sql_query = f"""
            SELECT annee_id, v_eng
            FROM fact_suivi_engagement_bud
            WHERE annee_id::int <= {previous_year}
            """


data = pd.read_sql_query(sql_query, con)


cursor.close()
con.close()


sum_by_year = data.groupby('annee_id')['v_eng'].sum()
total_engagement_by_year = pd.DataFrame(sum_by_year).reset_index()
total_engagement_by_year = total_engagement_by_year.rename(columns={'v_eng': 'TOTAL_V_ENG'})

# Convertir les engagements en millions
total_engagement_by_year['TOTAL_V_ENG'] /= 1e6  # Convertir en millions


X = total_engagement_by_year[['annee_id']].astype(int)
y = total_engagement_by_year['TOTAL_V_ENG']

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Régression linéaire
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)
linear_r2 = linear_model.score(X_test, y_test)
print("Linear Regression Model R^2:", linear_r2)

# Régression polynomiale
degree = 2
poly_features = PolynomialFeatures(degree=degree)
X_poly_train = poly_features.fit_transform(X_train)
X_poly_test = poly_features.transform(X_test)

poly_model = LinearRegression()
poly_model.fit(X_poly_train, y_train)
poly_r2 = poly_model.score(X_poly_test, y_test)
print("Polynomial Regression Model R^2:", poly_r2)

# Régression par forêt aléatoire
forest_model = RandomForestRegressor(random_state=42)
forest_model.fit(X_train, y_train)
forest_r2 = forest_model.score(X_test, y_test)
print("Random Forest Regression Model R^2:", forest_r2)

# Sélectionner le meilleur modèle basé sur le R^2
best_model = max(linear_r2, poly_r2, forest_r2)
if best_model == linear_r2:
    best_model_name = "Linear Regression"
elif best_model == poly_r2:
    best_model_name = "Polynomial Regression"
else:
    best_model_name = "Random Forest Regression"


future_year = np.array([[current_year]])
if best_model_name == "Linear Regression":
    future_prediction = linear_model.predict(future_year)
elif best_model_name == "Polynomial Regression":
    future_prediction = poly_model.predict(poly_features.transform(future_year))
else:
    future_prediction = forest_model.predict(future_year)

print("Meilleur Modèle:", best_model_name)
print("Prédiction Engagement pour l'année actuelle (Millions):", future_prediction[0])

# Ajouter la prédiction pour l'année actuelle aux données existantes
current_year_data = pd.DataFrame({'annee_id': [current_year], 'TOTAL_V_ENG': [future_prediction[0]]})
total_engagement_by_year = pd.concat([total_engagement_by_year, current_year_data], ignore_index=True)

# Convertir la colonne 'annee_id' en chaînes de caractères pour éviter les erreurs de type
total_engagement_by_year['annee_id'] = total_engagement_by_year['annee_id'].astype(str)

# Créer le graphique avec la prédiction
plt.figure(figsize=(10, 6))
plt.plot(total_engagement_by_year['annee_id'], total_engagement_by_year['TOTAL_V_ENG'], marker='o', color='b')
plt.scatter(str(current_year), future_prediction, color='r', zorder=5)  # Point prédictif en rouge
plt.title("Total de l'engagement au fil des années")
plt.xlabel('Année')
plt.ylabel('Total Engagement (en millions)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
