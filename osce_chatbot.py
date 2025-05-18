import streamlit as st
import json

# Multiple OSCE Cases with symptom_duration added for simulation
cases = {
    "001": {
        "presenting_complaint": "Cough and fever",
        "patient_info": {
            "age": 34,
            "gender": "Male",
            "symptoms": "Persistent dry cough for 5 days, fever at night, no sputum, no wheezing",
            "symptom_duration": "5 days",
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
            "symptom_duration": "2 weeks",
            "allergies": "Ibuprofen",
            "medications": "Paracetamol 1g PRN"
        },
        "expected_questions": ["Headache onset", "Pain characteristics", "Associated symptoms", "Medication history"],
        "red_flags": ["Sudden severe headache", "Neurological signs", "Vomiting", "Visual disturbances"],
        "model_answer": "Identify migraine features, exclude red flags, suggest lifestyle advice and medication options within scope."
    }
}

# Function to simulate patient responses locally
def mock_response(user_message, case):
    user_message_lower = user_message.lower()
    # Check for key expected questions and simulate answers
    if "how long" in user_message_lower or "duration" in user_message_lower:
        return f"I have had these symptoms for {case['patient_info'].get('symptom_duration', 'some time')}."
    elif "chest pain" in user_message_lower:
        return "No, I haven't had any chest pain."
    elif "travel history" in user_message_lower:
        return "No recent travel, I’ve been local."
    elif "vaccination" in user_message_lower:
        return "Yes, I am up to date with my vaccinations."
    elif "pain characteristics" in user_message_lower:
        return "The headache is throbbing and comes and goes."
    elif "associated symptoms" in user_message_lower:
        return "I sometimes feel nauseous and sensitive to light."
    elif "medication history" in user_message_lower:
        return "I usually take paracetamol when it gets bad."
    else:
        return "Can you please ask more questions to understand my condition better?"

# Streamlit UI
st.title("Pharmacy OSCE Chatbot Simulator (Offline)")

# Case selection
case_id = st.selectbox("Select an OSCE Case:", list(cases.keys()))
case = cases[case_id]

st.subheader(f"Presenting Complaint: {case['presenting_complaint']}")

# Initialize session state for chat and score
if "messages" not in st.session_state or st.session_state.get("current_case") != case_id:
    st.session_state.messages = [
        {"role": "system", "content": "You are simulating an OSCE case for a pharmacy intern. Respond as the patient. Provide info only when asked."},
    ]
    st.session_state.score = 0
    st.session_state.asked = []
    st.session_state.current_case = case_id

# User input
user_input = st.text_input("You (Pharmacy Intern):", "")

if st.button("Send") and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Simulate patient reply locally instead of calling OpenAI
    reply = mock_response(user_input, case)

    st.session_state.messages.append({"role": "assistant", "content": reply})

    # Score checking for expected questions
    for expected in case['expected_questions']:
        if expected.lower() in user_input.lower() and expected not in st.session_state.asked:
            st.session_state.score += 1
            st.session_state.asked.append(expected)

# Display chat history
for msg in st.session_state.messages:
    if msg['role'] != 'system':
        st.markdown(f"**{msg['role'].capitalize()}:** {msg['content']}")

# Performance feedback
st.markdown("---")
st.subheader("🧠 Performance Feedback")
st.markdown(f"**Expected questions asked:** {len(st.session_state.asked)} / {len(case['expected_questions'])}")
st.markdown(f"**Questions asked:** {', '.join(st.session_state.asked) if st.session_state.asked else 'None yet'}")

if len(st.session_state.asked) == len(case['expected_questions']):
    st.success("Great job! You've asked all the key questions expected for this case.")
elif len(st.session_state.messages) > 3:
    st.info("Try to explore more relevant questions to uncover key clinical information.")
