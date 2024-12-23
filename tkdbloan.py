#import modules
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from tkcalendar import *
from datetime import date
#python files
from tkdatabase import *
from tkdblist import *
from tkprint import *
from tkdbprocess import *


############ main frame :start ############

bill = Tk()
bill.title("omsakthi adagu kadai")
bill.geometry("1000x1000")
bill.configure(bg="#535c68")
bill.state("zoomed")

head_frame=Frame(bill,bg="#535c68")
head_frame.pack(side=TOP)

###### main frame : continous to  last part lines ############# 

#define font for all frame
lblfont="Calibri",16
todate="date"

# define datatype on all frame based on variable, total variable used :14
bill1=StringVar()
name1=StringVar()
date1=StringVar()
coname1=StringVar()
street1=StringVar()
address1=StringVar()
amount1=StringVar()
item1=StringVar()
weight1=StringVar()
noitem1=StringVar()
relese1=StringVar()
intrel=StringVar()
phvar=StringVar()
tday=(date.today()).strftime('%d-%m-%Y')   #get today

selected_value=None    #for get value from tree frame, later used

selected_var=[bill1,name1,date1,coname1,street1,address1,amount1,item1,weight1,noitem1,relese1,intrel,phvar]

#to intiate database to create or check database is availabe and ready to use .from tkdatabase.py
create_database_and_table()

#to clear all saved value on defined variable
def selected_value_clear():
    global selected_value
    for var in selected_var:
        var.set("")
    selected_value=None


############## date frame ############
# to select date from calender
def select_time(event):
    global datewindow,cal
    datewindow=Toplevel()
    datewindow.grab_set()
    datewindow.title("dd")
    datewindow.geometry("250x220+590+370")
    cal=Calendar(datewindow,selectmode="day",date_pattern="dd-mm-y")
    cal.place(x=0,y=0)
    bb=Button(datewindow,text="date",command=pic)
    bb.place(x=80,y=190)
    return cal.get_date()
def pic():
    date1.set(cal.get_date())   #assign value to date variable
    datewindow.destroy()
 ########################################   


################################### code for loan page start ###############################################################
def loan():
    global billing_frame
    try:
        search_frame.destroy()     #to clear all data 
        tree_frame.destroy()
        update_frame.destroy()
        tkinterest_frameme.destroy()
    except:
        pass
    try:
        billing_frame.destroy()      # to clear previous opened frame
    except:
        pass
    
    selected_value_clear() #clear variable values

    new_bill_no=int(find_max_bill_no())+1  #get last bill number from database .tkdatabase fn

    billing_frame=Frame(bill,bg="#535c68")
    billing_frame.pack(side=TOP,fill=X)

    title= Label(billing_frame, text="new loan", font=( "Calibri", 16, "bold"),bg="#535c68",height=0)
    title.grid(row=0, columnspan=2,padx=20,pady=20)

    lbldate=Label(billing_frame,text="தேதி",font=lblfont,bg="#535c68")
    lbldate.grid(row=1,column=1)
    txtdate=Entry(billing_frame,font=lblfont,width=20,textvariable=date1)
    txtdate.grid(row=1,column=2,pady=5)

    date1.set(tday)
    txtdate.bind("<1>",select_time)            #to access date frame by on one click on date input field

    lblbill=Label(billing_frame,text="கடன் எண்",font=lblfont,bg="#535c68")
    lblbill.grid(row=2,column=1)
    txtbill=Entry(billing_frame,font=lblfont,width=20,textvariable=bill1)
    txtbill.grid(row=2,column=2,pady=5)
    try:
        bill1.set(new_bill_no)            #to check bill number is not none
    except:
        bill.set("000")




    lblname=Label(billing_frame,text="பெயர்",font=lblfont,bg="#535c68")
    lblname.grid(row=3,column=1)
    txtname=Entry(billing_frame,font=lblfont,width=20)
    txtname.grid(row=3,column=2,pady=5)


    lblconame=Label(billing_frame,text="த/க பெயர்",font=lblfont,bg="#535c68")
    lblconame.grid(row=4,column=1)
    txtconame=Entry(billing_frame,font=lblfont,width=20)
    txtconame.grid(row=4,column=2,pady=5)

    lblstreet=Label(billing_frame,text="தெரு",font=lblfont,bg="#535c68")
    lblstreet.grid(row=5,column=1)
    txtstreet=Entry(billing_frame,font=lblfont,width=20,textvariable=street1)
    txtstreet.grid(row=5,column=2,pady=5)

    lbladress=Label(billing_frame,text="ஊர்",font=lblfont,bg="#535c68")
    lbladress.grid(row=6,column=1)
    txtadress=Entry(billing_frame,font=lblfont,width=20)
    txtadress.grid(row=6,column=2,pady=5)

    lblamount=Label(billing_frame,text="கடன் தொகை",font=lblfont,bg="#535c68")
    lblamount.grid(row=7,column=1)
    txtamount=Entry(billing_frame,font=lblfont,width=20)
    txtamount.grid(row=7,column=2,pady=5)

    lblitem=Label(billing_frame,text="பொருள்",font=lblfont,bg="#535c68")
    lblitem.grid(row=8,column=1)
    txtitem=Entry(billing_frame,font=lblfont,width=20)
    txtitem.grid(row=8,column=2,pady=5)

    lblweight=Label(billing_frame,text="எடை",font=lblfont,bg="#535c68")
    lblweight.grid(row=9,column=1)
    txtweight=Entry(billing_frame,font=lblfont,width=20)
    txtweight.grid(row=9,column=2,pady=5)

    lblnoitem=Label(billing_frame,text="மொத்த பொருள்",font=lblfont,bg="#535c68")
    lblnoitem.grid(row=10,column=1)
    txtnoitem=Entry(billing_frame,font=lblfont,width=20)
    txtnoitem.grid(row=10,column=2,pady=5)

    lblph=Label(billing_frame,text="Phone No.",font=lblfont,bg="#535c68")
    lblph.grid(row=11,column=1)
    txtph=Entry(billing_frame,font=lblfont,width=20)
    txtph.grid(row=11,column=2,pady=5)


    ############################# code to add data ###################################
    def new_loan():    #funtion for add new value after all ok

        #get value from tkinder frame
        bill=txtbill.get()
        date=txtdate.get()
        try:
            date=datechange(date)     
        except:
            pass
        name=txtname.get()
        coname=txtconame.get()
        address=txtadress.get()
        item=txtitem.get()
        weight=txtweight.get()
        amount=txtamount.get()
        noitem=txtnoitem.get()
        street=txtstreet.get()
        phno=txtph.get()

        #to process new loan
        def new_loan():
        
            loan_print_ok=messagebox.askyesnocancel(title="print",message="do you want to print")
            ##db
            columns = [
                "loan_date", "bill_no", "name", "co_name", "street", "address",
                "int_amt", "weight", "item", "no_item", "phone_no"
            ]
            data=[date,bill,name,coname,street,address,amount,weight,item,noitem,phno]

            loan_data=dict(zip(columns,data))

            if isinstance(loan_print_ok,bool):
                insert_record(loan_data)                 #tkdatabase - to add data in database
                print("1")
                ws_save(loan_data)                       #tkdblist - to add data in excell
                print("2")
                loanprint(loan_data,loan_print_ok)       #tkprint - to made document to print
                print("3")
                loan()                                   #return to loan page  
            
        ### to check input values is ok       
        try:
            b=int(bill)                                  #check it is integer and if it already stored
            if check_bill_no_exists(b):
                messagebox.showwarning(title="error",message="bill number exit")

                c=messagebox.askyesno(title="new bill no",
                                      message=f"next bill no is {new_bill_no} click yes to select this number")
                if c:
                    bill1.set(new_bill_no)
                    bill=new_bill_no
                else:
                    raise Error
                    
            try:
                phn=int(phno)    
                if len(phno)!=10:
                    raise "billerror"
            except "billerror":
                    messagebox.showwarning(title="error",message="ph number invalid")
                    
            am=int(amount)
            w=float(weight)
            n=int(noitem)
            d=datechange(date)

            #if all ok then goes to add data to database and excell
            new_loan()   

        except:
            messagebox.showwarning(title="error",message="invalid entry")
                       
        
    ######################### code for add data : END ############################### 

    btnEdit = Button(billing_frame, command=new_loan, text="Save", width=15, font=("Calibri", 16, "bold"),
                    fg="white", bg="#2980b9",
                    bd=0).grid(row=12, column=1, padx=10)


    btnEdit = Button(billing_frame, command=loan, text="reset", width=15, font=("Calibri", 16, "bold"),
                    fg="white", bg="#2980b9",
                    bd=0).grid(row=12, column=2, padx=10)
    
############################################## loan page code END  ############################################################


def reprint():      ### funtion for reprint existing loan bill 
    if selected_value:
        reprint_ok=messagebox.askyesno(title="reprint",message=f"want to reprint {selected_value[1]}")
        if reprint_ok:
            #db
            reloan_data=read_records_by_field("bill_no",selected_value[1])              #tkdatabase fn
             
            loan_status="reprint"
            loanprint(reloan_data[0],reprint_ok,loan_status)                            #tkprint fn
            messagebox.showinfo(title="reprint",message=f"{selected_value[1]} reprint completed")

            detail()
    else:
        messagebox.showwarning(message="select the bill",title="x")
    
def tkdelete():                                      #### delete record from both database and excell
    if selected_value:
        
        if messagebox.askyesno(title="delete",message="are you sure to delete"):
            
            delete_record(selected_value[1])            #tkdatabase fn   - delete data in database
            
            delete(selected_value[1])                   #tkdblist fn     - delete data in excell
            messagebox.showwarning(title="delete",message=f"{selected_value[1]} deleted")
            selected_value_clear()                      # clear variable value
            detail()                                    # to search ,tree frame
            
    else:
        messagebox.showwarning(title="error",message="select bill")

  


###################################### code for Search page : start  ####################################################################

def search():
    global search_frame
    try:
        search_frame.destroy()
        tree_frame.destroy()
        update_frame.destroy()
        tkinterest_frameme.destroy()
    except:
        pass
    try:
        tkinterest_frameme.destroy()
    except:
        pass
    try:
        billing_frame.destroy()
    except:
        pass
    
    selected_value_clear()
        
    search_frame=Frame(bill,bg="#535c68")
    search_frame.pack(side=TOP)
    global comb,combtxt,comb1,combtxt1,comb2,combtxt2

    ####### 1st search
    comb=ttk.Combobox(search_frame,width=15,state="readonly",textvariable="stringVar()",font=("Calibri",16, "bold"),height=10)
    comb["values"]=["select","கடன் தேதி","கடன் எண்","பெயர்","த/க பெயர்","ஊர்","கடன் தொகை","எடை","பொருள்","Phone No","மீட்ட தேதி"]
    comb.grid(row=1,column=0,padx=2,pady=2)
    comb.set("கடன் எண்")

    combtxt=Entry(search_frame,font=lblfont,width=15)
    combtxt.grid(row=1,column=1,pady=5)

    #### 2nd search
    comb1=ttk.Combobox(search_frame,width=15,state="readonly",font=("Calibri",16, "bold"),height=10)
    comb1["values"]=["select","கடன் தேதி","கடன் எண்","பெயர்","த/க பெயர்","ஊர்","கடன் தொகை","எடை","பொருள்","Phone No","மீட்ட தேதி"]
    comb1.grid(row=1,column=2,padx=2,pady=2)
    comb1.set("select")

    combtxt1=Entry(search_frame,font=lblfont,width=15)
    combtxt1.grid(row=1,column=3,pady=5)

    ####  3rd search
    comb2=ttk.Combobox(search_frame,width=15,state="readonly",font=("Calibri",16, "bold"),height=10)
    comb2["values"]=["select","கடன் தேதி","கடன் எண்","பெயர்","த/க பெயர்","ஊர்","கடன் தொகை","எடை","பொருள்","Phone No","மீட்ட தேதி"]
    comb2.grid(row=1,column=4,padx=2,pady=2)
    comb2.set("select")
    
    combtxt2=Entry(search_frame,font=lblfont,width=15)
    combtxt2.grid(row=1,column=5,pady=5)

    

    btnEdit = Button(search_frame, command=detail, text="search", width=15, font=("Calibri", 16, "bold"),
                 fg="white", bg="#2980b9",
                 bd=0).grid(row=1, column=6, padx=10)
    
 ############# search frame : END #########################   


############## tree frame : Start  ##########################

def detail():
        global tree_frame
        
        try:
            tree_frame.destroy()
            update_frame.destroy()
        except:
            pass
        try:
            tkinterest_frameme.destroy()  
        except:
            pass

        selected_value_clear()

        id=comb.get()
        c_val=combtxt.get()

        id1=comb1.get()
        c_val1=combtxt1.get()

        id2=comb2.get()
        c_val2=combtxt2.get()
        #db
        dict_id={"கடன் தேதி":"loan_date","கடன் எண்":"bill_no","பெயர்":"name","த/க பெயர்":"co_name","ஊர்":"address","கடன் தொகை":"int_amt","எடை":"weight","பொருள்":"item","Phone No":"phone_no","மீட்ட தேதி":"release_date"}
        
        filter_data = {dict_id[key]: value for key, value in [(id, c_val), (id1, c_val1), (id2, c_val2)] if key != "select"}

        
        print(filter_data)
         

        
        
        load_data=find_records_by_multiple_fields(filter_data)

        # if dict_id[id] in like_list:
        #     load_data=read_records_alike(dict_id[id],c_val)       #return alike searched value 
        # else:
        #     load_data=read_records_by_field(dict_id[id],c_val)       #return exact to searched value

        if not load_data:
            messagebox.showwarning(title="error",message="no data found")
            return search()
            

        
        style=ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",highlightthicknes=0,font=('calibri',13),)
        style.configure("Treeview.Heading",highlightthicknes=0,font=('calibri',13,'bold'))
        
        tree_frame=Frame(bill,bg="#535c68")
        tree_frame.pack(side=TOP,fill="both",expand=False)
        treescroll=ttk.Scrollbar(tree_frame,orient="vertical")
        treescroll.pack(side="right",fill="y")
        
        # style=ttk.Style()
        # style.configure("mystyle.treeview",font=("Calibri", 16, "bold"),rowheight=50)
        global tree
        tree=ttk.Treeview(tree_frame,columns=(1,2,3,4,5,6,7,8,9,10,11,12),yscrollcommand=treescroll.set)
        v=["கடன் தேதி","கடன் எண்","பெயர்","த/க பெயர்","தெரு","ஊர்","கடன் தொகை","எடை","பொருள்","மொத்த பொருள்","Phone No","மீட்ட தேதி"]
        col=[1,2,3,4,5,6,7,8,9,10,11,12]
        for i in range(0,12):
            tree.heading(f"{col[i]}",text=v[i])
            tree.column(f"{col[i]}",width=5)
        tree["show"]="headings"
        tree.pack(fill="both")
        treescroll.config(command=tree.yview)
        

        up=LabelFrame(tree_frame,text="")
        up.pack(side="bottom",fill="both")
        upbutton=Button(up,text="update",command=tkupdate).grid(row=0,column=0,padx=5)
        delbutton=Button(up,text="delete",command=tkdelete).grid(row=0,column=1,padx=5)
        intbutton=Button(up,text="interest",command=tkinterest).grid(row=0,column=2,padx=5)
        pributton=Button(up,text="reprint",command=reprint).grid(row=0,column=3,padx=5)
        
        
        # set searched result to tree frame
        for data in load_data:
            try:
                data["loan_date"]=datechange(data["loan_date"])
                if data["release_date"] is not None:
                    data["release_date"]=datechange(data["release_date"])
            except:
                pass 
            data=list(data.values())[1:]            #to remove id , get ony data      
            tree.insert('',END,values=data)

        tree.bind("<Double-1>", select_tree)        #selete row by 'double click' on that row goes to function 'selected_tree'


########### tree frame : END ######################


def select_tree(event):
            i=tree.item(tree.focus())  #getting value from selected row and assign it to variable
            global selected_value
            selected_value=i["values"]
            bill1.set(selected_value[1])
            date1.set(selected_value[0])
            name1.set(selected_value[2])
            coname1.set(selected_value[3])
            street1.set(selected_value[4])
            address1.set(selected_value[5])
            item1.set(selected_value[8])
            weight1.set(selected_value[7])
            amount1.set(selected_value[6])
            noitem1.set(selected_value[9])
            relese1.set(selected_value[11])
            phvar.set(selected_value[10])
            if selected_value[11]==None or selected_value[11]==NONE or selected_value[11]=="None":
                intrel.set(tday)
            else:
                intrel.set(selected_value[11])   


############## Update frame : Start  ##############################

def tkupdate():
    global update_frame
    try:
        billing_frame.destroy()
    except:
        pass
    try:
        tkinterest_frameme.destroy()
    except:
        pass
     
    

    update_frame=Frame(bill,bg="#535c68")
    update_frame.pack(side="bottom",fill=X,pady=(5,50),padx=(5,20))

    title= Label(update_frame, text="update", font=( "Calibri", 16, "bold"),bg="#535c68")
    title.grid(row=0, columnspan=2,padx=5,pady=5)
        

    lblbill=Label(update_frame,text="கடன் எண்",font=lblfont,bg="#535c68")
    lblbill.grid(row=1,column=1,pady=5,padx=10)
    txtbill=Entry(update_frame,font=lblfont,width=20,textvariable=bill1)
    txtbill.grid(row=1,column=2,pady=5,padx=10)

    lbldate=Label(update_frame,text="தேதி",font=lblfont,bg="#535c68")
    lbldate.grid(row=1,column=3,pady=5,padx=10)
    txtdate=Entry(update_frame,font=lblfont,width=20,textvariable=date1)
    txtdate.grid(row=1,column=4,pady=5,padx=10)

    lblname=Label(update_frame,text="பெயர்",font=lblfont,bg="#535c68")
    lblname.grid(row=2,column=1,pady=5,padx=10)
    txtname=Entry(update_frame,font=lblfont,width=20,textvariable=name1)
    txtname.grid(row=2,column=2,pady=5,padx=10)


    lblconame=Label(update_frame,text="த/க பெயர்",font=lblfont,bg="#535c68")
    lblconame.grid(row=2,column=3,pady=5,padx=10)
    txtconame=Entry(update_frame,font=lblfont,width=20,textvariable=coname1)
    txtconame.grid(row=2,column=4,pady=5,padx=10)

    lblstreet=Label(update_frame,text="தெரு",font=lblfont,bg="#535c68")
    lblstreet.grid(row=3,column=1,pady=5,padx=10)
    txtstreet=Entry(update_frame,font=lblfont,width=20,textvariable=street1)
    txtstreet.grid(row=3,column=2,pady=5,padx=10)

    lbladress=Label(update_frame,text="ஊர்",font=lblfont,bg="#535c68")
    lbladress.grid(row=4,column=1,pady=5,padx=10)
    txtadress=Entry(update_frame,font=lblfont,width=20,textvariable=address1)
    txtadress.grid(row=4,column=2,pady=5,padx=10)

    lblitem=Label(update_frame,text="பொருள்",font=lblfont,bg="#535c68")
    lblitem.grid(row=3,column=5,pady=5,padx=10)
    txtitem=Entry(update_frame,font=lblfont,width=20,textvariable=item1)
    txtitem.grid(row=3,column=6,pady=5,padx=10)

    lblweight=Label(update_frame,text="எடை",font=lblfont,bg="#535c68")
    lblweight.grid(row=2,column=5,pady=5,padx=10)
    txtweight=Entry(update_frame,font=lblfont,width=20,textvariable=weight1)
    txtweight.grid(row=2,column=6,pady=5,padx=10)

    lblamount=Label(update_frame,text="கடன் தொகை",font=lblfont,bg="#535c68")
    lblamount.grid(row=1,column=5,pady=5,padx=10)
    txtamount=Entry(update_frame,font=lblfont,width=20,textvariable=amount1)
    txtamount.grid(row=1,column=6,pady=5,padx=10)

    lblnoitem=Label(update_frame,text="மொத்த பொருள்",font=lblfont,bg="#535c68")
    lblnoitem.grid(row=4,column=5,pady=5,padx=10)
    txtnoitem=Entry(update_frame,font=lblfont,width=20,textvariable=noitem1)
    txtnoitem.grid(row=4,column=6,pady=5,padx=10)

    lblph=Label(update_frame,text="Phone No",font=lblfont,bg="#535c68")
    lblph.grid(row=4,column=3,pady=5,padx=10)
    txtph=Entry(update_frame,font=lblfont,width=20,textvariable=phvar)
    txtph.grid(row=4,column=4,pady=5,padx=10)

    lblrelese=Label(update_frame,text="மீட்ட தேதி",font=lblfont,bg="#535c68")
    lblrelese.grid(row=3,column=3,pady=5,padx=10)
    txtrelese=Entry(update_frame,font=lblfont,width=20,textvariable=relese1)
    txtrelese.grid(row=3,column=4,pady=5,padx=10)
   

    def updat():
        bill=txtbill.get()
        date=datechange(txtdate.get())
        name=txtname.get()
        coname=txtconame.get()
        street=txtstreet.get()
        address=txtadress.get()
        item=txtitem.get()
        weight=txtweight.get()
        amount=txtamount.get()
        noitem=txtnoitem.get()
        phno=txtph.get()
        if len(str(phno))!=10:
            messagebox.showwarning(title="error",message="ph number invalid")
            return tkupdate()
           
        relese=datechange(txtrelese.get())
        if relese!="None":
            try:
                relese=(datetime.strptime(relese,"%d-%m-%Y")).strftime("%d-%m-%Y")
            except:
                relese=""

        sdate=(datetime.strptime(date,"%d-%m-%Y")).strftime("%Y-%m-%d")
        if relese !="None":
            srelese=(datetime.strptime(relese,"%d-%m-%Y")).strftime("%Y-%m-%d")
        else:
            srelese=None

        dlist=[date,bill,name,coname,street,address,amount,weight,item,noitem,phno,relese] #for excell

        up_data = {
                "loan_date":sdate, "bill_no":bill, "name":name, "co_name":coname, "street":street, "address":address,
                "int_amt":amount, "weight":weight, "item":item, "no_item":noitem, "phone_no":phno,"release_date":srelese
        }
        if messagebox.askyesno(title="update",message="conform to update"):
            #db

            update_record(selected_value[1],up_data)

            
            alter(selected_value[1],dlist)
            messagebox.showinfo(title="update",message="update copleted")
            selected_value_clear()
            return detail()
    
    btnEdit = Button(update_frame, command=updat, text="update", width=15, font=("Calibri", 16, "bold"),
                    fg="white", bg="#2980b9",
                    bd=0).grid(row=0, column=5, padx=10)

########################  Update frame : END ##############################################################
       


################## interest frame : Start ####################################################################       
def tkinterest():
    global tkinterest_frameme
    try:
        billing_frame.destroy()
    except:
        pass
    try:
        update_frame.destroy()
    except:
        pass
    try:
        tkinterest_frameme.destroy()
    except:
        pass

    
   
    
    tkinterest_frameme=Frame(bill,bg="#535c68")
    tkinterest_frameme.pack(side="bottom",fill=X,pady=(5,10))

    title= Label(tkinterest_frameme, text="interest", font=( "Calibri", 16, "bold"),bg="#535c68")
    title.grid(row=0, columnspan=2,padx=5,pady=5)
        

    lblbill=Label(tkinterest_frameme,text="கடன் எண்",font=lblfont,bg="#535c68")
    lblbill.grid(row=1,column=1)
    txtbill=Entry(tkinterest_frameme,font=lblfont,width=20,textvariable=bill1)
    txtbill.grid(row=1,column=2,pady=5)

    lbldate=Label(tkinterest_frameme,text="தேதி",font=lblfont,bg="#535c68")
    lbldate.grid(row=1,column=3)
    txtdate=Entry(tkinterest_frameme,font=lblfont,width=20,textvariable=date1)
    txtdate.grid(row=1,column=4,pady=5)

    lblname=Label(tkinterest_frameme,text="பெயர்",font=lblfont,bg="#535c68")
    lblname.grid(row=2,column=1)
    txtname=Entry(tkinterest_frameme,font=lblfont,width=20,textvariable=name1)
    txtname.grid(row=2,column=2,pady=5)


    lblconame=Label(tkinterest_frameme,text="த/க பெயர்",font=lblfont,bg="#535c68")
    lblconame.grid(row=2,column=3)
    txtconame=Entry(tkinterest_frameme,font=lblfont,width=20,textvariable=coname1)
    txtconame.grid(row=2,column=4,pady=5)

    lbladress=Label(tkinterest_frameme,text="ஊர்",font=lblfont,bg="#535c68")
    lbladress.grid(row=3,column=1)
    txtadress=Entry(tkinterest_frameme,font=lblfont,width=20,textvariable=address1)
    txtadress.grid(row=3,column=2,pady=5)

    lblitem=Label(tkinterest_frameme,text="பொருள்",font=lblfont,bg="#535c68")
    lblitem.grid(row=3,column=3)
    txtitem=Entry(tkinterest_frameme,font=lblfont,width=20,textvariable=item1)
    txtitem.grid(row=3,column=4,pady=5)

    lblweight=Label(tkinterest_frameme,text="எடை",font=lblfont,bg="#535c68")
    lblweight.grid(row=4,column=1)
    txtweight=Entry(tkinterest_frameme,font=lblfont,width=20,textvariable=weight1)
    txtweight.grid(row=4,column=2,pady=5)

    lblamount=Label(tkinterest_frameme,text="Amount",font=lblfont,bg="#535c68")
    lblamount.grid(row=4,column=3)
    txtamount=Entry(tkinterest_frameme,font=lblfont,width=20,textvariable=amount1)
    txtamount.grid(row=4,column=4,pady=5)

    lblnoitem=Label(tkinterest_frameme,text="மொத்த பொருள்",font=lblfont,bg="#535c68")
    lblnoitem.grid(row=5,column=1)
    txtnoitem=Entry(tkinterest_frameme,font=lblfont,width=20,textvariable=noitem1)
    txtnoitem.grid(row=5,column=2,pady=5)

    lbltoday=Label(tkinterest_frameme,text="மீட்பு தேதி",font=lblfont,bg="#535c68")
    lbltoday.grid(row=5,column=3)
    txttoday=Entry(tkinterest_frameme,font=lblfont,width=20,textvariable=intrel)
    txttoday.grid(row=5,column=4,pady=5)

    intpay=StringVar()
    totpay=StringVar()
        
    
    

    def intcal():
        bill=txtbill.get()
        date=datechange(txtdate.get())
        name=txtname.get()
        coname=txtconame.get()
        address=txtadress.get()
        item=txtitem.get()
        weight=txtweight.get()
        amount=txtamount.get()
        noitem=txtnoitem.get()
        redate=datechange(txttoday.get())
        if redate==None:
            messagebox.showwarning(title="release date",message="enter release date")
        elif redate!=tday:
            messagebox.showwarning(title="loan released",message=f"loan released on {redate}")
            return
           

        dlist=[date,bill,name,coname,address,amount,weight,item,noitem]
        
        interestamt=interest(amount,date,redate)
        
        
        lblinterest=Label(tkinterest_frameme,text="interest",font=lblfont,bg="#535c68")
        lblinterest.grid(row=1,column=6)
        txtinterest=Entry(tkinterest_frameme,font=lblfont,width=20,textvariable=intpay)
        txtinterest.grid(row=1,column=7,pady=5)

        lbltotal=Label(tkinterest_frameme,text="total",font=lblfont,bg="#535c68")
        lbltotal.grid(row=2,column=6)
        txttotal=Label(tkinterest_frameme,font=lblfont,width=20)
        txttotal.grid(row=2,column=7,pady=5)
        totl=float(interestamt)+float(amount)
        intpay.set(interestamt)
        txttotal['text']=totl
        def tt():
            global totl
            totl=float(txtinterest.get())+float(amount)
            txttotal['text']=int(totl)
            


        btnint=Button(tkinterest_frameme,command=tt,text="total",width=5).grid(row=1,column=8)
        
        
        # paylist=[name,date,bill,amount,redate,int(txtinterest.get()),totl,selected _value[12]]
        
        def payint():
            paylist=[name,date,bill,amount,redate,int(txtinterest.get()),txttotal['text']]
        
            c=messagebox.askyesno(title="print",message="do  you want to print")
            interestprint(paylist,c)

            xlupdate_release(bill,redate)
            #db
            sqldate=(datetime.strptime(redate,"%d-%m-%Y")).strftime("%Y-%m-%d")
            update_release(bill,sqldate)
            
            return detail()
            

        btnEdit = Button(tkinterest_frameme, command=payint, text="pay", width=15, font=("Calibri", 16, "bold"),
                    fg="white", bg="#2980b9",
                    bd=0).grid(row=3, column=7, padx=10)
        
        


    btnEdit = Button(tkinterest_frameme, command=intcal, text="interest", width=15, font=("Calibri", 16, "bold"),
                    fg="white", bg="#2980b9",
                    bd=0).grid(row=6, column=4, padx=10)

################## interest Frame : END ######################



################ main frame continous #################

btnEdit = Button(head_frame, command=loan, text="loan", width=15, font=("Calibri", 16, "bold"),height=-5,
                 fg="white", bg="#2980b9",
                 bd=0).grid(row=1, column=1,pady=1,padx=10)


btnEdit = Button(head_frame, command=search, text="search", width=15, font=("Calibri", 16, "bold"),height=-5,
                 fg="white", bg="#2980b9",
                 bd=0).grid(row=1, column=2,pady=1,padx=10)



################################## Search page code : END  ###############################################################################

bill.mainloop()