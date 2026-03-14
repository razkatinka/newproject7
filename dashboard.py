import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Titanic Dashboard", layout="wide")

# Title
st.title("Titanic Data Dashboard")

# Load dataset
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    df = pd.read_csv(url)
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filters")

pclass_options = sorted(df['Pclass'].dropna().unique())
sex_options = sorted(df['Sex'].dropna().unique())
embarked_options = sorted(df['Embarked'].dropna().unique())

selected_pclass = st.sidebar.multiselect("Passenger Class", pclass_options, default=pclass_options)
selected_sex = st.sidebar.multiselect("Sex", sex_options, default=sex_options)
selected_embarked = st.sidebar.multiselect("Port of Embarkation", embarked_options, default=embarked_options)

# Filtered Data
filtered_df = df[
    df['Pclass'].isin(selected_pclass) &
    df['Sex'].isin(selected_sex) &
    df['Embarked'].isin(selected_embarked)
]

# Metrics Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Passengers", int(filtered_df.shape[0]))
with col2:
    survived = int(filtered_df['Survived'].sum())
    st.metric("Survivors", survived)
with col3:
    pct_survived = 100 * survived / filtered_df.shape[0] if filtered_df.shape[0] > 0 else 0
    st.metric("Survival Rate", f"{pct_survived:.1f}%")
with col4:
    avg_age = filtered_df['Age'].mean()
    st.metric("Avg Age", f"{avg_age:.1f}" if not pd.isna(avg_age) else "N/A")

# Charts
st.subheader("Survival by Class")
fig_class = px.bar(
    filtered_df.groupby('Pclass')['Survived'].mean().reset_index(),
    x='Pclass',
    y='Survived',
    labels={'Survived': 'Survival Rate'},
    title='Survival Rate by Passenger Class'
)
st.plotly_chart(fig_class, use_container_width=True)

st.subheader("Survival by Sex")
fig_sex = px.bar(
    filtered_df.groupby('Sex')['Survived'].mean().reset_index(),
    x='Sex',
    y='Survived',
    labels={'Survived': 'Survival Rate'},
    title='Survival Rate by Sex'
)
st.plotly_chart(fig_sex, use_container_width=True)

st.subheader("Age Distribution by Survival Status")
fig_age = px.histogram(
    filtered_df, x="Age", color="Survived",
    barmode="overlay",
    nbins=30,
    labels={"Survived": "Survived", "Age": "Age"},
    title="Age Distribution (0 = Did not survive, 1 = Survived)"
)
st.plotly_chart(fig_age, use_container_width=True)

# Data table
st.subheader("Filtered Data")
st.dataframe(filtered_df, use_container_width=True)