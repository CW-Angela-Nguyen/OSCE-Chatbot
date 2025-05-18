if "messages" not in st.session_state or st.session_state.get("current_case") != case_id:
    st.session_state.messages = [
        {"role": "system", "content": "You are simulating an OSCE case for a pharmacy intern. Respond as the patient in a realistic, emotionally appropriate way. Provide information only when asked. Use this patient data: " + json.dumps(case['patient_info'])}
    ]
    st.session_state.score = 0
    st.session_state.asked = []
    st.session_state.current_case = case_id
