import streamlit as st
import pandas as pd
from pathlib import Path

hide_menu_and_deploy_button = """
<style>
#MainMenu {
    visibility: hidden;
}

/* Hide the deploy button */
.css-1v3fvcr {
    display: none !important;
}

/* Hide the header */
.st-emotion-cache-1n4a2v9 {
    display: none !important;
}

/* Hide any other elements if necessary */
.css-1rs6os {
    display: none !important;
}
</style>
"""

def add_custom_css():
    css_file = Path(__file__).parent / "static" / "decode" / "custom.css"
    if css_file.exists():
        with open(css_file) as f:
            css_content = f.read()
            st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)
            st.write(f"Custom CSS applied: {css_content[:100]}...")  # Print the first 100 characters of CSS for debugging

# Inject custom CSS
add_custom_css()

st.markdown(hide_menu_and_deploy_button, unsafe_allow_html=True)

# Load the data from Excel with the new caching command
@st.cache_data
def load_data():
    df = pd.read_csv('decode/data/colleges2.xls')
    return df

# Function to filter colleges based on year, rank, seat type, gender, and institute type
def filter_colleges(df, year, rank, seat_type, gender, institute_category, quota):
    return df[(df['Year'] == year) &
              (df['Closing Rank'] >= rank) &
              (df['Seat Type'] == seat_type) &
              (df['Gender'] == gender) &
              (df['Quota'] == quota) &
              (df['institute_type'] == institute_category)].sort_values(by='Closing Rank')

# Main function to render the Streamlit app
def main():
    st.title("When JOSAA frustrates , wee Illustrate <3")
    st.title("Ease in college and branch prediction using simplified lists...")

    year = st.selectbox("Select the Year:", [2018, 2019, 2020, 2021, 2022, 2023])
    rank = st.number_input("Enter your JEE Advanced/Main Rank:", min_value=1, step=1)

    seat_types = ['OPEN', 'EWS', 'OBC-NCL', 'SC', 'ST', 'OPEN (PwD)', 'EWS (PwD)', 'OBC-NCL (PwD)', 'SC (PwD)', 'ST (PwD)']
    seat_type = st.selectbox("Select your Seat Type:", seat_types)

    genders = ['Gender-Neutral', 'Female-only (including Supernumerary)']
    gender = st.selectbox("Select your Gender:", genders)

    institute_category = st.selectbox("Select Institute Category:", ['IITs', 'Others'])

    quotas = ['AI', 'OS', 'HS', 'GO', 'AP', 'JK', 'LA']
    quota = st.selectbox("Select your Quota:", quotas)

    if st.button("Get Colleges"):
        df = load_data()
        filtered_colleges = filter_colleges(df, year, rank, seat_type, gender, institute_category, quota)

        if not filtered_colleges.empty:
            filtered_colleges['Closing Rank'] = filtered_colleges['Closing Rank'].astype(int)  # Convert Closing Rank to integer
            filtered_colleges = filtered_colleges[['Institute', 'Branch', 'Closing Rank']].reset_index(drop=True)
            filtered_colleges.index += 1  # Start indexing from 1
            st.write("Based on your year, rank, seat type, gender, and institute category, you can get admission to the following colleges and branches:")
            st.table(filtered_colleges)
        else:
            st.write("No colleges found for this year, rank, seat type, gender, and institute category.")

if __name__ == "__main__":
    main()
