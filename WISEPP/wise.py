import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import sqlite3
import timetable_stud
import timetable_fac
import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from subprocess import call
from PIL import Image, ImageTk
def subjects():
    # inputs in this window
    subcode = subname = subtype = None

    # create treeview (call this function once)
    def create_treeview():
        tree['columns'] = ('one', 'two', 'three')
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("one", width=70, stretch=tk.NO)
        tree.column("two", width=300, stretch=tk.NO)
        tree.column("three", width=60, stretch=tk.NO)
        tree.heading('#0', text="")
        tree.heading('one', text="Code")
        tree.heading('two', text="Name")
        tree.heading('three', text="Type")

    # update treeview (call this function after each update)
    def update_treeview():
        for row in tree.get_children():
            tree.delete(row)
        cursor = conn.execute("SELECT * FROM SUBJECTS")
        for row in cursor:
            if row[2] == 'T':
                t = 'Theory'
            elif row[2] == 'P':
                t = 'Practical'
            tree.insert(
                "",
                0,
                values=(row[0], row[1], t)
            )
        tree.place(x=500, y=100)

    # Parse and store data into the database and treeview upon clicking of the add button
    def parse_data():
        subcode = str(subcode_entry.get())
        subname = str(subname_entry.get("1.0", tk.END)).upper().rstrip()
        subtype = str(radio_var.get()).upper()

        if subcode == "":
            subcode = None
        if subname == "":
            subname = None

        if subcode is None or subname is None:
            messagebox.showerror("Bad Input", "Please fill up Subject Code and/or Subject Name!")
            subcode_entry.delete(0, tk.END)
            subname_entry.delete("1.0", tk.END)
            return

        conn.execute(f"REPLACE INTO SUBJECTS (SUBCODE, SUBNAME, SUBTYPE) VALUES ('{subcode}','{subname}','{subtype}')")
        conn.commit()
        update_treeview()

        subcode_entry.delete(0, tk.END)
        subname_entry.delete("1.0", tk.END)

    # update a row in the database
    def update_data():
        subcode_entry.delete(0, tk.END)
        subname_entry.delete("1.0", tk.END)
        try:
            if len(tree.selection()) > 1:
                messagebox.showerror("Bad Select", "Select one subject at a time to update!")
                return

            row = tree.item(tree.selection()[0])['values']
            subcode_entry.insert(0, row[0])
            subname_entry.insert("1.0", row[1])
            if row[2][0] == "T":
                R1.select()
            elif row[2][0] == "P":
                R2.select()

            conn.execute(f"DELETE FROM SUBJECTS WHERE SUBCODE = '{row[0]}'")
            conn.commit()
            update_treeview()

        except IndexError:
            messagebox.showerror("Bad Select", "Please select a subject from the list first!")
            return

    # remove selected data from the database and treeview
    def remove_data():
        if len(tree.selection()) < 1:
            messagebox.showerror("Bad Select", "Please select a subject from the list first!")
            return
        for i in tree.selection():
            conn.execute(f"DELETE FROM SUBJECTS WHERE SUBCODE = '{tree.item(i)['values'][0]}'")
            conn.commit()
            tree.delete(i)
            update_treeview()

    # database connections and setup
    # connecting database
    conn = sqlite3.connect("timetable.db")

    # TKinter Window
    subtk = tk.Tk()
    subtk.geometry('1000x450')
    subtk.title("subjects")
    subtk.title('Add/Update Subjects')

    # Label1
    tk.Label(
        subtk,
        text='List of Subjects',
        font=('Consolas', 20, 'bold')
    ).place(x=600, y=50)

    # Label2
    tk.Label(
        subtk,
        text='Add/Update Subjects',
        font=('Consolas', 20, 'bold')
    ).place(x=100, y=50)

    # Label3
    tk.Label(
        subtk,
        text='Add information in the following prompt!',
        font=('Consolas', 10, 'italic')
    ).place(x=100, y=85)

    # Label4
    tk.Label(
        subtk,
        text='Subject code:',
        font=('Consolas', 15)
    ).place(x=100, y=150)

    # Entry1
    subcode_entry = tk.Entry(
        subtk,
        font=('Consolas', 15),
        width=11
    )
    subcode_entry.place(x=270, y=150)

    # Label5
    tk.Label(
        subtk,
        text='Subject Name:',
        font=('Consolas', 15)
    ).place(x=100, y=200)

    # Text
    subname_entry = tk.Text(
        subtk,
        font=('Consolas', 10),
        width=17,
        height=3,
        wrap=tk.WORD
    )
    subname_entry.place(x=270, y=200)

    # Label6
    tk.Label(
        subtk,
        text='Subject Type:',
        font=('Consolas', 15)
    ).place(x=100, y=270)

    # RadioButton variable to store RadioButton Status
    radio_var = tk.StringVar()

    # RadioButton1
    R1 = tk.Radiobutton(
        subtk,
        text='Theory',
        font=('Consolas', 12),
        variable=radio_var,
        value="T"
    )
    R1.place(x=270, y=270)
    R1.select()

    # RadioButton2
    R2 = tk.Radiobutton(
        subtk,
        text='Practical',
        font=('Consolas', 12),
        variable=radio_var,
        value="P"
    )
    R2.place(x=270, y=300)
    R2.select()

    # Button1
    B1 = tk.Button(
        subtk,
        text='Add Subject',
        font=('Consolas', 12),
        command=parse_data
    )
    B1.place(x=150, y=350)

    # Button2
    B2 = tk.Button(
        subtk,
        text='Update Subject',
        font=('Consolas', 12),
        command=update_data
    )
    B2.place(x=410, y=350)

    # Treeview1
    tree = ttk.Treeview(subtk)
    create_treeview()
    update_treeview()

    # Button3
    B3 = tk.Button(
        subtk,
        text='Delete Subject(s)',
        font=('Consolas', 12),
        command=remove_data
    )
    B3.place(x=650, y=350)

    # looping Tkiniter window
    subtk.mainloop()
    conn.close()  # close database after all operations

# Call the subjects function when the script is executed



def admin_interface():
    def run_sub(): call(["python","subjects.py"])
    def run_fac(): call(["python","faculty.py"])
    def run_stud(): call(["python","student.py"])
    def run_sch(): call(["python","scheduler.py"])
    def run_tt_s(): call(["python","timetable_stud.py"])
    def run_tt_f(): call(["python","timetable_fac.py"])

    ad = tk.Tk()
    ad.geometry('500x430')
    ad.title('Administrator')

    tk.Label(
        ad,
        text='A D M I N I S T R A T O R',
        font=('Consolas', 20, 'bold'),
        pady=10
    ).pack()

    tk.Label(
        ad,
        text='You are the Administrator',
        font=('Consolas', 12, 'italic'),
    ).pack(pady=9)

    modify_frame = tk.LabelFrame(text='Modify', font=('Consolas'), padx=20)
    modify_frame.place(x=50, y=100)

    tk.Button(
        modify_frame,
        text='Subjects',
        font=('Consolas'),
        command=run_sub
    ).pack(pady=20)

    tk.Button(
        modify_frame,
        text='Faculties',
        font=('Consolas'),
        command=run_fac
    ).pack(pady=20)

    tk.Button(
        modify_frame,
        text='Students',
        font=('Consolas'),
        command=run_stud
    ).pack(pady=20)

    tt_frame = tk.LabelFrame(text='Timetable', font=('Consolas'), padx=20)
    tt_frame.place(x=250, y=100)

    tk.Button(
        tt_frame,
        text='Schedule Periods',
        font=('Consolas'),
        command=run_sch
    ).pack(pady=20)

    tk.Button(
        tt_frame,
        text='View Section-Wise',
        font=('Consolas'),
        command=run_tt_s
    ).pack(pady=20)

    tk.Button(
        tt_frame,
        text='View Faculty-wise',
        font=('Consolas'),
        command=run_tt_f
    ).pack(pady=20)

    tk.Button(
        ad,
        text='Quit',
        font=('Consolas'),
        command=ad.destroy
    ).place(x=220, y=360)
    ad.mainloop()

def challenge():
    conn = sqlite3.connect("timetable.db")
    user = str(combo1.get())
    if user == "Student":
        cursor = conn.execute(f"SELECT PASSW, SECTION, NAME, ROLL FROM STUDENT WHERE SID='{id_entry.get()}'")
        cursor = list(cursor)
        if len(cursor) == 0:
            messagebox.showwarning('Bad id', 'No such user found!')
        elif passw_entry.get() != cursor[0][0]:
            messagebox.showerror('Bad pass', 'Incorret Password!')
        else:
            nw = tk.Tk()
            tk.Label(
                nw,
                text=f'{cursor[0][2]}\tSection: {cursor[0][1]}\tRoll No.: {cursor[0][3]}',
                font=('Consolas', 12, 'italic'),
            ).pack()
            # m.destroy()
            timetable_stud.student_tt_frame(nw, cursor[0][1])
            nw.mainloop()


    elif user == "Faculty":
        cursor = conn.execute(f"SELECT PASSW, INI, NAME, EMAIL FROM FACULTY WHERE FID='{id_entry.get()}'")
        cursor = list(cursor)
        if len(cursor) == 0:
            messagebox.showwarning('Bad id', 'No such user found!')
        elif passw_entry.get() != cursor[0][0]:
            messagebox.showerror('Bad pass', 'Incorret Password!')
        else:
            nw = tk.Tk()
            tk.Label(
                nw,
                text=f'{cursor[0][2]} ({cursor[0][1]})\tEmail: {cursor[0][3]}',
                font=('Consolas', 12, 'italic'),
            ).pack()
            # m.destroy()
            timetable_fac.fac_tt_frame(nw, cursor[0][1])
            nw.mainloop()

    elif user == "Admin":
        if id_entry.get() == 'admin' and passw_entry.get() == 'admin':
            m.destroy()
            admin_interface()
        else:
            messagebox.showerror('Bad Input', 'Incorrect Username/Password!')

m = tk.Tk()

m.geometry('400x430')
m.title('Welcome')

tk.Label(
    m,
    text='TIMETABLE MANAGEMENT SYSTEM',
    font=('Consolas', 20, 'bold'),
    wrap=400
).pack(pady=20)

tk.Label(
    m,
    text='Welcome!\nLogin to continue',
    font=('Consolas', 12, 'italic')
).pack(pady=10)

tk.Label(
    m,
    text='Username',
    font=('Consolas', 15)
).pack()

id_entry = tk.Entry(
    m,
    font=('Consolas', 12),
    width=21
)
id_entry.pack()

# Label5
tk.Label(
    m,
    text='Password:',
    font=('Consolas', 15)
).pack()

# toggles between show/hide password
def show_passw():
    if passw_entry['show'] == "●":
        passw_entry['show'] = ""
        B1_show['text'] = '●'
        B1_show.update()
    elif passw_entry['show'] == "":
        passw_entry['show'] = "●"
        B1_show['text'] = '○'
        B1_show.update()
    passw_entry.update()

pass_entry_f = tk.Frame()
pass_entry_f.pack()
# Entry2
passw_entry = tk.Entry(
    pass_entry_f,
    font=('Consolas', 12),
    width=15,
    show="●"
)
passw_entry.pack(side=tk.LEFT)

B1_show = tk.Button(
    pass_entry_f,
    text='○',
    font=('Consolas', 12, 'bold'),
    command=show_passw,
    padx=5
)
B1_show.pack(side=tk.LEFT, padx=15)

combo1 = ttk.Combobox(
    m,
    values=['Student', 'Faculty', 'Admin']
)
combo1.pack(pady=15)
combo1.current(0)

tk.Button(
    m,
    text='Login',
    font=('Consolas', 12, 'bold'),
    padx=30,
    command=challenge
).pack(pady=10)
m.resizable(False,False)
ico = Image.open(r"C:/Users/JYOSHNA/Downloads/logo.jpeg")
photo = ImageTk.PhotoImage(ico)
m.wm_iconphoto(False, photo)
m.mainloop()
