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
    for frame in ["search_frame", "tree_frame", "update_frame", "tkinterest_frameme", "billing_frame"]:
        try:
            globals()[frame].destroy()
        except KeyError:
            pass

    selected_value_clear() #clear variable values

    new_bill_no=int(find_max_bill_no())+1  #get last bill number from database .tkdatabase fn

    billing_frame=Frame(bill,bg="#535c68")
    billing_frame.pack(side=TOP,fill=X)

    title= Label(billing_frame, text="new loan", font=( "Calibri", 16, "bold"),bg="#535c68",height=0)
    title.grid(row=0, columnspan=2,padx=20,pady=20)

    # Input Fields
    def create_input(label_text, row, var, bind_event=False):
        Label(billing_frame, text=label_text, font=lblfont, bg="#535c68").grid(row=row, column=1)
        entry = Entry(billing_frame, font=lblfont, width=20, textvariable=var)
        entry.grid(row=row, column=2, pady=5)
        if bind_event:
            entry.bind("<1>", select_time)

    create_input("தேதி", 1, date1, bind_event=True)
    date1.set(tday)

    create_input("கடன் எண்", 2, bill1)
    try:
        bill1.set(new_bill_no)            #to check bill number is not none
    except:
        bill.set("000")

    create_input("பெயர்", 3, name1)
    create_input("த/க பெயர்", 4, coname1)
    create_input("தெரு", 5, street1)
    create_input("ஊர்", 6, address1)
    create_input("கடன் தொகை", 7, amount1)
    create_input("பொருள்", 8, item1)
    create_input("எடை", 9, weight1)
    create_input("மொத்த பொருள்", 10, noitem1)
    create_input("Phone No.", 11, phvar)


    ############################# code to add data ###################################
    def new_loan():    #funtion for add new value after all ok
        ### to check input values is ok       
        try:
            bill = int(bill1.get())                                 #check it is integer and if it already stored
            if check_bill_no_exists(bill):
                messagebox.showwarning(title="error",message="bill number exit")

                c=messagebox.askyesno(title="new bill no",
                                      message=f"next bill no is {new_bill_no} click yes to select this number")
                if c:
                    bill1.set(new_bill_no)
                    bill=new_bill_no
                else:
                    raise Error
                            
            amount = int(amount1.get())
            weight = float(weight1.get())
            no_items = int(noitem1.get())
            phone_no = phvar.get()
            if len(phone_no) != 10 or not phone_no.isdigit():
                raise ValueError("Invalid phone number")
            
            loan_data = {
                "loan_date": date1.get(),
                "bill_no": bill,
                "name": name1.get(),
                "co_name": coname1.get(),
                "street": street1.get(),
                "address": address1.get(),
                "int_amt": amount,
                "weight": weight,
                "item": item1.get(),
                "no_item": no_items,
                "phone_no": phone_no
            }
            loan_ok=messagebox.askyesno(title="save",message="do you want to save")
            if loan_ok:
                insert_record(loan_data)
                ws_save(loan_data)
                loanprint(loan_data, messagebox.askyesno("Print", "Do you want to print?"))
            loan()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
           
        
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
    for frame in ["search_frame", "tree_frame", "update_frame", "tkinterest_frameme", "billing_frame"]:
        try:
            globals()[frame].destroy()
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
        
        for frame in ["tree_frame", "update_frame", "tkinterest_frameme"]:
            try:
                globals()[frame].destroy()
            except:
                pass

        selected_value_clear()

        # Collect search criteria
        criteria = [
        (comb.get(), combtxt.get()),
        (comb1.get(), combtxt1.get()),
        (comb2.get(), combtxt2.get())
        ]
        #db
        dict_id={"கடன் தேதி":"loan_date","கடன் எண்":"bill_no","பெயர்":"name","த/க பெயர்":"co_name","ஊர்":"address","கடன் தொகை":"int_amt","எடை":"weight","பொருள்":"item","Phone No":"phone_no","மீட்ட தேதி":"release_date"}
        
        filter_data = {dict_id[key]: value for key, value in criteria if key != "select"}

        
        load_data=find_records_by_multiple_fields(filter_data)

        # if dict_id[id] in like_list:
        #     load_data=read_records_alike(dict_id[id],c_val)       #return alike searched value 
        # else:
        #     load_data=read_records_by_field(dict_id[id],c_val)       #return exact to searched value

        if not load_data:
            messagebox.showwarning(title="error",message="no data found")
            return search()
            

        #tree frame
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
        tree_header=["கடன் தேதி","கடன் எண்","பெயர்","த/க பெயர்","தெரு","ஊர்","கடன் தொகை","எடை","பொருள்","மொத்த பொருள்","Phone No","மீட்ட தேதி"]
        col=[1,2,3,4,5,6,7,8,9,10,11,12]
        for i in range(0,12):
            tree.heading(f"{col[i]}",text=tree_header[i])
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

    # Destroy existing frames if they exist
    for frame in ["billing_frame", "tkinterest_frameme"]:
        try:
            globals()[frame].destroy()
        except:
            pass

    # Create the update frame
    update_frame = Frame(bill, bg="#535c68")
    update_frame.pack(side="bottom", fill=X, pady=(5, 50), padx=(5, 20))

    # Title
    Label(update_frame, text="update", font=("Calibri", 16, "bold"), bg="#535c68").grid(row=0, columnspan=2, padx=5, pady=5)

    # Input fields and labels
    field_data = {
        "bill": ("கடன் எண்", bill1, 1, 1),
        "date": ("தேதி", date1, 1, 3),
        "name": ("பெயர்", name1, 2, 1),
        "coname": ("த/க பெயர்", coname1, 2, 3),
        "street": ("தெரு", street1, 3, 1),
        "address": ("ஊர்", address1, 4, 1),
        "item": ("பொருள்", item1, 3, 5),
        "weight": ("எடை", weight1, 2, 5),
        "amount": ("கடன் தொகை", amount1, 1, 5),
        "noitem": ("மொத்த பொருள்", noitem1, 4, 5),
        "phno": ("Phone No", phvar, 4, 3),
        "relese": ("மீட்ட தேதி", relese1, 3, 3),
    }

    entry_widgets = {}  # Dictionary to store Entry widget references

    for key, (label_text, var, row, column) in field_data.items():
        Label(update_frame, text=label_text, font=lblfont, bg="#535c68").grid(row=row, column=column, pady=5, padx=10)
        entry_widgets[key] = Entry(update_frame, font=lblfont, width=20, textvariable=var)
        entry_widgets[key].grid(row=row, column=column + 1, pady=5, padx=10)

    # Update logic
    def updat():
        # Retrieve values from fields
        values = {key: widget.get() for key, widget in entry_widgets.items()}

        if len(values["phno"]) != 10:
            messagebox.showwarning(title="error", message="Phone number invalid")
            return tkupdate()

        try:
            values["relese"] = (datetime.strptime(values["relese"], "%d-%m-%Y")).strftime("%d-%m-%Y") if values["relese"] != "None" else ""
        except:
            pass
        
        # values["sdate"] = (datetime.strptime(values["date"], "%d-%m-%Y")).strftime("%Y-%m-%d")
        # try:
        #     values["srelese"] = (datetime.strptime(values["relese"], "%d-%m-%Y")).strftime("%Y-%m-%d") if values["relese"] != "None" or values["relese"] != " " else None
        # except:
        #     values["srelese"]=None

        dlist = [values[key] for key in ["date", "bill", "name", "coname", "street", "address", "amount", "weight", "item", "noitem", "phno", "relese"]]
        up_data = {
            "loan_date": values["date"], "bill_no": values["bill"], "name": values["name"], "co_name": values["coname"],
            "street": values["street"], "address": values["address"], "int_amt": values["amount"], "weight": values["weight"],
            "item": values["item"], "no_item": values["noitem"], "phone_no": values["phno"], "release_date": values["relese"]
        }

        if messagebox.askyesno(title="update", message="confirm to update"):
            try:
                stat=update_record(selected_value[1], up_data)
                if stat[0]:
                    messagebox.showinfo(title="update", message=stat[1])
                else:
                    messagebox.showinfo(title="update", message=stat[1])
                    raise Error

                alter(selected_value[1], dlist)
                messagebox.showinfo(title="update", message="Update completed")
                selected_value_clear()
                return detail()
            except:
                pass

    # Update button
    Button(update_frame, command=updat, text="update", width=15, font=("Calibri", 16, "bold"), fg="white", bg="#2980b9", bd=0).grid(row=0, column=5, padx=10)

########################  Update frame : END ##############################################################
       


################## interest frame : Start ####################################################################   

def tkinterest():
    global tkinterest_frameme

    # Destroy existing frames if they exist
    for frame in ["billing_frame", "update_frame", "tkinterest_frameme"]:
        try:
            globals()[frame].destroy()
        except:
            pass

    # Create the interest frame
    tkinterest_frameme = Frame(bill, bg="#535c68")
    tkinterest_frameme.pack(side="bottom", fill=X, pady=(5, 10))

    # Title
    Label(tkinterest_frameme, text="Interest", font=("Calibri", 16, "bold"), bg="#535c68").grid(row=0, columnspan=2, padx=5, pady=5)

    # Field definitions
    field_data = {
        "bill": ("கடன் எண்", bill1, 1, 1),
        "date": ("தேதி", date1, 1, 3),
        "name": ("பெயர்", name1, 2, 1),
        "coname": ("த/க பெயர்", coname1, 2, 3),
        "address": ("ஊர்", address1, 3, 1),
        "item": ("பொருள்", item1, 3, 3),
        "weight": ("எடை", weight1, 4, 1),
        "amount": ("கடன் தொகை", amount1, 4, 3),
        "noitem": ("மொத்த பொருள்", noitem1, 4, 1),
        "relese": ("மீட்ட தேதி", intrel, 5, 3),
    }

    entry_widgets = {}  # Dictionary to store Entry widget references

    for key, (label_text, var, row, column) in field_data.items():
        Label(tkinterest_frameme, text=label_text, font=lblfont, bg="#535c68").grid(row=row, column=column, pady=5, padx=10)
        entry_widgets[key] = Entry(tkinterest_frameme, font=lblfont, width=20, textvariable=var)
        entry_widgets[key].grid(row=row, column=column + 1, pady=5, padx=10)

    # Variables for interest calculation
    intpay = StringVar()
    int_rate = StringVar()
    reduce_amt=StringVar()
    int_rate.set("1.5")
    reduce_amt.set("0")

    def intcal():
        try:
            # Gather input values from entry_widgets
            inputs = {key: widget.get() for key, widget in entry_widgets.items()}

            bill = inputs["bill"]
            date = datechange(inputs["date"])
            name = inputs["name"]
            coname = inputs["coname"]
            address = inputs["address"]
            item = inputs["item"]
            weight = inputs["weight"]
            amount = float(inputs["amount"]) if inputs["amount"] else 0
            noitem = inputs["noitem"]
            redate = datechange(inputs["relese"])
            amount1.set(amount)

            if redate==None or redate=="none":
                messagebox.showwarning(title="Release Date", message="Enter release date")
                return

            if redate != tday:
                messagebox.showwarning(title="Loan Released", message=f"Loan released on {redate}")
                return


            # Display interest and total
            Label(tkinterest_frameme, text="asal", font=lblfont, bg="#535c68").grid(row=1, column=6)
            txtinterest = Entry(tkinterest_frameme, font=lblfont, width=20, textvariable=amount1)
            txtinterest.grid(row=1, column=7, pady=5)

            Label(tkinterest_frameme, text="Interest_rate", font=lblfont, bg="#535c68").grid(row=2, column=6)
            txtinterest = Entry(tkinterest_frameme, font=lblfont, width=20, textvariable=int_rate)
            txtinterest.grid(row=2, column=7, pady=5)

            Label(tkinterest_frameme, text="reduce", font=lblfont, bg="#535c68").grid(row=3, column=6)
            txttotal = Entry(tkinterest_frameme, font=lblfont, width=20, textvariable=reduce_amt)
            txttotal.grid(row=3, column=7, pady=5)

            Label(tkinterest_frameme, text="Interest", font=lblfont, bg="#535c68").grid(row=4, column=6)
            txtinterest = Label(tkinterest_frameme, font=lblfont, width=20, textvariable=intpay)
            txtinterest.grid(row=4, column=7, pady=5)

            Label(tkinterest_frameme, text="Total", font=lblfont, bg="#535c68").grid(row=5, column=6)
            txttotal = Label(tkinterest_frameme, font=lblfont, width=20)
            txttotal.grid(row=5, column=7, pady=5)

            #to be called multi times for alter rate and reduce amount
            def cal_total():
                rate=int_rate.get()
                reduce_amount=reduce_amt.get() 
                release_amt = interest(amount, date, redate, rate,reduce_amount)
                intpay.set(release_amt["interest"])
                txttotal["text"] = release_amt["total"]

            #to get total ,interest
            cal_total()

            # Button to update interest rate
            Button(tkinterest_frameme, command=cal_total, text="rate", width=5).grid(row=2, column=8)

            # Button to update total
            Button(tkinterest_frameme, command=cal_total, text="reduce", width=5).grid(row=3, column=8)


            def pay_interest():
                paylist = [
                    name, date, bill, amount, redate, txtinterest["text"], txttotal["text"]
                ]

                confirm = messagebox.askyesno(title="Print", message="Do you want to print?")
                interestprint(paylist, confirm)
                xlupdate_release(bill, redate)

                sqldate = (datetime.strptime(redate, "%d-%m-%Y")).strftime("%Y-%m-%d")
                update_release(bill, sqldate)

                detail()

            # Pay button
            Button(tkinterest_frameme, command=pay_interest, text="Pay", width=15, font=("Calibri", 16, "bold"),
                   fg="white", bg="#2980b9", bd=0).grid(row=8, column=7, padx=10)

        except Exception as e:
            messagebox.showerror(title="Error", message=f"An error occurred: {str(e)}")

    # Button to calculate interest``
    Button(tkinterest_frameme, command=intcal, text="Interest", width=15, font=("Calibri", 16, "bold"),
           fg="white", bg="#2980b9", bd=0).grid(row=8, column=4, padx=10)


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