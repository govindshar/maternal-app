import streamlit as st
from utils.groq_chat import query_groq_llm
# from utils.ocr_utils import extract_text_from_image  # Disabled for now
from langdetect import detect

st.set_page_config(page_title="AI Maternal Health Assistant", layout="centered")
st.title("🤰 AI Maternal Health Assistant")
st.markdown("Built using **Groq (LLaMA3-70B)** — multilingual, doctor-style health assistant for pregnancy support.")

# Sidebar Navigation
feature = st.sidebar.radio("🔍 Choose a Feature", [
    "1. AI Risk Report",
    "2. AI Chatbot (Q&A)",
    "3. Nutrition Guide",
    "4. Daily Health Tracker",
    "5. Symptom Checker",
    "6. ASHA/ANM Note Summary",
    "7. Lab/Prescription Explainer"
])

# ------------------ FEATURE 1: AI RISK REPORT ------------------
if feature == "1. AI Risk Report":
    st.subheader("🩺 Risk Assessment (Doctor-style)")
    with st.form("risk_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", 10, 60)
        weeks = st.number_input("Weeks Pregnant", 1, 42)
        bp = st.text_input("Blood Pressure (e.g. 120/80)")
        anemia = st.selectbox("Anemia?", ["Yes", "No", "Not Sure"])
        diabetes = st.selectbox("Diabetes?", ["Yes", "No", "Gestational"])
        movement = st.selectbox("Fetal Movement?", ["Yes", "No", "Not Sure"])
        bleeding = st.selectbox("Bleeding or pain?", ["Yes", "No"])
        submitted = st.form_submit_button("Generate Report")
    if submitted:
        with st.spinner("Analyzing..."):
            prompt = f"""
You are a senior pregnancy doctor AI.
Patient:
- Name: {name}, Age: {age}
- {weeks} weeks pregnant
- Blood Pressure: {bp}, Anemia: {anemia}, Diabetes: {diabetes}
- Fetal Movement: {movement}, Bleeding/Pain: {bleeding}

Give a 3-part answer:
1. 🧠 Risk Summary
2. ⚠️ Risk Level: HIGH / MODERATE / LOW
3. ✅ Advice (next steps) in simple terms
"""
            output = query_groq_llm(prompt)
            st.success("✅ AI Response")
            st.markdown(output)

# ------------------ FEATURE 2: AI CHATBOT ------------------
elif feature == "2. AI Chatbot (Q&A)":
    st.subheader("💬 Ask Pregnancy Questions (Chatbot)")
    with st.expander("💡 Try Examples"):
        st.markdown("""
- What to eat during the 6th month of pregnancy?
- I feel tired every morning. Is it normal?
- Is it safe to travel in the 8th month?
- How to reduce swelling in the feet?
""")
    user_input = st.text_area("Ask your question here")
    if st.button("Ask AI"):
        if user_input:
            with st.spinner("Responding..."):
                lang = detect(user_input)
                prompt = f"You are a friendly pregnancy assistant. Answer clearly:\n{user_input}"
                reply = query_groq_llm(prompt)
                st.success("🤖 AI says:")
                st.markdown(reply)
        else:
            st.warning("Please type your question first.")

# ------------------ FEATURE 3: NUTRITION ------------------
elif feature == "3. Nutrition Guide":
    st.subheader("🥗 Trimester-Based Diet Plan")
    trimester = st.selectbox("Which Trimester?", ["1st", "2nd", "3rd"])
    diet = st.selectbox("Diet Type", ["Vegetarian", "Non-Vegetarian"])
    anemia = st.selectbox("Do you have anemia?", ["Yes", "No"])
    if st.button("Get Diet Plan"):
        with st.spinner("Creating your personalized Indian diet..."):
            prompt = f"""
You are a dietitian for pregnant Indian women.
Prepare a sample 1-day meal plan for a {diet} woman in her {trimester} trimester.
Anemia: {anemia}. Use local Indian foods and headings: Breakfast, Lunch, Snacks, Dinner.
"""
            result = query_groq_llm(prompt)
            st.success("🍽️ Here's your diet plan:")
            st.markdown(result)
            st.download_button("⬇️ Download Diet Plan", result, file_name="pregnancy_diet.txt")
            st.code(result)

# ------------------ FEATURE 4: DAILY TRACKER ------------------
elif feature == "4. Daily Health Tracker":
    st.subheader("📅 Daily Check-in")
    with st.form("daily_tracker"):
        mood = st.slider("How is your mood today?", 1, 5, 3, format="%d (😞 to 😄)")
        sleep = st.slider("Sleep (hours)", 0, 12, 6)
        food = st.text_input("What did you eat today?")
        movement = st.text_input("Any baby movement or symptoms?")
        submit = st.form_submit_button("Get Health Summary")
    if submit:
        input_text = f"Mood: {mood}, Sleep: {sleep}, Food: {food}, Symptoms: {movement}"
        prompt = f"You are a pregnancy wellness coach. Analyze this daily log and give short feedback:\n{input_text}"
        response = query_groq_llm(prompt)
        st.success("🧘 Daily Summary:")
        st.markdown(response)

# ------------------ FEATURE 5: SYMPTOM CHECKER ------------------
elif feature == "5. Symptom Checker":
    st.subheader("🧾 Symptom Checker")
    user_symptom = st.text_area("Describe your symptom (e.g. dizziness, pain, blurred vision)")
    if st.button("Check Symptom"):
        if user_symptom:
            prompt = f"""
You are a clinical AI that triages pregnancy symptoms.
Patient says: {user_symptom}
1. What could it mean?
2. Is it dangerous?
3. Should they go to hospital or rest at home?
4. Language: simple and non-scary
"""
            result = query_groq_llm(prompt)
            st.success("📋 AI Symptom Review:")
            st.markdown(result)
        else:
            st.warning("Please describe your symptom first.")

# ------------------ FEATURE 6: ASHA/ANM NOTE SUMMARY ------------------
elif feature == "6. ASHA/ANM Note Summary":
    st.subheader("📸 Upload ASHA/ANM Handwritten Note or Form")
    file = st.file_uploader("Upload image (PNG/JPG)", type=["png", "jpg", "jpeg"])
    if file:
        st.image(file, width=300, caption="Uploaded Note")
        with st.spinner("Extracting text..."):
            extracted = "OCR temporarily disabled. Please enter the text manually."
        st.text_area("✍️ Editable Text (OCR result)", extracted, key="editable_note", height=200)
        if st.button("Summarize Note"):
            prompt = f"You are a medical assistant. Summarize the following ASHA/ANM pregnancy field note into 3 lines:\n{st.session_state.editable_note}"
            summary = query_groq_llm(prompt)
            st.success("📄 AI Summary:")
            st.markdown(summary)

# ------------------ FEATURE 7: LAB REPORT EXPLAINER ------------------
elif feature == "7. Lab/Prescription Explainer":
    st.subheader("📋 Upload Lab Report or Prescription")
    report_file = st.file_uploader("Upload an image (clear only)", type=["png", "jpg", "jpeg"])
    if report_file:
        st.image(report_file, width=300, caption="Uploaded Document")
        with st.spinner("Reading image..."):
            raw_text = "OCR temporarily disabled. Please enter the text manually."
        st.text_area("✍️ Editable Lab/Medicine Text", raw_text, key="editable_report", height=200)
        explain_lang = st.radio("Explain in:", ["English", "Hindi"])
        if st.button("Explain this Report"):
            prompt = f"""
You are a maternal health explainer bot.
Read this lab report or prescription:
{st.session_state.editable_report}
Explain it in simple {explain_lang} like talking to a patient.
"""
            explanation = query_groq_llm(prompt)
            st.success(f"🧾 Explanation in {explain_lang}")
            st.markdown(explanation)
            st.download_button("⬇️ Download Explanation", explanation, file_name="report_explained.txt")
