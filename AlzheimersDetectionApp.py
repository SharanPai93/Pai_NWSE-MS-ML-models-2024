import streamlit as st
import time
from streamlit import session_state as ss
from country_list import countries_for_language
import pandas as pd
import altair as alt
import pickle
from sklearn.preprocessing import StandardScaler
import numpy as np
from functions import *


#Pages and Descriptions
pages = ['Glossary',
         'Phase 1',
         'Phase 2',
         'Phase 3',
         'Results']

pages_sidebar = {'Glossary':'Definitions of Key Vocabulary',
                 'Phase 1':'Basic Information',
                 'Phase 2':'Genetic Information',
                 'Phase 3':'Environmental Information',
                 'Results':'Results Page'}

pages_titles = {'Glossary':'Glossary ➟ Definitions',
                'Phase 1':'Alzheimer\'s Prediction Tool ➟ Phase 1',
                'Phase 2':'Alzheimer\'s Prediction Tool ➟ Phase 2',
                'Phase 3':'Alzheimer\'s Prediction Tool ➟ Phase 3',
                'Results':'Alzheimer\'s Prediction Tool ➟ Results'}

page = st.sidebar.selectbox(label="Choose Section",
                            options=pages)

#Global/Session variables and functions
def Vars():
    if "age" not in ss:
        ss['age'] = 65

    if "gender" not in ss:
        ss['gender'] = ""

    if "education" not in ss:
        ss['education'] = 16

    if 'heartRate' not in ss:
        ss['heartRate'] = 33

    if 'systolicBP' not in ss:
        ss['systolicBP'] = 70

    if 'diastolicBP' not in ss:
        ss['diastolicBP'] = 30

    if 'hypertension' not in ss:
        ss['hypertension'] = None

    if 'diabetes' not in ss:
        ss['diabetes'] = None

    if 'lipid' not in ss:
        ss['lipid'] = None

    if 'depression' not in ss:
        ss['depression'] = None

    if 'antiFlam' not in ss:
        ss['antiFlam'] = None

    if 'animalQuestion' not in ss:
        ss['animalQuestion'] = None

    if 'animalRecalls' not in ss:
        ss['animalRecalls'] = 0

    if 'anyMeds' not in ss:
        ss['anyMeds'] = None

    if 'gene' not in ss:
        ss['gene'] = None

    if 'aqiQuestion' not in ss:
        ss['aqiQuestion'] = None

    if 'country' not in ss:
        ss['country'] = None

    if 'countryTwoCode' not in ss:
        ss['countryTwoCode'] = None

    if 'zipcode' not in ss:
        ss['zipcode'] = None
    
    if 'aqi' not in ss:
        ss['aqi'] = None

def set_age():
    ss['age'] = ss['Age']

def set_education():
    ss['education'] = ss['education_level']

def set_HeartRate():
    ss['heartRate'] = ss["HeartRate_value"]

def set_SystolicBP():
    ss['systolicBP'] = ss["systolicBP_value"]

def set_DiastolicBP():
    ss['diastolicBP'] = ss["diastolicBP_value"]

#Model Algorithm
def Algorithm(Genetic,
              EnvironmentRisk,
              ModelPredict,
              DiseaseCount,
              GeneticRisk = None):
    '''
Genetic: bool --> if participant is a carrier of APOE e4 gene
EnvironmentalRisk: int --> AQI levels of given location classified into 0,1,2
ModelPredict: bool --> if model predicts disease or not
DiseaseCount: bool --> number of coexisting diseases
GeneticRisk: int --> double or single carrier of APOE e4 gene
    '''

    assert float(EnvironmentRisk).is_integer() and \
           float(DiseaseCount).is_integer() and \
           type(ModelPredict) == bool and \
           type(Genetic) == bool
    
    probability = 0

    if ModelPredict:
        probability += 0.5*DiseaseCount

    if Genetic:
        assert float(GeneticRisk).is_integer() and 0 <= GeneticRisk <= 2
        if GeneticRisk == 0: pass
        elif GeneticRisk == 1: probability += 2.5
        elif GeneticRisk == 2: probability += 10

    if EnvironmentRisk == 0: pass
    elif EnvironmentRisk == 1: probability += 0.02
    elif EnvironmentRisk == 2: probability += 0.04

    return probability

#First Page --> Glossary
#Also define global variables in sessions
if page == pages[0]:
    Vars()
    st.header(pages_titles[page],
              divider='gray')
    st.sidebar.write(f'**_{pages_sidebar[page]}_**')
    
    st.write("### *Education*")
    st.info("##### Education is taken as an input in years. For example, \
12 years of education would result in a high school diploma (or GRE), 16 years \
would result in a bachelor's degree, 18 years would result in a master's \
degree, and 20 years would result in a doctorate.", icon='ℹ')

    
    #st.write("### *Body Mass Index (BMI)*")
    #st.info("##### Body Mass Index is a measure of body fat based on height \
#and weight. It is calculated via the following formula:\n \
# ###### *B = (W * 703) ÷ (H ^ 2)*,\n ##### where B is the BMI, W is the Weight (Pounds), and H is the \
#Height (Inches)", icon='ℹ')
    
    
    st.write("### *Animal Recalls*")
    st.info("##### Animal Recalls is a test to determine how many animals \
you can think of in under a minute. This serves as an additional factor to \
increase the accuracy of the model's prediction.", icon='ℹ')

    st.write("### *APOE E4 Gene*")
    st.info("##### APOE4 is the strongest risk factor gene that plays a \
role in the chance to develop Alzheimer's disease. Although, having the gene \
(even from both parents) does not guarantee development of the disease, it is \
important to take it into account. This factor, however, is optional, \
in case you do not know whether you have it or not.", icon='ℹ')

    st.write("### *Environmental Factors*")
    st.info("##### Another important factor that can be taken into account \
would be environmental risk factors. Although moving to a different city might \
not always be possible, it is still important to know the Air Quality Index \
(AQI) of your city, to make choices accordingly.", icon='ℹ')

#Second Page --> Required/Basic Info
if page == pages[1]:
    Vars()
    st.header(pages_titles[page],
              divider='gray')
    st.sidebar.write(f'**_{pages_sidebar[page]}_**')

    lastValue = None
                
    #Section one
    st.write("### 1. Demographics")

    ss['age'] = st.slider("##### How old are you?",
                          18,
                          120,
                          value=ss['age'],
                          on_change=set_age,
                          key='Age')

    ss['gender'] = st.selectbox("##### Gender at birth:",
                                ['Male','Female'])

    if ss['gender'] == 'Male': ss['gender'] = 1
    elif ss['gender'] == 'Female': ss['gender'] = 2

    ss['education'] = st.slider("##### How many years of education do you have?",
                                0,
                                36,
                                ss['education'],
                                on_change = set_education,
                                key = 'education_level')

    #Section two
    st.write("### 2. Wellness and Illness Information")

    ss['heartRate'] = st.number_input("##### From your last Doctor visit, what was your \
measured Heart Rate?",
                                      min_value=33,
                                      max_value=160,
                                      step=1,
                                      value=ss['heartRate'],
                                      on_change=set_HeartRate,
                                      key="HeartRate_value")

    ss['systolicBP'] = st.number_input("##### From your last Doctor visit, what was your \
measured Systolic Blood Pressure?",
                                      min_value=70,
                                      max_value=230,
                                      step=1,
                                      value=ss['systolicBP'],
                                      on_change=set_SystolicBP,
                                      key="systolicBP_value")

    ss['diastolicBP'] = st.number_input("##### From your last Doctor visit, what was your \
measured Diastolic Blood Pressure?",
                                      min_value=30,
                                      max_value=140,
                                      step=1,
                                      value=ss['diastolicBP'],
                                      on_change=set_DiastolicBP,
                                      key="diastolicBP_value")

    st.write("### 3. Medications")

    

    ss['diabetes'] = st.radio("##### Do you take Diabetes Medication?",
                              ['Yes','No'],
                              None,
                              horizontal=True)

    ss['hypertension'] = st.radio("##### Do you take High Blood Pressure \
    (Hypertension) Medication?",
                                  ["Yes","No"],
                                  index=None,
                                  horizontal=True)

    

    ss['lipid'] = st.radio("##### Do you take High Cholesterol \
(Hypercholesterolemia\Lipid-lowering) Medication?",
                                     ["Yes","No"],
                                     index=None,
                                     horizontal=True)

    ss['depression'] = st.radio("##### Do you take Anti-Depressant Medications?",
                                ["Yes","No"],
                                index=None,
                                horizontal=True)

    ss['antiFlam'] = st.radio("##### Do you take any Anti-Inflammatory Medications?",
                              ['Yes','No'],
                              index=None,
                              horizontal=True)

    if ss['diabetes'] == "Yes" or \
       ss['hypertension'] == "Yes" or \
       ss['lipid'] == "Yes" or \
       ss['depression'] == "Yes" or \
       ss['antiFlam'] == "Yes":
        ss['anyMeds'] = "Yes"

    elif ss['diabetes'] == None or \
       ss['hypertension'] == None or \
       ss['lipid'] == None or \
       ss['depression'] == None or \
       ss['antiFlam'] == None:
        ss['anyMeds'] = None

    else:
        ss['anyMeds'] = st.radio("##### Do you take any Medications?",
                                 ["Yes","No"],
                                 index=None,
                                 horizontal=True)
       
        

    
    #Section Four
    st.write("### 4. Neurological Information")

    animalRadio = st.empty()

    ss['animalQuestion'] = animalRadio.radio("##### Have you been tested on Recall \
Memory?",
                                       ["Yes","No"],
                                       index=None,
                                       horizontal=True,
                                       key='first')

    if ss['animalQuestion'] == "Yes":
        ss['animalRecalls'] = st.slider("###### How many animals \
can you name in under a minute?",
                                        0,
                                        80,
                                        0)


    elif ss['animalQuestion'] == "No":
        st.write("Take a quick one minute test to see how many animals \
you can recall in a minute. Start the timer when you are ready! If available, \
have a friend check your answers.")

        #Create timer to time Memory Recalls
        start = st.button("Start/Reset Timer")
        if start:
            msg = st.toast("Readying Timer..")
            time.sleep(0.5)
            msg.toast("Starting in 3..")
            time.sleep(0.5)
            msg.toast("Starting in 2..")
            time.sleep(0.8)
            msg.toast("Starting in 1..Go!")
            time.sleep(0.5)
            ph = st.empty()
            N = 60
            for secs in range(N,0,-1):
                m, s = secs//60, secs%60
                ph.metric("List as many Animals as you can!",
                          f"{m:02d}:{s:02d}")
                time.sleep(1)
            lastValue = secs

        ss['animalRecalls'] = st.number_input("###### How many \
animal did you name in under a minute?",
                                              0,
                                              80,
                                              0)

#Third Page --> Genetic Information (APOE E4)
if page == pages[2]:
    Vars()
    st.header(pages_titles[page],
              divider='gray')
    st.sidebar.write(f'**_{pages_sidebar[page]}_**')
    
    #Section 1
    st.write("### Genetic Information (Optional)")
    
    ss['gene'] = st.radio("#### Do you have APOE E4 Gene?",
                    ["###### Not a Carrier",
                     "###### Single Carrier",
                    "###### Double Carrier",
                     "###### Unsure"],
                    index=None)

    if ss['gene'] != None:
        if "Unsure" in ss['gene']:
            st.write("###### *Consult a doctor or a genetic counselor about getting\
     tested. You can also order a kit online.*")

#Fourth Page --> Environmental Information (Zip code and Country)
if page == pages[3]:
    Vars()
       
    st.header(pages_titles[page],
              divider='gray')
    st.sidebar.write(f'**_{pages_sidebar[page]}_**')

    #Section 1
    st.write("### Environmental Factors (Optional)")

    countries = {i[1]: i[0] for i in countries_for_language('en')}
    countriesL = [i[1] for i in countries_for_language('en')]
    countriesL.insert(0,'Select Country')
    countries['Select Country'] = None

    if 'key' not in ss:
        ss['key'] = None

    if 'askKey' not in ss:
        ss['askKey'] = None

    apiUrl = 'https://developers.google.com/maps/documentation/embed/get-api-key'
    
    ss['askKey'] = st.radio(f"##### Do you have a Google Maps API Key? Find out how to get \
one [here]({apiUrl}).",
                            ["###### Yes",
                            "###### No"],
                            index=None)

    if ss['askKey'] != None:
        if 'No' in ss['askKey']:
            AQIurl = 'https://www.airnow.gov/'
            ss['aqi'] = st.number_input(f"##### Enter your Air Quality Index (AQI). You can find this out \
[here]({AQIurl}), or through a weather app on your phone.",
                                        0,
                                        200)
            ss['key'] = False

        elif 'Yes' in ss['askKey']:
            ss['key'] = True
            ss['Key'] = st.text_input("##### Please enter your Google API key.")
    

    if ss['key']:
        ss['country'] = st.selectbox("What country do you live in?",
                                     countriesL,
                                     placeholder='Select Country')
        
        ss['countryTwoCode'] = countries[str(ss['country'])]
        
        ss['zipcode'] = st.number_input("##### What is your zipcode?",
                                        value=ss['zipcode'],
                                        step=1,
                                        placeholder="Type zipcode here...")

#Results Page
if page == pages[4]:
    Vars()
    st.header(pages_titles[page],
              divider='gray')
    st.sidebar.write(f'**_{pages_sidebar[page]}_**')

    #Define function to check values to make sure participant is not missing anything
    #Write Error Messages accordingly
    def checkPage1():
        checkDiabetes = True if ss['diabetes'] != None else False
        checkHypertension = True if ss['hypertension'] != None else False
        checkLipid = True if ss['lipid'] != None else False
        checkDepression = True if ss['depression'] != None else False
        checkAntiFlam = True if ss['antiFlam'] != None else False
        checkAnyMeds = True if ss['anyMeds'] != None else False
        checkAnimals = True if ss['animalRecalls'] != None else False
        
        if checkDiabetes and \
           checkHypertension and \
           checkLipid and \
           checkDepression and \
           checkAntiFlam and \
           checkAnyMeds and \
           checkAnimals:
            return True

        else:
            error_list = []
            
            if not checkDiabetes:
                error_list.append("1. Diabetes question not answered (Section 2)")

            if not checkHypertension:
                l = len(error_list)
                if l > 0:
                    error_list.append(f"{l+1}. Hypertension question not answered (Section 2)")
                else:
                    error_list.append("1. Hypertension question not answered (Section 2)")

            if not checkLipid:
                l = len(error_list)
                if l > 0:
                    error_list.append(f"{l+1}. Cholesterol question not answered (Section 2)")
                else:
                    error_list.append("1. Cholesterol question not filled out (Section 2)")

            if not checkDepression:
                l = len(error_list)
                if l > 0:
                    error_list.append(f"{l+1}. Depression question not answered (Section 3)")
                else:
                    error_list.append("1. Depression question not filled out (Section 3)")

            if not checkAntiFlam:
                l = len(error_list)
                if l > 0:
                    error_list.append(f"{l+1}. AntiFlammatory question not answered (Section 3)")
                else:
                    error_list.append("1. AntiFlammatory question not filled out (Section 3)")

            if not checkAnyMeds:
                l = len(error_list)
                if l > 0:
                    error_list.append(f"{l+1}. Other Medications question not answered \
(Section 3)")
                else:
                    error_list.append("1. Other Medications question not filled out (Section 3)")
                    
            if not checkAnimals:
                l = len(error_list)
                if l > 0:
                    error_list.append(f"{l+1}. Animal Recalls question not filled in (Section 4)")
                else:
                    error_list.append("1. Animal Recalls question not filled in (Section 4)")

            return error_list
        
    check = checkPage1()

    checkGene = True

    #Warn Participant if they miss any optional info, then move on
    warning_list = []

    if ss['gene'] == None:
        warning_list.append('You have not chosen an option for the Genetic Information\
 (Phase 2).')
        checkGene = False
        
    elif "Unsure" in ss['gene']:
        warning_list.append('You have chosen option \'Unsure\' (Phase 2).')
        checkGene = False
        
    if ss['key']:
        if ss['countryTwoCode'] == None:
            warning_list.append("You have not chosen a country (Phase 3).")
            if ss['zipcode'] != None:
                warning_list.append("You have specified a zipcode, but not a country. \
    Therefore, both factors will not be considered.")
                ss['zipcode'] = None

        if ss['zipcode'] == None:
            warning_list.append("You have not specified your zipcode.")
            if ss['countryTwoCode'] != None:
                warning_list.append("You have specified a country, but not a \
    zipcode. Therefore, both factors will not be considered.")
                ss['country'] = None
                ss['countryTwoCode'] = None

    elif ss['key'] == False:
        if ss['aqi'] == None:
            warning_list.append("You have not inputted the AQI of your location. Therefore, the \
Environmental Factors will not be considered.")

    #If Participant isn't missing any required info, start results
    if check == True:
        if len(warning_list) > 0:
            warning_container = st.empty()
            
            with warning_container.container():
                st.warning('##### Some (optional) factors were left out. You \
can wait and load results in, then restart, reload the page immediately and \
    restart, or continue without specifying any of the factors.', icon="⚠️")
                count = 1
                for element in warning_list:
                    st.warning(f"###### {count}. {element}\n")
                    count += 1

            time.sleep(1)       
            msg = st.toast("3...")
            time.sleep(1)
            msg.toast("2...")
            time.sleep(1)
            msg.toast("1...")
            time.sleep(2)
            warning_container.empty()

        #If Participant added in location info, convert to (longitude,latitude)
        if ss['key']:
            try:
                lnglat = zipToLngLat(ss['zipcode'],ss['country'],ss['Key'])
            except Exception:
                try:
                    lnglat = zipToLngLat(ss['zipcode'],ss['countryTwoCode'],ss['Key'])
                except Exception:
                    st.error("###### Sorry, there seems to be an error with the \
location details. The model will disregard any location factors and continue.",
                 icon="🚨")
                    lnglat = None

            #Convert longitude and latitude to AQI
            if lnglat != None:
                client = Client(key=ss['Key'])
                current_data = current_conditions(
                    client,
                    lnglat,
                    include_health_suggestion=True,
                    include_additional_pollutant_info=True)

                history_data = historical_conditions(
                    client,
                    lnglat,
                    lag_time=720)

                #Custom module from internal_external_modules
                df = historical_conditions_to_df(history_data)

                indexes = df[df['code'] == 'uaqi'].index.values

                df2 = df.drop(indexes)
                df3,df4,df5,df6,df7 = df2.copy(),df2.copy(),df2.copy(),df2.copy(),df2.copy()

                try:
                    ss['aqi'] = current_data['page_1']['indexes'][1]['aqi']
                    
                except Exception:
                    st.error("##### Sorry, there seems to be an error with the zipcode \
provided. Either it is not a real zipcode, or the zipcode does not exist in Google's API\
/AQI Database. Sorry for the inconvenience, The model will disregard any location \
factors and continue with the results.",
                 icon="🚨")

        #Load results
        with st.status("Loading Results...", expanded=True) as status:
            st.write("Checking data...")
            time.sleep(1)
            st.write("Loading Model and Algorithm...")
            
            #Load in the model, and convert given data to csv for input to model
            with open('gradientBoosting_Model.pkl',
                      'rb') as f:
                model = pickle.load(f)

            with open('scaler.pkl',
                      'rb') as s:
                scaler = pickle.load(s)

            #Start count to input to Algorithm
            if ss['diabetes'] == "Yes": ss['diabetes'] = 1
            else: ss['diabetes'] = 0
            if ss['hypertension'] == "Yes": ss['hypertension'] = 1
            else: ss['hypertension'] = 0
            if ss['lipid'] == "Yes": ss['lipid'] = 1
            else: ss['lipid'] = 0
            if ss['antiFlam'] == "Yes": ss['antiFlam'] = 1
            else: ss['antiFlam'] = 0
            if ss['depression'] == "Yes": ss['depression'] = 1
            else: ss['depression'] = 0
            if ss['anyMeds'] == "Yes": ss['anyMeds'] = 1
            else: ss['anyMeds'] = 0
            
            data = [ss['age'],
                    ss['gender'],
                    ss['education'],
                    ss['heartRate'],
                    ss['systolicBP'],
                    ss['diastolicBP'],
                    ss['diabetes'],
                    ss['hypertension'],
                    ss['lipid'],
                    ss['animalRecalls'],
                    ss['depression'],
                    ss['antiFlam'],
                    ss['anyMeds']]

            #Reshape the Data
            array = np.array(data)
            array = array.reshape(1,-1)
            #Transform\Pre-Process the Data and Predict using the Model
            arrayScaled = scaler.transform(array)
            prediction = model.predict(arrayScaled)

            diseaseCount = 0
            if ss['diabetes'] == 1: diseaseCount += 1
            if ss['hypertension'] == 1: diseaseCount += 1
            if ss['lipid'] == 1: diseaseCount += 1
            if ss['depression'] == 1: diseaseCount += 1
            if ss['antiFlam'] == 1: diseaseCount += 1
            
            gene = 0

            if ss['gene'] != None and \
               'Unsure' not in ss['gene']:
                if 'Single' in ss['gene']: gene = 1
                elif 'Double' in ss['gene']: gene = 2

            aqiLevel = 0
            if 'aqi' in ss:
                if ss['aqi'] <= 50: pass
                elif ss['aqi'] <= 100: aqiLevel = 1
                else: aqiLevel = 2

            if gene == 0: Gene = False
            else: Gene = True

            assert float(prediction).is_integer()

            BooleanPrediction = True if prediction == 1 else False

            try:
                probability = Algorithm(Gene,
                                        aqiLevel,
                                        BooleanPrediction,
                                        diseaseCount,
                                        gene)
                
            except Exception:
                probability = -1
            
            
            time.sleep(2)
            st.write("Loading Figures...")
            
            #Create graphs
            try:

                #Define function to drop unnecessary values
                def drop(totalNotSingle,DF):
                    for element in totalNotSingle:
                        indexes = DF[DF['name'] == element].index.values
                        DF = DF.drop(indexes)
                    return DF
                
                #Write Graphs
                Total = ['AQI (US)',
                         "Ozone",
                         "Carbon monoxide",
                         'Inhalable particulate matter (<10µm)',
                        'Fine particulate matter (<2.5µm)',
                         "Nitrogen dioxide",
                         "Sulfur dioxide"]

                l2 = Total.copy()
                del l2[l2.index('AQI (US)')]
                df2 = drop(l2,df2)

                l3 = Total.copy()
                del l3[l3.index('Ozone')]
                df3 = drop(l3,df3)

                l4 = Total.copy()
                del l4[l4.index('Inhalable particulate matter (<10µm)')]
                df4 = drop(l4,df4)

                l5 = Total.copy()
                del l5[l5.index('Sulfur dioxide')]
                df5 = drop(l5,df5)

                l6 = Total.copy()
                del l6[l6.index('Fine particulate matter (<2.5µm)')]
                df6 = drop(l6,df6)

                l7 = Total.copy()
                del l7[l7.index('Nitrogen dioxide')]
                df7 = drop(l7,df7)

                #Create Line-Frequency-Charts Depicting the Variables
                chartAQI = alt.Chart(df2).mark_trail().encode(
                        x=alt.X('time:T',title='Date Time'),
                        y=alt.Y('value:Q',title='Value'),
                        size='value:Q'
                        )

                chartOzone = alt.Chart(df3).mark_trail().encode(
                        x=alt.X('time:T',title='Date Time'),
                        y=alt.Y('value:Q',title='Value'),
                        size='value:Q'
                        )

                chartInhale = alt.Chart(df4).mark_trail().encode(
                        x=alt.X('time:T',title='Date Time'),
                        y=alt.Y('value:Q',title='Value'),
                        size='value:Q'
                        )

                chartSulfur = alt.Chart(df5).mark_trail().encode(
                        x=alt.X('time:T',title='Date Time'),
                        y=alt.Y('value:Q',title='Value'),
                        size='value:Q'
                        )

                chartFine = alt.Chart(df6).mark_trail().encode(
                        x=alt.X('time:T',title='Date Time'),
                        y=alt.Y('value:Q',title='Value'),
                        size='value:Q'
                        )

                chartNitro = alt.Chart(df7).mark_trail().encode(
                        x=alt.X('time:T',title='Date Time'),
                        y=alt.Y('value:Q',title='Value'),
                        size='value:Q'
                        )

            except Exception as e:
                #st.write(e) --> use for debugging errors
                pass
            
            time.sleep(0.5)
            #Update Loading status --> Loading is finished, display loaded graphs and content
            status.update(label="Loading Finished!", state="complete", expanded=False)

        st.balloons()
        time.sleep(0.5)

        if ss['gene'] != None and 'Unsure' not in ss['gene']:
            if "Not a Carrier" in ss['gene']:
                st.success("##### You have ***no*** additional risk from genetic factors.")

            elif "Single Carrier" in ss['gene']:
                st.warning("##### You have a ***mild-to-moderate*** additional risk from \
genetic factors.")

            elif "Double Carrier" in ss['gene']:
                st.error("##### You have a ***moderate-to-severe*** additional risk from \
genetic factors.")
        else:
            if ss['gene'] == None:
                st.info("##### ***You chose not to use the Genetic Factor.***")
            elif 'Unsure' in ss['gene']:
                st.info("##### ***You chose option 'Unsure' in the gene section. Please consider \
consulting a genetics counselor or doctor about it.***")

        try:
            if ss['aqi'] != None:
                if ss['aqi'] < 50:
                    st.success(f"##### Your city, in {ss['country']} \
    ({ss['countryTwoCode']}), has a ***mild*** additional risk, with AQI levels \
    being around {ss['aqi']}.")
                elif ss['aqi'] < 100:
                    st.warning(f"##### Your city, in {ss['country']} \
    ({ss['countryTwoCode']}), has a ***moderate*** additional risk, with AQI levels \
    being around {ss['aqi']}.")
                elif ss['aqi'] < 150:
                    st.warning(f"##### Your city, in {ss['country']} \
    ({ss['countryTwoCode']}), is ***unhealthy*** for sensitive groups. \
    Excersize caution. The AQI levels are around {ss['aqi']}.")
                else:
                    st.error(f"##### Your city, in {ss['country']} \
    ({ss['countryTwoCode']}), is ***unhealthy.*** \
    Excersize caution. The AQI levels are around {ss['aqi']}.")

        except KeyError:
            st.info("##### ***You chose not to use the Location Factor.***")

        if ss['aqi'] != None:
            try:
                tab1,tab2,tab3,tab4,tab5,tab6 = st.tabs(["US AQI",
                                                         "Ozone",
                                                         "Inhalable particulate matter (<10µm)",
                                                         "Sulfur Dioxide",
                                                         "Fine particulate matter (<2.5µm))",
                                                         "Nitrogen Dioxide"])

                #Display Graphs in Separate Tabs
                with tab1:
                    st.altair_chart(chartAQI, use_container_width=True)
                with tab2:
                    st.altair_chart(chartOzone, use_container_width=True)
                with tab3:
                    st.altair_chart(chartInhale, use_container_width=True)
                with tab4:
                    st.altair_chart(chartSulfur, use_container_width=True)
                with tab5:
                    st.altair_chart(chartFine, use_container_width=True)
                with tab6:
                    st.altair_chart(chartNitro, use_container_width=True)
                st.write("*Click on tab, then use right and left arrows to move to next tabs*")
                    
            except Exception as e:
                st.toast("Sorry, something went wrong with the location-related graphs.")
                #st.write(e) --> for debugging
                
        else:
            st.toast('*As you chose not to use the Location feature, no figures \
    pertaining to AQI or pollutants in your location were created.*')

        if probability == -1:
            st.error("#### Sorry, there was an error with the Algorithm. Please \
try again some other time.")

        elif probability == 0:
            st.success("#### Your combined Risk based on provided information \
indicates that you are around 0-0.2 times as likely to get Alzheimer's Dementia \
than a normal person.")

        elif probability < 1:
            st.success(f"#### Your combined Risk based on provided information \
indicates that you are around {probability} times as likely to get \
Alzheimer's Dementia than a normal person.")

        elif 1 < probability < 2.5:
            st.warning(f"#### Your combined Risk based on provided information \
indicates that you are around {probability} times as likely to get \
Alzheimer's Dementia than a normal person.")

        elif probability > 2.5:
            st.error(f"#### Your combined Risk based on provided information \
indicates that you are around {probability} times as likely to get \
Alzheimer's Dementia than a normal person.")
            

    else:
        st.error("##### Sorry, results cannot be loaded in, as there are some questions \
unanswered in Phase 1. They are listed as follows:",
                 icon="🚨")
        

        for element in check:
            st.error(f"###### {element}\n")

        st.markdown('#')

        st.warning('##### Additionally, some (optional) factors were left out.',
                   icon="⚠️")
        count = 1
        for element in warning_list:
            st.warning(f"###### {count}. {element}\n")
            count += 1
