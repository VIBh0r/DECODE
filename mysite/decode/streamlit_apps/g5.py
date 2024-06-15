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
@st.cache_data
def load_data():
    df = pd.read_csv('decode/data/final.csv')
    df['Closing Rank'] = pd.to_numeric(df['Closing Rank'], errors='coerce')
    return df


def filter_and_plot(institute, seat_type, gender, quota):
    df = load_data()
    filtered_df = df[(df['Institue'].str.strip() == institute) &
                     (df['Gender'] == gender) &
                     (df['Seat Type'] == seat_type) &
                     (df['Quota'] == quota)]

    last_rounds = {
        2016: 6,
        2017: 7,
        2018: 7,
        2019: 6,
        2020: 6,
        2021: 6,
        2022: 6,
        2023: 6
    }

    filtered_data = pd.concat([
        filtered_df[(filtered_df['Year'] == year) & (filtered_df['Round'] == last_round)]
        for year, last_round in last_rounds.items()
    ])

    filtered_data = filtered_data.dropna(subset=['Closing Rank'])
    filtered_data = filtered_data.drop_duplicates(subset=['Year', 'Branch'])
    pivot_df = filtered_data.pivot(index='Year', columns='Branch', values='Closing Rank')

    plt.figure(figsize=(14, 10))

    for branch in pivot_df.columns:
        plt.plot(pivot_df.index, pivot_df[branch], marker='o', linestyle='-', label=branch)

    plt.title(f'Closing Ranks for All Branches in {institute} ({seat_type}, {gender}, {quota}) (2016-2023)')
    plt.xlabel('Year')
    plt.ylabel('Closing Rank')
    plt.legend(title='Branch', bbox_to_anchor=(0.5, -0.15), loc='upper center', ncol=3)
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt)


def main():
    st.title("IIT Closing Ranks Over the Years")

    institutes = [
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

        # Add other IITs as necessary
    ]
    seat_types = ['OPEN', 'EWS', 'OBC-NCL', 'SC', 'ST', 'OPEN (PwD)', 'EWS (PwD)', 'OBC-NCL (PwD)', 'SC (PwD)',
                  'ST (PwD)']
    genders = ['Gender-Neutral', 'Female-only (including Supernumerary)']
    quotas = ['AI', 'HS', 'OS']

    institute = st.selectbox("Select Institute:", institutes)
    seat_type = st.selectbox("Select Seat Type:", seat_types)
    gender = st.selectbox("Select Gender:", genders)
    quota = st.selectbox("Select Quota:", quotas)

    if st.button("Submit"):
        filter_and_plot(institute, seat_type, gender, quota)


if __name__ == "__main__":
    main()