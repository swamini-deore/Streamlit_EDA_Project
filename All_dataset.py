import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="EDA analysis Dashboard", layout="wide")

# ---------------- THEME TOGGLE ----------------
theme = st.sidebar.radio("🎨 Select Theme", ["Light", "Dark"])

if theme == "Dark":
    st.markdown("""
    <style>
    .stApp {background-color: #0e1117; color: white;}
    </style>
    """, unsafe_allow_html=True)


# ---------------- TITLE ----------------
st.markdown("""
<h1 style='text-align:center; color:#4CAF50;'>
📊 Interactive EDA Dashboard
</h1>
""", unsafe_allow_html=True)

st.write("Upload your dataset and explore it with interactive visualizations")

# ---------------- FILE UPLOAD ----------------
file = st.file_uploader("📂 Upload CSV file", type=["csv"])

if file is not None:
    df = pd.read_csv(file)

    # ---------------- DATA PREVIEW ----------------
    st.subheader("📄 Dataset Preview")
    st.dataframe(df.head())

    # ---------------- KPI METRICS ----------------
    st.subheader("📌 Dataset Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())

    # ---------------- FILTER ----------------
    st.sidebar.header("🔍 Data Filters")

    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

    selected_column = st.sidebar.selectbox("Filter Column", numeric_cols)

    min_val = float(df[selected_column].min())
    max_val = float(df[selected_column].max())

    range_val = st.sidebar.slider(
        "Select Range",
        min_value=min_val,
        max_value=max_val,
        value=(min_val, max_val)
    )

    filtered_df = df[(df[selected_column] >= range_val[0]) &
                     (df[selected_column] <= range_val[1])]

    st.subheader("🔎 Filtered Data")
    st.dataframe(filtered_df)

    # Download filtered data
    st.download_button(
        "⬇ Download Filtered Data",
        filtered_df.to_csv(index=False),
        "filtered_data.csv",
        "text/csv"
    )

    # ---------------- VISUALIZATION ----------------
    st.header("📈 Data Visualizations")

    col1, col2 = st.columns(2)

    # Histogram
    with col1:
        st.subheader("Histogram")
        fig, ax = plt.subplots()
        ax.hist(filtered_df[selected_column], bins=20)
        st.pyplot(fig)

    # Boxplot
    with col2:
        st.subheader("Boxplot")
        fig, ax = plt.subplots()
        sns.boxplot(x=filtered_df[selected_column], ax=ax)
        st.pyplot(fig)

    # Line Chart
    st.subheader("Line Chart")
    st.line_chart(filtered_df[selected_column])

    # Bar Chart
    st.subheader("Bar Chart")
    st.bar_chart(filtered_df[selected_column].value_counts())

    # Scatter Plot
    st.subheader("Scatter Plot")
    col_x = st.selectbox("X Axis", numeric_cols)
    col_y = st.selectbox("Y Axis", numeric_cols, index=1)

    fig = px.scatter(filtered_df, x=col_x, y=col_y)
    st.plotly_chart(fig)

    # Violin Plot
    st.subheader("Violin Plot")
    fig = px.violin(filtered_df, y=selected_column, box=True)
    st.plotly_chart(fig)

    # Correlation Heatmap
    st.subheader("Correlation Heatmap")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(filtered_df[numeric_cols].corr(), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

    # ---------------- TREE MAP ----------------
    st.header("🌳 Tree Map")

    cat_col = st.selectbox("Select Category Column", df.columns)

    fig = px.treemap(df, path=[cat_col], values=selected_column)
    st.plotly_chart(fig)

    # ---------------- PIE CHART ----------------
    st.subheader("Pie Chart")
    fig = px.pie(df, names=cat_col)
    st.plotly_chart(fig)

    # ---------------- 3D PLOT ----------------
    st.header("📌 3D Visualization")

    x3 = st.selectbox("X Axis", numeric_cols, key="x3")
    y3 = st.selectbox("Y Axis", numeric_cols, key="y3")
    z3 = st.selectbox("Z Axis", numeric_cols, key="z3")

    fig = px.scatter_3d(filtered_df, x=x3, y=y3, z=z3)
    st.plotly_chart(fig)

    # ---------------- PAIR PLOT ----------------
    st.header("🔗 Pair Plot")
    fig = sns.pairplot(filtered_df[numeric_cols])
    st.pyplot(fig)
    
    

else:
    st.info("👆 Upload a CSV file to start visualization")
