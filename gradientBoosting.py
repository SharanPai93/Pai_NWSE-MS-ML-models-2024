# Load libraries
import pandas as pd
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report
from sklearn import svm
import pickle
'''
#for display purposes
from sklearn.tree import export_graphviz
from six import StringIO  
from IPython.display import Image  
import pydotplus
'''
# load dataset
#As I cannot put the NACC Data in public, make an account there and access the data, then paste it in the placeholder file name
#df = pd.read_csv("your/file/name.csv")

#split dataset in features and target variable

X=df.drop(columns=["AlzheimerStage","AntiAlzMed",'BMI'])
y=df["AlzheimerStage"]
feature_cols = X.columns

'''
#Another way to represent
feature_cols = ['Age', 'Sex', 'Education', 'BMI', 'HeartRate', 'SystolicBP', 'DiastolicBP', 'DiabetesMed','HyperTenMed','LipidMed','AntiAlzMed','AnimalRecalls','TotalScore']
X = df[feature_cols] # Features
y = df.AlzheimerStage # Target variable
labels = y.unique()
'''
# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size=0.3,
                                                    random_state=100)


from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

# Create a SVM classifer object
#clf = KNeighborsClassifier(n_neighbors=5)
#clf = svm.SVC(kernel='linear')
clf = GradientBoostingClassifier(learning_rate=0.1,
                                 n_estimators=300)
# Train Decision Tree Classifer
clf = clf.fit(X_train,y_train)

#Predict the response for test dataset
y_pred = clf.predict(X_test)
# Model Accuracy, how often is the classifier correct?

print("GB Accuracy:",metrics.accuracy_score(y_test, y_pred))
print(classification_report(y_test,y_pred))

from sklearn import tree
import matplotlib.pyplot as plt
import numpy as np

labels = y.unique()

#Load model as pickle file
filename = 'gradientBoosting_Model.pkl'
pickle.dump(clf, open(filename, 'wb'))

with open('scaler.pkl','wb') as f:
    pickle.dump(scaler,f)

#Check out the class names - how its converted to string...it was originally just y.unique()
