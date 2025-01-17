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
# Function to Precompute Data for All Income Classes
def precompute_data(base_year, initial_house_price, initial_wage, low_middle_wage, middle_wage, max_years=4000):
    years = list(range(base_year, base_year + max_years))
    
    # House price increases by 5.3% per year
    house_prices = [initial_house_price * (1.053) ** i for i in range(max_years)]
    
    # Wage increases by 3.89% per year for general wage
    wages = [initial_wage * (1.0389) ** i for i in range(max_years)]
    
    # Low-middle-class wage increases by 3.66% per year
    low_middle_wages = [low_middle_wage * (1.0366) ** i for i in range(max_years)]
    
    # Middle-class wage increases by 3.57% per year
    middle_wages = [middle_wage * (1.0357) ** i for i in range(max_years)]
    
    # Total yearly wage for 2080 hours
    total_wages = [wage * 2080 for wage in wages]
    low_middle_total_wages = [wage * 2080 for wage in low_middle_wages]
    middle_total_wages = [wage * 2080 for wage in middle_wages]
    
    # Average of the three yearly wages, multiplied by 10 (as requested)
    avg_total_wages = [(w + lm + m) / 3 * 20800 for w, lm, m in zip(wages, low_middle_wages, middle_wages)]
    
    data = pd.DataFrame({
        'Year': years,
        'House Price': house_prices,
        'Wage': wages,
        'Low-Middle Wage': low_middle_wages,
        'Middle Wage': middle_wages,
        'Total Wage': total_wages,
        'Low-Middle Total Wage': low_middle_total_wages,
        'Middle Total Wage': middle_total_wages,
        'Average Total Wage (x10)': avg_total_wages
    })
    return data

# -----------------------------------------------------------------------------
# Initialize Session State Variables
if 'current_year' not in st.session_state:
    st.session_state.current_year = None

if 'base_year' not in st.session_state:
    st.session_state.base_year = None

if 'precomputed_data' not in st.session_state:
    st.session_state.precomputed_data = pd.DataFrame()

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
    initial_wage = 1.25
    low_middle_wage = 4000 / 2080  # Convert annual salary to hourly wage
    middle_wage = 9000 / 2080      # Convert annual salary to hourly wage
elif base_year == 2010:
    initial_house_price = 172000
    initial_wage = 11.00
    low_middle_wage = 40000 / 2080  # Placeholder for 2010 values (adjust as needed)
    middle_wage = 90000 / 2080      # Placeholder for 2010 values (adjust as needed)

# Initialize or Reset Session State based on Base Year
if st.session_state.base_year != base_year:
    st.session_state.base_year = base_year
    st.session_state.current_year = base_year
    st.session_state.precomputed_data = precompute_data(base_year, initial_house_price, initial_wage, low_middle_wage, middle_wage)
    # No st.experimental_rerun() to prevent immediate rerun

# -----------------------------------------------------------------------------
# Display Initial House Price and Wage
st.markdown(f"**Starting House Price in {base_year}:** ${initial_house_price:,.2f}")
st.markdown(f"**Starting Wage in {base_year}:** ${initial_wage:,.2f}")
st.markdown(f"**Low-Middle Class Starting Wage in {base_year}:** ${low_middle_wage:,.2f}")
st.markdown(f"**Middle Class Starting Wage in {base_year}:** ${middle_wage:,.2f}")

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
            new_year = st.session_state.current_year + 10
            max_year = st.session_state.precomputed_data['Year'].max()
            if new_year <= max_year:
                st.session_state.current_year = new_year
            else:
                st.session_state.current_year = max_year
                st.warning("Reached the maximum available year (4000).")

# -----------------------------------------------------------------------------
# Display Current Year Data
if st.session_state.current_year:
    current_data = st.session_state.precomputed_data[
        st.session_state.precomputed_data['Year'] == st.session_state.current_year
    ]
    
    if not current_data.empty:
        current_data = current_data.iloc[0]
        st.markdown(f"**Current Year:** {current_data['Year']}")
        st.markdown(f"**House Price:** ${current_data['House Price']:,.2f}")
        st.markdown(f"**Hourly Wage:** ${current_data['Wage']:,.2f}")
        st.markdown(f"**Low-Middle Hourly Wage:** ${current_data['Low-Middle Wage']:,.2f}")
        st.markdown(f"**Middle Hourly Wage:** ${current_data['Middle Wage']:,.2f}")
        st.markdown(f"**Total Yearly Wage (2080 hours):** ${current_data['Total Wage']:,.2f}")
        st.markdown(f"**Low-Middle Total Yearly Wage:** ${current_data['Low-Middle Total Wage']:,.2f}")
        st.markdown(f"**Middle Total Yearly Wage:** ${current_data['Middle Total Wage']:,.2f}")
        st.markdown(f"**Average Total Wage (x10):** ${current_data['Average Total Wage (x10)']:,.2f}")
    else:
        st.error("Data for the selected year is not available.")
else:
    st.markdown("**Current Year:** N/A")
    st.markdown("**House Price:** N/A")
    st.markdown("**Hourly Wage:** N/A")
    st.markdown("**Low-Middle Hourly Wage:** N/A")
    st.markdown("**Middle Hourly Wage:** N/A")
    st.markdown("**Total Yearly Wage:** N/A")

# -----------------------------------------------------------------------------
# Display Line Chart for House Prices and Total Wages
if st.session_state.current_year:
    display_data = st.session_state.precomputed_data[
        st.session_state.precomputed_data['Year'] <= st.session_state.current_year
    ]

    st.header('House Prices and Total Wages Over Time')
    st.line_chart(
        display_data.set_index('Year')[['House Price', 'Total Wage', 'Low-Middle Total Wage', 'Middle Total Wage', 'Average Total Wage (x10)']]
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
