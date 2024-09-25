# Projet d'intégration web et IA

## Démarrage du projet

```sh
git clone https://github.com/operdrix/cours-web-ia.git rendu-olivier-perdrix

cd rendu-olivier-perdrix

# Démarrage du backend ExpressJs
cd backend-express
npm install
npm run dev

# Démarrage du backend Python pour les prédictions
cd backend-python
pip install fastapi uvicorn scikit-learn loguru pandas numpy
uvicorn api:app --reload

# Démarrage du frontend VueJs
cd frontend
npm install
npm run dev
```

- Le backend Express.js écoute le port http://localhost:3002
- Le backend Python écoute le port http://localhost:8000. 
  - La doc est accessible via http://localhost:8000/docs
- Le frontend écoute le port http://localhost:3000

## Rendu du TP

Le rendu du TP est disponible sous [./rendu/rendu.ipynb](./rendu/rendu.ipynb)

Le fichier csv est disponible sous [./backend-express/data](./backend-express/data)
