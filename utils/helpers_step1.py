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



##### STEP 1

## DATA SOURCE 

def show_data_metrics(completeness, uniqueness, outliers):
    st.markdown("#### Data Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Completeness", f"{completeness:.1f}%")
    col2.metric("Uniqueness", f"{uniqueness:.1f}%")
    col3.metric("Outliers", f"{outliers:.1f}%")

def show_data_pie():
    st.markdown("#### Data Quality Weight Distribution")
    col1, col2 = st.columns(2)
    # --- Left column: sliders ---
    with col1:
        completeness = st.slider("Completeness weight", 0, 100, 45)
        uniqueness = st.slider("Uniqueness weight", 0, 100, 25)
        outliers = st.slider("Outliers weight", 0, 100, 30)
        # Normalize weights
        total = completeness + uniqueness + outliers
        weights = {
            "Completeness": completeness / total * 100,
            "Uniqueness": uniqueness / total * 100,
            "Outliers": outliers / total * 100
        }
        # Display normalized values above the sliders
        st.markdown(
            f"**Normalized weights:** Completeness: {weights['Completeness']:.1f}%, "
            f"Uniqueness: {weights['Uniqueness']:.1f}%, Outliers: {weights['Outliers']:.1f}%"
        )
    # --- Right column: pie chart ---
    with col2:
        df = pd.DataFrame({
            "Dimension": list(weights.keys()),
            "Weight": list(weights.values())
        })
        fig = px.pie(
            df,
            names="Dimension",
            values="Weight",
            color="Dimension",
            color_discrete_map={"Completeness":"green","Uniqueness":"orange","Outliers":"red"},
            hover_data=["Weight"]
        )
        fig.update_traces(textinfo="percent+label", pull=[0.05,0.05,0.05])
        st.plotly_chart(fig, use_container_width=True)

    return completeness / total * 100, uniqueness / total * 100, outliers / total * 100
        
def show_global_score(score, threshold=75):
    st.markdown("#### Global Data Quality Score")
    color = "green" if score >= threshold else "red"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={"text": "Global Data Quality Score"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": color},
            "steps": [
                {"range": [0, threshold], "color": "lightcoral"},
                {"range": [threshold, 100], "color": "lightgreen"}
            ],
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

def show_data_sample(df):
    st.markdown("#### Sample of Dataset")
    st.dataframe(df.head())

def show_qualitative_analysis(df, numeric_only=True):
    """
    Muestra un resumen estadístico del DataFrame.
    
    Parameters:
        df: pd.DataFrame
        numeric_only: bool, si True solo columnas numéricas
    """
    st.markdown("#### Data Qualitative Analysis")
    
    if numeric_only:
        df_summary = df.describe().T  # Transpose for better visualization
    else:
        df_summary = df.describe(include='all').T

    # Add count of nulls and unique values
    df_summary['null_count'] = df.isnull().sum()
    df_summary['unique_count'] = df.nunique()

    # Round it off to make it look nicer
    df_summary = df_summary.round(2)

    # Display table in Streamlit
    st.dataframe(df_summary, use_container_width=True)


# PLOTS
def plot_histograms(df, group_size=4, section_title="Column Distributions"):
    """
    Plot histograms for all numeric columns in the dataframe using Plotly + Streamlit.
    - df: pandas DataFrame
    - group_size: number of columns per row
    - section_title: optional markdown title
    """
    st.markdown(section_title)

    numeric_columns = df.select_dtypes(include=['number']).columns
    if len(numeric_columns) == 0:
        st.info("No numeric columns to plot.")
        return

    total_cols = min(group_size, len(numeric_columns))
    rows = math.ceil(len(numeric_columns) / total_cols)

    fig = make_subplots(
        rows=rows, cols=total_cols,
        subplot_titles=numeric_columns,
        horizontal_spacing=0.1, vertical_spacing=0.15
    )

    for i, col in enumerate(numeric_columns):
        col_data = df[col].dropna()
        unique_vals = col_data.nunique()

        if col_data.min() == col_data.max():
            # Constant column → no histogram
            st.warning(f"La columna **{col}** tiene un valor constante, no se grafica histograma.")
            continue

        # Dynamic bin calculation
        if unique_vals <= 5:
            nbins = unique_vals
        elif unique_vals <= 30:
            nbins = 15
        else:
            q75, q25 = np.percentile(col_data, [75 ,25])
            iqr = q75 - q25
            bin_width = 2 * iqr * len(col_data) ** (-1/3)
            data_range = col_data.max() - col_data.min()

            if bin_width <= 0 or data_range == 0:
                nbins = 10
            else:
                nbins = max(int(np.ceil(data_range / bin_width)), 10)

        row_pos = i // total_cols + 1
        col_pos = i % total_cols + 1

        fig.add_trace(
            go.Histogram(
                x=col_data,
                nbinsx=nbins,
                marker_color='skyblue',
                marker_line=dict(color='black', width=1),
                name=col
            ),
            row=row_pos, col=col_pos
        )

    fig.update_layout(
        showlegend=False,
        height=250 * rows,
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

def plot_boxplots(df, group_size=4, section_title="Column Boxplots"):
    """
    Plot boxplots for all numeric columns in the dataframe using Plotly + Streamlit.
    - df: pandas DataFrame
    - group_size: number of columns per row
    - section_title: optional markdown title
    """
    st.markdown(section_title)

    numeric_columns = df.select_dtypes(include=['number']).columns
    if len(numeric_columns) == 0:
        st.info("No numeric columns to plot.")
        return

    total_cols = min(group_size, len(numeric_columns))
    rows = math.ceil(len(numeric_columns) / total_cols)

    fig = make_subplots(
        rows=rows, cols=total_cols,
        subplot_titles=numeric_columns,
        horizontal_spacing=0.1,
        vertical_spacing=0.15
    )

    for i, col in enumerate(numeric_columns):
        col_data = df[col].dropna()

        # Detect outliers
        q1 = col_data.quantile(0.25)
        q3 = col_data.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
        n_outliers = len(outliers)

        row_pos = i // total_cols + 1
        col_pos = i % total_cols + 1

        fig.add_trace(
            go.Box(
                y=col_data,
                boxpoints='outliers', 
                marker_color='lightblue',
                line_color='deepskyblue',
                name=f"{col} ({n_outliers} outliers)"
            ),
            row=row_pos, col=col_pos
        )

    fig.update_layout(
        showlegend=False,
        height=350 * rows,
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)


