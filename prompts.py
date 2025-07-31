# prompts.py

# Step 1: Greeting Message
def get_greeting_message():
    return (
        "👋 Hello! I'm **TalentScout**, your AI hiring assistant.\n\n"
        "I'll guide you through a short screening process. "
        "First, I’ll ask a few basic questions about you, and then we’ll move on to technical questions based on your skills.\n\n"
        "Let's begin! 😊"
    )

# Step 2: Candidate Info Questions
def get_info_questions():
    return [
        "📛 What's your **full name**?",
        "📧 What's your **email address**?",
        "📱 What's your **phone number**?",
        "💼 How many **years of experience** do you have?",
        "🎯 What **position** are you applying for?",
        "📍 Where are you **currently located**?"
    ]

# Step 3: Ask for Tech Stack
def get_tech_stack_prompt():
    return (
        "🧠 Now tell me about your **top 3–5 strongest technologies** that you’re most confident in.\n\n"
        "You can include languages, frameworks, tools, or databases.\n"
        "_Example: Python, Django, React, MySQL_"
    )


# Step 4: Generate Technical Questions Prompt
def get_tech_questions_prompt(tech_stack: str) -> str:
    return (
        f"You are a technical interviewer.\n"
        f"Generate up to 5 technical interview questions to assess a candidate's knowledge of the following stack: {tech_stack}.\n"
        f"Do NOT include answers or explanations. Just output the questions as a numbered list like:\n"
        f"1. What is ...?\n2. How does ...?"
    )

# Step 5: Evaluate User's Answer to Each Question
def get_followup_prompt(question: str, answer: str) -> str:
    return (
        f"You are a strict but understanding technical interviewer.\n"
        f"The candidate was asked:\n'{question}'\n"
        f"And responded:\n'{answer}'\n\n"
        f"Instructions:\n"
        f"- If the answer is technically correct and clear, respond only with:\n✅ Acceptable answer.\n\n"
        f"- If the candidate says they 'don't know', 'not sure', or gives a similar vague response, respond only with:\n❎ No problem. Let's move to the next question.\n\n"
        f"- If the answer is incorrect or unclear, respond only with:\n❌ Please provide a clearer or more specific answer."
    )


# Step 6: Post-Answer Wait Prompt
def get_wait_message():
    return "✅ Nice job! Type **'next'** when you're ready for the next question."

# Step 7: Confirmation Before Starting Interview
def get_ready_for_interview_prompt():
    return (
        "📝 Thanks! I've collected all your details.\n\n"
        "Type **'start'** whenever you're ready to begin the technical interview questions. 💪"
    )

# Step 8: End Message
# prompts.py

def get_end_message():
    return (
        "✅ Thank you! Your responses have been recorded.\n\n"
        "📩 Our hiring team will review your answers and contact you soon via email.\n"
        "Have a great day! 🚀"
    )
