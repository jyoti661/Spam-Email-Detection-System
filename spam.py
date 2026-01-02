import re
from langdetect import detect

# ================== Spam Keywords ==================
spam_keywords = {
    "en": [
        "prize",
        "prize money",
        "won a prize",
        "claim your prize",
        "you got a prize",
        "cash prize",
        "reward",
        "free money", "make money fast", "earn money", "earned money",
        "you earned money", "earn cash", "double your income",
        "extra income", "cash bonus", "no investment", "risk-free",
        "act now", "apply now", "limited time", "urgent", "winner",
        "congratulations", "credit card offer", "exclusive deal"
    ],
    "hi": [
        "मुफ्त पैसा", "जल्दी पैसा कमाओ", "कैश बोनस",
        "बिना निवेश", "जोखिम मुक्त", "जीत"
    ]
}

SPAM_KEYWORD_THRESHOLD = 1

# ================== Helpers ==================

def detect_language(text):
    try:
        lang = detect(text)
    except:
        return "en"
    return lang[:2] if lang[:2] in spam_keywords else "en"

def generate_summary(is_spam, matched_keywords):
    if is_spam:
        return (
            "This email is likely spam. "
            "It contains promotional or urgent keywords such as "
            + ", ".join(matched_keywords[:3])
            + ". Users should avoid clicking suspicious links."
        )
    else:
        return (
            "This email appears safe. "
            "No strong spam indicators or suspicious keywords were detected."
        )

# ================== MAIN ANALYSIS ==================

def analyze_email(email_text):
    lang = detect_language(email_text)
    email_lower = email_text.lower()
    keywords = spam_keywords.get(lang, spam_keywords["en"])

    spam_score = 0
    matched_keywords = []

    # SMART PHRASE MATCHING
    for kw in keywords:
        words = kw.split()
        if all(word in email_lower for word in words):
            spam_score += 1
            matched_keywords.append(kw)

    # SPAM DECISION
    is_spam = spam_score >= SPAM_KEYWORD_THRESHOLD

    # SPAM PROBABILITY (simple estimate)
    spam_probability = min(spam_score * 20, 100)

    # RISK LEVEL
    if is_spam:
        if spam_probability >= 60:
            risk_level = "High Risk"
        elif spam_probability >= 30:
            risk_level = "Medium Risk"
        else:
            risk_level = "Spam (Low Severity)"
    else:
        risk_level = "Safe"

    summary = generate_summary(is_spam, matched_keywords)

    return {
        "language": lang,
        "spam_score": spam_score,
        "spam_probability": spam_probability,
        "risk_level": risk_level,
        "matched_keywords": matched_keywords,
        "is_spam": is_spam,
        "summary": summary
    }
