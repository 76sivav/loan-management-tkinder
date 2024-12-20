from datetime import date,datetime

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
        

##calculation
def interest(int_amt,loan_date,re_date):
    loan_date=datetime.strptime(loan_date,"%d-%m-%Y")
    re_date=datetime.strptime(re_date,"%d-%m-%Y")
    diff=re_date-loan_date
    intday=int(diff.days)
    if intday<15:
        intday=15
    intrest=(float(int_amt)*0.015*intday)/30
    # total=float(intrest)+float(int_amt)
    
    return (int(intrest)) 























