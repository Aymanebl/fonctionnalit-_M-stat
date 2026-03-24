import pandas as pd
import numpy as np

class StatistiquesDescriptives:
    def __init__(self, dataframe, nom_colonne):
        # ENCAPSULATION : Les attributs sont protégés avec un underscore
        self._df = dataframe
        self._colonne_actuelle = nom_colonne
        self._donnees_propres = self._df[nom_colonne].dropna()
        self._valeurs_vides = self._df[nom_colonne].isnull().sum()

    def get_audit_vides(self):
        """Retourne le nombre de valeurs vides"""
        return self._valeurs_vides

    def verifier_quantitatif(self):
        """Nettoie et vérifie si la colonne est numérique"""
        self._donnees_propres = pd.to_numeric(self._donnees_propres, errors='coerce').dropna()
        return len(self._donnees_propres) > 0

    def calculer_statistiques_quantitatives(self):
        n = len(self._donnees_propres)
        moyenne = np.mean(self._donnees_propres)
        ecart_type = np.std(self._donnees_propres, ddof=1)
        
        dict_stats = {
            "Moyenne": round(moyenne, 4),
            "Médiane": round(np.median(self._donnees_propres), 4),
            "Écart-type": round(ecart_type, 4),
            "Variance": round(np.var(self._donnees_propres, ddof=1), 4),
            "Minimum": np.min(self._donnees_propres),
            "Maximum": np.max(self._donnees_propres),
            "Taille valide (n)": n
        }
        return dict_stats, moyenne, ecart_type, n

    def calculer_statistiques_qualitatives(self):
        frequences = self._donnees_propres.value_counts()
        pourcentages = self._donnees_propres.value_counts(normalize=True) * 100
        mode_val = self._donnees_propres.mode()[0]
        
        df_resultats = pd.DataFrame({
            "Effectif (Fréquence absolue)": frequences,
            "Pourcentage (%)": pourcentages.round(2)
        })
        return df_resultats, mode_val