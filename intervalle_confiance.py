import numpy as np
import scipy.stats as stats
from statistiques_descriptives import StatistiquesDescriptives

# HÉRITAGE : La classe IntervalleConfiance hérite de StatistiquesDescriptives
class IntervalleConfiance(StatistiquesDescriptives):
    
    def __init__(self, dataframe, nom_colonne):
        # Appel du constructeur de la classe mère pour initialiser les données
        super().__init__(dataframe, nom_colonne)

    def calculer_intervalle(self, niveau_confiance):
        """Calcule l'IC en réutilisant les calculs de la classe mère"""
        
        # On utilise la méthode de la classe mère pour récupérer moyenne et écart-type
        dict_stats, moyenne, ecart_type, n = self.calculer_statistiques_quantitatives()
        
        alpha = 1 - (niveau_confiance / 100)
        valeur_t = stats.t.ppf(1 - alpha/2, df=n-1)
        marge_erreur = valeur_t * (ecart_type / np.sqrt(n))
        
        borne_inf = moyenne - marge_erreur
        borne_sup = moyenne + marge_erreur
        
        return borne_inf, borne_sup