import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

hide_menu_and_deploy_button = """
<style>
#MainMenu {
    visibility: hidden;
}
.css-1v3fvcr {
    display: none !important;
}
.css-1rs6os {
    display: none !important;
}
</style>
"""

# Set background color to black and text color to white
st.markdown(
    """
    <style>
    .main {
        background-color: black;
        color: white;
    }
    .title {
        color: white;
    }
    .box {
        border: 1px solid white;
        padding: 10px;
        margin-top: 20px;
        color: white;
        text-align: center;
    }
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
    """,
    unsafe_allow_html=True
)

def add_custom_css():
    css_file = Path(__file__).parent / "static" / "decode" / "custom.css"
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Inject custom CSS
add_custom_css()

st.markdown(hide_menu_and_deploy_button, unsafe_allow_html=True)

# Load the CSV file
@st.cache_data
def load_data():
    df = pd.read_csv('decode/data/final.csv')
    df['Closing Rank'] = pd.to_numeric(df['Closing Rank'], errors='coerce')
    df['Institue'] = df['Institue'].astype(str)
    return df


data = load_data()

# List of branches
branches = [
    'Computer Science and Engineering (4 Years, Bachelor of Technology)',
    'Mechanical Engineering (4 Years, Bachelor of Technology)',
    'Electronics and Communication Engineering (4 Years, Bachelor of Technology)',
    'Civil Engineering (4 Years, Bachelor of Technology)',
    'Electrical Engineering (4 Years, Bachelor of Technology)',
    'Chemical Engineering (4 Years, Bachelor of Technology)',
    'Electrical and Electronics Engineering (4 Years, Bachelor of Technology)',
    'Metallurgical and Materials Engineering (4 Years, Bachelor of Technology)',
    'Information Technology (4 Years, Bachelor of Technology)',
    'Architecture  (5 Years, Bachelor of Architecture)',
    'Bio Technology (4 Years, Bachelor of Technology)',
    'Engineering Physics (4 Years, Bachelor of Technology)',
    'Mining Engineering  (4 Years, Bachelor of Technology)',
    'Production and Industrial Engineering (4 Years, Bachelor of Technology)',
    'Computer Science and Engineering (5 Years, Bachelor and Master of Technology (Dual Degree))',
    'Aerospace Engineering (4 Years, Bachelor of Technology)',
    'Mathematics and Computing (4 Years, Bachelor of Technology)',
    'Electronics and Instrumentation Engineering (4 Years, Bachelor of Technology)',
    'Production Engineering (4 Years, Bachelor of Technology)',
    'Chemistry (5 Years, Integrated Master of Science)'
]

# List of IITs
iit_institutes = [
    "Indian Institute  of Technology Bhubaneswar",
    "Indian Institute  of Technology Bombay",
    "Indian Institute  of Technology Guwahati",
    "Indian Institute of Technology Bhilai",
    "Indian Institute of Technology Goa",
    "Indian Institute of Technology Jammu",
    "Indian Institute of Technology Dharwad",
    "Indian Institute  of Technology Mandi",
    "Indian Institute  of Technology Delhi",
    "Indian Institute  of Technology Indore",
    "Indian Institute  of Technology Kharagpur",
    "Indian Institute  of Technology Hyderabad",
    "Indian Institute  of Technology Jodhpur",
    "Indian Institute  of Technology Kanpur",
    "Indian Institute  of Technology Madras",
    "Indian Institute  of Technology Gandhinagar",
    "Indian Institute  of Technology Patna",
    "Indian Institute  of Technology Roorkee",
    "Indian Institute  of Technology (ISM) Dhanbad",
    "Indian Institute  of Technology Ropar",
    "Indian Institute  of Technology (BHU) Varanasi",
    "Indian Institute  of Technology Palakkad",
    "Indian Institute  of Technology Tirupati"
]

# List of non-IITs (excluding IITs from the data)
non_iit_institutes = sorted(set(data['Institue'].unique()) - set(iit_institutes))

# Year wise last rounds
last_rounds = {
    2018: 7,
    2019: 6,
    2020: 6,
    2021: 6,
    2022: 6,
    2023: 6
}

# Streamlit UI
st.markdown('<h1 class="title">Branch Cutoff Analysis</h1>', unsafe_allow_html=True)

# Select IIT or non-IIT
institute_type = st.radio("Select Institute Type:", ["IIT", "Non-IIT"])

# Select Institute
if institute_type == "IIT":
    institutes = iit_institutes
else:
    institutes = non_iit_institutes

# Select Branch
selected_branch = st.selectbox('Select Branch', branches)

# Additional filters
seat_types = ['OPEN', 'EWS', 'OBC-NCL', 'SC', 'ST', 'OPEN (PwD)', 'EWS (PwD)', 'OBC-NCL (PwD)', 'SC (PwD)', 'ST (PwD)']
genders = ['Gender-Neutral', 'Female-only (including Supernumerary)']
quotas = ['AI', 'HS', 'OS', '']

seat_type = st.selectbox("Select Seat Type:", seat_types)
gender = st.selectbox("Select Gender:", genders)
quota = st.selectbox("Select Quota:", quotas)

# Select Year
years = list(last_rounds.keys())
selected_year = st.selectbox("Select Year:", years)

if selected_branch and selected_year:
    # Filter data for the selected parameters
    filtered_data = data[(data['Branch'] == selected_branch) &
                         (data['Seat Type'] == seat_type) &
                         (data['Gender'] == gender) &
                         (data['Quota'] == quota) &
                         (data['Year'] == selected_year) &
                         (data['Round'] == last_rounds[selected_year]) &
                         (data['Institue'].isin(institutes))]

    if not filtered_data.empty:
        # Convert 'Closing Rank' to numeric and drop NaNs
        filtered_data['Closing Rank'] = pd.to_numeric(filtered_data['Closing Rank'], errors='coerce')
        filtered_data.dropna(subset=['Closing Rank'], inplace=True)

        # Sort by 'Closing Rank' and select the top 10 lowest closing ranks
        top_10_data = filtered_data.sort_values(by='Closing Rank').head(10)

        # Plot the line graph
        plt.figure(figsize=(14, 10))
        plt.plot(top_10_data['Institue'], top_10_data['Closing Rank'], marker='o', linestyle='--',
                 label=f'{selected_year}')
        plt.xticks(rotation=90)
        plt.title(f'Closing Ranks for {selected_branch} ({seat_type}, {gender}, {quota}) in {selected_year}')
        plt.xlabel('Institute')
        plt.ylabel('Closing Rank')
        plt.legend(title='Year', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True)
        plt.tight_layout()
        st.pyplot(plt)
    else:
        st.write('No data available for the selected parameters.')
else:
    st.write('Please select a branch and year to analyze.')