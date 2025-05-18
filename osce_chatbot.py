import streamlit as st
import openai
import json

openai.api_key = st.secrets["openai_api_key"]

cases = {
    "001": {
        "presenting_complaint": "Cough and fever",
        "patient_info": {
            "age": 34,
            "gender": "Male",
            "symptoms": "Persistent dry cough for 5 days, fever at night, no sputum, no wheezing",
            "allergies": "None",
            "medications": "Occasional paracetamol"
        },
        "expected_questions": ["Duration of symptoms", "Any chest pain", "Travel history", "Vaccination status"],
        "red_flags": ["Shortness of breath", "High fever >39°C", "Productive cough with blood"],
        "model_answer": "Ask relevant questions, rule out red flags, recommend supportive treatment or referral based on severity."
    },
    "002": {
        "presenting_complaint": "Headache",
        "patient_info": {
            "age": 28,
            "gender": "Female",
            "symptoms": "Intermittent throbbing headache over the past 2 weeks, worsens with light, improves with rest",
            "allergies": "Ibuprofen",
            "medications": "Paracetamol 1g PRN"
        },
        "expected_questions": ["Headache onset", "Pain characteristics", "Associated symptoms", "Medication history"],
        "red_flags": ["Sudden severe headache", "Neurological signs", "Vomiting", "Visual disturbances"],
        "model_answer": "Identify migraine features, exclude red flags, suggest lifestyle advice and medication options within scope."
    }
}

st.title("Pharmacy OSCE Chatbot")

def reset_conversation():
    for key in ["messages", "score", "asked", "current_case"]:
        if key in st.session_state:
            del st.session_state[key]
    st.experimental_rerun()

# Reset button with callback
st.button("🔁 Reset Conversation", on_click=reset_conversation)

case_id = st.selectbox("Select an OSCE Case:", list(cases.keys()))
case = cases[case_id]

st.subheader(f"Presenting Complaint: {case['presenting_complaint']}")

if "messages" not in st.session_state or st.session_state.get
