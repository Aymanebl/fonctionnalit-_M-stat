import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from statistiques_descriptives import StatistiquesDescriptives
from test_correlation import TestCorrelation

# ──────────────────────────────────────────────────────────────────────────────
#  Configuration de la page
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="M-STAT",
    page_icon="📊",
    layout="wide",
)

# ──────────────────────────────────────────────────────────────────────────────
#  En-tête principal
# ──────────────────────────────────────────────────────────────────────────────
st.title("📊 M-STAT : Module de Statistiques")
st.write("Application développée en **POO** avec **Encapsulation** et **Héritage**.")
st.markdown("---")

# ──────────────────────────────────────────────────────────────────────────────
#  Navigation : choix du module
# ──────────────────────────────────────────────────────────────────────────────
MODULE_DESCRIPTIF = "📈 Statistiques Descriptives"
MODULE_CORRELATION = "🔗 Test de Corrélation (Pearson)"

module_choisi = st.sidebar.radio(
    "🗂️ Choisissez un module :",
    [MODULE_DESCRIPTIF, MODULE_CORRELATION],
)

st.sidebar.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
#  MODULE 1 – STATISTIQUES DESCRIPTIVES
# ══════════════════════════════════════════════════════════════════════════════
if module_choisi == MODULE_DESCRIPTIF:

    st.header("📈 Module 1 — Statistiques Descriptives")
    st.caption(
        "Analysez une variable quantitative ou qualitative : "
        "mesures de tendance centrale, de dispersion, fréquences, etc."
    )
    st.markdown("---")

    # ── Chargement du fichier ──
    st.sidebar.header("1. Charger les données")
    fichier = st.sidebar.file_uploader(
        "Fichier Excel", type=["csv", "xlsx"], key="fichier_desc"
    )

    if fichier is not None:
        df = pd.read_csv(fichier) if fichier.name.endswith(".csv") else pd.read_excel(fichier)

        st.subheader("Aperçu du jeu de données")
        st.dataframe(df.head(), use_container_width=True)
        st.markdown("---")

        # ── Paramétrage ──
        st.sidebar.header("2. Paramétrage")
        col = st.sidebar.selectbox("Variable à analyser :", df.columns, key="col_desc")
        type_var = st.sidebar.radio(
            "Type de variable :", ["Quantitative", "Qualitative"], key="type_desc"
        )

        analyseur = StatistiquesDescriptives(df, col)

        # ── Audit des valeurs manquantes ──
        vides = analyseur.get_audit_vides()
        st.markdown(f"### 🧹 Audit de la variable : *{col}*")
        if vides > 0:
            st.warning(f"⚠️ Cette colonne contient **{vides} valeur(s) manquante(s)** ignorées.")
        else:
            st.success("✅ Cette colonne est 100 % propre.")
        st.markdown("---")

        # ── Analyse ──
        if type_var == "Quantitative":
            if analyseur.verifier_quantitatif():
                dict_stats, _, _, _ = analyseur.calculer_statistiques_quantitatives()
                st.subheader("📊 Statistiques Descriptives")
                st.table(
                    pd.DataFrame(dict_stats.items(), columns=["Statistique", "Valeur"])
                )
            else:
                st.error("❌ La colonne ne contient aucune donnée numérique valide.")
        else:
            st.subheader("📊 Fréquences et Répartition")
            df_qualitatif, mode_val = analyseur.calculer_statistiques_qualitatives()
            st.table(df_qualitatif)
            st.info(f"**Mode :** {mode_val}")
    else:
        st.info("👈 Chargez un fichier CSV ou Excel depuis le menu de gauche pour commencer.")


# ══════════════════════════════════════════════════════════════════════════════
#  MODULE 2 – TEST DE CORRÉLATION DE PEARSON
# ══════════════════════════════════════════════════════════════════════════════
elif module_choisi == MODULE_CORRELATION:

    st.header("🔗 Module 2 — Test de Corrélation de Pearson")
    st.caption(
        "Mesurez le lien linéaire entre deux variables quantitatives : "
        "coefficient r, coefficient de détermination r², p-valeur et interprétation."
    )
    st.markdown("---")

    # ── Chargement du fichier ──
    st.sidebar.header("1. Charger les données")
    fichier = st.sidebar.file_uploader(
        "Fichier CSV ou Excel", type=["csv", "xlsx"], key="fichier_corr"
    )

    if fichier is not None:
        df = pd.read_csv(fichier) if fichier.name.endswith(".csv") else pd.read_excel(fichier)

        st.subheader("Aperçu du jeu de données")
        st.dataframe(df.head(), use_container_width=True)
        st.markdown("---")

        testeur = TestCorrelation(df)
        cols_num = testeur.get_colonnes_numeriques()

        if len(cols_num) < 2:
            st.error(
                "❌ Le fichier doit contenir au moins **2 colonnes numériques** "
                "pour effectuer un test de corrélation."
            )
        else:
            # ── Paramétrage ──
            st.sidebar.header("2. Paramétrage")
            col_x = st.sidebar.selectbox("Variable X :", cols_num, key="col_x")
            col_y = st.sidebar.selectbox(
                "Variable Y :", [c for c in cols_num if c != col_x], key="col_y"
            )

            # ── Calcul ──
            try:
                resultats = testeur.calculer_correlation_pearson(col_x, col_y)
            except ValueError as e:
                st.error(str(e))
                st.stop()

            r      = resultats["r"]
            r2     = resultats["r²"]
            pval   = resultats["p_value"]
            n      = resultats["n"]
            interp = resultats["interpretation"]

            # ── Tableau de résultats ──
            st.subheader("📋 Résultats du test")
            resume = {
                "Coefficient de Pearson (r)": r,
                "Coefficient de détermination (r²)": r2,
                "P-valeur": pval,
                "Effectif valide (n)": n,
                "Force de la corrélation": interp["force"],
                "Direction": interp["direction"],
            }
            st.table(pd.DataFrame(resume.items(), columns=["Indicateur", "Valeur"]))

            # ── Interprétation ──
            st.subheader("🧠 Interprétation")
            alpha = interp["alpha"]
            if interp["significatif"]:
                st.success(
                    f"✅ La corrélation est **statistiquement significative** "
                    f"(p = {pval} < α = {alpha}).\n\n"
                    f"Il existe une corrélation **{interp['force']} {interp['direction']}** "
                    f"entre **{col_x}** et **{col_y}** (r = {r})."
                )
            else:
                st.warning(
                    f"⚠️ La corrélation **n'est pas statistiquement significative** "
                    f"(p = {pval} ≥ α = {alpha}).\n\n"
                    f"On ne peut pas conclure à l'existence d'un lien linéaire "
                    f"entre **{col_x}** et **{col_y}**."
                )

            # ── Nuage de points ──
            st.subheader("📉 Nuage de points avec droite de régression")
            fig, ax = plt.subplots(figsize=(7, 4))
            sns.regplot(
                data=df,
                x=col_x,
                y=col_y,
                ax=ax,
                scatter_kws={"alpha": 0.6, "color": "#4C72B0"},
                line_kws={"color": "#DD4444", "linewidth": 1.5},
            )
            ax.set_xlabel(col_x)
            ax.set_ylabel(col_y)
            ax.set_title(f"Corrélation entre {col_x} et {col_y}  (r = {r})")
            st.pyplot(fig)

    else:
        st.info("👈 Chargez un fichier CSV ou Excel depuis le menu de gauche pour commencer.")
