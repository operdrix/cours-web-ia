# Rendu Noté

Vous pouvez travailler en collectif pour l'entraide mais néanmoins chaque projet est individuel et noté.


Timing: Vous avez 15 Jours de rendu.

# Sur un Notebook
Sur un Jupiter Notebook avec votre CSV:
1. Manipulation de données: Ajouter les colonnes annee (entre 2005 et 2024), balcon, garage,note,price_category avec l'année, balcon et garage en booléan, note de 1 à 5 et category: low, normal high,scam (appréciation humaine si c'est une arnaque, bas prix, prix normal ou élevé).
2. Compléter votre dataset au plus vraissemblable. L'idée est d'en avoir entre 50 et 100.

3. Avec Numpy et Pandas:
- Sur la surface: Moyenne, écart-type, surface minimale et maximale.
- Sur l'année: Moyenne, construction la plus ancienne, la plus récente.
- Sur le balcon: Proportion d'appartements avec un balcon.
- Comptage du nombre d'appartements dans chaque catégorie de prix (low, normal, high, scam).
- Nombre de chambres (nbRooms): Moyenne, médiane, variance, écart-type.

Avec Matplop:
Créer un Diagramme à barres pour afficher la répartition des catégories de prix (par exemple, combien d'appartements sont "low", "normal", "high", "scam").

Bonus: Créer un Heatmap pour voir la correlation entre Année de construction et prix afin de voir si les appartements plus récents ont tendance à être plus chers.


1. Compléter avec une nouvelle colonne ville dans votre dataset si l'appartement est de Lyon, Paris ou Marseille 
2. Créer une prédiction par regression linéaire sur la note en fonction de la ville, de la surface et du prix
3. Créer une prédiction par regression linéaire sur l'année en fonction de la ville puis donnéer sa propabilité (R2) et son taux d'erreur en année (RSME ou MSE)
4. Créer une classification logistique pour savoir si il y a un garage en fonction du prix et de la ville 
5. Créer une classification par KNN pour savoir si il a un balcon en fonction du prix et de la ville
6.  Pour les 2 classifications précédente: afficher le accuracy, recall puis F1 Score
7.  Bonus: Comparer les 2 méthodes de classification KNN et logistique précédente pour voir celle qui prédits le mieux: (accuracy, recall puis F1 Score)
8.  Bonus ULTIMATE: Créer une classification avec Random Forest (new algo) pour savoir si il y a un balcon en fonction du prix et de la ville 

# Sur votre App et API
11. Mettre à disposition l'entraitement et la prédiction sous APIs des points 2, 3 et 4
12. Mettre en forme les prédictions dans le formulaire d'ajout d'appartement quand j'interagis avec les nouveaux champs prix, surface, ville


## Rendu

Un Repo Github avec votre Notebook et projet

## Ressources:
https://www.udemy.com/course/formation-machine-learning-python/learn/lecture/19330772?start=0#overview
https://www.udemy.com/course/draft/4938074/learn/lecture/34542072?start=0#overview
https://www.udemy.com/course/100-exercises-python-data-science-scikit-learn/learn/quiz/4958230#overview
https://www.youtube.com/watch?v=P6kSc3qVph0https://openclassrooms.com/fr/courses/8063076-initiez-vous-au-machine-learning/8298609-classifiez-les-donnees-avec-la-regression-logistique
https://fr.linedata.com/principaux-algorithmes-de-classification-partie-2
https://france.devoteam.com/paroles-dexperts/algorithme-n4-la-regression-lineaire-pour-comprendre-les-grands-principes-du-machine-learning/






