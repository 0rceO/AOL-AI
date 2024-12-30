from flask import Flask, render_template, request

app = Flask(__name__)

SYMPTOM_DISEASE_MAP = {
    "fever": {"Flu": 3, "COVID-19": 5, "Dengue": 4, "Typhoid": 3},
    "cough": {"Flu": 4, "COVID-19": 5, "Bronchitis": 4, "Tuberculosis": 3},
    "headache": {"Migraine": 5, "Flu": 2, "Sinusitis": 3, "Tension Headache": 4},
    "fatigue": {"Anemia": 5, "COVID-19": 4, "Diabetes": 3, "Hypothyroidism": 3},
    "sore throat": {"Flu": 3, "COVID-19": 5, "Strep Throat": 4, "Tonsillitis": 3},
    "chest pain": {"Heart Attack": 5, "Pneumonia": 4, "Bronchitis": 3, "Angina": 5},
    "shortness of breath": {"Asthma": 4, "COVID-19": 5, "Pneumonia": 5, "COPD": 4},
    "nausea": {"Food Poisoning": 4, "Gastritis": 4, "Pregnancy": 3, "Dengue": 3},
    "vomiting": {"Food Poisoning": 5, "Gastritis": 4, "Appendicitis": 4, "Dengue": 4},
    "diarrhea": {"Food Poisoning": 5, "Cholera": 5, "IBS": 3, "Dysentery": 4},
    "rash": {"Allergic Reaction": 4, "Chickenpox": 5, "Measles": 4, "Scabies": 3},
    "joint pain": {"Arthritis": 5, "Dengue": 4, "Lupus": 4, "Gout": 4},
    "abdominal pain": {"Appendicitis": 5, "Gastritis": 4, "Gallstones": 4, "IBS": 3},
    "weight loss": {"Diabetes": 5, "Hyperthyroidism": 4, "Cancer": 5, "Malnutrition": 3},
    "frequent urination": {"Diabetes": 5, "UTI": 4, "Prostate Enlargement": 3},
    "blurred vision": {"Diabetes": 4, "Cataracts": 5, "Glaucoma": 5, "Migraine": 3},
    "chills": {"Malaria": 4, "Dengue": 4, "Flu": 3, "Pneumonia": 4},
    "back pain": {"Kidney Stones": 5, "Muscle Strain": 4, "Sciatica": 4, "Osteoporosis": 3},
}

DISEASE_DOCTOR_MAP = {
    "Flu": "General Practitioner",
    "COVID-19": "Infectious Disease Specialist",
    "Dengue": "Infectious Disease Specialist",
    "Typhoid": "General Practitioner",
    "Bronchitis": "Pulmonologist",
    "Tuberculosis": "Pulmonologist",
    "Migraine": "Neurologist",
    "Sinusitis": "ENT Specialist",
    "Tension Headache": "Neurologist",
    "Anemia": "Hematologist",
    "Diabetes": "Endocrinologist",
    "Hypothyroidism": "Endocrinologist",
    "Strep Throat": "ENT Specialist",
    "Tonsillitis": "ENT Specialist",
    "Heart Attack": "Cardiologist",
    "Pneumonia": "Pulmonologist",
    "Asthma": "Pulmonologist",
    "COPD": "Pulmonologist",
    "Food Poisoning": "Gastroenterologist",
    "Gastritis": "Gastroenterologist",
    "Pregnancy": "Obstetrician",
    "Appendicitis": "Surgeon",
    "Cholera": "Infectious Disease Specialist",
    "IBS": "Gastroenterologist",
    "Dysentery": "Infectious Disease Specialist",
    "Allergic Reaction": "Allergist",
    "Chickenpox": "Dermatologist",
    "Measles": "Infectious Disease Specialist",
    "Scabies": "Dermatologist",
    "Arthritis": "Rheumatologist",
    "Lupus": "Rheumatologist",
    "Gout": "Rheumatologist",
    "Gallstones": "Gastroenterologist",
    "Cancer": "Oncologist",
    "Malnutrition": "Nutritionist",
    "UTI": "Urologist",
    "Prostate Enlargement": "Urologist",
    "Cataracts": "Ophthalmologist",
    "Glaucoma": "Ophthalmologist",
    "Malaria": "Infectious Disease Specialist",
    "Kidney Stones": "Urologist",
    "Muscle Strain": "Orthopedist",
    "Sciatica": "Orthopedist",
    "Osteoporosis": "Endocrinologist",
}

def diagnose_symptoms(symptoms):
    disease_scores = {}

    for symptom in symptoms:
        symptom = symptom.lower().strip()
        if symptom in SYMPTOM_DISEASE_MAP:
            for disease, weight in SYMPTOM_DISEASE_MAP[symptom].items():
                disease_scores[disease] = disease_scores.get(disease, 0) + weight

    sorted_diseases = sorted(disease_scores.items(), key=lambda x: x[1], reverse=True)

    total_score = sum(disease_scores.values())
    if total_score > 0:
        sorted_diseases = [(disease, round(score / total_score * 100, 2)) for disease, score in sorted_diseases]

    return sorted_diseases[:3]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        symptoms_input = request.form.get("symptoms")
        symptoms = symptoms_input.split(",")
        conditions = diagnose_symptoms(symptoms)
        return render_template("index.html", conditions=conditions, disease_doctor_map=DISEASE_DOCTOR_MAP)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
