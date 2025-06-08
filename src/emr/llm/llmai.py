import os
import sqlite3
from dotenv import load_dotenv
from groq import Groq
from google import genai
from google.genai import types
load_dotenv()
groq_key=os.environ.get("Groq_API_KEY")
google_key=os.environ.get("Google_API_KEY")


def llm_generic_text_to_text(system_prompt,user_prompt,model,stream=False,max_token=400):
     res_content="Select description from todoapp_todo where is_completed=true "
     try:
      if "google" in model:
       model=model.split("@")[0]
     
       client = genai.Client(api_key=google_key)
       s_prompt="you are a cat. your name is Neko"
       response = client.models.generate_content(  
               model=model,
               contents=[user_prompt],
               config=types.GenerateContentConfig(
               system_instruction=system_prompt,
               max_output_tokens=500,
               temperature=0.1
                 ))

       return response.text
      if "groq" in model:
          model=model.split("@")[0]
          #the prompt for diagnosis ,but we will add for plan as well
          client = Groq( api_key=groq_key)
          completion = client.chat.completions.create(
                model=model,
                messages=[
        {
            "role": "system",
            "content": system_prompt
              },
        {
            "role": "user", 
            "content": user_prompt
        }
                 ],
              max_completion_tokens=max_token,
               stream=stream,
    
                  )
          res_content= completion.choices[0].message.content
     except Exception as ex:
          res_content=f"try again , exception occured {ex}"
     return res_content     



def llm_generic_image_to_text(image_type,image_base64,system_prompt,user_prompt,model,stream=False,max_token=400):
     res_content="No response "
     try:
      if "google" in model:
       model=model.split("@")[0]
     
       client = genai.Client(api_key=google_key)
       
       response = client.models.generate_content(  
               model=model,
               contents=[user_prompt],
               config=types.GenerateContentConfig(
               system_instruction="You are a cat. Your name is Neko.",
               max_output_tokens=500,
               temperature=0.1
                 ))

       return response.text
      if "groq" in model:
          model=model.split("@")[0]
          #the prompt for diagnosis ,but we will add for plan as well
          client = Groq( api_key=groq_key)

          completion = client.chat.completions.create(
           model=model,
           messages=[
                {
                       "role": "system",
                      "content":system_prompt
                          },
                 {
                      "role": "user",
                  "content": [
                        {
                          "type": "text",
                          "text": user_prompt
                         },
                         {
                             "type": "image_url",
                             "image_url": {
                              "url":f"data:image/{image_type};base64,{image_base64}"
                    
                          }
                            }
                             ]
                             }
                            ],
               temperature=1,
               max_completion_tokens=max_token,
               top_p=1,
               stream=False, stop=None,)





          res_content= completion.choices[0].message.content
     except Exception as ex:
          res_content=f"try again , exception occured {ex}"
     return res_content     









def _imaging_analysis(img_type,img_base64,model,user_prompt):
  system_prompt ="""
     
     You are a highly knowledgeable and safety-focused medical assistant AI. Your role is to assist healthcare professionals in analyzing and interpreting medical images (such as X-rays, MRIs, CT scans, and ultrasound images).

    You must:
      - Accept and analyze medical images, detecting features like abnormalities, lesions, fractures, densities, or unusual patterns.
      - Reference typical imaging markers, anatomical structures, and known visual indicators of common diseases.
      - Combine image findings with textual context (e.g., patient symptoms, history, lab results) to provide reasoned differential diagnoses or clinical suggestions.
      - Use appropriate medical terminology clearly and accurately.
      - Always state your confidence level and acknowledge when findings are uncertain or require human specialist review.

    You must never:
     - Recommend treatment without clinical confirmation.
     - Assume a conclusion without sufficient visual or textual evidence.
 
    Always include:
    - A structured explanation of findings (e.g., "Findings", "Impression", "Suggested Next Steps").
     - Suggestions for follow-up, such as "Further imaging may be required", or "Referral to radiology/pathology".

     
     """


  return llm_generic_image_to_text(image_type=img_type,image_base64=img_base64,model=model,system_prompt=system_prompt,user_prompt=user_prompt)


def _db_data_manipulate(model,user_prompt):
     #text to sql
     sql_command=text_to_sql(model,user_prompt)
     #execute sql command
     raw_sql=_execute_db_command(sql_command,"db.sqlite3","read")
     #sql to text
     raw_sql= f"Input SQL:{sql_command} "+ raw_sql
     print(raw_sql)
     formatted_response=sql_to_text(model,user_prompt=raw_sql)
     
     return formatted_response
#convert user input to sql query/command
def text_to_sql(model,user_prompt):
     system_prompt="""
    
You are an AI that converts natural language into SQL queries.The sql should be funtional for sqllite. Use the schema below:

Tables:

emr_patient

id, first_name, last_name, phone_number, email, gender, created_at, address

emr_medicalrecord

id, chief_complaint, patient_id, service_date, mr_code, created_at, updated_at

patient_id is a foreign key referencing emr_patient.id

Rules:
The sql command shoudnot have '''sql or ''' in beginning  and ''' in the end. the result should be pure sql command only.
Return only SQL queries, no explanations.

Default patient info: first_name, last_name, phone_number

Use correct JOINs when needed.

Use aggregates like COUNT(*) when asked.

Filter with WHERE, GROUP BY, and date ranges when relevant.

Example 1:
User Prompt-
Get all patient data

SQL-
SELECT first_name, last_name, phone_number FROM emr_patient;
Example 2:
User Prompt-
How many entries of records are present in medical records?

SQL-
SELECT COUNT(*) FROM emr_medicalrecord;

Example 3:

User Prompt-
List the emails of all female patients

SQL-
SELECT email FROM emr_patient WHERE gender = 'female';


Example 4:
User Prompt-
Get medical record count for each patient
SQL-
SELECT p.first_name, p.last_name, COUNT(m.id) AS record_count FROM emr_patient p JOIN emr_medicalrecord m ON m.patient_id = p.id GROUP BY p.id, p.first_name, p.last_name;

Example 5:
User Prompt-
Find all records from January 2024

SQL-
SELECT * FROM emr_medicalrecord WHERE service_date BETWEEN '2024-01-01' AND '2024-01-31';


Example 6:

User Prompt-
Phone numbers of patients with records after May 2023

SQL-
SELECT DISTINCT p.phone_number FROM emr_patient p JOIN emr_medicalrecord m ON m.patient_id = p.id WHERE m.service_date > '2023-05-01';


"""
     llm_response=llm_generic_text_to_text(system_prompt=system_prompt,model=model,user_prompt=user_prompt)
     return llm_response

#convert  sql output to text
def sql_to_text(model,user_prompt):
     model=model
     system_prompt="""
You are a helpful medical data assistant. You will receive:

The user's original prompt in natural language as an input sql

A SQL result consisting of list of column names returned by the SQL query

and A list of row data corresponding to those columns

Your job is to:

Convert the SQL result into a clear and human-readable explanation

Display the data as a well-formatted table (markdown format)

If the result is empty, respond with: “No records were found for that query.”

Be concise, accurate, and structured. Do not include the raw SQL in your response.

Example Input:

Input Sql:
"fetch all patient records"
Result:
Column Names: ['first_name', 'last_name', 'phone_number']
Data Rows:
('Brielle', 'Lott', '+1 (226) 935-9282')
('Karina', 'Mcdonald', '+1 (849) 485-8906')
('Raven', 'Fischer', '+1 (192) 624-9004')

Expected Output:

➡️ "Here are the patient records retrieved:"

First Name	Last Name	Phone Number
Brielle	Lott	+1 (226) 935-9282
Karina	Mcdonald	+1 (849) 485-8906
Raven	Fischer	+1 (192) 624-9004
Examples:

Input SQL:
SELECT COUNT(*) FROM emr_medicalrecord;
Result:
[(15,)]
Output:
➡️ "There are 15 medical records in the database."

Input SQL:
SELECT first_name, phone_number FROM emr_patient WHERE gender = 'female';
Result:
[{'first_name': 'Amina', 'phone_number': '12345'}, {'first_name': 'Fatima', 'phone_number': '67890'}]
Output:
➡️ "List of female patients:"

First Name	Phone Number
Amina	12345
Fatima	67890

            """
     llm_response=llm_generic_text_to_text(system_prompt=system_prompt,model=model,user_prompt=user_prompt)
     return llm_response
 

def _speech_recognition(model,audio):
      pass
def _generate_image():
      pass
def _text_generation(model,user_prompt,history=None):
      system_prompt="you are mean helpfull assistant,act like a mean person"
      if history:
          system_prompt+="You are a helpful assistant. You will receive a user prompt and a history of previous interactions. Your task is to generate a response based on the current user prompt and the provided history."
          for item in history:
                 system_prompt += f"\nUser: {item['content']}" if item['role'] == 'user' else f"\nAssistant: {item['content']}"
      print(system_prompt)   
      llm_response=llm_generic_text_to_text(system_prompt=system_prompt,model=model,user_prompt=user_prompt)
      return llm_response
      
def _execute_db_command(sql_command,db,command_type):
     res=""
     try:
      if command_type=="read":
        conn=sqlite3.connect(db)
       # df=pd.read_sql_query(sql_command,conn)
    
        curr=conn.cursor()
        data=curr.execute(sql_command)
        names = [description[0] for description in data.description]
        print(names)
        rows=curr.fetchall()
        col_names=f"column name list:{names}"
        raw_sql="raw sql data:"
        conn.commit()
        conn.close()
        for row in rows:
             raw_sql+=str(row)+"\n"
             print(raw_sql)

        res=  col_names+""+raw_sql   
        return res
     except Exception as ex:
         res=f"exceptio of {ex} occured"
         return res 
     

     