import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score
df=pd.read_csv('LoanExport.csv')

df=df.drop(['FirstPaymentDate','MaturityDate','MSA','Occupancy','Channel','PPM','ProductType','PropertyState','PropertyType',
            'PostalCode','LoanSeqNum','LoanPurpose','NumBorrowers','SellerName','ServicerName'],axis=1)

df.dropna(inplace=True)

df['CreditScore'] = np.where(df['CreditScore'] == 0, 850, df['CreditScore'])
df['CreditRange'] = pd.cut(df.CreditScore,[550,650,700,750,850],4,labels=[1,2,3,4])
df = df[df.FirstTimeHomebuyer != 'X']
df['FirstTimeHomebuyer'] = np.where(df['FirstTimeHomebuyer'] == 'Y', 1, 0)
df['LTV_range'] = pd.cut(df.LTV,[0,25,50,1000],3,labels=['Low','Medium','High'])

df['Repay_range'] = pd.cut(df.MonthsInRepayment,[0,48,96,144,192,240],5,
                           labels=['0-4yrs','4-8yrs','8-12yrs', '12-16yrs', '16-20yrs'])

df=df.dropna()

df = df.rename(columns={"CreditScore": "CS", "FirstTimeHomebuyer": "IsFirstTime"}) 
df1=df.copy()    
df1=df1.drop(['CS','LTV','MonthsDelinquent','MonthsInRepayment'],axis=1)



df1[df1['EverDelinquent']==0]
data_with_dummies=pd.get_dummies(df1,drop_first=True)
#To make our data frame more organized, we prefer to place the dependent variable in the beginning of the df
cols=list(data_with_dummies.columns)
cols[-1],cols[7]=cols[7],cols[-1]

data_preprocessed=data_with_dummies[cols]



from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GridSearchCV

df_model=data_preprocessed.copy()
scaler = RobustScaler()

features = [['MIP', 'OCLTV', 'DTI', 'OrigUPB', 'OrigInterestRate','OrigLoanTerm']]
for feature in features:
    df_model[feature] = scaler.fit_transform(df_model[feature])

x = df_model.drop(columns=['EverDelinquent'])
y = df_model['EverDelinquent']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=27)
knn = KNeighborsClassifier()


knn.fit(x_train, y_train)

def predict(X):
    return knn.predict(X)

