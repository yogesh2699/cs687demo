import os
from dotenv import load_dotenv
import sys
from src.config import get_workdir


load_dotenv()
WORKDIR = get_workdir()

# WORKDIR = os.getenv("WORKDIR")
# os.chdir(WORKDIR)
# sys.path.append(WORKDIR)

from src.agent_tools import retrieve_faq_info

def test_retrieve_faq_info():
    test_questions = [
        "Do you offer discounts for senior citizens or students?",
        "Do you have a website?",
        "What types of dental services do you provide?",
        "How can I schedule an appointment?",
        "Do you accept insurance?",
        "What COVID-19 precautions are in place?",
        "Is there a cancellation policy for appointments?",
        "Do you offer emergency dental services?",
        "Are your facilities wheelchair accessible?",
        "What languages do your staff speak?"
    ]

    for question in test_questions:
        print(f"\nQuestion: {question}")
        try:
            answer = retrieve_faq_info(question)
            print(f"Answer: {answer}")
        except Exception as e:
            print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    print("Testing retrieve_faq_info function...")
    test_retrieve_faq_info()
    print("\nTesting complete.")