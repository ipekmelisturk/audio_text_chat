import re
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def agent_1_suggest_questions(patient_input, previous_questions):
    """
    AI Agent 1: Suggests multiple questions for the doctor to ask the patient dynamically.
    Returns exactly 5 new, relevant questions per input.
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": 
                "You are a medical assistant. Generate 5 **NEW** follow-up questions to ask the patient based on their response."
                "Do **NOT** repeat previous questions. Keep the questions medical and relevant."
                "Format output as a numbered list without extra text."},
            {"role": "user", "content": f"Previous questions: {previous_questions}. Patient said: {patient_input}. What 5 follow-up questions should I ask next?"}
        ],
        max_tokens=200,
        temperature=0.7
    )

    # Extract response text and clean it
    questions = response.choices[0].message.content.strip().split("\n")

    # Ensure only questions are included (skip AI-generated headers)
    filtered_questions = [q.strip() for q in questions if q[0].isdigit()]

    return {"questions": filtered_questions}
    
def agent_2_diagnose(patient_input):
    """
    AI Agent 2: Provides 5 possible medical causes with percentage likelihood.
    Ensures structured output using regex.
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a medical AI that provides possible diagnoses along with likelihood percentages based on symptoms. "
                                          "Format each response as: Cause - Percentage%. Provide exactly 5 causes."},
            {"role": "user", "content": f"The patient reports: {patient_input}. What are the possible causes with probability percentages?"}
        ],
        max_tokens=300,
        temperature=0.7
    )
    
    # Extracting response text
    response_text = response.choices[0].message.content.strip()
    causes_list = response_text.split("\n")

    # Use regex to extract properly formatted cause - percentage% pairs
    causes = []
    for cause in causes_list:
        match = re.match(r"^\d*\.*\s*(.+?)\s*-\s*(\d+)%", cause)  # Removes numbering
        if match:
            causes.append({"name": match.group(1).strip(), "percentage": int(match.group(2))})

    return causes[:5] if len(causes) >= 5 else []