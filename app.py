
import streamlit as st
import pandas as pd
import plotly as px
import plotly.express as px

df = pd.read_csv('D:/TripleTen/Projects/Sprint4projects/4-4WebApps/vehicles_us.csv')


# Set page configuration
st.set_page_config(
    page_title="Car Sales Dashboard",
    page_icon="🚗",
    layout="wide"
)

@st.cache_data  # Cache the data for better performance
def load_data():
    # Load the dataset
    df = pd.read_csv('vehicles_us.csv')
    
    # Clean the data (using your clean_data function)
    df = clean_data(df)
    
    return df

def clean_data(df):
    """Clean the dataframe by handling missing values and converting data types"""
    # Handle missing values
    df['model_year'] = df['model_year'].fillna(0).astype(int)
    df['cylinders'] = df['cylinders'].fillna(0)
    df['odometer'] = df['odometer'].fillna(df['odometer'].median())
    df['paint_color'] = df['paint_color'].fillna('unknown')
    
    # Convert boolean columns
    df['is_4wd'] = df['is_4wd'].fillna(False).astype(bool)
    
    return df

def main():
    st.title("🚗 Used Car Market Analysis Dashboard")
    st.markdown("Explore trends in the used car market based on advertisement data")
    
    # Load data
    df = load_data()
    
    # Add sidebar filters
    st.sidebar.header("Filter Data")
    min_year, max_year = int(df['model_year'].min()), int(df['model_year'].max())
    year_range = st.sidebar.slider(
        "Select Model Year Range",
        min_year, max_year,
        (min_year, max_year)
    )
    
    # Filter data based on selections
    filtered_df = df[
        (df['model_year'] >= year_range[0]) & 
        (df['model_year'] <= year_range[1])
    ]
    
    # Show raw data checkbox
    show_raw_data = st.checkbox("Show raw data")
    if show_raw_data:
        st.subheader("Raw Data")
        st.dataframe(filtered_df)
    
    # Create two columns for layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Price Distribution")
        
        # Checkbox to toggle log scale
        log_scale = st.checkbox("Logarithmic scale", key="log_scale_hist")
        
        fig1 = px.histogram(
            filtered_df,
            x='price',
            nbins=50,
            title='Distribution of Car Prices',
            log_y=log_scale
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.header("Price vs Mileage")
        
        # Checkbox to show/hide trendline
        show_trend = st.checkbox("Show trendline", value=True, key="trendline")
        
        fig2 = px.scatter(
            filtered_df,
            x='odometer',
            y='price',
            color='type',
            trendline="lowess" if show_trend else None,
            title='Price vs Mileage by Vehicle Type'
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Additional visualizations
    st.header("Vehicle Type Analysis")
    
    # Grouped bar chart
    fig3 = px.bar(
        filtered_df.groupby(['type', 'condition'], as_index=False)['price'].median(),
        x='type',
        y='price',
        color='condition',
        barmode='group',
        title='Median Price by Vehicle Type and Condition'
    )
    st.plotly_chart(fig3, use_container_width=True)

if __name__ == '__main__':
    main()
