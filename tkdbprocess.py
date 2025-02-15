from datetime import date,datetime,timedelta

#change the date format to  "%d-%m-%Y" format 
def datechange(a):        
        t1="%d-%m-%y %H:%M:%S"
        t2="%d-%m-%y"
        t3="%d %m %y %H:%M:%S"
        t4="%d %m %y"
        t5="%d/%m/%y %H:%M:%S"
        t6="%d/%m/%y"
        t7="%d-%m-%Y %H:%M:%S"
        t8="%d-%m-%Y"
        t9="%d %m %Y %H:%M:%S"
        t10="%d %m %Y"
        t11="%d/%m/%Y %H:%M:%S"
        t12="%d/%m/%Y"
        t13="%Y-%m-%d %H:%M:%S"
        t14="%Y-%m-%d"
        t=[t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14]
        try:
            for i in t:
                try:
                    a=datetime.strptime(a,i)
                    
                except:
                    pass
            return a.strftime("%d-%m-%Y")
        except:
            return a

## days different calculation
def days_calculation(loan_date,re_date):
    loan_date=datechange(loan_date)
    loan_date = datetime.strptime(loan_date, "%d-%m-%Y")
    if re_date:
        re_date=datechange(re_date)
        re_date = datetime.strptime(re_date, "%d-%m-%Y")
    else:
        re_date = datetime.now()
    

    # Calculate years and months
    diff_years = re_date.year - loan_date.year
    diff_months = re_date.month - loan_date.month

    # Adjust if months are negative
    if diff_months < 0:
        diff_months += 12
        diff_years -= 1

    # Calculate remaining days
    if re_date.day >= loan_date.day:
        remaining_days = re_date.day - loan_date.day
    else:
        # Borrow days from the previous month
        previous_month = (re_date.replace(day=1) - timedelta(days=1)).day  # Last day of the previous month
        remaining_days = (previous_month - loan_date.day) + re_date.day
        diff_months -= 1  # Adjust months if we borrow days
        if diff_months < 0:  # Handle negative months after borrowing
            diff_months += 12
            diff_years -= 1
    
    # Output the results
    result={"years": diff_years, "months": diff_months, "days": remaining_days}
    print(f"Years: {diff_years}, Remaining Months: {diff_months}, Remaining Days: {remaining_days}")
    return result


##calculation
def interest(int_amt,loan_date,re_date,int_rate,reduce_amt):
    date_diff=days_calculation(loan_date,re_date)

    if date_diff["days"]<15 and date_diff["months"]==0 and date_diff["years"]==0:
        date_diff["days"]=15

    if int_rate=="1.5&2":
        if date_diff["years"]<1:
            int_month=float(int_amt)*(1.5/100)*date_diff["months"]
            int_days=float(int_amt)*(1.5/100)*(date_diff["days"]/30)
            intrest=int_days+int_month
        else:
            year_1st=float(int_amt)*(1.5/100)*12    #for 1st year 1.5% interest (12 month)

            int_year=float(int_amt)*(2/100)*((date_diff["years"]-1)*12)
            int_month=float(int_amt)*(2/100)*date_diff["months"]
            int_days=float(int_amt)*(2/100)*(date_diff["days"]/30)
            
            intrest=int_days+int_month+int_year+year_1st

    else:
        int_year=float(int_amt)*(float(int_rate)/100)*(date_diff["years"]*12)
        int_month=float(int_amt)*(float(int_rate)/100)*date_diff["months"]
        int_days=float(int_amt)*(float(int_rate)/100)*(date_diff["days"]/30)
            
        intrest=int_days+int_month+int_year


    int_amt=float(int_amt)
    reduce_amt=float(reduce_amt)
    total=int(int_amt)+intrest-int(reduce_amt)
    values={"total":int(total),"interest":int(intrest),"days":date_diff}
    # total=float(intrest)+float(int_amt)
    
    return values 























