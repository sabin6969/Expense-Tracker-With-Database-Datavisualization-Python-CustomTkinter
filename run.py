import tkinter as tk
import customtkinter as ctk
import mysql.connector
import validators
from tkinter import messagebox
import smtplib
import random
import pdb
import tkcalendar
from datetime import datetime, timedelta
from tkinter import ttk
import matplotlib.pyplot as plt
import warnings


class ExpenseTracerApp:
    def __init__(self):
        self.landing_window = ctk.CTk()
        self.landing_window.geometry("450x350")
        self.landing_window.title("Expense Tracer | Login | Signup")
        self.landing_window.resizable(False, False)
        self.connection = mysql.connector.connect(
            host="localhost", username="root", password="poudeL46@", database="registered_users_expense_tracer")
        # Email Entry Box
        self.email_entry_box = ctk.CTkEntry(
            self.landing_window, placeholder_text="Enter Valid Email", width=170)
        self.email_entry_box.place(x=250, y=50)
        self.email_entry_box.focus()
        # Password Entry Box
        self.password_entry_box = ctk.CTkEntry(
            self.landing_window, placeholder_text="Password", width=170, show="*")
        self.password_entry_box.place(x=250, y=90)

        def login():
            self.login_user()

        def newuser():
            self.signup()
        # Old User Button
        self.login_button = ctk.CTkButton(
            self.landing_window, text="Login", command=login, width=170)
        self.login_button.place(x=250, y=140)
        # Adding Image
        expense_image = tk.PhotoImage(file="main image.png")
        expense_image_label = tk.Label(image=expense_image)
        expense_image_label.place(x=0, y=10)
        # Or Label
        self.or_label = ctk.CTkLabel(self.landing_window, text="OR")
        self.or_label.place(x=330, y=170)
        # New User Button
        self.new_user_button = ctk.CTkButton(
            self.landing_window, text="New User?", width=170, command=newuser)
        self.new_user_button.place(x=250, y=200)
        # dark mode call back function

        def dark():
            ctk.set_appearance_mode("Dark")
        # light mode call back function

        def light():
            ctk.set_appearance_mode("Light")

        # Switching between two modes
        # Dark Mode
        dark_mode_button = ctk.CTkButton(
            self.landing_window, text="Dark Mode", fg_color="black", width=20, command=dark)
        dark_mode_button.place(x=250, y=5)
        # Light Mode
        light_mode_button = ctk.CTkButton(
            self.landing_window, text="Light Mode", fg_color="white", width=20, text_color="black", command=light)
        light_mode_button.place(x=340, y=5)
        self.landing_window.mainloop()

    def login_sucess(self, email):
        logged_in_window = ctk.CTk()
        logged_in_window.geometry('600x500')
        logged_in_window.resizable(False, False)
        logged_in_window.title("Expense Tracer | Home")
        cursor = self.connection.cursor()
        query = f"select db_name from registered_users where email='{email}'"
        cursor.execute(query)
        database_name = cursor.fetchone()[0]
        connection_with_indivisual_database = mysql.connector.connect(
            host="localhost", username="root", password="poudeL46@", database=f"{database_name}")
        option_frame = ctk.CTkFrame(
            logged_in_window, height=500, width=150, fg_color="#0fffef")
        # Home button callback function

        def home():
            self.main_window_frame.destroy()
            self.main_window_frame = ctk.CTkFrame(
                logged_in_window, height=500, width=450)
            self.main_window_frame.place(x=150, y=0)
            logged_in_window.title("Expense Tracer | Home")
            # Home Label
            home_label = ctk.CTkLabel(
                self.main_window_frame, text="Home", font=("sans serif", 19, "bold"))
            home_label.place(x=210, y=5)
            # Your Expense at Glance labels
            # Getting Starting and ending date
            current_date = datetime.now()
            first_day = current_date.replace(day=1)
            next_month = (current_date.replace(day=28) +
                          timedelta(days=4)).replace(day=1)
            last_day = next_month - timedelta(days=1)
            first_day = first_day.strftime("%Y-%m-%d")
            last_day = last_day.strftime("%Y-%m-%d")
            max_expense = None
            min_expense = None
            total_expense_all_time = None
            expense_this_month = None
            cursor = connection_with_indivisual_database.cursor()
            query_to_find_max_expense = "select expense_category,expense_amount from expenses where expense_amount=(select max(expense_amount) from expenses);"
            query_to_find_min_expense = "select expense_category,expense_amount from expenses where expense_amount = (select min(expense_amount) from expenses);"
            query_to_find_total_expense = "select sum(expense_amount) from expenses;"
            query_to_find_expense_this_month = f"select sum(expense_amount) from expenses where date_added between '{first_day}' and '{last_day}';"
            cursor.execute(
                query_to_find_total_expense)
            total_expense_all_time = cursor.fetchone()
            cursor.reset()
            cursor.execute(
                query_to_find_expense_this_month)
            expense_this_month = cursor.fetchone()
            cursor.reset()
            try:
                if None not in total_expense_all_time or None not in expense_this_month:
                    total_expense_all_time_label = ctk.CTkLabel(
                        self.main_window_frame, text=f"Your total expense recorded {total_expense_all_time[0]}", font=("sans serif", 15, "bold"))
                    total_expense_all_time_label.place(x=110, y=140)
                    expense_this_month_label = ctk.CTkLabel(
                        self.main_window_frame, text=f"Your total expense this month {expense_this_month[0]}", font=("sans serif", 15, "bold"))
                    expense_this_month_label.place(x=110, y=165)
                    progress_bar = ctk.CTkProgressBar(
                        self.main_window_frame, orientation="horizontal", mode="indeterminate")
                    progress_bar.place(x=130, y=200)
                    progress_bar.start()
                else:
                    info2_label = ctk.CTkLabel(
                        self.main_window_frame, text="Add Expenses to See snippet", font=("sans serif", 15))
                    info2_label.place(x=135, y=140)
                    # Show this progress bar if user is new
                    progress_bar = ctk.CTkProgressBar(
                        self.main_window_frame, orientation="horizontal", mode="indeterminate")
                    progress_bar.place(x=130, y=170)
                    progress_bar.start()
            except:
                info2_label = ctk.CTkLabel(
                    self.main_window_frame, text="Add Expenses to See snippet", font=("sans serif", 15))
                info2_label.place(x=150, y=140)
                # Show this progress bar if user is new
                progress_bar = ctk.CTkProgressBar(
                    self.main_window_frame, orientation="horizontal", mode="indeterminate")
                progress_bar.place(x=130, y=170)
                progress_bar.start()

        home_button = ctk.CTkButton(
            option_frame, text="Home", width=140, bg_color="#0fffef", command=home)
        home_button.place(x=5, y=5)
        # ---------------Add Expense Callback function-----------------------#

        def add_expense():
            # ---------Add Expense------------#
            self.main_window_frame.destroy()
            logged_in_window.title("Expense Tracer | Add Expense")
            self.main_window_frame = ctk.CTkFrame(
                logged_in_window, height=500, width=450)
            self.main_window_frame.place(x=150, y=0)
            add_expense_label = ctk.CTkLabel(
                self.main_window_frame, text="Add Expense", font=("Futura", 20, 'bold'))
            add_expense_label.place(x=160, y=5)
            expense_title_label = ctk.CTkLabel(
                self.main_window_frame, text="Expense Title", font=("Futura", 12))
            expense_title_label.place(x=40, y=40)
            expense_title_entry = ctk.CTkEntry(
                self.main_window_frame, placeholder_text="Expense Title", width=160, corner_radius=5, height=10)
            expense_title_entry.place(x=150, y=40)
            select_date_label = ctk.CTkLabel(
                self.main_window_frame, text="Select Date", font=("Futura", 12))
            select_date_label.place(x=40, y=70)
            date_picker = tkcalendar.DateEntry(
                self.main_window_frame, width=21, height=30)
            date_picker.place(x=190, y=90)
            # Expense Category label
            select_expense_category_label = ctk.CTkLabel(
                self.main_window_frame, text="Select Category", font=("Futura", 12))
            select_expense_category_label.place(
                x=40, y=100)
            # Expense Category drop down
            expense_category_dropdown = ctk.CTkComboBox(
                self.main_window_frame, width=160, values=["Rent", "Education", "Insurance", "Entertainment", "Other"], state="readonly")
            expense_category_dropdown.set("Rent")
            expense_category_dropdown.place(x=150, y=100)
            # Expense amount
            expense_amount_label = ctk.CTkLabel(
                self.main_window_frame, text="Expense Amount", font=("Futura", 12))
            expense_amount_label.place(x=40, y=140)
            expense_amount_entry = ctk.CTkEntry(
                self.main_window_frame, placeholder_text="Expense Amount", width=160, corner_radius=5, height=10)
            expense_amount_entry.place(x=150, y=140)
            # submit expense details call back function

            def submit_expense_details():
                self.submit_expense_details_button.place(x=150, y=170)
                expense_title = expense_title_entry.get()
                date_of_expense_added = str(date_picker.get_date())
                expense_category = expense_category_dropdown.get()
                expense_amount = expense_amount_entry.get()

                users_entry = (expense_title, date_of_expense_added,
                               expense_category, expense_amount)
                # To check wheather the input field is empty or not

                def isEmpty(data):
                    return len(data)
                result = map(isEmpty, users_entry)
                result = list(result)
                try:
                    if 0 in result:
                        messagebox.showerror(
                            "Required", "All Input fields are required")
                    else:
                        expense_amount = int(expense_amount)
                        query = f'insert into expenses values ("{expense_title}","{date_of_expense_added}","{expense_category}","{expense_amount}");'
                        cursor = connection_with_indivisual_database.cursor()
                        cursor.execute(query)
                        connection_with_indivisual_database.commit()
                        messagebox.showinfo(
                            "Sucess", "Record Inserted Sucessfully")
                        expense_title_entry.delete(0, ctk.END)
                        expense_amount_entry.delete(0, ctk.END)

                except ValueError:
                    messagebox.showerror(
                        "Error", "Number is expected in amount field")
                    expense_amount_entry.delete(0, tk.END)
                except:
                    messagebox.showerror(
                        "Error", "Error While inserting data into database")
            self.submit_expense_details_button = ctk.CTkButton(
                self.main_window_frame, text="Add", width=160, command=submit_expense_details)
            self.submit_expense_details_button.place(x=150, y=170)
            # ------------------End of add expense callback function------------------#
        add_expense_button = ctk.CTkButton(
            logged_in_window, text="Add Expense", width=140, bg_color="#0fffef", command=add_expense)
        add_expense_button.place(x=5, y=65)

        def visualize_expense():
            self.main_window_frame.destroy()
            warnings.filterwarnings("ignore")
            logged_in_window.title("Expense Tracer | Visualize Expense")
            self.main_window_frame = ctk.CTkFrame(
                logged_in_window, height=500, width=450)
            self.main_window_frame.place(x=150, y=0)
            categories = ["Rent", "Education",
                          "Insurance", "Entertainment", "Other"]
            cursor = connection_with_indivisual_database.cursor()
            expenses = []
            query_to_find_total_expense_in_rent = "select sum(expense_amount) from expenses where expense_category='Rent';"
            cursor.execute(query_to_find_total_expense_in_rent)
            rent_expense = cursor.fetchone()
            cursor.reset()
            expenses.append(rent_expense)
            query_to_find_total_expense_in_education = "select sum(expense_amount) from expenses where expense_category='Education';"
            cursor.execute(query_to_find_total_expense_in_education)
            education_expense = cursor.fetchone()
            cursor.reset()
            expenses.append(education_expense)
            query_to_find_total_expense_insurance = "select sum(expense_amount) from expenses where expense_category='insurance';"
            cursor.execute(query_to_find_total_expense_insurance)
            insurance_expense = cursor.fetchone()
            cursor.reset()
            expenses.append(insurance_expense)
            query_to_find_total_expense_in_entertainment = "select sum(expense_amount) from expenses where expense_category='Entertainment';"
            cursor.execute(query_to_find_total_expense_in_entertainment)
            entertainment_expense = cursor.fetchone()
            cursor.reset()
            expenses.append(entertainment_expense)
            query_to_find_total_expense_in_others = "select sum(expense_amount) from expenses where expense_category='Other';"
            cursor.execute(query_to_find_total_expense_in_others)
            other_expenses = cursor.fetchone()
            expenses.append(other_expenses)
            expense_amount_only = [i[0] for i in expenses]
            try:
                plt.figure(figsize=(4, 4))
                plt.pie(expense_amount_only, labels=categories,
                        autopct='%1.1f%%', startangle=90)
                plt.axis('equal')
                plt.title('Expense Distribution')
                # Save the pie chart as an image
                plt.savefig('expense_pie_chart.png', dpi=100)
                plt.close()
                image = tk.PhotoImage(file="expense_pie_chart.png")
                image_label = ctk.CTkLabel(self.main_window_frame, image=image)
                image_label.place(x=40, y=40)
            except:
                info2_label = ctk.CTkLabel(
                    self.main_window_frame, text="Add expenses of all category to visualize", font=("sans serif", 15))
                info2_label.place(x=110, y=140)
                progress_bar = ctk.CTkProgressBar(
                    self.main_window_frame, orientation="horizontal", mode="indeterminate")
                progress_bar.place(x=135, y=170)
                progress_bar.start()

            # -----------------End of Visualize Expense function------------#
        visualize_expense_button = ctk.CTkButton(
            logged_in_window, text="Visualize Expense", width=140, bg_color="#0fffef", command=visualize_expense)
        visualize_expense_button.place(x=5, y=125)
        # Delete Expense Call Back function

        def delete_expense():
            self.main_window_frame.destroy()
            logged_in_window.title("Expense Tracer | Delete Expense")
            self.main_window_frame = ctk.CTkFrame(
                logged_in_window, height=500, width=450)
            self.main_window_frame.place(x=150, y=0)
            delete_expense_label = ctk.CTkLabel(
                self.main_window_frame, text="Delete Expense", font=("sans serif", 19, "bold"))
            delete_expense_label.place(x=160, y=5)
            # Search expense by Category
            search_expense_by_category_label = ctk.CTkLabel(
                self.main_window_frame, text="Search Expense by Category")
            search_expense_by_category_label.place(x=160, y=40)
            search_by_category_combobox = ctk.CTkComboBox(self.main_window_frame, width=160, values=[
                                                          "Rent", "Education", "Insurance", "Entertainment", "Other"], state="readonly")
            search_by_category_combobox.set("Rent")
            search_by_category_combobox.place(x=160, y=70)

        # End of Delete Expense Callback function
        delete_expense_button = ctk.CTkButton(
            logged_in_window, text="Delete Expense", width=140, bg_color="#0fffef", command=delete_expense)
        delete_expense_button.place(x=5, y=185)
        self.main_window_frame = ctk.CTkFrame(
            logged_in_window, height=500, width=450)
        self.main_window_frame.place(x=150, y=0)

        def show_all_expense_log():
            self.main_window_frame.destroy()
            logged_in_window.title("Expense Trace | Expense Log")
            self.main_window_frame = ctk.CTkFrame(
                logged_in_window, height=500, width=450)
            self.main_window_frame.place(x=150, y=0)
            your_expense_log_label = ctk.CTkLabel(
                self.main_window_frame, text="Your Expense Log", font=("sans serif", 19, "bold"))
            your_expense_log_label.place(x=150, y=5)
            tree = ttk.Treeview(self.main_window_frame, height=25, columns=(
                "Title", "Date", "Category", "Amount"))
            tree.column("#0", width=0)
            tree.column("Title", width=140)
            tree.column("Date", width=120)
            tree.column("Category", width=125)
            tree.column("Amount", width=120)
            tree.heading("Title", text="Title")
            tree.heading("Date", text="Date")
            tree.heading("Category", text="Category")
            tree.heading("Amount", text="Amount")
            tree.place(x=20, y=50)
            cursor = connection_with_indivisual_database.cursor()
            query = "select * from expenses;"
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.reset()
            sum = 0
            for row in rows:
                tree.insert("", "end", text="", values=(
                    row[0], row[1], row[2], row[3]))
                sum += row[3]
            else:
                row = ["", "", "Total Amount-->", f"{sum}"]
                tree.insert("", "end", text="", values=(
                    row[0], row[1], row[2], row[3]))
        show_all_expense_log_button = ctk.CTkButton(
            option_frame, text="Show All Expense Log", command=show_all_expense_log)
        show_all_expense_log_button.place(x=5, y=245)
        option_frame.place(x=0, y=0)
        logged_in_window.mainloop()

    def login_user(self):
        user_email = self.email_entry_box.get()
        user_email = user_email.strip()
        user_password = self.password_entry_box.get()
        if len(user_email) != 0 and len(user_password) != 0:
            isValid = validators.email(user_email)
            if isValid is True:
                cursor = self.connection.cursor()
                query = f"Select email,password from registered_users where email='{user_email}' and password='{user_password}'"
                cursor.execute(query)
                data = cursor.fetchall()
                try:
                    if user_email == data[0][0] and user_password == data[0][1]:
                        messagebox.showinfo("Sucess", "Login Sucess")
                        # -----------------------------------------------#_________________
                        self.landing_window.destroy()
                        self.login_sucess(user_email)
                    else:
                        messagebox.showerror(
                            "Incorrect", "Incorrect Email or Password")
                        self.email_entry_box.delete(0, tk.END)
                        self.password_entry_box.delete(0, tk.END)
                except:
                    messagebox.showerror(
                        "Incorrect", "Incorrect Email or Password")
                    self.email_entry_box.delete(0, tk.END)
                    self.password_entry_box.delete(0, tk.END)
            else:
                messagebox.showerror(
                    "Invlalid Email", "Invalid email provided")
                self.email_entry_box.delete(0, tk.END)
                self.password_entry_box.delete(0, tk.END)
        else:
            messagebox.showerror("Required", "Both Input Fields are Required")

    def signup(self):
        self.email_entry_box.destroy()
        self.password_entry_box.destroy()
        self.login_button.destroy()
        self.new_user_button.destroy()
        self.or_label.destroy()
        # create account call back function

        # verify call back function

        def verify():
            def create_account():
                entered_otp = self.otp_entry_box.get()
                entered_password = self.password_define_entry.get()
                confirm_password = self.confirm_passwor_entry_box.get()
                generatedotp = otp
                database_to_be_generated = entered_mail.split("@")
                if len(entered_otp) == 0 or len(entered_password) == 0 or len(confirm_password) == 0:
                    messagebox.showerror(
                        "Required", "Fill All the input fileds")
                else:
                    if entered_otp == generatedotp:
                        if entered_password == confirm_password:
                            try:
                                cursor = self.connection.cursor()
                                db = ""
                                for i in database_to_be_generated:
                                    db += i
                                db = db.replace('.com', '')
                                db = db.replace('.', '')
                                query = f"Insert into registered_users values('{entered_mail}','{entered_password}','{db}')"
                                cursor.execute(query)
                                self.connection.commit()
                                messagebox.showinfo(
                                    "Sucess", "Account Created, now you can login")
                            except:
                                messagebox.showerror(
                                    "Account is Already Created", "Your Account has already been created proceed towards login")
                            else:
                                def login_after_signup():
                                    def new_login_again():
                                        self.login_after_account_creation()
                                    self.login_button_after_signup.destroy()
                                    self.otp_entry_box.destroy()
                                    self.create_account_button.destroy()
                                    self.confirm_passwor_entry_box.destroy()
                                    self.password_define_entry.place(
                                        x=250, y=80)
                                    self.new_login_button = ctk.CTkButton(
                                        self.landing_window, text="Login", width=170, command=new_login_again)
                                    self.new_login_button.place(x=250, y=110)
                                    self.password_define_entry.configure(
                                        state="disabled")
                                    self.email_entry.configure(
                                        state="disabled")
                                self.login_button_after_signup = ctk.CTkButton(
                                    self.landing_window, text="Login", command=login_after_signup, width=170)
                                self.login_button_after_signup.place(
                                    x=250, y=200)
                        else:
                            messagebox.showwarning(
                                "Didnot Matched", "Password Didnot Matched")
                            self.password_define_entry.delete(0, tk.END)
                            self.confirm_passwor_entry_box.delete(0, tk.END)
                    else:
                        messagebox.showerror("Error", "OTP didnot matched")
                        self.otp_entry_box.delete(0, tk.END)
            # --------------------------------------End of function--------------------------------------------#
            entered_mail = self.email_entry.get()
            entered_mail = entered_mail.strip()
            isValid = validators.email(entered_mail)
            if isValid:
                if len(entered_mail) != 0:
                    cursor = self.connection.cursor()
                    query = f"select email from registered_users where email='{entered_mail}'"
                    cursor.execute(query)
                    result = cursor.fetchall()
                    if (len(result) == 1):
                        messagebox.showerror(
                            "Already Registered", "This email address is already registered.")
                    else:
                        try:
                            connection = smtplib.SMTP("smtp.gmail.com", 587)
                            connection.ehlo()
                            connection.starttls()
                            connection.login(
                                "youremail@gmail.com", "passwordforthatemail")
                            otp = ""
                            for i in range(4):
                                otp += str(random.randrange(0, 9, 1))
                            connection.sendmail(
                                "youremail@gmail.com", f"{entered_mail}", f"Subject: Regarding OTP \n\nYour One time Password is {otp}\nDo not share it with others\nif you have not requested for otp ignore it")

                        except:
                            messagebox.showerror(
                                "Failed to Mail", "Failed to Send Mail Check Your internet Status")
                        else:
                            verify_email_button.destroy()
                            messagebox.showinfo(
                                "Sucess", "Check Email for Otp")
                            self.otp_entry_box = ctk.CTkEntry(
                                self.landing_window, placeholder_text="Enter OTP", width=170)
                            self.otp_entry_box.place(x=250, y=80)
                            self.password_define_entry = ctk.CTkEntry(
                                self.landing_window, placeholder_text="Define Your Password", width=170, show="*")
                            self.password_define_entry.place(x=250, y=110)
                            self.confirm_passwor_entry_box = ctk.CTkEntry(
                                self.landing_window, placeholder_text="Confirm Password", width=170, show="*")
                            self.confirm_passwor_entry_box.place(x=250, y=140)
                            self.create_account_button = ctk.CTkButton(
                                self.landing_window, text="Create Account", width=170, command=create_account)
                            self.create_account_button.place(x=250, y=170)
                else:
                    messagebox.showerror("Required", "Email is Required")
            else:
                messagebox.showerror(
                    "Invalid", "Invalid Email Address Provided")
        self.email_entry = ctk.CTkEntry(
            self.landing_window, placeholder_text="Enter a Valid Email id", width=170)
        self.email_entry.place(x=250, y=50)
        verify_email_button = ctk.CTkButton(
            self.landing_window, text="verify", width=40, command=verify)
        verify_email_button.place(x=400, y=50)

    def login_after_account_creation(self):
        try:
            user_entered_mail = self.email_entry.get()
            cursor = self.connection.cursor()
            query = f"Select db_name from registered_users where email='{user_entered_mail}' "
            cursor.execute(query)
            database_to_be_created = cursor.fetchone()[0]
            query = f"create database {database_to_be_created}"
            cursor.execute(query)
            self.connection.commit()
            self.connection_with_new_db = mysql.connector.connect(
                host="localhost", user="root", password="poudeL46@", database=f"{database_to_be_created}")
            query_to_create_new_table = 'create table expenses (expense_title_entry varchar(255), date_added date, expense_category varchar(20),expense_amount int);'
            cursor = self.connection_with_new_db.cursor()
            cursor.execute(query_to_create_new_table)
            self.connection_with_new_db.commit()
            self.landing_window.destroy()
            self.login_sucess(user_entered_mail)
        except:
            messagebox.showinfo("Login", "You can now login into your account")
            self.landing_window.destroy()
            self.login_sucess(user_entered_mail)


if __name__ == "__main__":
    app = ExpenseTracerApp()
