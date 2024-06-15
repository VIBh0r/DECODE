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
    return pd.read_csv('decode/data/final.csv')

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

# Year wise last rounds
last_rounds = {
    2021: 6,
    2017: 7,
    2018: 7,
    2019: 6,
    2020: 6,
    2021: 6,
    2022: 6,
    2023: 6
}

# Streamlit UI
st.markdown('<h1 class="title">Branch Cutoff Analysis</h1>', unsafe_allow_html=True)
selected_branch = st.selectbox('Select Branch', branches)

if selected_branch:
    # Filter data for the selected branch
    branch_data = data[data['Branch'] == selected_branch]

    # Filter for 2021 and 2023 data
    data_2021 = branch_data[(branch_data['Year'] == 2021) & (branch_data['Round'] == last_rounds[2021])]
    data_2023 = branch_data[(branch_data['Year'] == 2023) & (branch_data['Round'] == last_rounds[2023])]

    # Merge data on the common column (assuming 'Institute' is the common identifier)
    merged_data = pd.merge(data_2021, data_2023, on='Institue', suffixes=('_2021', '_2023'))

    if not merged_data.empty:
        # Convert 'Closing Rank' columns to numeric, forcing errors to NaN
        merged_data['Closing Rank_2021'] = pd.to_numeric(merged_data['Closing Rank_2021'], errors='coerce')
        merged_data['Closing Rank_2023'] = pd.to_numeric(merged_data['Closing Rank_2023'], errors='coerce')

        # Drop rows with NaN values in 'Closing Rank' columns
        merged_data.dropna(subset=['Closing Rank_2021', 'Closing Rank_2023'], inplace=True)

        # Calculate the difference
        merged_data['Difference'] = merged_data['Closing Rank_2023'] - merged_data['Closing Rank_2021']

        # Count positive and negative differences
        positive_count = (merged_data['Difference'] > 0).sum()
        negative_count = (merged_data['Difference'] < 0).sum()

        labels = ['Cutoff Increased', 'Cutoff Decreased']
        sizes = [positive_count, negative_count]
        colors = ['#ff9999','#66b3ff']

        # Add the message before the pie chart
        st.markdown(
            """
            <div class="box">
            THIS IS AN OVERALL ANALYSIS OF THE BRANCH, SHOWING THE % OF INSTITUTES WHERE THE BRANCH CUTOFF IS INCREASING OR DECREASING.
            </div>
            """,
            unsafe_allow_html=True
        )

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')

        st.pyplot(fig1)
    else:
        st.write('No data available for the selected branch for the specified years.')
else:
    st.write('Please select a branch to analyze.')