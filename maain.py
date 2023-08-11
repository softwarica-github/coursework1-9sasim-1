from tkinter import *
import socket
from tkinter import filedialog
from tkinter import messagebox
import os
from PIL import Image, ImageTk
root=Tk()
root.title("ByteSync")
root.geometry("450x560+500+200")
root.configure(bg="#f4fdfe")
root.resizable(False,False)

#defining select_file function
def select_file():
    global filename
    filename=filedialog.askopenfilename(initialdir=os.getcwd(),
                                        title='Select Image File',
                                        filetypes=(('file_type','*.txt'),('all files','*.*')))

def sender():
    s = socket.socket()
    host = socket.gethostname()
    port = 8989
    s.bind((host, port))
    s.listen(1)
    print(host)
    print('Waiting for connection.......')
    conn, addr = s.accept()
    print('Connection established with:', addr)
    file = open(filename, 'rb')
    while True:
        file_data = file.read(4096)  # Read 4096 bytes from the file
        if not file_data:
            break
        conn.send(file_data)
    file.close()
    print("Data has been transmitted successfully!")




#defining send function
def send():
    Window=Toplevel(root)
    Window.title("send")
    Window.geometry('450x560+500+200')
    Window.configure(bg="#f4fdfe")
    Window.resizable(False,False)

    #icon
    icon1=PhotoImage(file="img/send.png")
    Window.iconphoto(False,icon1)

    Sbg=PhotoImage(file="img/sender.png")
    Label(Window,image=Sbg).place(x=-2,y=0)

    Mbg=PhotoImage(file="img/id.png")
    Label(Window,image=Mbg,bg="#f4fdfe").place(x=100,y=260)

    host=socket.gethostname()
    Label(Window,text=f'ID: {host}',bg='white',fg='black').place(x=140,y=290)


    Button(Window,text="+ select file",width=10,height=1,font="arial 14 bold", bg="#fff", fg="#000",command=select_file).place(x=160,y=150)
    Button(Window,text="Send",width=8,height=1,font="arial 14 bold", fg="#fff", bg="#000",command=sender).place(x=300,y=150)

    Window.mainloop()

def receive():
    recc=Toplevel(root)
    recc.title("receive")
    recc.geometry('450x560+500+200')
    recc.configure(bg="#f4fdfe")
    recc.resizable(False,False)



    def receiver():
        ID = SenderID.get()
        filename1 = InFile.get()

        s = socket.socket()
        port = 8989
        s.connect((ID, port))
        file = open(filename1, 'wb')
        while True:
            file_data = s.recv(4096)  # Receive 4096 bytes of data
            if not file_data:
                break
            file.write(file_data)
        file.close()
        print("File received successfully!")


    #icon
    icon1=PhotoImage(file="img/receive.png")
    recc.iconphoto(False,icon1)

    Rbg = Image.open("img/lll.png")
    Rbg = Rbg.resize((479, 237), Image.ANTIALIAS)
    Rbg = ImageTk.PhotoImage(Rbg)
    Label(recc, image=Rbg).place(x=-15, y=0)



    logo=PhotoImage(file='img/profile.png')
    Label(recc,image=logo,bg='#f4fdfe').place(x=10,y=250)

    Label (recc, text="Receive",font=('arial',20),bg="#f4fdfe").place(x=100, y=280)
    Label (recc, text="Input sender id",font=('arial',10, 'bold'),bg="#f4fdfe").place(x=20, y=340)
    SenderID = Entry (recc, width=25,fg="black", border=2, bg='white', font=('arial',15))
    SenderID.place(x=20, y=370)
    SenderID.focus()

    Label (recc, text="Enter Filename for incoming file : ",font=('arial',10, 'bold'),bg="#f4fdfe").place(x=20, y=420)
    InFile= Entry (recc, width=25,fg="black", border=2, bg='white', font=('arial',15))
    InFile.place(x=20, y=450)

    imageicon=PhotoImage(file="img/arrow.png")
    rr=Button(recc,text="Receive",compound=LEFT,image=imageicon,width=130,bg="#39c790",font="arial 14 bold",command=receiver)
    rr.place(x=20,y=500)





    recc.mainloop()

#icon 
image_icon=PhotoImage(file="img/pp.png")
root.iconphoto(False,image_icon)

Label(root,text="File sharing software",font=('Acumin Variable Concept',20,'bold'),bg="#f4fdfe").place(x=95,y=30)

Frame(root,width=400,height=2,bg="#f3f5f6").place(x=2)

send_img=PhotoImage(file="img/send.png")
send=Button(root,image=send_img,bg="#f4fdfe",bd=0,command=send)
send.place(x=50,y=100)

rec_img=PhotoImage(file="img/receive.png")
rec=Button(root,image=rec_img,bg="#f4fdfe",bd=0,command=receive)
rec.place(x=300,y=100)

#label
Label(root, text="Send", font=('Acumin Variable Concept', 17, 'bold'),bg="#f4fdfe").place(x=65,y=200)
Label (root, text="Receive", font=('Acumin Variable Concept',17,'bold'),bg="#f4fdfe").place(x=300,y=200)

bg = Image.open("img/bak.png")
# Resize the image to the desired dimensions
new_width = 505
new_height = 235
bg = bg.resize((new_width, new_height), Image.ANTIALIAS)
bg = ImageTk.PhotoImage(bg)
Label(root, image=bg).place(x=-32, y=323)




root.mainloop()
