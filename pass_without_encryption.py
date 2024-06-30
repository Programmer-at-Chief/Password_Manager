from tkinter import *
from tkinter import messagebox
import pyperclip
import random
import json
import base64
import codecs

FONT=("Arial",15)
PINK = "#e2979c"
GREEN = "#9bdeac"
BLUE= '#1B81A8'
ORANGE= '#FC4301'
PASSWORD=""


# ---------------------------- Additional Windows ------------------------------- #

def empty_input():
    error_window=Tk()
    error_window.minsize(500,150)

    error_label=Label(error_window,font=FONT,text="Please don't leave any fields empty!")
    error_label.place(x=20,y=50)
    
    ok_button=Button(error_window,text="OK",font=FONT,bg=BLUE,command=lambda: error_window.destroy())
    ok_button.place(x=400,y=120)
    
    error_label.mainloop()
    
def incorrect_format():
    error_window=Tk()
    error_window.minsize(700,450)

    error_label=Label(error_window,justify="left",font=FONT,text="Please enter password satisfying there formats.")
    error_label.place(x=10,y=15)
    
    pass_format="""
/*-------------------------------------------------------------------*/\t\t
1. Must be 8-32 characters long.\t\t\t\t
2. Must include at least two of the following formats\t\t
    > At least one letter(Uppercase or Lowercase)\t\t\t
    > At least one number\t\t\t\t\t
    > At least one special character like $,#,*\t\t\t
3. Must no match your user id\t\t\t\t
4. Must not include more than two identical characters\t\t
5. Must not include more than two consecutive characters\t\t
/*-------------------------------------------------------------------*/\t\t
"""
    
    passformat_label=Label(error_window,font=FONT,text=pass_format)
    passformat_label.place(x=10,y=60)
    
    exit_button=Button(error_window,font=FONT,text="OK",command=lambda: error_window.destroy(),bg=GREEN)
    exit_button.place(x=600,y=400)

    error_label.mainloop()
    
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    pass_length=random.randrange(8,33)
    password=""
    alphabets="abcdefghijklmnopqrstuvwxyzABCDEFGHIJLMNOPQRSTUVWXYZ"
    symbols="@#$%&*()-=_+[]}<>{?;:"
    choice =random.randrange(0,3)
    if choice==0:
        password+=random.choice(alphabets)
        password+=f"{random.randrange(0,11)}"
    elif choice ==1:
        password+=random.choice(alphabets)
        password+=(random.choice(symbols))
    else:
        password+=(random.choice(symbols))
        password+=f"{(random.randrange(0,11))}"
    for i in range(pass_length-2):
        choice=random.randrange(3)
        if (choice ==0):
            password+=random.choice(alphabets)
        elif (choice ==1):
            password+=str(random.choice(symbols))
        else:
            password+=f"{(random.randrange(0,11))}"
    return password


def get_password():
    password=generate_password()
    while True:
        two_consecutive=True
        two_identical=True
        for i in range(len(password)-2):
            if (password.count(password[i])>=3):
                two_identical=False
            if (ord(password[i+2])-ord(password[i+1])==1 and ord(password[i+1])-ord(password[i])==1):
                two_consecutive=False
        if (two_consecutive and two_identical):
            break
        password=generate_password()

    global PASSWORD
    PASSWORD=password
    password_input.delete(0,'end')
    password_input.insert(0,PASSWORD)
    pyperclip.copy(PASSWORD)
    
    pass_copied=Label(text="Password copied to clipboard!!",font=FONT,bg=PINK)
    pass_copied.place(x=200,y=530)
    
    pass_copied.after(1000,lambda: pass_copied.destroy())
    # print(password," Length : ",len(password) )

# ---------------------------- SEARCH PASSWORD ------------------------------- #
def info(website,username,password):
    info_window=Tk()
    info_window.minsize(700,250)
    info_window.config(bg=GREEN)
    
    info_title=Label(info_window,font=FONT,text=f"{website} Info: ",bg=GREEN)
    info_title.place(x=260,y=10)
    
    username_label=Label(info_window,text=f"Username: {username}",font=FONT,bg=BLUE)
    username_label.place(x=50,y=60)
    password_label=Label(info_window,text=f"Password: {password}",font=FONT,bg=BLUE)
    password_label.place(x=50,y=120)


    copy_username=Button(info_window,text="Copy",font=("Arial",13),command=lambda: pyperclip.copy(username),bg=PINK)
    copy_username.place(x=600,y=55)
    copy_password=Button(info_window,text="Copy",font=("Arial",13),command=lambda: pyperclip.copy(password),bg=PINK)
    copy_password.place(x=600,y=115)
    
    ok=Button(info_window,text="OK",font=FONT,command=info_window.destroy,bg=PINK)
    ok.place(x=600,y=200)


    info_window.mainloop()



def search_for_entry():
    website=website_input.get()
    if (not website):
        error_label=Label(text="Enter a website to search for !",font=FONT,bg=PINK)
        error_label.place(x=250,y=530)
        
        error_label.after(2000,lambda: error_label.destroy())

    else:
        data=""
        try:
            with open("data.json","r") as file:
                data=json.load(file)
            if (website not in data):
                error_label=Label(text="Password not in file !",font=FONT,bg=PINK)
                error_label.place(x=300,y=530)
                
                error_label.after(2000,lambda: error_label.destroy())
            else:
                info(website,data[website]["Email"],data[website]["Password"])
                
                
        except:
            # messagebox.showwarning("Warning","Password file is empty!")
            error_label=Label(text="Password file is empty !",font=FONT,bg=PINK)
            error_label.place(x=300,y=530)
            
            error_label.after(2000,lambda: error_label.destroy())
       

# ---------------------------- SAVE PASSWORD ------------------------------- #
def display_info(website,username,password):
    info=Tk()
    info.minsize(600,300)
    
    to_be_displayed=f"Website: {website}\nUsername: {username}\nPassword: {password}\nIs this okay?"
    info_label=Label(info,text=to_be_displayed,font=FONT)
    info_label.place(x=50,y=50)
    
    
    send=False
    def to_send():
        info.destroy()
        nonlocal send
        send=True
        
    def not_to_send():
        info.destroy()
    
    cancel_button=Button(info,text="Cancel",font=FONT,command= not_to_send)
    cancel_button.place(x=50,y=250)
    
    ok_button=Button(info,text="OK",font=FONT,command=to_send)
    ok_button.place(x=400,y=250)
    

    info.mainloop()
    return send

def add_password():
    website=website_input.get()
    username=username_input.get()
    password=password_input.get()
    
    len_sat=False
    two_props=False
    no_user=False
    two_identical=True
    two_consecutive=True
    length=len(password)
    
    if (length>=8 and length<=32):
        len_sat=True

    one_letter=0
    one_number=0
    one_special=0
    for i in password:
        if (i.isupper() or i.islower()):
            one_letter=1
        elif (i.isdigit()):
            one_number=1
        else:
            one_special=1

    if (one_letter+one_number+one_special>=2):
        two_props=True

    if (username not in password):
        no_user=True

    for i in range(len(password)-2):
        if (password.count(password[i])>=3):
            two_identical=False
        if (ord(password[i+2])-ord(password[i+1])==1 and ord(password[i+1])-ord(password[i])==1):
            two_consecutive=False

    if (not website or not username or not password):
        empty_input()
    elif (len_sat and two_props and no_user and two_identical and two_consecutive):
        choice=display_info(website,username,password)
        # print(choice)
        if (choice):
            new_data={website:{
                "Email":username,
                "Password":password
            }}
            try:
                with open("data.json",'r') as file:
                    data=json.load(file)
            except:
                with open("data.json",'w') as file:
                    json.dump(new_data,file,indent=4)
            else:
                data.update(new_data)
                with open("data.json",'w') as file:
                    # file.write(f"{website} | {username} | {password}\n")
                    # data=json.load(file)
                    json.dump(data,file, indent=4)
                    # data=json.load(file)
                    # print(data)
            finally:
                pass
                # password_input.delete(0,'end')
                # website_input.delete(0,'end')
                # username_input.delete(0,'end')
        else:
            pass
    else:
        incorrect_format()
        

# ---------------------------- UI SETUP ------------------------------- #

window=Tk()
window.minsize(800,600)
window.config(bg=PINK)
window.title("My Pass")

canvas=Canvas(width=200,height=220,bg=PINK,highlightthickness=0)
try:
    image_logo=PhotoImage(file="logo.png")
except:
    print("logo.png not found !!")
else:
    canvas.create_image(100,110,image=image_logo)
canvas.place(x=300,y=80)

website_name=Label(text="Website: ",highlightthickness=0,font=FONT,bg=PINK)
website_name.place(x=100,y=320)

email_name=Label(text="Email/Username:",highlightthickness=0,font=FONT,bg=PINK)
email_name.place(x=50,y=370)

password_name=Label(text="Password:",highlightthickness=0,bg=PINK,font=FONT)
password_name.place(x=100,y=420)

website_input=Entry(font=FONT,width=24)
website_input.place(x=280,y=320)

username_input=Entry(font=FONT,width=34)
username_input.place(x=280,y=370)

password_input=Entry(font=FONT,width=20)
password_input.place(x=280,y=420)

######################### Buttons -------------------- 

gen_pass=Button(font=("Arial",10),text="Generate Password",bg=GREEN,command=get_password)
gen_pass.place(x=590,y=422)

add_pass=Button(font=FONT,text="Add Entry",bg=ORANGE,width=50,highlightthickness=0,command=add_password)
add_pass.place(x=50,y=480)

exit_button=Button(font=("JetBrains Mono Nerd",15),text="❌",highlightthickness=0,command=window.destroy)
exit_button.place(x=750,y=0)

search_button=Button(font=("Arial",13),text="Search",highlightthickness=0,command=search_for_entry,bg=BLUE)
search_button.place(x=640,y=318)

window.mainloop()
