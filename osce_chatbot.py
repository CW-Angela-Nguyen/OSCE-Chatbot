import streamlit as st
import json
import time
from openai import OpenAI
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages
    )
    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})

    for expected in case['expected_questions']:
        if expected.lower() in user_input.lower() and expected not in st.session_state.asked:
            st.session_state.score += 1
            st.session_state.asked.append(expected)

except Exception as e:
    # Check if it's a rate limit error
    if "RateLimitError" in str(e) or "rate limit" in str(e).lower():
        st.error("API rate limit exceeded. Please wait a moment and try again.")
    else:
        st.error(f"An unexpected error occurred: {e}")


# Initialize OpenAI client with API key from secrets
client = OpenAI(api_key=st.secrets["openai_api_key"])

# Multiple OSCE Cases
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

# Case selection
case_id = st.selectbox("Select an OSCE Case:", list(cases.keys()))
case = cases[case_id]

st.subheader(f"Presenting Complaint: {case['presenting_complaint']}")

# Initialize or reset session state on case change
if "messages" not in st.session_state or st.session_state.get("current_case") != case_id:
    st.session_state.messages = [
        {"role": "system", "content": "You are simulating an OSCE case for a pharmacy intern. Respond as the patient in a realistic, emotionally appropriate way. Provide information only when asked. Use this patient data: " + json.dumps(case['patient_info'])}
    ]
    st.session_state.score = 0
    st.session_state.asked = []
    st.session_state.current_case = case_id

# User input
user_input = st.text_input("You (Pharmacy Intern):", "")

if st.button("Send") and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})

        # Check for key expected questions and update score
        for expected in case['expected_questions']:
            if expected.lower() in user_input.lower() and expected not in st.session_state.asked:
                st.session_state.score += 1
                st.session_state.asked.append(expected)

    except RateLimitError:
        st.error("API rate limit exceeded. Please wait a moment and try again.")
        time.sleep(10)

# Display chat history
for msg in st.session_state.messages:
    if msg['role'] != 'system':
        st.markdown(f"**{msg['role'].capitalize()}:** {msg['content']}")

# Display performance evaluation
st.markdown("---")
st.subheader("🧠 Performance Feedback")
st.markdown(f"**Expected questions asked:** {len(st.session_state.asked)} / {len(case['expected_questions'])}")
st.markdown(f"**Questions asked:** {', '.join(st.session_state.asked) if st.session_state.asked else 'None yet'}")

if len(st.session_state.asked) == len(case['expected_questions']):
    st.success("Great job! You've asked all the key questions expected for this case.")
elif len(st.session_state.messages) > 3:
    st.info("Try to explore more relevant questions to uncover key clinical information.")
