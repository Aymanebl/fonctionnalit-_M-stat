import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats

# Configuration de la page
st.set_page_config(page_title="M-STAT Clone", page_icon="📊")

st.title("📊 M-STAT : Module de Statistiques")
st.write("Application développée pour le calcul des statistiques descriptives et intervalles de confiance.")

# 1. Chargement du fichier
st.sidebar.header("1. Charger les données")
fichier_charge = st.sidebar.file_uploader("Chargez un fichier CSV ou Excel", type=['csv', 'xlsx'])

if fichier_charge is not None:
    # Lecture du fichier
    if fichier_charge.name.endswith('.csv'):
        df = pd.read_csv(fichier_charge)
    else:
        df = pd.read_excel(fichier_charge)
        
    st.subheader("Aperçu du jeu de données")
    st.dataframe(df.head())
    st.markdown("---")

    # 2. Paramétrage de l'analyse
    st.sidebar.header("2. Paramétrage")
    colonne_choisie = st.sidebar.selectbox("Sélectionnez la variable à analyser :", df.columns)
    type_variable = st.sidebar.radio("Type de la variable :", ["Quantitative", "Qualitative"])

    # ==========================================
    # AUDIT DE LA VARIABLE SÉLECTIONNÉE
    # ==========================================
    st.markdown(f"### 🧹 Audit de la variable : *{colonne_choisie}*")
    
    # On compte les vides UNIQUEMENT dans la colonne choisie
    vides_colonne = df[colonne_choisie].isnull().sum()
    donnees_propres = df[colonne_choisie].dropna() # On garde les données valides
    
    if vides_colonne > 0:
        st.warning(f"⚠️ **Attention :** Cette colonne contient **{vides_colonne} valeur(s) vide(s)** (NaN). Elles ont été automatiquement ignorées pour ne pas fausser les calculs.")
    else:
        st.success("✅ **Parfait :** Cette colonne est 100% propre (aucune valeur vide).")

    st.markdown("---")

    # ==========================================
    # CAS 1 : VARIABLE QUANTITATIVE
    # ==========================================
    if type_variable == "Quantitative":
        donnees_propres = pd.to_numeric(donnees_propres, errors='coerce').dropna()
        n = len(donnees_propres)
        
        if n > 0:
            moyenne = np.mean(donnees_propres)
            ecart_type = np.std(donnees_propres, ddof=1)
            
            st.subheader("📈 Statistiques Descriptives")
            
            stats_desc = {
                "Moyenne": round(moyenne, 4),
                "Médiane": round(np.median(donnees_propres), 4),
                "Écart-type": round(ecart_type, 4),
                "Variance": round(np.var(donnees_propres, ddof=1), 4),
                "Minimum": np.min(donnees_propres),
                "Maximum": np.max(donnees_propres),
                "Taille valide (n)": n
            }
            st.table(pd.DataFrame(stats_desc.items(), columns=["Statistique", "Valeur"]))

            # --- INTERVALLE DE CONFIANCE ---
            st.subheader("🎯 Intervalle de Confiance pour la Moyenne")
            niveau_confiance = st.slider("Choisissez le niveau de confiance (%) :", 80, 99, 95)
            alpha = 1 - (niveau_confiance / 100)
            
            valeur_t = stats.t.ppf(1 - alpha/2, df=n-1)
            marge_erreur = valeur_t * (ecart_type / np.sqrt(n))
            
            borne_inf = moyenne - marge_erreur
            borne_sup = moyenne + marge_erreur
            
            st.success(f"**IC à {niveau_confiance}% : [ {borne_inf:.4f} ; {borne_sup:.4f} ]**")
            st.write(f"*Interprétation : Nous sommes sûrs à {niveau_confiance}% que la vraie moyenne se situe entre ces deux valeurs.*")
            
        else:
            st.error("Erreur : La colonne ne contient aucune donnée numérique valide.")

    # ==========================================
    # CAS 2 : VARIABLE QUALITATIVE
    # ==========================================
    else:
        st.subheader("📊 Fréquences et Répartition")
        
        frequences = donnees_propres.value_counts()
        pourcentages = donnees_propres.value_counts(normalize=True) * 100
        
        df_qualitatif = pd.DataFrame({
            "Effectif (Fréquence absolue)": frequences,
            "Pourcentage (%)": pourcentages.round(2)
        })
        
        st.table(df_qualitatif)
        
        mode_val = donnees_propres.mode()[0]
        st.info(f"**Le Mode** (la modalité la plus fréquente) est : **{mode_val}**")

else:
    st.info("👈 Veuillez charger un fichier de données depuis le menu de gauche pour commencer.")
