import numpy as np
import pandas as pd
from scipy import stats

class TestCorrelation:
    """
    Classe pour réaliser un test de corrélation de Pearson.
    Encapsule les données et fournit le calcul du coefficient r,
    sa p-valeur, et l'interprétation statistique.
    """

    def __init__(self, dataframe: pd.DataFrame):
        # ENCAPSULATION : Les attributs sont protégés avec un underscore
        self._df = dataframe

    def get_colonnes_numeriques(self):
        """Retourne la liste des colonnes numériques du dataframe."""
        return self._df.select_dtypes(include=[np.number]).columns.tolist()

    def calculer_correlation_pearson(self, col_x: str, col_y: str):
        """
        Calcule le coefficient de corrélation de Pearson entre deux variables.

        Returns:
            dict: dictionnaire contenant r, p_value, n, et l'interprétation.
        """
        # Suppression des lignes avec valeurs manquantes sur les deux colonnes
        data = self._df[[col_x, col_y]].dropna()
        n = len(data)

        if n < 3:
            raise ValueError(
                f"Pas assez d'observations valides ({n}). "
                "Au moins 3 paires complètes sont nécessaires."
            )

        r, p_value = stats.pearsonr(data[col_x], data[col_y])

        return {
            "r": round(r, 4),
            "r²": round(r ** 2, 4),
            "p_value": round(p_value, 6),
            "n": n,
            "interpretation": self._interpreter(r, p_value),
        }

    # ------------------------------------------------------------------ #
    #  Méthode privée – interprétation de la force de la corrélation      #
    # ------------------------------------------------------------------ #
    @staticmethod
    def _interpreter(r: float, p_value: float, alpha: float = 0.05) -> dict:
        """Interprète le coefficient r et la significativité du test."""
        abs_r = abs(r)
        if abs_r >= 0.9:
            force = "très forte"
        elif abs_r >= 0.7:
            force = "forte"
        elif abs_r >= 0.5:
            force = "modérée"
        elif abs_r >= 0.3:
            force = "faible"
        else:
            force = "très faible ou nulle"

        direction = "positive" if r > 0 else "négative"
        significatif = p_value < alpha

        return {
            "force": force,
            "direction": direction,
            "significatif": significatif,
            "alpha": alpha,
        }
