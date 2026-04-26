from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy
import re

app = Flask(__name__)
CORS(app)

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Define regex patterns
regex_patterns = {
    "non_refund": r"\b(non[- ]?refundable|no refunds?)\b",
    "contact": r"\b(contact (us)? at|email\s?:?|phone\s?:?|call (us)?)\b[\s\S]{0,50}",
    "location": r"\b\d{1,5}\s[\w\s]{1,30}(Street|St|Road|Rd|Avenue|Ave|City|Country|Lane|Ln|Boulevard|Blvd)\b",
    "bank": r"\b(bank account|account number|IFSC|SWIFT|routing number|card number|credit card|debit card)\b[\s\S]{0,50}",
    "age": r"\b(18\+|13\+|over 18|must be.*(13|18).*(years old))\b",
    "data_usage": r"\b(data collected|data usage|tracking|third[- ]?party|web beacon|cookies?)\b[\s\S]{0,50}",
    "name_email": r"\b(full name|first name|last name|email address)\b",
    "sensitive_data": r"\b(sensitive data|personal data|PII|personally identifiable information)\b",
    "behavior_tracking": r"\b(behavioral tracking|user behavior|track.*activity)\b",
    "cookies": r"\b(cookie policy|use of cookies|cookies enable|cookies help)\b",
    "log_files": r"\b(log files|server logs|access logs|error logs)\b",
    "third_party_tracking": r"\b(third[- ]?party tracking|external trackers|partner trackers)\b",
    "analytics_usage": r"\b(analytics services|Google Analytics|advertising partners)\b",
    "data_retention": r"\b(data retention|how long.*(store|keep)|retain.*data)\b",
    "data_deletion": r"\b(delete.*data|data deletion|request.*erasure)\b",
    "data_sharing": r"\b(data shared with|share.*partner|third[- ]?party access)\b",
    "data_selling": r"\b(sell.*data|data sale|monetize.*information)\b",
    "marketing_consent": r"\b(consent.*marketing|receive.*promotions|opt[- ]?in to emails)\b",
    "email_communication": r"\b(email communications?|send.*emails|newsletter subscription)\b",
    "push_notifications": r"\b(push notifications?|app alerts|mobile notifications?)\b",
    "children_protection": r"\b(children.*data|under.*(13|16)|COPPA)\b",
    "payment_info": r"\b(payment information|payment details|process.*payment)\b",
    "credit_score": r"\b(credit score|credit report|credit history)\b",
    "health_data": r"\b(health data|medical records|HIPAA)\b",
    "gdpr": r"\b(GDPR|General Data Protection Regulation|EU data rights)\b",
    "ccpa": r"\b(CCPA|CPRA|California Consumer Privacy Act|California Privacy Rights Act)\b",
    "user_content": r"\b(user content|upload.*content|submit.*information)\b",
    "monitoring_content": r"\b(monitor.*content|moderate.*posts|review submissions)\b",
    "remove_content": r"\b(remove.*content|delete.*uploads|right to delete)\b",
    "upload_restrictions": r"\b(prohibited uploads|restricted content|upload rules)\b",
    "backups": r"\b(data backups|restore.*data|backup and recovery)\b",
    "software_updates": r"\b(software updates|patches|new features release)\b",
    "api_access": r"\b(API access|API key|API usage limits)\b",
    "rate_limiting": r"\b(rate limit|throttle.*requests|request limits)\b",
    "beta_features": r"\b(beta features|early access|experimental features)\b",
    "system_integration": r"\b(system integration|third[- ]?party tools|external service)\b",
    "error_reporting": r"\b(report.*bug|error logs|feedback submission)\b",
    "sla": r"\b(Service Level Agreement|SLA|uptime guarantee)\b",
    "uptime": r"\b(uptime guarantee|downtime|service availability)\b",
    "data_export": r"\b(export.*data|download.*information|data portability)\b",
    "portability": r"\b(data portability|transfer.*data|move.*account)\b",
    "audit_rights": r"\b(audit rights|inspect.*records|compliance checks)\b",
    "accessibility": r"\b(accessibility standards|WCAG|inclusive design)\b",
    "localization": r"\b(localization|internationalization|language support)\b",
    "mobile_permissions": r"\b(mobile app permissions|camera access|location access)\b",
    "version_control": r"\b(version control|change log|revision history)\b"
}

def extract_info(text):
    doc = nlp(text)
    key_points = []

    # Named Entity Recognition
    for ent in doc.ents:
        if ent.label_ in ['GPE', 'ORG', 'PERSON', 'DATE']:
            key_points.append(f"{ent.label_}: {ent.text}")

    # Regex pattern detection
    for label, pattern in regex_patterns.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                match = ' '.join([m for m in match if m])
            key_points.append(f"{label.upper()}: {match.strip()}")

    return key_points

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Invalid request"}), 400

    text = data['text']
    key_points = extract_info(text)

    summary = f"This page contains {len(key_points)} key information points."
    return jsonify({
        "summary": summary,
        "key_points": key_points
    })

if __name__ == '__main__':
    app.run(debug=True)
