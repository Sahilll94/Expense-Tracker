from tkinter import *
from tkinter import ttk, messagebox
import datetime as dt
import matplotlib.pyplot as plt
from mydb import Database  # Assuming mydb.py contains the Database class


# Create the database object
data = Database(db='test.db')

# Global variables
count = 0
selected_rowid = 0

# Functions

def save_record():
    global data
    data.insertRecord(item_name=namevar.get(), item_price=amtvar.get(), purchase_date=dopvar.get())
    refresh_data()

def set_date():
    date = dt.datetime.now()
    dopvar.set(f'{date:%d %B %Y}')

def clear_entries():
    item_name.delete(0, 'end')
    item_amt.delete(0, 'end')
    transaction_date.delete(0, 'end')

def fetch_records():
    global count
    records = data.fetchRecord('select rowid, * from expense_record')
    for rec in records:
        tv.insert(parent='', index='0', iid=count, values=(rec[0], rec[1], rec[2], rec[3]))
        count += 1

def select_record(event):
    global selected_rowid
    selected = tv.focus()
    val = tv.item(selected, 'values')
    try:
        selected_rowid = val[0]
        d = val[3]
        namevar.set(val[1])
        amtvar.set(val[2])
        dopvar.set(str(d))
    except Exception as ep:
        pass

def update_record():
    global selected_rowid
    selected = tv.focus()
    try:
        data.updateRecord(namevar.get(), amtvar.get(), dopvar.get(), selected_rowid)
        tv.item(selected, text="", values=(namevar.get(), amtvar.get(), dopvar.get()))
    except Exception as ep:
        messagebox.showerror('Error',  ep)
    item_name.delete(0, END)
    item_amt.delete(0, END)
    transaction_date.delete(0, END)
    refresh_data()

def total_balance():
    total_expenses = data.fetchRecord("SELECT SUM(item_price) FROM expense_record")[0][0]
    if total_expenses is not None:
        balance_remaining = 5000 - total_expenses
        messagebox.showinfo('Current Balance', f"Total Expense: {total_expenses}\nBalance Remaining: {balance_remaining}")
    else:
        messagebox.showinfo('Current Balance', f"Total Expense: 0\nBalance Remaining: 5000")

def refresh_data():
    for item in tv.get_children():
        tv.delete(item)
    fetch_records()

def delete_row():
    global selected_rowid
    data.removeRecord(selected_rowid)
    refresh_data()

def display_pie_chart(item_names, item_prices, balance_remaining):
    # Data for the pie chart
    if item_names and item_prices:
        item_prices.append(balance_remaining)
        item_names.append("Balance Remaining")
        # Create a new figure for the pie chart
        fig, ax = plt.subplots()
        ax.pie(item_prices, labels=item_names, autopct='%1.1f%%', startangle=140)
        # Add a title
        plt.title('Expense Breakdown')
        # Display the pie chart
        plt.show()
    else:
        messagebox.showwarning("No Data", "No expense data available to display.")

# Create tkinter object
ws = Tk()
ws.title('Daily Expenses')

# Variables
f = ('Times new roman', 14)
namevar = StringVar()
amtvar = DoubleVar()
dopvar = StringVar()

# Frame widget
f2 = Frame(ws)
f2.pack() 

f1 = Frame(
    ws,
    padx=10,
    pady=10,
)
f1.pack(expand=True, fill=BOTH)

# Label widget
Label(f1, text='ITEM NAME', font=f).grid(row=0, column=0, sticky=W)
Label(f1, text='ITEM PRICE', font=f).grid(row=1, column=0, sticky=W)
Label(f1, text='PURCHASE DATE', font=f).grid(row=2, column=0, sticky=W)

# Entry widgets 
item_name = Entry(f1, font=f, textvariable=namevar)
item_amt = Entry(f1, font=f, textvariable=amtvar)
transaction_date = Entry(f1, font=f, textvariable=dopvar)

# Entry grid placement
item_name.grid(row=0, column=1, sticky=EW, padx=(10, 0))
item_amt.grid(row=1, column=1, sticky=EW, padx=(10, 0))
transaction_date.grid(row=2, column=1, sticky=EW, padx=(10, 0))

# Action buttons
cur_date = Button(f1, text='Current Date', font=f, bg='#04C4D9', command=set_date, width=15)
submit_btn = Button(f1, text='Save Record', font=f, command=save_record, bg='#04C4D9', fg='white')
clr_btn = Button(f1, text='Clear Entry', font=f, command=clear_entries, bg='#04C4D9', fg='white')
quit_btn = Button(f1, text='Exit', font=f, command=ws.destroy, bg='#04C4D9', fg='white')
total_bal = Button(f1, text='Total Balance', font=f, bg='#04C4D9', command=total_balance)
update_btn = Button(f1, text='Update', bg='#04C4D9', command=update_record, font=f)
del_btn = Button(f1, text='Delete', bg='#04C4D9', command=delete_row, font=f)

# grid placement
cur_date.grid(row=3, column=1, sticky=EW, padx=(10, 0))
submit_btn.grid(row=0, column=2, sticky=EW, padx=(10, 0))
clr_btn.grid(row=1, column=2, sticky=EW, padx=(10, 0))
quit_btn.grid(row=2, column=2, sticky=EW, padx=(10, 0))
total_bal.grid(row=0, column=3, sticky=EW, padx=(10, 0))
update_btn.grid(row=1, column=3, sticky=EW, padx=(10, 0))
del_btn.grid(row=2, column=3, sticky=EW, padx=(10, 0))

# Treeview widget
tv = ttk.Treeview(f2, columns=(1, 2, 3, 4), show='headings', height=8)
tv.pack(side="left")

# add heading to treeview
tv.column(1, anchor=CENTER, stretch=NO, width=70)
tv.column(2, anchor=CENTER)
tv.column(3, anchor=CENTER)
tv.column(4, anchor=CENTER)
tv.heading(1, text="Serial no")
tv.heading(2, text="Item Name")
tv.heading(3, text="Item Price")
tv.heading(4, text="Purchase Date")

# binding treeview
tv.bind("<ButtonRelease-1>", select_record)

# style for treeview
style = ttk.Style()
style.theme_use("default")
style.map("Treeview")

# Vertical scrollbar
scrollbar = Scrollbar(f2, orient='vertical')
scrollbar.configure(command=tv.yview)
scrollbar.pack(side="right", fill="y")
tv.config(yscrollcommand=scrollbar.set)

# calling function
fetch_records()

# Calculate total expenses and balance remaining
total_expenses = data.fetchRecord("SELECT SUM(item_price) FROM expense_record")[0][0]
balance_remaining = 5000 - total_expenses if total_expenses is not None else 5000

# Fetch item names and item prices
item_data = data.fetchRecord("SELECT item_name, item_price FROM expense_record")

if item_data:
    item_names, item_prices = zip(*item_data)  # Separate item names and item prices
    item_names = list(item_names)
    item_prices = list(item_prices)
else:
    item_names = []
    item_prices = []

# Display the pie chart inside the Daily Expenses window
display_pie_chart(item_names, item_prices, balance_remaining)

# Infinite loop
ws.mainloop()
