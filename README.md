# Pai_NWSE-MS-ML-models-2024
Hello, following my research of ML Models in 2023 (you can find my previous project on ML Models [here](https://github.com/SharanPai93/Pai_NWSE-MS-ML-models-2023)), I have developed another project involving the research of Alzheimer's Dementia (AD). The result of my project is a web-based tool, which can be found online [through this link.](https://alzheimersdetection.streamlit.app/) The code for this tool is shown above, by the file name "AlzheimersDetectionApp.py".  
The following overview of my project is included below:

## Abstract
> Millions of people are affected by Alzheimer’s Disease for which there is no cure. Nearly 80% of people with memory problems have at least one chronic condition
related to cardiovascular/metabolic disease. In addition, people who carry the genetic risk factor for Alzheimer’s (APOE e4), and have a metabolic disease have a higher
risk of developing Alzheimer’s Dementia in the future. By creating a tool that can be easily accessed and cost-effective with high accuracy, I can help seniors detect their
risk of developing Alzheimer’s Disease based on their demographics, current health, along with their genetic predisposition and environmental factor information. Using
real datasets that contain dementia risk-factors, I performed classification through Machine Learning, and produced a >78% accuracy model for AD Dementia risk
prediction. A working web-based tool to provide the risk outcome using novel weights-based algorithm for the risk factors has been developed.

## Purpose and Goal
There are multiple purposes of this project. They are, as follows:
1. Choose a few models to compare from a large pool of models, to build a better understanding of AI/ML models and their classification methods. These models must satisfy a decent Validation Accuracy, and use different classification methods for better comparisons. These models will be trained on large datasets based on Alzheimer's Dementia Risk Factors, mostly from NACC/ADRC. Out of the multiple models, four classification models were chosen, namely:
    - *Gradient Boosting Classifier*
    - *Support Vector Machine/Classifier*
    - *Random Forest Classifier*
    - *k-Nearest Neighbors Classifier*

2. Build an Algorithm that takes factors others have not considered, and use it to calculate the combined risk of Alzheimer's Dementia for the participant.  
    - Genetic Factors --> Research of APOE e4 (Apolipoprotein epsilon4 Genotype) to determine additional risk of AD.
    - Environmental Factors --> Research of Air Quality Index (AQI), and how it impacts the health of individuals in terms of risk of AD remains important to consider.  

3. Program a free-to-use/cost-effective Web-based Tool to predict AD given input from participant. This tool will implement The Algorithm, as well as a chosen Model from the Models I hand-picked from the pool of models I tested on.

Additionally, I decided to compare the four classifier models to the Neural Network Model from the Python Module Keras, *Artificial Neural Network* (ANN) Model. After all the training and pre-processing, I created the Algorithm, and I programmed the Web-based Tool using Streamlit such that it can be widely available to the population.

## Training and Testing the Models
After training the models with over 110,000 rows of Data (Both Multi-input and Binary-input), I calculated the accuracy of each of the five models using the following metrics:
1. *Validation Accuracy* --> the testing accuracy of the model
2. *Sensitivity* --> also known as recall, a measurement to detect how well the model can predict positive instances (TP/(TP + FN))
3. *Specificity* --> a measurement to detect how well the model can predict negative instances (TN/(TN + FP))
4. *Precision* --> a measurement to detect how well the model can predict the positive class as a whole (TP/(TP + FP))
5. *F1 Score* --> the harmonic mean of the precision and recall/sensitivity (TP/(TP + 0.5*(FP + FN)))
6. *AUC SCore* --> used for drawing the ROC (receiver operating characteristic) curves

Finally, after drawing PCA (Principal Component Analysis) graphs and narrowing down unnecessary values and columns in my data, I found that Gradient Boosting got a Validation Accuracy of 0.7782, and ANN got 0.7811. Since both accuracies were very close, it was a tough call, however, I decided to use Gradient Boosting as it had a sensitivity of 0.6885, while ANN had 0.6862, and True Positives are very useful/much more important in these ML predictions. Gradient Boosting is also more versatile and easy-to-deploy, although both models would work for the tool.


## Building the Algorithm
After choosing the model, I decided to build my algorithm. I decided to add weights for each of the following:
1. Comorbidities and Demographic Information --> This was the Model-part of the algorithm. If the Model predicted AD, then the weights would come in play. Otherwise, this factor would be 0.
    - Case 1: One coexisting disease: weight of 0.5
    - Case *n*: *n* coexisting diseases: weight of 0.5*n*

2. Genetic Risk  
    - If the participant is a Carrier (This factor is optional, so the participant can just skip this section):
        - If participant is a Single-Carrier of the gene: 2.5-fold
        - If participant is a Double-Carrier of the gene: 10-fold
    - If the participant is not a carrier, this option is equivalent to 0.  

3. Environmental Risk. Analyzing the AQI levels can increase the accuracy of the Algorithm. See [here](https://www.airnow.gov/aqi/aqi-basics/) for AQI classification (This factor is optional, so the participant can just skip this section)
    - If AQI Levels is Good, then factor is 0  
    - If AQI Levels is Moderate, a weight of 1 is multiplied to the fold --> 15% impact over 7 years: 0.02 ∗ 1 fold increase per year
    - If AQI Levels is Unhealthy (or worse), a weight of 2 is multiplied to the fold --> 15% impact over 7 years: 0.04 ∗ 1 fold increase per year  

Adding these factors up, we see how likely the participant is to get AD given current conditions compared to a normal person (value of 1). We can also plot a graph to show the likeliness of getting AD over the next *x* years using the environmental factors linearly (assuming participant does not gain any more comorbidities and does not move to a different location)  

## Writing the Web-Based Tool and Results/Reflection
Using Streamlit and Python, I programmed a web-based tool from scratch to implement all of this and more. I found this project very fun and challenging, as it was especially hard to find an API to give me AQI levels of a certain location, and convert a zip code (the input for the location-factor) to latitude and longitude. I ended up using GoogleV3 Module in Python to conduct the location-information, and use [Google's AQI Service](https://developers.google.com/maps/documentation/air-quality). I learned a lot more from this project, and I hope to continue on learning about AI/ML and dive deeper into the field!


## Data and Code
I will add the Code of the Models and Web-Based tool soon. Unfortunately, NACC does not allow its data to be publicly accessible, however, you can make an account to access the data [here](https://naccdata.org/). I have added the Model Code and the Pickle file for it to load it. I also added in the code for the Tool, in which I am using functions and code in the file (I uploaded as "functions.py") that are inspired from [this website.](https://towardsdatascience.com/a-python-tool-for-fetching-air-pollution-data-from-google-maps-air-quality-apis-7cf58a7c63cb)
