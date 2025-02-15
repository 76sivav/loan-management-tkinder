from flask import Flask, request, jsonify, render_template,redirect,url_for,flash

from tkdatabase import *
from tkdblist import *
from tkprint import *
from tkdbprocess import *

app = Flask(__name__)
app.secret_key = "your_secret_key" 

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template("home.html")


@app.route('/newloan', methods=['GET', 'POST'])
def loan_form():
    if request.method == 'POST':
        # Retrieve all form data as a dictionary
        form_data = request.form.to_dict()

        # Optionally, you can process specific fields if necessary
        form_data['int_amt'] = float(form_data['int_amt']) if 'int_amt' in form_data else None
        form_data['weight'] = float(form_data['weight']) if 'weight' in form_data else None
        form_data['no_item'] = int(form_data['no_item']) if 'no_item' in form_data else None
        
        insert_record(form_data)
        ws_save(form_data)
        loanprint(form_data,True)
            
        # For debugging, print the JSON data
        print("Received JSON data:", form_data)

        # Return the data as a JSON response
        jsonify({"status": "success", "data": form_data})
        return render_template('loan.html')

    # Render the form
    return render_template('loan.html')  # Save your HTML file as 'loan.html'

@app.route('/viewloan', methods=['GET', 'POST'])
def get_loan():
    key_list={"கடன் தேதி":"loan_date","கடன் எண்":"bill_no","பெயர்":"name","த/க பெயர்":"co_name",
             "ஊர்":"address","கடன் தொகை":"int_amt","எடை":"weight","பொருள்":"item",
             "Phone No":"phone_no","மீட்ட தேதி":"release_date"}
    if request.method == 'POST':
        # Retrieve all form data as a dictionary
        form_data = request.form.to_dict()
        print(form_data)
        criteria = [
        (form_data["search1"], form_data["s1_value"]),
        (form_data["search2"], form_data["s2_value"]),
        (form_data["search3"], form_data["s3_value"])
        ]

        filter_data = {key: value for key, value in criteria if key != "select"}
        loan_data=find_records_by_multiple_fields(filter_data)
            
        # For debugging, print the JSON data
        print("Received JSON data:", loan_data)

        # Return the data as a JSON response
        jsonify({"status": "success", "data": loan_data})
        return render_template('view.html',records=loan_data,klist=key_list)

    # Render the form
  
    return render_template('view.html',klist=key_list)  # Save your HTML file as 'loan.html'

@app.route('/updateloan/<num>', methods=['GET', 'POST'])
def update_loan(num):
    if request.method == 'POST':
        # Retrieve all form data as a dictionary
        form_data = request.form.to_dict()

        loan_data=update_record(num,form_data)
            
        # For debugging, print the JSON data
        print("Received JSON post data:", loan_data)

        # Return the data as a JSON response
        jsonify({"status": "success", "data": loan_data})
        return redirect(url_for('get_loan'))
    
    else:
        loan_data=read_records_by_field("bill_no",num)
        # For debugging, print the JSON data
        print("Received JSON data:", loan_data)
        # Return the data as a JSON response
        jsonify({"status": "success", "data": loan_data})
        return render_template('update.html',data=loan_data[0])



@app.route('/deleteloan/<num>', methods=['GET', 'POST'])
def delete_loan(num):
        loan_data=delete_record(num)
        flash("Record deleted successfully!", "success")
        # For debugging, print the JSON data
        print("Received JSON data:", loan_data)
        # Return the data as a JSON response
        jsonify({"status": "success", "data": loan_data})
        return redirect(url_for('get_loan'))

@app.route('/reprintloan/<num>', methods=['GET', 'POST'])
def reprint_loan(num):
        loan_data=read_records_by_field("bill_no",num)

        loanprint(loan_data[0],True,"reprint")
        # For debugging, print the JSON data
        print("Received JSON data:", loan_data)
        # Return the data as a JSON response
        jsonify({"status": "success", "data": loan_data})
        return redirect(url_for('get_loan'))

@app.route('/loaninterest/<num>', methods=['GET', 'POST'])
def loan_interest(num):
    if request.method == 'POST':
        if request.form["submit"]=="total_cal":
        # Retrieve all form data as a dictionary
            form_data = request.form.to_dict()

            interest_value=interest(form_data['int_amt'],form_data['loan_date'],form_data['release_date'],form_data['int_rate'],form_data['reduce_amt'])
            total=interest_value['total']
            interest_amt=interest_value['interest']
            no_days=interest_value['days']
            form_data.update(interest_value)
            print(interest_value)
            print(form_data)
                
            # For debugging, print the JSON data
            print("Received JSON data:", form_data)

            # Return the data as a JSON response
            jsonify({"status": "success", "data": interest_value})
            return render_template('interest.html',data=form_data)
        
        elif request.form["submit"]=="final":
            form_data = request.form.to_dict()

            interestprint(form_data,True)
            xlupdate_release(form_data ['bill_no'], form_data ['release_date'])

            sqldate = (datetime.strptime(form_data ['release_date'], "%d-%m-%Y")).strftime("%Y-%m-%d")
            update_release(form_data ['bill_no'], sqldate)
            # For debugging, print the JSON data
            print("Received JSON final data:", form_data)

            # Return the data as a JSON response
            jsonify({"status": "success", "data": form_data})
            return redirect(url_for('home'))

    # Render the form
    else:
        loan_data=(read_records_by_field("bill_no",num))[0]
        if loan_data['release_date']==None or loan_data['release_date']=="None":
             loan_data['release_date']=(date.today()).strftime('%d-%m-%Y') 
        # For debugging, print the JSON data
        print("Received JSON data:", loan_data)
        # Return the data as a JSON response
        jsonify({"status": "success", "data": loan_data})
        return render_template('interest.html',data=loan_data)

if __name__ == '__main__':
    app.run(debug=True)
