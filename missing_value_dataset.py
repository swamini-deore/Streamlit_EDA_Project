import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns 
import plotly.express as px 

#---------------------PAGE CONFIG--------------------------------------

st.set_page_config(page_title="Advanced EDA Dashboard", layout="wide")

#------------------------------THEME-------------------------------------
theme = st.sidebar.radio("Theme" , ["Light","Dark"])

if theme == "Dark":
    st.markdown("""
    <style>
    .stApp {background-color: #0e1117; color:white;}
    </style>
    """, unsafe_allow_html=True)
    
#-----------------------------------Title--------------------------------
st.markdown("""
<h1 style='text-align:center; color:#4CAF50;'>
Advanced Themed Dashboard
</h1>
""", unsafe_allow_html=True)
#--------------------------------File upload ----------------------

file = st.file_uploader("Upload csv file", type=["csv"])

if file is not None:
    df = pd.read_csv(file)
    
    st.subheader("dataset preview")
    st.dataframe(df.head())
    
    st.subheader("dataset inf0")
    st.dataframe(df.describe())

    st.subheader("📌 Dataset Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())
    
    #---------------Mising values handler------------------------
    st.subheader("Missing value handler")
    
    if df.isnull().sum().sum() > 0:
        method = st.selectbox("choose method", ["Drop rows", "fill with mean", "fill with median"])
        
    if st.button("Apply missing value handling"):
        if method == "Drop rows":
            df = df.dropna()
        elif method == "fill with mean":
            df = df.fillna(df.mean(numeric_only=True))
        else:
            df = df.fillna(df.median(numeric_only=True))
        
        st.success("Missing values handled sucessfully!")
    #-----------------------FILTER----------------------------------
    
    st.sidebar.header("Filter data")
    
    numeric_cols = df.select_dtypes(include=['int64','float64']).columns.tolist()
    
    num_col = st.sidebar.selectbox("select numeric column", numeric_cols)
    
    min_val = float(df[num_col].min())
    max_val = float(df[num_col].max())
    
    range_val = st.sidebar.slider("select range", min_val, max_val, (min_val, max_val))
    
    filtered_df = df[(df[num_col] >= range_val[0]) & (df[num_col] <= range_val[1])]
    
    st.subheader("filtered data")
    st.dataframe(filtered_df)
    
    #-----------------------------Visualization-----------------------------------------
    
st.header("Visualization Hub")

chart_type = st.selectbox("select chart type", [
    "histogram", "boxplot", "scatter", "line", "bar", "violin", "heatmap", "pie", "treemap", "3D"
])

if chart_type == "Histogram":
    fig = px.histogram(filtered_df, x=num_col)
    st.plotly_chart(fig)

elif chart_type == "Boxplot":
    fig = px.histogram(filtered_df, y=num_col)
    st.plotly_chart(fig)
    
elif chart_type == "scatter":
    y_col = st.selectbox("Select Y column", numeric_cols)
    fig = px.scatter(filtered_df, x=num_col, y=y_col)
    st.plotly_chart(fig)

elif chart_type == "Line":
    fig = px.line(filtered_df, y=num_col)
    st.plotly_chart(fig)

elif chart_type == "Violin":
    fig = px.violin(filtered_df, y=num_col, box=True)
    st.plotly_chart(fig)
    
elif chart_type == "bar":
    fig = px.bar(filtered_df, x = num_col,y=num_col)
    st.plotly_chart(fig)

elif chart_type == "pie":
    fig = px.pie(df, names=num_col)
    st.plotly_chart(fig)

elif chart_type == "treemap":
    fig = px.treemap(df, path=[num_col], values=num_col)
    st.plotly_chart(fig)

elif chart_type == "heatmap":
    fig, ax = plt.subplots(figsize=(10,6))
    sns.heatmap(filtered_df[numeric_cols].corr(), annot=True, cmap="coolwarm",ax=ax)
    st.pyplot(fig)
    
elif chart_type == "3D":
    x3 = st.selectbox("X axis", numeric_cols)
    y3 = st.selectbox("Y axis", numeric_cols, index=1)
    z3 = st.selectbox("Z axis", numeric_cols, index=2)
    fig = px.scatter_3d(filtered_df,x=x3,y=y3,z=z3)
    st.plotly_chart(fig)

    