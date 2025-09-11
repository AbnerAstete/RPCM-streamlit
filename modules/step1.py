import streamlit as st
import pandas as pd
import numpy as np
import json
import math


import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


from utils.helpers_step1 import  show_data_sample, plot_histograms, plot_boxplots, show_data_metrics, show_data_pie, show_global_score, show_qualitative_analysis

df_student = pd.read_csv("assets/dataset/student/Student_performance_data _.csv")
df_retail_features = pd.read_csv("assets/dataset/retail/Features data set.csv")
df_retail_features_clean = pd.read_csv("assets/dataset/retail/clean/clean_Features data set.csv")

def show(proyecto):
    """Paso 1: Preparación de Datos"""

    st.header("Step 1: Data Quality Assessment.")
    # st.subheader(f"Proyecto: {proyecto}")

    st.markdown("""
    In this Step we evaluate the reliability of the Kaggle User who created the datasets used in the project, as well as the condition and quality of the data. This includes detection of missing values, duplicates, and other integrity metrics.
    """)
    
    st.image("assets/step1.svg", caption="Data Quality Assessment Step")

    st.subheader("🕵️‍♂️ Source Facet Report")

    if proyecto == "Student Performance Analysis":
        show_source_facet("assets/jsons/realibility_report/student_reliability_report.json")
    elif proyecto == "Retail Data Analytics":
        show_source_facet("assets/jsons/realibility_report/retail_reliability_report.json")

    st.subheader("📊 Data Facet")

    if proyecto == "Student Performance Analysis":
        show_data_facet(df = df_student, completeness=100, uniqueness=100, outliers=100, threshold=75)
    elif proyecto == "Retail Data Analytics":
        if 'data_cleaned' not in st.session_state:
            st.session_state.data_cleaned = False
            
        if not st.session_state.data_cleaned:
            completeness, uniqueness, outliers = 75.5, 100, 30
            threshold = 75
            c, u, o = 0.4, 0.3, 0.3 
            global_score = c*completeness/100 + u*uniqueness/100 + o*outliers/100
            
            show_data_facet(df = df_retail_features, completeness=completeness, uniqueness=uniqueness, outliers=outliers, threshold=threshold)
            
            # Display the clear button only if the score is less than 75.
            if global_score < threshold:
                st.markdown("---")
                st.warning("⚠️ The data quality is below the acceptable threshold.")
                
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if st.button("Data Cleaning", type="primary", use_container_width=True):
                        st.session_state.data_cleaned = True
                        st.rerun()
        else:
            # Display clean data
            show_data_facet_clean(df = df_retail_features_clean, completeness=100, uniqueness=100, outliers=70, threshold=75)
            
            # Option to revert to original data
            st.markdown("---")
            st.success("Data successfully cleaned.")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("View Original Data", use_container_width=True):
                    st.session_state.data_cleaned = False
                    st.rerun()
    
def show_source_facet(json_path: str):

    with open(json_path, "r", encoding="utf-8") as f:
        full_evaluation = json.load(f)

    dataset_info = full_evaluation.get("dataset_info", {})
    assessment = full_evaluation.get("reliability_assessment", {})

    st.markdown(f"**{dataset_info.get('dataset_name','')}** — by **{dataset_info.get('author','')}**")
    if "kaggle_url" in dataset_info:
        st.markdown(f"[🌐 View on Kaggle]({dataset_info['kaggle_url']}) | License: **{dataset_info.get('license','')}**")
    else:
        st.markdown(f"License: **{dataset_info.get('license','')}**")

    st.caption(
        f"Downloads: {dataset_info.get('total_downloads',0):,}  |  Votes: {dataset_info.get('votes',0)}"
    )

    # --- Results table ---
    rows = []
    for key, val in assessment.items():
        # Normalize key and result
        name = key.split("_", 1)[1].replace("_", " ").title()
        result = val.get("assessment", "")
        emoji = "✅" if "✓" in result else ("⚠️" if "⚠" in result else "❌")
        rows.append({"Section": name, "State": f"{emoji} {result[1:]}"})

    if rows:
        df_results = pd.DataFrame(rows)
        st.table(df_results)
    else:
        st.warning("⚠️ No se encontraron evaluaciones en el JSON")
    

def show_data_facet(df, completeness, uniqueness, outliers, threshold):   
    # Data exploration
    show_data_sample(df)

    # qualitative analysis
    show_qualitative_analysis(df)

    # histograms y boxplots
    tab1, tab2 = st.tabs(["Histograms", "Boxplots"])
    with tab1:
        plot_histograms(df)
    with tab2:
        plot_boxplots(df)

    # Metric cards
    show_data_metrics(completeness, uniqueness, outliers)

    # Pie chart
    c, u, o = show_data_pie()

    # Global Score
    global_score = c*completeness/100 + u*uniqueness/100 + o*outliers/100
    show_global_score(global_score, threshold)


def show_data_facet_clean(df, completeness, uniqueness, outliers, threshold):   
    """
    Función para mostrar los datos limpios (similar a show_data_facet pero para datos procesados)
    """
    st.info("Data After the Cleaning Process")
    
    # Data exploration
    show_data_sample(df)

    # qualitative analysis
    show_qualitative_analysis(df)

    # histograms y boxplots
    tab1, tab2 = st.tabs(["Histograms (Clean)", "Boxplots (Clean)"])
    with tab1:
        plot_histograms(df)
    with tab2:
        plot_boxplots(df)

    # Metric cards
    show_data_metrics(completeness, uniqueness, outliers)

    # Pie chart
    c, u, o = show_data_pie()

    # Global Score
    global_score = c*completeness/100 + u*uniqueness/100 + o*outliers/100
    show_global_score(global_score, threshold)