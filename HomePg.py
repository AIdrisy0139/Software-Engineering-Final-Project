from tkinter import*
# PIL import ImageTk, Image
import Login2
import SignUp
import sqlite3
import Users1
from DocumentDB import doc_cli
import DocumentFileTest
from DocumentScreenTester import user

class HomePg():
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Home")
        self._geom = '800x800+0+0'
        parent.geometry("{0}x{1}+0+0".format(
            parent.winfo_screenwidth(), parent.winfo_screenheight()))
        self.docName = StringVar()
        self.documentSearch = []
        self.docvar = StringVar(value=self.documentSearch)
        self.createWidget()

    def createWidget(self):
        frame1 = Frame(self.parent)
        frame2 = LabelFrame(frame1)
        frame2.configure(background = "")
        frame2.pack(fill= X, expand= TRUE)
        #frame2.grid(row=0, column=0, sticky=W)
        frame3 = Frame(frame1)
        frame3.pack(fill = X, expand= TRUE)
        #frame3.grid(row=1, column=0, sticky=W)
        frame4 = Frame(frame3)
        frame4.pack(side=LEFT, expand=TRUE)
        frame5 = Frame(frame3)
        frame5.pack(side=LEFT, expand=TRUE)

        img = PhotoImage(file = "SmartD.gif")
        logo = Label(frame4, image=img)
        logo.image = img
        logo.grid(sticky=W)

        Label(frame2, text="", height =0, width=100).grid(row=0, column=1)
        Label(frame2, text= "SmartDSS", font=('Arial', 48), fg = "medium blue").grid(row=0,column=0)
        Button(frame2, text="Log in", font=('Ariel', 30), fg= "medium blue", borderwidth = 0,  command = self.login, height=1, width=10).grid(row=0, column=2, sticky=E, padx=10)
        Button(frame2, text="Get Started",font=('Arial', 30), fg= "medium blue", borderwidth = 0, command = self.signup, height=1, width=10).grid(row=0, column=3, sticky=E, padx=10)

        Label(frame5, text="Search Documents", font=('Ariel', 22), fg="medium blue", width=15).grid(
            sticky=E)
        Entry(frame5, textvariable=self.docName, width=38).grid(row=1, column=0, sticky=E, padx=10)
        simg = PhotoImage(file="images.gif")
        searchpicD = Button(frame5, image=simg, command=self.docsearch)
        searchpicD.image = simg
        searchpicD.grid(row=1, column=1)
        self.searchResult = Listbox(frame5, listvariable=self.docvar, width=38)
        self.searchResult.grid(row=2, column=0, sticky=E, padx=10)
        for entry in self.documentSearch:
            self.searchResult.insert(entry)
        Button(frame5, text="Open Document", command = self.opendocument, font=('Ariel', 22), fg="medium blue", background="white", width =14).grid(
            row=3, column=0, pady=5)

        self.docsearch()
        frame1.pack()


    def login(self):
        Login2.Login.main(self)

    def signup(self):
        SignUp.SignUp.main(self)

#Function to search for Public documents
# Documents must exist and be Public
    def docsearch(self):
        docs = doc_cli.get_all_documents()
        searchItem = self.docName.get()
        names = []
        for doc in docs:
            print(doc.docName)
            print(searchItem)
            if searchItem in doc.docName and (doc.privacyLevel=="public" or doc.privacyLevel=="restricted"):
                entry = (doc.docName, doc.owner, doc.versionNumber)
                names.append(entry)
        self.documentSearch = names
        self.docvar.set(names)


#Function to open a document
    def opendocument(self):
        item = self.searchResult.curselection()
        idx = item[0]
        docdetail = self.documentSearch[idx]
        print(docdetail)
        document = docdetail[0]
        print(document)
        usern = docdetail[1]
        versionNo = docdetail[2]
        DocumentFileTest.DocumentScreen(user(usern), doc_cli.get_document(document, usern, versionNo))


if __name__== "__main__":
    root = Tk()
    HomePg(root)
    root.mainloop()
