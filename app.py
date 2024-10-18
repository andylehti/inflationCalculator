import streamlit as st
import pandas as pd

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='House Prices vs Wages Dashboard',
    page_icon=':house:',  # You can choose any emoji or URL for the icon.
)

# -----------------------------------------------------------------------------
# Initialize Session State for House Price and Wage

if 'house_price' not in st.session_state:
    st.session_state.house_price = None

if 'wage' not in st.session_state:
    st.session_state.wage = None

if 'current_year' not in st.session_state:
    st.session_state.current_year = None

if 'base_year' not in st.session_state:
    st.session_state.base_year = None

if 'precomputed_data' not in st.session_state:
    st.session_state.precomputed_data = pd.DataFrame()

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
st.markdown(
    """
    # 🏠 House Prices vs Wages Dashboard

    Explore how the disparity between house prices and wages evolves over time, starting from different base years.
    """
)

# Add some spacing
st.write("")
st.write("")

# Sidebar for Settings
st.sidebar.header("Settings")

# Base year selection using Radio Buttons
base_year = st.sidebar.radio('Select the starting year', [1960, 2010])

# Set initial house price and wage based on the base year
if base_year == 1960:
    initial_house_price = 11600
    initial_wage = 1.00
elif base_year == 2010:
    initial_house_price = 172000
    initial_wage = 11.00

# Initialize or Reset Session State based on Base Year
if st.session_state.base_year != base_year:
    st.session_state.house_price = initial_house_price
    st.session_state.wage = initial_wage
    st.session_state.current_year = base_year
    st.session_state.base_year = base_year

    # Precompute data for up to 4000 years from the base year
    years = list(range(base_year, base_year + 4000))
    house_prices = [initial_house_price * (1.05) ** i for i in range(4000)]
    wages = [initial_wage * (1.03) ** i for i in range(4000)]

    st.session_state.precomputed_data = pd.DataFrame({
        'Year': years,
        'House Price': house_prices,
        'Wage': wages
    })

# Display initial house price and wage
st.markdown(f"**Starting House Price in {base_year}:** ${st.session_state.house_price:,.2f}")
st.markdown(f"**Starting Wage in {base_year}:** ${st.session_state.wage:,.2f}")

# Buttons to increment the number of years displayed
col1, col2 = st.columns(2)
with col1:
    if st.button('+1 Year'):
        if st.session_state.current_year < st.session_state.precomputed_data['Year'].max():
            st.session_state.current_year += 1
            # Update house price and wage
            new_data = st.session_state.precomputed_data[
                st.session_state.precomputed_data['Year'] == st.session_state.current_year
            ]
            if not new_data.empty:
                st.session_state.house_price = new_data['House Price'].values[0]
                st.session_state.wage = new_data['Wage'].values[0]
        else:
            st.warning("Reached the maximum available year (4000).")

with col2:
    if st.button('+10 Years'):
        new_year = st.session_state.current_year + 10
        max_year = st.session_state.precomputed_data['Year'].max()
        if new_year <= max_year:
            st.session_state.current_year = new_year
            # Update house price and wage
            new_data = st.session_state.precomputed_data[
                st.session_state.precomputed_data['Year'] == st.session_state.current_year
            ]
            if not new_data.empty:
                st.session_state.house_price = new_data['House Price'].values[0]
                st.session_state.wage = new_data['Wage'].values[0]
        else:
            st.session_state.current_year = max_year
            new_data = st.session_state.precomputed_data[
                st.session_state.precomputed_data['Year'] == st.session_state.current_year
            ]
            if not new_data.empty:
                st.session_state.house_price = new_data['House Price'].values[0]
                st.session_state.wage = new_data['Wage'].values[0]
            st.warning("Reached the maximum available year (4000).")

# Add some spacing
st.write("")
st.write("")

# Display Current Year Data
st.markdown(f"**Current Year:** {st.session_state.current_year}")
st.markdown(f"**House Price:** ${st.session_state.house_price:,.2f}")
st.markdown(f"**Wage:** ${st.session_state.wage:,.2f}")

# Add some spacing
st.write("")
st.write("")

# Precompute the data up to the current year for visualization
display_data = st.session_state.precomputed_data[
    st.session_state.precomputed_data['Year'] <= st.session_state.current_year
]

# Display House Prices and Wages Over Time Line Chart
st.header('House Prices and Wages Over Time', divider='gray')
st.line_chart(
    display_data.set_index('Year')[['House Price', 'Wage']]
)

