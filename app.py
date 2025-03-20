import streamlit as st
import pandas as pd

# -------------------------------------
# Load Medication Matrix CSV
# -------------------------------------
@st.cache_data
def load_matrix():
    df = pd.read_csv("medication_matrix.csv", on_bad_lines='skip')  # Skip bad lines if formatting issues
    return df

df = load_matrix()

# -------------------------------------
# App Title
# -------------------------------------
st.title("🧠 Psychiatric Medication Decision Support Tool")

# -------------------------------------
# Patient Input Section
# -------------------------------------
st.header("📋 Patient Information")

gender = st.selectbox("Select Gender", ["Any", "Male", "Female"])
age = st.slider("Select Age", 5, 90, 35)
age_group = st.selectbox("Select Age Group", ["Pediatric", "Adolescent", "Adult", "Elderly"])
special_pop = st.multiselect("Select Special Population", [
    "None",
    "Women in Reproductive Years",
    "Cardiac Impairment",
    "Hepatic Impairment",
    "Renal Impairment",
    "Obesity"
])

# -------------------------------------
# Diagnosis Dropdown (Dynamically Loaded)
# -------------------------------------
st.subheader("🩺 Diagnosis & Symptoms")

diagnosis_options = sorted(df["Diagnosis"].dropna().unique())
show_all = st.checkbox("🔓 Show All Treatments (Ignore Diagnosis Filter)")

if show_all:
    diagnosis_input = diagnosis_options
else:
    diagnosis_input = st.multiselect("📂 Select Diagnosis", options=diagnosis_options)

symptoms_input = st.text_input("Enter Symptoms (comma-separated)").lower().split(",")

# -------------------------------------
# Generate Treatment Recommendations
# -------------------------------------
if st.button("🔍 Generate Treatment Plan"):
    st.subheader("📑 Results Summary")
    st.write(f"**Gender:** {gender}")
    st.write(f"**Age:** {age}  → **Age Group:** {age_group}")
    st.write(f"**Special Population:** {', '.join(special_pop) if special_pop else 'None'}")
    st.write(f"**Diagnosis:** {', '.join(diagnosis_input)}")
    st.write(f"**Symptoms Entered:** {', '.join(symptoms_input)}")

    # Filter the DataFrame
    filtered_df = df[
        (df['Gender'].isin([gender, "Any"])) &
        (df['AgeGroup'].isin([age_group])) &
        (df['SpecialPopulation'].isin(special_pop + ["Any"]))
    ]

    # Loop through diagnoses
    for diag in diagnosis_input:
        diag_df = filtered_df[filtered_df["Diagnosis"] == diag]
        if not diag_df.empty:
            st.markdown(f"---\n### 💊 Recommendations for **{diag}**")
            for index, row in diag_df.iterrows():
                st.markdown(f"""
**Treatment Line:** {row['TreatmentLine']}  
**Class:** {row['Class']}  
**Medication:** {row['Medication']}  
**Start Dose:** {row['StartDose']}  
**Titration Plan:** {row['Titration']}  
**Contraindications:** _{row['Contraindications']}_  
**Notes:** {row['Notes']}  
---
""")
        else:
            st.warning(f"No treatment options found for diagnosis: {diag}")

