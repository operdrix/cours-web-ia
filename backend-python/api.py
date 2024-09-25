from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sklearn.linear_model import LinearRegression, LogisticRegression
from loguru import logger
from sklearn.model_selection import train_test_split
import uvicorn
import numpy as np
import pandas as pd

# Initialisation de FastAPI
app = FastAPI()

# Ajoute le middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Définition d'un modèle pour les données d'entrée
class PredictionDataModel1(BaseModel):
    city: str
    area: float
    price: float
class PredictionDataModel2(BaseModel):
    city: str
class PredictionDataModel3(BaseModel):
    city: str
    price: float

# Initialisation du modèle de régression linéaire
model1 = LinearRegression()
model2 = LinearRegression()
model3 = LogisticRegression()

# Variable pour vérifier si le modèle est entraîné
is_model1_trained = False
is_model2_trained = False
is_model3_trained = False

# Endpoint pour entraîner les modèle
@app.post("/train")
async def train():
    global is_model1_trained
    global is_model2_trained
    global is_model3_trained

    # Lire le fichier CSV
    df = pd.read_csv('../backend-express/data/apartments.csv')
    df['is_Paris'] = (df['city'] == 'Paris').astype(int)
    df['is_Lyon'] = (df['city'] == 'Lyon').astype(int)
    df['is_Marseille'] = (df['city'] == 'Marseille').astype(int)
    logger.info(df.head())

    # Entrainement sur la note par regression linéaire
    X = df[['is_Paris', 'is_Lyon', 'is_Marseille', 'area', 'price']]
    y = df['rating']
    logger.info(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model1.fit(X_train, y_train)

    # Entrainement sur lannée de construction par regression linéaire
    X = df[['is_Paris', 'is_Lyon', 'is_Marseille']]
    y = df['years_of_construction']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model2.fit(X_train, y_train)

    # Entrainement sur la la probabilité d'avoir un balcon par regression logistique
    X = df[['is_Paris', 'is_Lyon', 'is_Marseille', 'price']]
    y = df['have_balcony']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model3.fit(X_train, y_train)

    # Marquer le modèle comme entraîné
    is_model1_trained = True
    is_model2_trained = True
    is_model3_trained = True

    # Logging avec Loguru
    logger.info("Modèles entraînés avec succès.")
    logger.info(f"Modèle 1: {is_model1_trained}")
    logger.info(f"Coefficients: {model1.coef_}, Intercept: {model1.intercept_}")
    logger.info(f"Modèle 2: {is_model2_trained}")
    logger.info(f"Coefficients: {model2.coef_}, Intercept: {model2.intercept_}")
    logger.info(f"Modèle 3: {is_model3_trained}")
    logger.info(f"Coefficients: {model3.coef_}, Intercept: {model3.intercept_}")

    return {"message": "Modèle entraîné avec succès."}

# Endpoint pour prédire une note en fonction de la ville, la surface et le prix
@app.post("/predict-rating")
async def predict(data: PredictionDataModel1):
    global is_model1_trained

    # Vérifier si le modèle a été entraîné
    if not is_model1_trained:
        raise HTTPException(
            status_code=400, detail="Le modèle rating n'est pas encore entraîné. Veuillez entraîner le modèle d'abord.")

    isParis = (data.city == 'Paris')
    isLyon = (data.city == 'Lyon')
    isMarseille = (data.city == 'Marseille')
    X_new = np.array([[isParis, isLyon, isMarseille, data.area, data.price]])

    # Prédire le prix
    predicted_rating = model1.predict(X_new)[0]

    # Logging avec Loguru
    logger.info(f"Prédiction faite pour ville : {data.city}, surface: {data.area} et prix: {data.price}")
    logger.info(f"Note prédite: {predicted_rating}")

    return {"predicted_rating": predicted_rating}

# Endpoint pour prédire une année de construction en fonction de la ville
@app.post("/predict-years-of-construction")
async def predict(data: PredictionDataModel2):
    global is_model2_trained

    # Vérifier si le modèle a été entraîné
    if not is_model2_trained:
        raise HTTPException(
            status_code=400, detail="Le modèle years_of_construction n'est pas encore entraîné. Veuillez entraîner le modèle d'abord.")

    isParis = (data.city == 'Paris')
    isLyon = (data.city == 'Lyon')
    isMarseille = (data.city == 'Marseille')
    X_new = np.array([[isParis, isLyon, isMarseille]])

    # Prédire l'année de construction
    predicted_years_of_construction = model2.predict(X_new)[0]

    # Logging avec Loguru
    logger.info(f"Prédiction faite pour ville : {data.city}")
    logger.info(f"Année de construction prédite: {predicted_years_of_construction}")

    return {"predicted_years_of_construction": round(predicted_years_of_construction)}

# Endpoint pour prédire la probabilité d'avoir un balcon en fonction de la ville et le prix
@app.post("/predict-have-balcony")
async def predict(data: PredictionDataModel3):
    global is_model3_trained

    # Vérifier si le modèle a été entraîné
    if not is_model3_trained:
        raise HTTPException(
            status_code=400, detail="Le modèle have_balcony n'est pas encore entraîné. Veuillez entraîner le modèle d'abord.")

    isParis = (data.city == 'Paris')
    isLyon = (data.city == 'Lyon')
    isMarseille = (data.city == 'Marseille')
    X_new = np.array([[isParis, isLyon, isMarseille, data.price]])

    # Prédire la probabilité d'avoir un balcon
    predicted_have_balcony = model3.predict(X_new)[0]

    # Logging avec Loguru
    logger.info(f"Prédiction faite pour ville : {data.city} et prix: {data.price}")
    logger.info(f"Probabilité d'avoir un balcon prédite: {predicted_have_balcony}")

    return {"predicted_have_balcony": int(predicted_have_balcony)}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
