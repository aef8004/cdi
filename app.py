import streamlit as st

st.title("🧠 Psychiatric Decision Support Tool")

gender = st.selectbox("Select Gender", ["Any", "Male", "Female"])
age = st.slider("Select Age", 5, 90, 35)
diagnosis = st.multiselect("Diagnosis", ["Depression", "Anxiety", "ADHD"])
symptoms = st.text_input("Enter Symptoms (comma-separated)")

if st.button("Generate Treatment Plan"):
    st.subheader("📋 Results")
    st.write(f"Gender: {gender}")
    st.write(f"Age: {age}")
    st.write(f"Diagnosis: {', '.join(diagnosis)}")
    st.write(f"Symptoms: {symptoms}")
    st.info("Here’s where your logic engine will show recommended meds.")
