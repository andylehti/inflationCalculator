import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Define initial data based on selected start year
def getInitialData(start_year):
    if start_year == 1920:
        house_price = 6200
        wage = 0.33
    elif start_year == 1960:
        house_price = 11600
        wage = 1.00
    else:
        house_price = 172000
        wage = 11.00
    return house_price, wage

# Update data for each year
def updateData(current_year, house_price, wage):
    house_price *= 1.05
    wage *= 1.03
    return house_price, wage

# Start of Streamlit app
st.title("House Price vs Wage Growth Calculator")

# Button and slider widgets
if "year" not in st.session_state:
    st.session_state.year = 1920
    st.session_state.data = pd.DataFrame({"Year": [], "House Price": [], "Wage": []})

start_year = st.slider("Select start year", 1920, 2010, step=40, value=1920)
reset_chart = st.button("Reset Chart")

# Initialize/reset data when slider or reset button is used
if reset_chart or st.session_state.year != start_year:
    st.session_state.year = start_year
    house_price, wage = getInitialData(start_year)
    st.session_state.data = pd.DataFrame({"Year": [start_year], "House Price": [house_price], "Wage": [wage]})

# Display the initial house price and wage
st.write(f"Year: {st.session_state.year}, Initial House Price: ${st.session_state.data['House Price'].iloc[0]:,.2f}, Wage: ${st.session_state.data['Wage'].iloc[0]:,.2f}")

# Increment year and update data when button is clicked
if st.button("Add +1 Year"):
    st.session_state.year += 1
    last_year = st.session_state.data.iloc[-1]
    house_price, wage = updateData(last_year["Year"], last_year["House Price"], last_year["Wage"])
    st.session_state.data = st.session_state.data.append({"Year": st.session_state.year, "House Price": house_price, "Wage": wage}, ignore_index=True)

# Plotting the data
fig, ax = plt.subplots()
ax.plot(st.session_state.data["Year"], st.session_state.data["House Price"], label="House Price", color="blue")
ax.plot(st.session_state.data["Year"], st.session_state.data["Wage"], label="Wage", color="green")
ax.set_xlabel("Year")
ax.set_ylabel("Price / Wage")
ax.legend()

st.pyplot(fig)
