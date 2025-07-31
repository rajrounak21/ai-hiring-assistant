# translate.py

def t(text, lang="English"):
    hindi = {
        "Type your response here...": "अपना उत्तर यहाँ लिखें...",
        "🌐 Select Interface Language": "🌐 इंटरफ़ेस भाषा चुनें",
        "🤖 TalentScout – AI Hiring Assistant": "🤖 टैलेंटस्काउट – एआई हायरिंग सहायक",
        "📤 Export Your Interview Summary:": "📤 अपना इंटरव्यू सारांश डाउनलोड करें:",
        "⬇️ Download as TXT": "⬇️ TXT के रूप में डाउनलोड करें",
        "⬇️ Download as PDF": "⬇️ PDF के रूप में डाउनलोड करें",
    }

    if lang == "Hindi":
        return hindi.get(text, text)
    return text
