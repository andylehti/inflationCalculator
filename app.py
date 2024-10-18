import streamlit as st
import pandas as pd

# -----------------------------------------------------------------------------
# Set Page Configuration
st.set_page_config(
    page_title='House Prices vs Wages Dashboard',
    page_icon='🏠',
    layout='centered',  # Use 'wide' if you prefer
)

# -----------------------------------------------------------------------------
# Initialize Session State Variables
if 'current_year' not in st.session_state:
    st.session_state.current_year = None

if 'base_year' not in st.session_state:
    st.session_state.base_year = None

if 'precomputed_data' not in st.session_state:
    st.session_state.precomputed_data = pd.DataFrame()

# -----------------------------------------------------------------------------
# Function to Precompute Data
def precompute_data(base_year, initial_house_price, initial_wage, max_years=4000):
    years = list(range(base_year, base_year + max_years))
    house_prices = [initial_house_price * (1.05) ** i for i in range(max_years)]
    wages = [initial_wage * (1.03) ** i for i in range(max_years)]
    years_elapsed = [i + 1 for i in range(max_years)]
    total_wages = [wage * 2080 * elapsed for wage, elapsed in zip(wages, years_elapsed)]
    
    data = pd.DataFrame({
        'Year': years,
        'House Price': house_prices,
        'Wage': wages,
        'Total Wage': total_wages
    })
    return data

# -----------------------------------------------------------------------------
# Title and Description
st.markdown("""
# 🏠 House Prices vs Wages Dashboard

Explore how the disparity between house prices and wages evolves over time, starting from different base years.
""")

# -----------------------------------------------------------------------------
# Sidebar for Base Year Selection
st.sidebar.header("Settings")

base_year = st.sidebar.radio('Select the Starting Year', [1960, 2010])

# Set initial values based on selected base year
if base_year == 1960:
    initial_house_price = 11600
    initial_wage = 1.00
elif base_year == 2010:
    initial_house_price = 172000
    initial_wage = 11.00

# Initialize or Reset Session State based on Base Year
if st.session_state.base_year != base_year:
    st.session_state.base_year = base_year
    st.session_state.current_year = base_year
    st.session_state.precomputed_data = precompute_data(base_year, initial_house_price, initial_wage)
    
    # Reset scroll to top on base year change (optional)
    st.experimental_rerun()

# -----------------------------------------------------------------------------
# Display Initial House Price and Wage
st.markdown(f"**Starting House Price in {base_year}:** ${initial_house_price:,.2f}")
st.markdown(f"**Starting Wage in {base_year}:** ${initial_wage:,.2f}")

# -----------------------------------------------------------------------------
# Buttons for Incrementing Years
# Using a fixed container at the bottom for mobile-friendly access

button_container = st.container()

with button_container:
    st.markdown("---")  # Separator
    cols = st.columns([1, 1])

    with cols[0]:
        if st.button("+1 Year"):
            if st.session_state.current_year < st.session_state.precomputed_data['Year'].max():
                st.session_state.current_year += 1
            else:
                st.warning("Reached the maximum available year (4000).")

    with cols[1]:
        if st.button("+10 Years"):
            if st.session_state.current_year + 10 <= st.session_state.precomputed_data['Year'].max():
                st.session_state.current_year += 10
            else:
                st.session_state.current_year = st.session_state.precomputed_data['Year'].max()
                st.warning("Reached the maximum available year (4000).")

# -----------------------------------------------------------------------------
# Display Current Year Data
if st.session_state.current_year:
    current_data = st.session_state.precomputed_data[
        st.session_state.precomputed_data['Year'] == st.session_state.current_year
    ].iloc[0]
    
    st.markdown(f"**Current Year:** {current_data['Year']}")
    st.markdown(f"**House Price:** ${current_data['House Price']:,.2f}")
    st.markdown(f"**Total Wage:** ${current_data['Total Wage']:,.2f}")
else:
    st.markdown("**Current Year:** N/A")
    st.markdown("**House Price:** N/A")
    st.markdown("**Total Wage:** N/A")

# -----------------------------------------------------------------------------
# Display Line Chart for House Prices and Total Wages
if st.session_state.current_year:
    display_data = st.session_state.precomputed_data[
        st.session_state.precomputed_data['Year'] <= st.session_state.current_year
    ]

    st.header('House Prices and Total Wages Over Time')
    st.line_chart(
        display_data.set_index('Year')[['House Price', 'Total Wage']]
    )
else:
    st.write("Use the buttons below to start exploring the data.")

# -----------------------------------------------------------------------------
# Optional: Adjust Layout for Mobile
# You can add custom CSS to enhance mobile responsiveness
st.markdown(
    """
    <style>
    /* Make the app more mobile-friendly */
    @media only screen and (max-width: 600px) {
        /* Adjust font sizes */
        h1, h2, h3, h4, h5, h6 {
            font-size: 1.5em !important;
        }
        /* Center align text */
        .css-1aumxhk {
            text-align: center;
        }
        /* Adjust button size */
        button {
            width: 100% !important;
            height: 50px !important;
            font-size: 1.2em !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)
