# 🤖 AI Hiring Assistant – TalentScout

This project is an interactive AI-based Hiring Assistant that automates the initial screening interview process using Streamlit and OpenAI. It collects candidate information, evaluates technical knowledge based on a chosen tech stack, and generates downloadable interview summaries.

---

## 📌 Features

* 💬 Conversational chatbot interface using **Streamlit**
* 🔍 Collects personal information (name, email, experience, etc.)
* 🧠 Asks **technical questions** based on user-defined tech stack
* ✅ Evaluates answers for correctness using **OpenAI GPT-4o**
* 📅 Exports interview summary as `.txt` and `.pdf`
* 🌐 Supports **Multilingual UI** (English & Hindi)



## 🧰 Tech Stack

* **Frontend**: Streamlit
* **Backend AI**: OpenAI GPT-4o API
* **Language Handling**: Python
* **PDF Generation**: `fpdf`
* **Environment Management**: `python-dotenv`

---

## 🗂️ Project Structure

```
├── main.py                # Streamlit chatbot logic
├── prompts.py             # All LLM prompts structured per phase
├── translate.py           # UI translation helper (EN ↔ HI)
├── requirements.txt       # Required Python packages
├── interview_summary.txt  # Exported Q&A summary (TXT)
├── interview_summary.pdf  # Exported Q&A summary (PDF)
├── .env.example           # API key example
├── flow.txt               # Step-by-step breakdowns 
├── README.md              # You're reading it
```

---

## ⬆️ Flow Overview 

1. ✅ Greet user and explain process
2. 🗞️ Collect personal information
3. 🧑‍💻 Ask for tech stack
4. 🤖 Generate 3–5 technical questions
5. 🧠 Evaluate each answer
6. 📄 Allow user to download `.txt`/`.pdf` summary
7. 🌐 Language selector added (English, Hindi)

---

## 🌍 Multilingual Support

You can switch between **English** and **Hindi** using the dropdown at the top. Only the interface changes — technical questions remain in English for consistency and accuracy.

---

## ⚙️ Installation

1. Clone or download this repo:

```bash
git clone https://github.com/your-username/ai-hiring-assistant.git
cd ai-hiring-assistant
```

2. Create virtual environment (optional):

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Add your OpenAI key in `.env`:

```
OPENAI_API_KEY=your_openai_api_key
```

5. Run the app:

```bash
streamlit run main.py
```

---

## 🗞️ Output

After completing the interview, the app generates:

* `interview_summary.txt` — plain text Q\&A summary
* `interview_summary.pdf` — formatted exportable report

---


## 👨‍💼 Developed By
 
**Rounak Raj**
Diploma in AI & ML | Project – AI Hiring Assistant
July 2025
