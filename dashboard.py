import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#pip install streamlit
#pip install pandas numpy matplotlib seaborn


# --- 1. SET UP THE PAGE ---
# Set the title of your app
st.title("My Interactive Data Explorer 📊")

# Add some text to explain what the app does
st.write("Upload your CSV file, and I will perform a quick analysis!")

# --- 2. FILE UPLOAD ---
# Section for uploading a file OR providing a URL

st.header("1. Get Your Data")

# Option 1: File Uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

# Option 2: Text Input for URL
data_url = st.text_input("Or, paste a URL to a CSV file")

# --- 3. LOAD THE DATA ---
# This 'if' block ensures that the rest of the code only runs ONCE data is loaded
# We'll create a 'df' (DataFrame) variable to hold the data

df = None  # Initialize df as None

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error reading file: {e}")
elif data_url:
    try:
        # Simple validation for a csv link
        if data_url.endswith('.csv'):
            df = pd.read_csv(data_url)
        else:
            st.warning("Please provide a valid URL ending in .csv")
    except Exception as e:
        st.error(f"Error reading URL: {e}")

# --- 4. RUN THE ANALYSIS (Only if df exists) ---
if df is not None:

    st.success("Data loaded successfully!")

    # --- Section: Show Raw Data ---
    st.header("2. Quick Look at the Data")
    if st.checkbox("Show raw data"):
        st.dataframe(df.head(10)) # Show first 10 rows

    # --- Section: Descriptive Statistics ---
    st.header("3. Descriptive Statistics")
    st.write("Here is the summary of all numerical columns:")
    st.dataframe(df.describe()) # This is your Pandas skill!

    # --- Section: Columns & Data Types ---
    st.header("4. Column Information")
    st.write("Columns, data types, and non-null counts:")
    # To display df.info(), we capture its output
    import io
    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)


    # --- 5. INTERACTIVE VISUALIZATIONS ---
    st.header("5. Visualize Your Data")
    st.write("Select columns to create plots.")

    # Get a list of all column names
    all_columns = df.columns.tolist()
    
    # Separate numeric and categorical columns
    numeric_columns = df.select_dtypes(include=np.number).columns.tolist()
    categorical_columns = df.select_dtypes(exclude=np.number).columns.tolist()

    # --- Plot 1: Histogram (using Seaborn) ---
    st.subheader("Distribution (Histogram)")
    hist_col = st.selectbox("Select a numeric column for the histogram:", numeric_columns)
    
    if hist_col:
        st.write(f"Plotting histogram for: {hist_col}")
        # Create the figure
        fig, ax = plt.subplots()
        sns.histplot(df[hist_col], kde=True, ax=ax)
        # Display the plot in Streamlit
        st.pyplot(fig)

    # --- Plot 2: Scatter Plot (using Seaborn) ---
    st.subheader("Relationship (Scatter Plot)")
    x_col = st.selectbox("Select the X-axis:", numeric_columns)
    y_col = st.selectbox("Select the Y-axis:", numeric_columns)
    
    if x_col and y_col:
        st.write(f"Plotting scatter plot: {x_col} vs. {y_col}")
        fig2, ax2 = plt.subplots()
        sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax2)
        st.pyplot(fig2)

    # --- Plot 3: Box Plot (using Seaborn) ---
    st.subheader("Distribution by Category (Box Plot)")
    cat_col = st.selectbox("Select a categorical column:", categorical_columns)
    num_col = st.selectbox("Select a numeric column:", numeric_columns, key="boxplot_num") # 'key' avoids widget conflict

    if cat_col and num_col:
        st.write(f"Plotting boxplot: {num_col} by {cat_col}")
        fig3, ax3 = plt.subplots()
        sns.boxplot(data=df, x=cat_col, y=num_col, ax=ax3)
        plt.xticks(rotation=45) # Rotate labels for readability
        st.pyplot(fig3)

    # --- Plot 4: Correlation Heatmap ---
    st.subheader("Correlation Heatmap")
    if len(numeric_columns) > 1:
        corr = df[numeric_columns].corr()
        fig4, ax4 = plt.subplots()
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', ax=ax4)
        st.pyplot(fig4)
    else:
        st.write("You need at least two numeric columns to create a correlation heatmap.")