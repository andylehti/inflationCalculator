import streamlit as st
import pandas as pd

# Set the page configuration
st.set_page_config(
    page_title='House Prices vs Wages',
    page_icon=':house:',
)

# Title and description
st.title(':house: House Prices vs Wages Over Time')
st.write("""
Explore how the disparity between house prices and wages evolves over time, starting from different base years.
""")

# Base year selection
base_year = st.radio('Select the starting year', [1960, 2010])

# Initialize session state variables
if 'num_years' not in st.session_state or 'prev_base_year' not in st.session_state or st.session_state.prev_base_year != base_year:
    st.session_state.num_years = 1
    st.session_state.prev_base_year = base_year

# Set initial house price and wage based on the base year
if base_year == 1960:
    initial_house_price = 11600
    initial_wage = 1.00
else:  # base_year == 2010
    initial_house_price = 172000
    initial_wage = 11.00

# Precompute data for 1000 years
years = list(range(base_year, base_year + 1000))

house_prices = [initial_house_price * (1.05) ** i for i in range(1000)]
wages = [initial_wage * (1.03) ** i for i in range(1000)]

data = pd.DataFrame({
    'Year': years,
    'House Price': house_prices,
    'Wage': wages
})

# Display initial house price and wage
st.markdown(f"**Starting House Price in {base_year}:** ${initial_house_price:,.2f}")
st.markdown(f"**Starting Wage in {base_year}:** ${initial_wage:,.2f}")

# Buttons to increment the number of years displayed
col1, col2 = st.columns(2)
with col1:
    if st.button('+1 year'):
        if st.session_state.num_years < 1000:
            st.session_state.num_years += 1
with col2:
    if st.button('+10 years'):
        if st.session_state.num_years < 1000:
            st.session_state.num_years += 10
            if st.session_state.num_years > 1000:
                st.session_state.num_years = 1000

# Display the chart with the current number of years
display_data = data.iloc[:st.session_state.num_years]
st.line_chart(display_data.set_index('Year'))
