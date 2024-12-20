
import os,sys
from docxtpl import DocxTemplate
from tkinter import *
from tkcalendar import *
from datetime import datetime
from tkdblist import * 

#to access the file path
def resource(relative_path):
     try:
          base_path=sys._MEIPASS
     except Exception:
           base_path=os.path.abspath(".")
     return os.path.join(base_path,relative_path)



#print new loan and reprint existing loan
def loanprint(loan_data,c,l="loan"):
    loan_date=datechange(loan_data["loan_date"])
    l_date=datetime.strptime((loan_date),'%d-%m-%Y')
    max_date=(l_date.replace(year=l_date.year+1))  #to increase date to 1 year as max date
    max_date=max_date.strftime('%d-%m-%Y')

    newloan=DocxTemplate(resource('src/loan.docx')) 
    # newloan.render({'loan_day':date,'bill_no':bill,'name':name,'coname':coname,'address':address,
    #                 'street':street,'item':item,'weight':weight,'amount':amount,'noitem':noitem,
    #                 'max_date':max_date,'Ph_no':phnum})
    newloan.render(loan_data)
    loan_name=f"{loan_data["bill_no"]} {loan_data["name"]} {l}.docx"
    if l=="loan":
        loan_path=r'.\loan'
    elif l=="reprint":
        loan_path=r'.\reprint'
    n_path=resource(os.path.join(loan_path,loan_name))
    newloan.save(n_path)
    if c==True:#print the bill if c is true
        filepath=loan_path
        os.startfile(n_path,'print')

    return


#to print released loan bill
def interestprint(paylist,c):
    doc=DocxTemplate(resource('src/omm.docx')) 
 
    name=paylist[0]
    loan_date=paylist[1]
    bill_no=paylist[2]
    int_amt=paylist[3]
    to_day=paylist[4]
    interest=paylist[5]
    total=paylist[6]

    doc.render({'name':name,'to_day':to_day,'loan_date':loan_date,'bill_no':bill_no,'interest':interest,'total':total,'int_amt':int_amt})
    r_name=f"{bill_no} {name}.docx"
    patth=r'.\relese'
    r_path=resource(os.path.join(patth,r_name))
    doc.save(r_path)
    if c==True:
        filepath=r_path
        os.startfile(filepath,'print')
    
    return



