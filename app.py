import streamlit as st
from datetime import datetime, timedelta
import time
import pickle
import numpy as np
import os
from datetime import date, timedelta
import joblib
import pandas as pd
from sqlalchemy import create_engine
print("packages loaded successfully :)")


# Set the page layout to wide
st.set_page_config(layout="wide")

min_date = datetime(1900,1,1)
max_date = datetime.now()


# Custom CSS to change label color
st.markdown(
    """
    <style>
    /* Change the font color of all input field labels */
    label {
        color: #c07a7a !important;  /* Change to desired color */
        font-weight: bold;  /* Make it bold (optional) */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Custom CSS for toast notification effect
st.markdown(
    """
    <style>
    .toast {
        background-color: #c07a7a;
        color: white;
        padding: 15px;
        border-radius: 10px;
        position: fixed;
        bottom: 10px;
        left: 50%;
        transform: translateX(-50%);
        animation: slideUp 2s ease-out, fadeOut 2s ease-out 3s forwards;
    }

    @keyframes slideUp {
        from { bottom: -100px; opacity: 0; }
        to { bottom: 10px; opacity: 1; }
    }

    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; display: none; }
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Initialize session state for notification visibility
if "show_notification" not in st.session_state:
    st.session_state.show_notification = False


st.sidebar.title("Info")
st.sidebar.write("Group No. 4 PG-DBDA project")
st.sidebar.write("[Tableau Visualizations](https://public.tableau.com/app/profile/akash.vishwakarma5526/viz/lung-cancer-extra-tree-classifier/AgeDistributionBySurvivalStatus?publish=yes)")


# st.title("Lung Cancer Survival Prediction")

st.markdown("<h1 style='color: #c07a7a;'>Lung Cancer Survival Prediction</h1>", unsafe_allow_html=True)


# User Form
with st.form(key = "user_info_form"):

    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input("Name : ",  placeholder="Enter your name here")
        age = st.text_input("Age : ",  placeholder="Enter your age here")
        bmi = st.text_input("BMI : ",  placeholder="Enter your BMI here")
        cholesterol = st.text_input("Cholesterol level : ",  placeholder="Enter cholestrol level")
        gender = st.selectbox("Gender", ["Male", "Female"])
        family_history = st.selectbox("Family History :", ["Yes", "No"])
    
    with col2:
        smoking_status = st.selectbox("Smoking Status :",  ['Never Smoked','Former Smoker','Passive Smoker','Current Smoker'])
        treatement_type = st.selectbox("Treatement Type :", ['Surgery','Radiation','Chemotherapy','Combined'])
        diagnosis_date = st.date_input("Enter Date of Diagnosis", value = datetime.now(), min_value = min_date, max_value = max_date)
        begining_of_treatment_date = st.date_input("Begining of treatement date : ", value = datetime.now(), min_value = min_date, max_value = max_date)
        end_treatment_date = st.date_input("End of treatement date : ", value = datetime.now(), min_value = min_date, max_value = max_date)
        cancer_stage = st.selectbox("Cancer Stage", ["I", "II", "III", "IV"])

    with col3:
        hypertension = st.radio("Hypertension", ["Yes", "No"])
        st.markdown("<br>", unsafe_allow_html=True)  # Adds one line break
        asthma = st.radio("Asthma", ["Yes", "No"])
        st.markdown("<br>", unsafe_allow_html=True)  # Adds one line break
        cirrhosis = st.radio("Cirrhosis", ["Yes", "No"])
        st.markdown("<br>", unsafe_allow_html=True)  # Adds one line break
        other_cancer = st.radio("Other Cancer", ["Yes", "No"])
        
        st.markdown("<br>", unsafe_allow_html=True)  # Adds one line break
        st.markdown("<br>", unsafe_allow_html=True)  # Adds one line break
        st.markdown("<br>", unsafe_allow_html=True)  # Adds one line break
    submit_button = st.form_submit_button("Submit")

# Mapping (Categorical to Numerical)

if smoking_status == 'Never Smoked':
    smoking_status = 0
if smoking_status == 'Former Smoker':
    smoking_status = 1
if smoking_status == 'Passive Smoker':
    smoking_status = 2
if smoking_status == 'Current Smoker':
    smoking_status = 3
    
if gender == 'Male':
    gender = 1
if gender == 'Female':
    gender = 0

if family_history == "Yes":
    family_history = 1
if family_history == "No":
    family_history = 0
    
if treatement_type == 'Surgery':
    treatement_type = 0
if treatement_type == 'Radiation':
    treatement_type = 1
if treatement_type == 'Chemotherapy':
    treatement_type = 2
if treatement_type == 'Combined':
    treatement_type = 3

if cancer_stage == 'I':
    cancer_stage = 0
if cancer_stage == 'II':
    cancer_stage = 1
if cancer_stage == 'III':
    cancer_stage = 2
if cancer_stage == 'IV':
    cancer_stage = 3
    
if hypertension == 'Yes':
    hypertension = 1
if hypertension == 'No':
    hypertension = 0

if asthma == 'Yes':
    asthma = 1
if asthma == 'No':
    asthma = 0
    
if cirrhosis == 'Yes':
    cirrhosis = 1
if cirrhosis == 'No':
    cirrhosis = 0

if other_cancer == 'Yes':
    other_cancer = 1
if other_cancer == 'No':
    other_cancer = 0



print(type(smoking_status))
print(smoking_status)


# stage1 = 0
# stage2 = 1
# stage3 = 2
# stage4 = 3

# never smoke=0
#former =1
#passive = 2
#current = 3

# surgery=0
# radia = 1
# chemo = 2
# combined = 3

# gender
# male = 1
# female = 0

# family history
#no = 0
#yes = 1


# if submit_button:
#     st.write("Submitted Successfully...")
a = 0
if submit_button:

    a = 1
    st.session_state.show_notification = True
    st.rerun()  # Rerun the app to display the notification

# Display toast only if the form was submitted
if st.session_state.show_notification:
    st.markdown(
        f"""
        <div class="toast">
            <strong>Your form has been successfully submitted ✔️</strong> {name}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Wait for 3 seconds, then clear the notification and rerun the app
    time.sleep(3)
    st.session_state.show_notification = False
    st.rerun()

    st.toast("✅ Form submitted successfully!", icon="✅")  # Auto-disappears


st.divider()
print(name, age, bmi, cholesterol, gender, family_history, cancer_stage, hypertension, asthma, cirrhosis, other_cancer, smoking_status, treatement_type, diagnosis_date, begining_of_treatment_date)
treatment_delay_days = (begining_of_treatment_date - diagnosis_date).days
treatment_duration_days = (end_treatment_date - begining_of_treatment_date).days
print("treatement_delay_days",treatment_delay_days)
print("treatement_duration_days",treatment_duration_days)
print(type(treatment_delay_days))
print(type(treatment_duration_days))

# from connector import display
# display(name)
# st.write(name)




# # Load the trained model
# with open("trained_model.pkl", "rb") as file:
#     model = pickle.load(file)
#     # scaler = pickle.load(file)
# print("inside the model")


# Load the trained model
# Load the model
model = "Lung Cancer_model (2).sav"
@st.cache_resource
def load_model():
    return joblib.load(model)

model = load_model()



# Prepare input data for prediction

# input_data = np.array([[age, cancer_stage,smoking_status, cholesterol,hypertension, asthma, cirrhosis,other_cancer, treatement_type, gender, family_history, treatment_delay_days, treatment_delay_days]]) 
received_array = np.array([[age, cancer_stage,smoking_status, bmi, cholesterol,hypertension, asthma, cirrhosis,other_cancer, treatement_type, gender, family_history, treatment_delay_days, treatment_delay_days]], dtype=object)
# Convert to numeric (float or int)
# numeric_array = input_data.astype(int)  # Change to int if needed
# input_data = np.array([[int(age), int(cancer_stage),int(smoking_status), int(cholesterol),int(hypertension), int(asthma), int(cirrhosis),int(other_cancer), int(treatement_type), int(gender), int(family_history), int(treatment_delay_days), int(treatment_delay_days)]]) 
# print(numeric_array)
print("After input data")

# Predict and show results
    
    # Scale input data before predicting

# input_data_scaled = scaler.transform(input_data)
# prediction = model.predict(input_data_scaled)

    # Make predictions using the model
# if submit_button:



if st.button("Predict"):
    prediction = model.predict(received_array)  
    result = prediction[0]
    if prediction[0] == 1:
        st.success("✅ The model predicts a HIGH chance of survival!")
        result = "SURVIVED"
    else:
        st.error("⚠️ The model predicts a LOW chance of survival.")
        result = "NOT SURVIVED"
    print(prediction[0])
    
    
    #Dumping output
    
    data_dict = {
    "name": [name],  
    "age": [age],    
    "bmi": [bmi],
    "cholesterol":[cholesterol],
    "gender":[gender],
    "family_history":[family_history],
    "treatement_type":[smoking_status],
    "diagnosis_date":[diagnosis_date],
    "begining_of_treatement": [begining_of_treatment_date],
    "end_treatment_date" :[end_treatment_date],
    "cancer_stage": [cancer_stage] ,
    "hypertension":[hypertension],
    "asthma":[asthma],
    "cirrhosis":[cirrhosis],
    "other_cancer":[other_cancer],
    "result": [result]
     
    }
    
    
# Step : Define MySQL Connection
    DATABASE_URI = "mysql+pymysql://root:manager@localhost:3306/project"
    engine = create_engine(DATABASE_URI)

    # df = pd.DataFrame(data_dict)
    df = pd.DataFrame(data_dict)
    df.to_sql(name="output1", con=engine, if_exists="append", index=False)
    print("Data inserted successfully....")
print("End")


