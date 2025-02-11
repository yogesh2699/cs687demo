import os
from dotenv import load_dotenv
import sys
import json
from typing import Dict, Any
from src.config import get_workdir


load_dotenv()
WORKDIR = get_workdir()

from langchain_core.tools import tool
from src.validators.agent_validators import *
from typing import  Literal
import pandas as pd
import json
from src.vector_database.main import PineconeManagment
from src.utils import format_retrieved_docs

pinecone_conn = PineconeManagment()
pinecone_conn.loading_vdb(index_name = 'ovidedentalclinic')
retriever = pinecone_conn.vdb.as_retriever(search_type="similarity", 
                                    search_kwargs={"k": 2})
rag_chain = retriever | format_retrieved_docs

#All the tools to consider
@tool
def check_availability_by_doctor(desired_date:DateModel, doctor_name:Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe']):
    """
    Checking the database if we have availability for the specific doctor.
    The parameters should be mentioned by the user in the query
    """
    #Dummy data
    df = pd.read_csv(f"{WORKDIR}/data/syntetic_data/availability.csv")
    df['date_slot_time'] = df['date_slot'].apply(lambda input: input.split(' ')[-1])
    rows = list(df[(df['date_slot'].apply(lambda input: input.split(' ')[0]) == desired_date.date)&(df['doctor_name'] == doctor_name)&(df['is_available'] == True)]['date_slot_time'])

    if len(rows) == 0:
        output = "No availability in the entire day"
    else:
        output = f'This availability for {desired_date.date}\n'
        output += "Available slots: " + ', '.join(rows)

    return output


def check_availability_by_specialization(desired_date:DateModel, specialization:Literal["general_dentist", "cosmetic_dentist", "prosthodontist", "pediatric_dentist","emergency_dentist","oral_surgeon","orthodontist"]):
    """
    Checking the database if we have availability for the specific specialization.
    The parameters should be mentioned by the user in the query
    """
    #Dummy data
    df = pd.read_csv(f"{WORKDIR}/data/syntetic_data/availability.csv")
    df['date_slot_time'] = df['date_slot'].apply(lambda input: input.split(' ')[-1])
    rows = df[(df['date_slot'].apply(lambda input: input.split(' ')[0]) == desired_date.date) & (df['specialization'] == specialization) & (df['is_available'] == True)].groupby(['specialization', 'doctor_name'])['date_slot_time'].apply(list).reset_index(name='available_slots')

    if len(rows) == 0:
        output = "No availability in the entire day"
    else:
        output = f'This availability for {desired_date.date}\n'
        for row in rows.values:
            output += row[1] + ". Available slots: " + ', '.join(row[2])+'\n'

    return output

@tool
def reschedule_appointment(old_date:DateTimeModel, new_date:DateTimeModel, id_number:IdentificationNumberModel, doctor_name:Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe']):
    """
    Rescheduling an appointment.
    The parameters MUST be mentioned by the user in the query.
    """
    #Dummy data
    df = pd.read_csv(f'{WORKDIR}/data/syntetic_data/availability.csv')
    available_for_desired_date = df[(df['date_slot'] == new_date.date)&(df['is_available'] == True)&(df['doctor_name'] == doctor_name)]
    if len(available_for_desired_date) == 0:
        return "Not available slots in the desired period"
    else:
        cancel_appointment.invoke({'date':old_date, 'id_number':id_number, 'doctor_name':doctor_name})
        set_appointment.invoke({'desired_date':new_date, 'id_number': id_number, 'doctor_name': doctor_name})
        return "Succesfully rescheduled for the desired time"

@tool
def cancel_appointment(date:DateTimeModel, id_number:IdentificationNumberModel, doctor_name:Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe']):
    """
    Canceling an appointment.
    The parameters MUST be mentioned by the user in the query.
    """
    df = pd.read_csv(f'{WORKDIR}/data/syntetic_data/availability.csv')
    case_to_remove = df[(df['date_slot'] == date.date)&(df['patient_to_attend'] == id_number.id)&(df['doctor_name'] == doctor_name)]
    if len(case_to_remove) == 0:
        return "You don´t have any appointment with that specifications"
    else:
        df.loc[(df['date_slot'] == date.date) & (df['patient_to_attend'] == id_number.id) & (df['doctor_name'] == doctor_name), ['is_available', 'patient_to_attend']] = [True, None]
        df.to_csv(f'{WORKDIR}/data/syntetic_data/availability.csv', index = False)

        return "Succesfully cancelled"

@tool
def get_catalog_specialists():
    """
    Obtain information about the doctors and specializations/services we provide.
    The parameters MUST be mentioned by the user in the query
    """
    with open(f"{WORKDIR}/data/catalog.json","r") as file:
        file = json.loads(file.read())
    
    return file

@tool
def set_appointment(desired_date:DateTimeModel, id_number:IdentificationNumberModel, doctor_name:Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe']):
    """
    Set appointment with the doctor.
    The parameters MUST be mentioned by the user in the query.
    """
    df = pd.read_csv(f'{WORKDIR}/data/syntetic_data/availability.csv')
    case = df[(df['date_slot'] == desired_date.date)&(df['doctor_name'] == doctor_name)&(df['is_available'] == True)]
    if len(case) == 0:
        return "No available appointments for that particular case"
    else:
        df.loc[(df['date_slot'] == desired_date.date)&(df['doctor_name'] == doctor_name) & (df['is_available'] == True), ['is_available','patient_to_attend']] = [False, id_number.id]

        df.to_csv(f'{WORKDIR}/data/syntetic_data/availability.csv', index = False)

        return "Succesfully done"

@tool
def check_results(id_number:IdentificationNumberModel):
    """
    Check if the result of the pacient is available.
    The parameters MUST be mentioned by the user in the query
    """
    #Dummy data
    df = pd.read_csv(f'{WORKDIR}/data/syntetic_data/studies_status.csv')
    rows = df[(df['patient_id'] == id_number.id)][['medical_study','is_available']]
    if len(rows) == 0:
        return "The patient doesn´t have any study made"
    else:
        return rows

@tool
def reminder_appointment(id_number: IdentificationNumberModel):
    """
    Returns when the patient has its appointment with the doctor
    The parameters MUST be mentioned by the user in the query
    """
    df = pd.read_csv(f'{WORKDIR}/data/syntetic_data/availability.csv')
    
    # Print column names for debugging
    print("Columns in the DataFrame:", df.columns)
    
    # Check if 'patient_to_attend' column exists
    if 'patient_to_attend' not in df.columns:
        return "Error: 'patient_to_attend' column not found in the data"
    
    # Assuming 'date_slot' is the correct column name instead of 'time_slot'
    columns_to_select = ['date_slot', 'doctor_name', 'specialization']
    columns_to_select = [col for col in columns_to_select if col in df.columns]
    
    rows = df[df['patient_to_attend'] == id_number.id][columns_to_select]
    
    if len(rows) == 0:
        return "The patient doesn't have any appointment yet"
    else:
        return rows.to_dict(orient='records')


@tool
def retrieve_faq_info(question: str):
    """
    Retrieve documents or additional info from general questions about the medical clinic.
    Call this tool if question is regarding center:
    For example: is it open? Do you have parking? Can I go with bike? etc...

    Args:
    question (str): The question to search for in the FAQ database.

    Returns:
    str: The retrieved answer from the FAQ database.
    """
    try:
        results = rag_chain.invoke(question)
        
        # Parse the JSON results
        parsed_results = [json.loads(r) for r in results.split('\n') if r.strip()]
        
        # Sort results by relevance (you might need to implement a relevance scoring method)
        sorted_results = sorted(parsed_results, key=lambda x: relevance_score(x, question), reverse=True)
        
        if sorted_results:
            best_match = sorted_results[0]
            return json.dumps({
                "question": best_match["question"],
                "answer": best_match["answer"],
                "confidence": relevance_score(best_match, question)
            })
        else:
            return json.dumps({
                "question": question,
                "answer": "I'm sorry, I don't have specific information about that. Please contact our office for more details.",
                "confidence": 0
            })
    except Exception as e:
        print(f"Error in retrieve_faq_info: {str(e)}")
        return json.dumps({
            "question": question,
            "answer": "I'm sorry, there was an error processing your question. Please try again or contact our office directly.",
            "confidence": 0
        })

def relevance_score(result: Dict[str, str], query: str) -> float:
    return float(query.lower() in result["question"].lower())

@tool
def obtain_specialization_by_doctor(doctor_name:Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe']):
    """
    Retrieve which specialization covers a specific doctor.
    Use this internal tool if you need more information about a doctor for setting an appointment.
    """
    with open(f"{WORKDIR}/data/catalog.json","r") as file:
        catalog = json.loads(file.read())

    return str([{specialization['specialization']: [dentist['name'] for dentist in specialization['dentists']]} for specialization in catalog])
    