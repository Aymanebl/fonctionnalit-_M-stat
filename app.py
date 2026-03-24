import streamlit as st
import pandas as pd
# Importation de notre classe Fille (qui contient aussi les méthodes de la classe Mère)
from intervalle_confiance import IntervalleConfiance

st.set_page_config(page_title="M-STAT Clone", page_icon="📊")

st.title("📊 M-STAT : Module de Statistiques")
st.write("Application développée en **POO** avec **Encapsulation** et **Héritage**.")

st.sidebar.header("1. Charger les données")
fichier_charge = st.sidebar.file_uploader("Chargez un fichier CSV ou Excel", type=['csv', 'xlsx'])

if fichier_charge is not None:
    if fichier_charge.name.endswith('.csv'):
        df = pd.read_csv(fichier_charge)
    else:
        df = pd.read_excel(fichier_charge)
        
    st.subheader("Aperçu du jeu de données")
    st.dataframe(df.head())
    st.markdown("---")

    st.sidebar.header("2. Paramétrage")
    colonne_choisie = st.sidebar.selectbox("Sélectionnez la variable à analyser :", df.columns)
    type_variable = st.sidebar.radio("Type de la variable :", ["Quantitative", "Qualitative"])

    # INSTANCIATION DE L'OBJET
    # En créant un objet IntervalleConfiance, on a accès à toutes les stats descriptives grâce à l'héritage !
    analyseur = IntervalleConfiance(df, colonne_choisie)

    # AUDIT DES VIDES
    vides = analyseur.get_audit_vides()
    st.markdown(f"### 🧹 Audit de la variable : *{colonne_choisie}*")
    if vides > 0:
        st.warning(f"⚠️ **Attention :** Cette colonne contient **{vides} valeur(s) vide(s)** ignorées.")
    else:
        st.success("✅ **Parfait :** Cette colonne est 100% propre.")
    st.markdown("---")

    # ANALYSE QUANTITATIVE
    if type_variable == "Quantitative":
        if analyseur.verifier_quantitatif():
            # 1. Utilisation de la méthode de la classe Mère
            dict_stats, _, _, _ = analyseur.calculer_statistiques_quantitatives()
            st.subheader("📈 Statistiques Descriptives")
            st.table(pd.DataFrame(dict_stats.items(), columns=["Statistique", "Valeur"]))

            # 2. Utilisation de la méthode de la classe Fille
            st.subheader("🎯 Intervalle de Confiance pour la Moyenne")
            niveau_confiance = st.slider("Choisissez le niveau de confiance (%) :", 80, 99, 95)
            
            borne_inf, borne_sup = analyseur.calculer_intervalle(niveau_confiance)
            st.success(f"**IC à {niveau_confiance}% : [ {borne_inf:.4f} ; {borne_sup:.4f} ]**")
        else:
            st.error("Erreur : La colonne ne contient aucune donnée numérique valide.")

    # ANALYSE QUALITATIVE
    else:
        st.subheader("📊 Fréquences et Répartition")
        # Utilisation de la méthode de la classe Mère
        df_qualitatif, mode_val = analyseur.calculer_statistiques_qualitatives()
        st.table(df_qualitatif)
        st.info(f"**Le Mode** est : **{mode_val}**")

else:
    st.info("👈 Veuillez charger un fichier de données depuis le menu de gauche pour commencer.")