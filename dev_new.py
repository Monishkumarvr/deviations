import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
data = pd.read_csv('Final_Deviation_Cleaned.csv')

# Streamlit app setup
st.title('Elemental Deviation Analysis')

# Sidebar filters
st.sidebar.header('Filters')
customer_names = data['Customer Name'].dropna().unique()
elements = ['C', 'Cr', 'Cu', 'Mg', 'Mn', 'P', 'S', 'Si', 'Al', 'Mo', 'Sn', 'V', 'Ni', 'Fe', 'B', 'Ce', 'Co']

selected_customer = st.sidebar.selectbox('Select Customer', ['All'] + list(customer_names))

# Filter grades based on selected customer
if selected_customer != 'All':
    grade_names = data[data['Customer Name'] == selected_customer]['grade_name'].dropna().unique()
else:
    grade_names = data['grade_name'].dropna().unique()

selected_grade = st.sidebar.selectbox('Select Grade', ['All'] + list(grade_names))
selected_element = st.sidebar.selectbox('Select Element', elements)

# Filter data
filtered_data = data
if selected_customer != 'All':
    filtered_data = filtered_data[filtered_data['Customer Name'] == selected_customer]
if selected_grade != 'All':
    filtered_data = filtered_data[filtered_data['grade_name'] == selected_grade]

# Display statistics and plot
if selected_element:
    element_data = pd.to_numeric(filtered_data[selected_element], errors='coerce').dropna()
    if not element_data.empty:
        # Calculate statistics
        avg_deviation = element_data.mean()
        median_deviation = element_data.median()
        std_dev_deviation = element_data.std()

        st.subheader(f'Statistics for {selected_element}')
        st.write(f'Average Deviation: {avg_deviation:.2f}')
        st.write(f'Median Deviation: {median_deviation:.2f}')
        st.write(f'Standard Deviation: {std_dev_deviation:.2f}')

        # Generate violin plot
        plt.figure(figsize=(10, 6))
        sns.violinplot(y=element_data)
        plt.title(f'Violin Plot for {selected_element}')
        plt.ylabel('Deviation')
        st.pyplot(plt)

        # Generate KDE plot
        plt.figure(figsize=(10, 6))
        sns.kdeplot(element_data, shade=True)
        plt.title(f'KDE Plot for {selected_element}')
        plt.xlabel('Deviation')
        st.pyplot(plt)

        # Generate box plot
        plt.figure(figsize=(10, 6))
        sns.boxplot(y=element_data)
        plt.title(f'Box Plot for {selected_element}')
        plt.xlabel('Deviation')
        st.pyplot(plt)
    else:
        st.write('No data available for the selected filters.')