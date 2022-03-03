import numpy as np
from flask import Flask,render_template,request
import ML_model 

app = Flask(__name__)



@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("AboutUs.html")

@app.route("/sub",methods=['POST'])
def submit():
    if request.method=="POST" :
        CS=float(request.form['CreditScore'])
        IsFirstTime=float(request.form['IsFirstTime'])
        MIP=float(request.form['MIP'])
        Units=float(request.form['Units'])
        OCLTV=float(request.form['OCLTV'])
        DTI=float(request.form['DTI'])
        OrigUPB=float(request.form['OrigUPB'])
        LTV=float(request.form['LTV'])
        OrigInterestRate=float(request.form['OrigInterestRate'])
        OrigLoanTerm=float(request.form['OrigLoanTerm'])
        MonthsInRepayment=float(request.form['MonthsInRepayment'])

        years_repayment = MonthsInRepayment/12
        
        
        MIP_log = np.log(MIP+1)
        OCLTV_log = np.log(OCLTV+1)
        DTI_log = np.log(DTI+1)
        OrigUPB_log = np.log(OrigUPB+1)
        int_rate_log = np.log(OrigInterestRate+1)
        LoanTerm_log=np.log(OrigLoanTerm)

        if (CS >= 0) & (CS < 650):
            CreditRange = 'Poor'
        elif (CS >= 650) & (CS < 700):
            CreditRange = 'Fair'
        elif (CS >= 700) & (CS < 750):
            CreditRange = 'Good'
        elif (CS >= 750):
            CreditRange = 'Excellent'

        
        if (years_repayment >= 0) & (years_repayment <4):
            RepayRange = '0-4yrs'
        elif (years_repayment >= 4) & (years_repayment <10):
            RepayRange = '4-10yrs'
        elif (years_repayment >= 10) & (years_repayment <15):
            RepayRange = '10-15yrs'
        elif (years_repayment >= 15):
            RepayRange = '15-20yrs'


        if (LTV >= 0) & (LTV < 45):
            LTVRange = 'Low'
        elif (LTV >= 45) & (LTV < 80):
            LTVRange = 'Medium'
        elif (LTV >= 80):
            LTVRange = 'High'        

        
        if (CreditRange == 'Poor'):
            CreditRange_Fair = 0
            CreditRange_Good = 0
            CreditRange_Poor = 1
        elif (CreditRange == 'Fair'):
            CreditRange_Fair = 1
            CreditRange_Good = 0
            CreditRange_Poor = 0
        elif (CreditRange == 'Good'):
            CreditRange_Fair = 0
            CreditRange_Good = 1
            CreditRange_Poor = 0
        else:
            CreditRange_Fair = 0
            CreditRange_Good = 0
            CreditRange_Poor = 0
    
        if (RepayRange == '0-4yrs'):
            Repay_range_in_years_0_4yrs = 1
            Repay_range_in_years_10_15yrs = 0
            Repay_range_in_years_15_20yrs = 0
            Repay_range_in_years_4_10yrs = 0
        elif (RepayRange == '4-10yrs'):
            Repay_range_in_years_0_4yrs = 0
            Repay_range_in_years_10_15yrs = 0
            Repay_range_in_years_15_20yrs = 0
            Repay_range_in_years_4_10yrs = 1
        elif (RepayRange == '10-15yrs'):
            Repay_range_in_years_0_4yrs = 0
            Repay_range_in_years_10_15yrs = 1
            Repay_range_in_years_15_20yrs = 0
            Repay_range_in_years_4_10yrs = 0
        else:
            Repay_range_in_years_0_4yrs = 0
            Repay_range_in_years_10_15yrs = 0
            Repay_range_in_years_15_20yrs = 1
            Repay_range_in_years_4_10yrs = 0
    

        if (LTVRange == 'Low'):
            LTV_range_Low = 1
            LTV_range_Medium = 0
        elif (LTVRange == 'Medium'):
            LTV_range_Low = 0
            LTV_range_Medium = 1
        else:
            LTV_range_Low = 0
            LTV_range_Medium = 0


        prediction = ML_model.predict([[IsFirstTime, MIP_log, Units, OCLTV_log, DTI_log, OrigUPB_log, int_rate_log,\
                             Repay_range_in_years_15_20yrs, CreditRange_Fair, CreditRange_Good,\
                             CreditRange_Poor, LTV_range_Low, LTV_range_Medium,Repay_range_in_years_0_4yrs,Repay_range_in_years_4_10yrs,Repay_range_in_years_10_15yrs,LoanTerm_log]])
        

        if prediction=="Yes":
            return render_template('sub.html', prediction_text='This User Is Risky To Give Loan')
        else:
            return render_template('sub.html',prediction_text='This User Is Good For Loan')
            


if __name__== "__main__":
    app.run(debug=True)
