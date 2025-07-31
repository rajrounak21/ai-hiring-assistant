# main.py

import streamlit as st
import openai
import os
from dotenv import load_dotenv
from translate import t
from prompts import (
    get_greeting_message,
    get_info_questions,
    get_tech_stack_prompt,
    get_tech_questions_prompt,
    get_followup_prompt,
    get_end_message,
    get_ready_for_interview_prompt,
    get_wait_message
)

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
st.set_page_config(page_title="TalentScout", page_icon="🤖")

# ---- Language Selector ----
if "language" not in st.session_state:
    st.session_state.language = "English"

# Show dropdown to user
st.session_state.language = st.selectbox(
    t("🌐 Select Interface Language", st.session_state.language),
    ["English", "Hindi"]
)

language = st.session_state.language  # Use this everywhere below
st.title(t("🤖 TalentScout – AI Hiring Assistant", language))




# ---- Initialize Session State ----
if "step" not in st.session_state:
    st.session_state.step = "greeting"
    st.session_state.info_index = 0
    st.session_state.candidate_info = []
    st.session_state.tech_stack = ""
    st.session_state.questions = []
    st.session_state.current_q_index = 0
    st.session_state.awaiting_answer = False
    st.session_state.awaiting_next = False
    st.session_state.just_finished_info = False
    st.session_state.just_finished_tech = False

# ---- Chat Input ----
user_input = st.chat_input(t("Type your response here...", language))

# ---- GREETING ----
if st.session_state.step == "greeting":
    st.chat_message("assistant").markdown(get_greeting_message())
    st.session_state.step = "info"

# ---- CANDIDATE INFO COLLECTION ----
elif st.session_state.step == "info":
    questions = get_info_questions()

    if st.session_state.info_index < len(questions):
        current_q = questions[st.session_state.info_index]
        st.chat_message("assistant").markdown(current_q)

        if user_input:
            st.chat_message("user").markdown(user_input)
            st.session_state.candidate_info.append(user_input.strip())
            st.session_state.info_index += 1

            if st.session_state.info_index >= len(questions):
                st.session_state.step = "tech"
                st.rerun()

# ---- TECH STACK PROMPT ----
elif st.session_state.step == "tech":
    st.chat_message("assistant").markdown(get_tech_stack_prompt())

    if user_input:
        st.chat_message("user").markdown(user_input)
        st.session_state.tech_stack = user_input.strip()

        # Generate technical questions
        prompt = get_tech_questions_prompt(st.session_state.tech_stack)
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        raw = response.choices[0].message.content.strip().split('\n')
        st.session_state.questions = [
            q.strip().split('. ', 1)[1] for q in raw if '. ' in q
        ]
        st.session_state.step = "ready_for_interview"
        st.rerun()

# ---- WAIT FOR 'start' TO BEGIN INTERVIEW ----
elif st.session_state.step == "ready_for_interview":
    st.chat_message("assistant").markdown(get_ready_for_interview_prompt())

    if user_input:
        st.chat_message("user").markdown(user_input)
        if user_input.lower().strip() in ["start", "yes", "go", "ready"]:
            st.session_state.step = "interview"
            st.rerun()

# ---- TECHNICAL INTERVIEW SECTION ----
elif st.session_state.step == "interview":
    idx = st.session_state.current_q_index
    questions = st.session_state.questions

    # Step 1: Ask question if not already waiting for answer
    if not st.session_state.awaiting_answer and not st.session_state.awaiting_next:
        q = questions[idx]
        st.chat_message("assistant").markdown(f"**Q{idx + 1}:** {q}")
        st.session_state.awaiting_answer = True

    # Step 2: Evaluate the answer
    elif user_input and st.session_state.awaiting_answer:
        st.chat_message("user").markdown(user_input)
        question = questions[idx]
        eval_prompt = get_followup_prompt(question, user_input)

        eval_response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": eval_prompt}]
        )
        result = eval_response.choices[0].message.content.strip()
        if "✅" in result:
            if "answers" not in st.session_state:
                st.session_state.answers = []
            st.session_state.answers.append((question, user_input.strip(), "✅ Acceptable"))

            st.chat_message("assistant").markdown(get_wait_message())
            st.session_state.awaiting_answer = False
            st.session_state.awaiting_next = True

        elif "❎" in result:
            if "answers" not in st.session_state:
                st.session_state.answers = []
            st.session_state.answers.append((question, user_input.strip(), "❎ Skipped"))

            st.chat_message("assistant").markdown(result)
            st.session_state.awaiting_answer = False
            st.session_state.awaiting_next = False
            st.session_state.current_q_index += 1

            if st.session_state.current_q_index >= len(st.session_state.questions):
                st.session_state.step = "end"
            st.rerun()

        else:
            st.chat_message("assistant").markdown("❌ That was unclear. Please try again.")
            st.chat_message("assistant").markdown(f"**Q{idx + 1}:** {question}")

    # Step 3: Wait for 'next' to continue
    elif user_input and st.session_state.awaiting_next:
        st.chat_message("user").markdown(user_input)
        if user_input.strip().lower() in ["next", "yes", "okay", "ready"]:
            st.session_state.current_q_index += 1
            st.session_state.awaiting_next = False

            if st.session_state.current_q_index >= len(st.session_state.questions):
                st.session_state.step = "end"
                st.rerun()
            else:
                st.rerun()


# ---- ENDING ----
elif st.session_state.step == "end":
    # Final message to the user
    st.chat_message("assistant").markdown(get_end_message())
    from datetime import datetime
    from fpdf import FPDF
    # Save interview summary as TXT
    def save_summary_txt(txt_file="interview_summary.txt"):
        info = st.session_state.get("candidate_info", [])
        tech = st.session_state.get("tech_stack", "")
        answers = st.session_state.get("answers", [])
        questions = st.session_state.get("questions", [])

        name = info[0] if len(info) > 0 else "N/A"
        email = info[1] if len(info) > 1 else "N/A"
        phone = info[2] if len(info) > 2 else "N/A"
        experience = info[3] if len(info) > 3 else "N/A"
        position = info[4] if len(info) > 4 else "N/A"
        location = info[5] if len(info) > 5 else "N/A"

        with open(txt_file, "w", encoding="utf-8") as f:
            f.write(f"Candidate Name: {name}\n")
            f.write(f"Email: {email}\nPhone: {phone}\n")
            f.write(f"Experience: {experience} years\n")
            f.write(f"Position Applied: {position}\nLocation: {location}\n")
            f.write(f"Tech Stack: {tech}\n\n")
            f.write("Technical Q&A:\n")

            for i in range(len(questions)):
                q = questions[i]
                a = answers[i][1] if i < len(answers) else "Not recorded"
                status = answers[i][2] if i < len(answers) else "-"
                f.write(f"{i+1}. Q: {q}\n   A: {a}\n   Evaluation: {status}\n\n")

            f.write("Interview Completed on: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # Convert TXT to PDF (cleaning unsupported characters)
    def convert_txt_to_pdf(txt_file="interview_summary.txt", pdf_file="interview_summary.pdf"):
        def clean_text(line):
            return line.encode("latin-1", "ignore").decode("latin-1")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        with open(txt_file, "r", encoding="utf-8") as f:
            for line in f:
                pdf.multi_cell(0, 10, clean_text(line))

        pdf.output(pdf_file)

    # Run summary creation and PDF conversion
    save_summary_txt()
    convert_txt_to_pdf()

    # Divider
    st.markdown("---")
    st.markdown("### " + t("📤 Export Your Interview Summary:", language))

    # Side-by-side download buttons
    col1, col2 = st.columns(2)

    with col1:
        with open("interview_summary.txt", "r", encoding="utf-8") as txt_file:
            st.download_button(
                label=t("⬇️ Download as TXT", language),
                data=txt_file.read(),
                file_name="interview_summary.txt",
                mime="text/plain"
            )

    with col2:
        with open("interview_summary.pdf", "rb") as pdf_file:
            st.download_button(
                label=t("⬇️ Download as PDF", language),
                data=pdf_file,
                file_name="interview_summary.pdf",
                mime="application/pdf",
            )
