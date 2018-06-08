import tkinter as tk
from tkinter import ttk
from tkinter import StringVar
from tkinter import messagebox
import sqlite3
import cv2
import numpy as np
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
from TextPrep import ImgPrep
import threading
import predictor
from multiprocessing.pool import ThreadPool
TEXT13 = ("helvetica", 13)
COLOR_MAIN = "#262626"




class Handwriting(tk.Tk):
    uname =[]

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Handwriting Recognition")
        uname = tk.StringVar(self)
        fname = tk.StringVar(self)
        lname = tk.StringVar(self)
        country = tk.StringVar(self)
        w = 1300
        h = 950
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))

        container = tk.Frame(self)
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight=1)
        container.grid(row = 0, column = 0, sticky = "NSEW")
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)



        self.frames = {}

        for F in (LoginPage, RegisterPage, MainPage):
            frame = F(container,self)
            self.frames[F] = frame
            frame.grid(row=0, column = 0, sticky = tk.NSEW)
        self.show_frame(LoginPage)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self["background"] = COLOR_MAIN

        pLabel = tk.Label(self, text="Password", borderwidth=0, background=COLOR_MAIN,
                          font=TEXT13,
                          fg="#E0E0E0")
        lLabel = tk.Label(self, text="UserName", borderwidth=0, background=COLOR_MAIN,
                          font=TEXT13,
                          fg="#E0E0E0")
        self.unText = ttk.Entry(self, font=TEXT13)
        self.pwText = ttk.Entry(self, font=TEXT13, show="*")
        btn = tk.Button(self, text="Login", background="#65625F", borderwidth=0, fg="#E0E0E0",
                        activebackground="#6FB2E7", activeforeground="#E0E0E0", font = TEXT13, command=lambda: self.loginClick(controller))
        btn2 = tk.Button(self, text="Register", background="#65625F", borderwidth=0,
                        fg="#E0E0E0", activebackground="#6FB2E7", activeforeground="#E0E0E0", font = TEXT13,
                        command=lambda: controller.show_frame(RegisterPage))

        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(5, weight=1)
        lLabel.grid(row=1, column=1, sticky = tk.E,  padx=(0, 10), pady=(15, 0))
        pLabel.grid(row=2, column=1,sticky = tk.E,  padx=(0, 10), pady=(15, 10))


        self.unText.grid(row=1, column=2,sticky = tk.W, padx=(10, 0), pady=(15, 0))
        self.pwText.grid(row=2, column=2,sticky = tk.W, padx=(10, 0), pady=(15, 10))

        btn.grid(row=3, column=2, sticky=tk.EW, padx=(10, 0), pady=(5, 0))
        btn2.grid(row=4, column=2,sticky = tk.EW, padx=(10, 0), pady=(5, 0))

    def loginClick(self, controller):
        s = SQL()
        s.getLoginInfo(controller, self.unText.get(), self.pwText.get())
class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self["background"] = COLOR_MAIN

        unLabel = tk.Label(self, text="UserName", borderwidth=0, background=COLOR_MAIN,
                           font=TEXT13,
                           fg="#E0E0E0")
        self.unText = ttk.Entry(self, font=TEXT13)
        pwLabel = tk.Label(self, text="Password", borderwidth=0, background=COLOR_MAIN,
                           font=TEXT13,
                           fg="#E0E0E0")
        self.pwText = ttk.Entry(self, font=TEXT13, show="*")
        pwLabel2 = tk.Label(self, text="Re-Type Password", borderwidth=0, background=COLOR_MAIN,
                            font=TEXT13,
                            fg="#E0E0E0")
        self.pwText2 = ttk.Entry(self, font=TEXT13, show="*")
        fnLabel = tk.Label(self, text="First Name", borderwidth=0, background=COLOR_MAIN,
                           font=TEXT13,
                           fg="#E0E0E0")
        self.fnText = ttk.Entry(self, font=TEXT13)
        lLabel = tk.Label(self, text="Last Name", borderwidth=0, background=COLOR_MAIN,
                          font = TEXT13,
                          fg="#E0E0E0")
        self.lText = ttk.Entry(self, font=TEXT13)

        cLabel = tk.Label(self, text="Country", borderwidth=0, background=COLOR_MAIN,
                          font=TEXT13,
                          fg="#E0E0E0")
        self.cText = ttk.Entry(self, font=TEXT13)

        unLabel.grid(row=1, column=1, sticky=tk.EW, padx=(0, 10))
        self.unText.grid(row=1, column=2, sticky=tk.EW, padx=(0, 10))
        pwLabel.grid(row=2, column=1, sticky=tk.EW, padx=(0, 10), pady=(10, 0))
        self.pwText.grid(row=2, column=2, sticky=tk.EW, padx=(0, 10), pady=(10, 0))
        pwLabel2.grid(row=3, column=1, sticky=tk.EW, padx=(0, 10), pady=(10, 0))
        self.pwText2.grid(row=3, column=2, sticky=tk.EW, padx=(0, 10), pady=(10, 0))
        fnLabel.grid(row=4, column=1, sticky=tk.EW, padx=(0, 10), pady=(10, 0))
        self.fnText.grid(row=4, column=2, sticky=tk.EW, padx=(0, 10), pady=(10, 0))
        lLabel.grid(row=5, column=1, sticky=tk.EW, padx=(0, 10), pady=(10, 0))
        self.lText.grid(row=5, column=2, sticky=tk.EW, padx=(0, 10), pady=(10, 0))
        cLabel.grid(row=7, column=1, sticky=tk.EW, padx=(0, 10), pady=(10, 0))
        self.cText.grid(row=7, column=2, sticky=tk.EW, padx=(0, 10), pady=(10, 0))

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(9, weight=1)


        btn = tk.Button(self,text="Register",background="#65625F", borderwidth=0, fg="#E0E0E0",
                        activebackground="#6FB2E7", activeforeground="#E0E0E0", font = TEXT13,
                        command = lambda:self.reg(controller, self.unText, self.pwText, self.pwText2, self.fnText, self.lText, self.cText))
        btn.grid(row=8, column=1, sticky=tk.EW, padx=(0, 10), pady=(10, 0))
        btn2 = tk.Button(self, text="Cancel", background="#65625F", borderwidth=0, fg="#E0E0E0",
                        activebackground="#6FB2E7", activeforeground="#E0E0E0", font = TEXT13, command = lambda: controller.show_frame(LoginPage) )
        btn2.grid(row=8, column=2, sticky=tk.EW, padx=(0, 10), pady=(10, 0))

    def reg(self, controller,name,pasw,pasw2, fn,ln,cont):
        print(self.unText.get())
        SQL.register(self, controller, self.unText, self.pwText, self.pwText2, self.fnText, self.lText, self.cText)
class SQL():
    uname = ""
    fname = ""
    lname = ""
    country = ""
    def __init__(self):
        pass
    def register(self, controller,name,pasw,pasw2, fn,ln,cont):
        if fn.get().isalpha() & ln.get().isalpha() & cont.get().isalpha():

            if (pasw.get() == pasw2.get()):
                try:

                    flag = 0
                    try:
                        con = sqlite3.connect("database.db")

                        result = con.execute("SELECT COUNT (uname) FROM userdata WHERE uname = %s" % (name.get(),))

                        for a in result:
                            if (a[0] > 0):
                                flag = 1
                    except:
                        print("asdf")
                    con = sqlite3.connect("database.db")
                    c = con.cursor()
                    if (flag == 0):
                        c.execute("INSERT INTO userdata (uname,pword,fname,lname,conty) VALUES (?,?,?,?,?)",
                                  (name.get(), pasw.get(), fn.get(), ln.get(), cont.get()))
                        con.commit()
                        messagebox.showinfo("Success", "Account Registered")
                        name.delete(0, tk.END)
                        pasw.delete(0, tk.END)
                        pasw2.delete(0, tk.END)
                        fn.delete(0, tk.END)
                        ln.delete(0, tk.END)
                        cont.delete(0, tk.END)
                        controller.show_frame(LoginPage)

                    else:
                        messagebox.showinfo("Error", "Username already exists")
                except:
                    print("qwer")
            else:
                messagebox.showinfo("Error", "Passwords don't match")
        else:
            messagebox.showinfo("Invalid Inputs",
                                "First Name, Last Name, Country can't have numbers and should not be empty")


    def getLoginInfo(self, controller, name, password):

        con = sqlite3.connect("database.db")
        c = con.cursor()
        result = c.execute("SELECT * FROM userdata WHERE uname = '%s' AND pword = '%s'"%(name,password))
        result = result.fetchall()
        if(result.__len__()>0):
            #for a in result:
            #    asd.update(a[0],a[2],a[3],a[4])
            controller.uname = result[0]

            print(controller.uname)
            controller.show_frame(MainPage)
        else:
            messagebox.showinfo("Authentication Failure", "Username or password is incorrect")



    def create_db(self):
        try:
            con = sqlite3.connect("database.db")
            c = con.cursor()
            c.execute("create table userdata (id integer primary key autoincrement,uname text not null,pword text not null,fname text,lname text,conty text)")
            con.commit()
            print("database creation successful")
        except:
            pass

class MainPage(tk.Frame):
    img = []

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.currImg = []
        colorMain = "#262626"
        tp = ImgPrep()
        tp1 = ImgPrep()
        # -------Base Frame---------------------------

        # -------------------------------------------

        # ------Button Images------------------------
        upImg = Image.open("upload.png")
        upImg = ImageTk.PhotoImage(upImg)
        anImg = Image.open("analyse.png")
        anImg = ImageTk.PhotoImage(anImg)
        # -------------------------------------------

        # -----Main Panel----------------------------
        mainPanel = tk.Frame(self)
        mainPanel.pack(fill=tk.BOTH, expand=1, side=tk.TOP)
        # -------------------------------------------

        # ------Main Panel Divisions-----------------
        LCPanel = tk.Frame(mainPanel, background="#FFFFFF")
        RCPanel = tk.Frame(mainPanel, background="#FEFEFE")
        ICPanel = tk.Frame(mainPanel, background="#123123")
        IcRcsep = tk.Frame(mainPanel, background="#494949", width=3)
        #LCPanel.pack(fill=tk.BOTH, side=tk.LEFT)
        ICPanel.pack(fill=tk.BOTH, expand=1, side=tk.LEFT, ipady = 10)
        IcRcsep.pack(fill=tk.Y, expand=0, side=tk.LEFT)
        RCPanel.pack(fill=tk.BOTH, side=tk.LEFT)
        # -------------------------------------------

        # -------ICPanel Divisions-------------------
        imgPanel1 = tk.Frame(ICPanel, background="#098876")
        imgPanel2 = tk.Frame(imgPanel1, background="#678890")

        imgPanel1.pack(fill=tk.BOTH, expand=1)
        imgPanel2.pack(fill=tk.BOTH, expand=1)
        # -------------------------------------------

        # -------Search Panel------------------------
        searchPanel = tk.Frame(imgPanel2, background=COLOR_MAIN)
        searchPanel.pack(side=tk.TOP, pady=10)
        # -------------------------------------------

        # -------Search Panel Elements---------------

        '''txt = tk.Text(searchPanel, height=2)

        txt.pack(side=tk.LEFT, fill=tk.Y, expand=1)'''

        # -------------------------------------------

        # -------------------------------------------
        self.imgLbl = tk.Label(imgPanel2, background=COLOR_MAIN)
        self.imgLbl.pack(fill=tk.BOTH, expand=1)

        self.imgText = tk.Label(imgPanel2, background = COLOR_MAIN, fg = "#E0E0E0", font = ("helvetica", 19) )

        self.imgText.pack(pady = 10)
        # -------------------------------------------

        # ----RC Panel Elements---------------------
        btnPanel = tk.Frame(RCPanel, background=COLOR_MAIN)
        btnPanel.grid(row=0, column=1, sticky=tk.EW, pady=(15, 15), padx=(15,15))
        upButton = tk.Button(btnPanel, image=upImg, width=150, height=150, background="#65625F", borderwidth=0,
                             activebackground="#347289", command = lambda:self.upload(tp1, controller))
        upButton.configure(image=upImg)
        upButton.image = upImg
        anButton = tk.Button(btnPanel, image=anImg, width=150, height=150, background="#65625F", borderwidth=0,
                             activebackground="#347289", command = lambda:self.analyse(tp))
        anButton.configure(image=anImg)
        anButton.image = anImg
        upButton.pack(side=tk.LEFT, padx=(0, 5))
        anButton.pack(side=tk.RIGHT, padx=(5, 0))
        svBtn = tk.Button(RCPanel, text="Open", borderwidth=0, background="#65625F",
                          font=TEXT13,
                          fg="#E0E0E0", activebackground="#347289", activeforeground="#E0E0E0",
                          command=lambda: self.openImage(self.imgLbl))
        svBtn.grid(row=1, column=1, sticky=tk.EW, pady=(15, 0), padx=15)
        sep2 = tk.Frame(RCPanel, background="#494949", height=3)
        sep2.grid(row=2, column=1, sticky=tk.EW, pady=(15, 0), padx=15)

        lbl = tk.Label(RCPanel, text="Threshold", font=TEXT13, fg="#E0E0E0",
                       background=COLOR_MAIN)
        lbl.grid(row=3, column=1, sticky=tk.EW, pady=(15, 0), padx=15)

        thresh = tk.Scale(RCPanel, from_=0, to=255, command=lambda x: self.threshold(thresh.get(), self.imgLbl),
                          orient=tk.HORIZONTAL, background=COLOR_MAIN, fg="#E0E0E0", bd=0,
                          font=TEXT13, highlightthickness=0)
        thresh.set(120)
        thresh.grid(row=4, column=1, sticky=tk.EW, padx=15)
        # -------------------------------------------



    def openImage(self, lbl):
        try:
            name = askopenfilename(initialdir="",
                                   filetypes=(("PNG files", "*.png"),("jpg files", "*.jpg"), ("All Files", "*.*")),
                                   title="Choose a file."
                                   )

            self.img = cv2.imread(name, 0)
            self.setImg(lbl, self.img)
            self.currImg = self.img
        except:
            pass

    def threshold(self, val, lbl):

        try:
            ret, self.currImg = cv2.threshold(self.currImg, val, 255, cv2.THRESH_BINARY)

            height, width = self.currImg.shape
            self.setImg(lbl, self.currImg)
        except:
            pass
    def CropTop(self, val, lbl):

        try:
            height, width = self.currImg.shape
            img = cv2.Line(self.currImg, (0,int(val*height/100),(width,int(val*height/100))),thickness = 1,color = (0,0,0))
            self.setImg(lbl, self.currImg)
        except:
            pass

    def setImg(self, lbl, img):
        tkImg = Image.fromarray(img)
        width, height = tkImg.size
        heightMax = height
        widthMax = width
        if (width > height):
            hwRatio = height / width
            width = lbl.winfo_width()
            height = int(lbl.winfo_height() * hwRatio)
        elif (width < height):
            hwRatio = width / height
            width = int(lbl.winfo_width() * hwRatio)
            height = lbl.winfo_height()
        if(width>widthMax):
            tkImg = tkImg.resize((widthMax, height))
        elif(height>heightMax):
            tkImg = tkImg.resize((width, heightMax))
        else:
            tkImg = tkImg.resize((width, height))
        tkImg = ImageTk.PhotoImage(tkImg)
        lbl["image"] = tkImg
        lbl.img = tkImg

    def upload(self, tp, controller):
        uname1 = controller.uname[0]
        try:
            tp.saveCsv(self.img, uname1)

        except:
            pass

    def analyse(self, tp):
        print("1")
        txt = tp.analyse(np.array(self.currImg))
        print(txt)
        self.imgText["text"] = txt
        #thread = threading.Thread(target=tp.analyse(self.img))
        #thread.daemon = True
        #thread.start()


#ab = SQL()
#ab.create_db()


if __name__ == '__main__':
    app = Handwriting()
    app.mainloop()