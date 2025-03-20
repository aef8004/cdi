import streamlit as st
import pandas as pd

# Load the medication matrix from CSV
@st.cache_data
def load_matrix():
    df = pd.read_csv("medication_matrix.csv")
    return df

df = load_matrix()

st.title("🧠 Psychiatric Decision Support Tool")

# Patient inputs
gender = st.selectbox("Select Gender", ["Any", "Male", "Female"])
age = st.slider("Select Age", 5, 90, 35)
age_group = st.selectbox("Select Age Group", ["Pediatric", "Adolescent", "Adult", "Elderly"])
special_pop = st.multiselect("Select Special Population", ["None", "Women in Reproductive Years", "Cardiac Impairment", "Hepatic Impairment", "Renal Impairment", "Obesity"])

# Dynamically load diagnoses from CSV
diagnosis_options = sorted(df["Diagnosis"].dropna().unique())
show_all = st.checkbox("🔓 Show all treatments (ignore diagnosis filter)")

if show_all:
    diagnosis_input = diagnosis_options
else:
    diagnosis_input = st.multiselect("📂 Choose Diagnosis", options=diagnosis_options)

symptoms = st.text_input("Enter Symptoms (comma-separated)").lower().split(",")

# Generate output
if st.button("🔍 Generate Treatment Plan"):
    st.subheader("📋 Results")
    st.write(f"Gender: {gender}")
    st.write(f"Age: {age} ({age_group})")
    st.write(f"Special Population: {', '.join(special_pop)}")
    st.write(f"Diagnosis: {', '.join(diagnosis_input)}")
    st.write(f"Symptoms: {', '.join(symptoms)}")
    st.info("Here’s where your logic engine will show matching medication recommendations from the matrix.")

    # Sample output logic preview
    filtered_df = df[
        (df['Gender'].isin([gender, "Any"])) &
        (df['AgeGroup'].isin([age_group])) &
        (df['SpecialPopulation'].isin(special_pop + ["Any"]))
    ]

    for diag in diagnosis_input:
        matches = filtered_df[filtered_df["Diagnosis"] == diag]
        if not matches.empty:
            st.markdown(f"### 💊 Recommendations for {diag}")
            for i, row in matches.iterrows():
                st.markdown(f"""
                **Treatment Line:** {row['TreatmentLine']}  
                **Class:** {row['Class']}  
                **Medication:** {row['Medication']}  
                **Start Dose:** {row['StartDose']}  
                **Titration:** {row['Titration']}  
                **Contraindications:** _{row['Contraindications']}_  
                **Notes:** {row['Notes']}  
                ---
                """)
