from tkinter import *
import tkinter.simpledialog as tkSimpleDialog 
import TabooWords
import DeltaObjects

import time
from threading import Thread

'''Document View'''
#TODO: Real User Class Integration
class DocumentScreen:
    def __init__(self,user,document):
        from DocumentDB import doc_cli
        self.lastChange = -1
        self.currentUser = user;
        self.userRank =user.getRank()
        #self.userRank = doc_cli.getRank(self.currentUser)
        self.currentDoc= document
        # self.docMembers = document.getMembers()
        self.allUsers = doc_cli.get_all_users() #TODO: Server Call
        self.allMembers = doc_cli.get_members(self.currentDoc.doc_id)
        #self.allUsers = ["ARI","ME","JAS"]
        
        
        Thread(target=self.deferUpdates).start()
        self.makeScreen()

    
    def deferUpdates(self):
        time.sleep(5)
        print("AUTOPULLING")
        self.submitChanges()
        Thread(target=self.deferUpdates).start()

    def makeScreen(self):
        from DocumentDB import doc_cli
        DocHeight=1024
        DocWidth = 720
        
        TextPlaceHolder="PLACEHOLDER"

        self.root= Tk()
        #root.title(self.currentDoc.getTitle() +" || "+ self.currentUser.getUserName())
        self.root.title(self.currentDoc.docName)
        self.root.geometry(str(DocHeight)+"x"+str(DocHeight))
        
        # --Menu Set Up -------------------------------------------------------------------------
        self.mainMenu = Menu(self.root)
        
        # All Following Menus are submenus of the self.mainMenu object
        # Back Menu
        backMenu = Menu(self.mainMenu,tearoff=0)
        backMenu.add_command(label="Undo",command=self.undo)#command ~~ openHomePg()
        self.mainMenu.add_cascade(label="<--",menu=backMenu)

        # Complain Menu
        complainMenu = Menu(self.mainMenu)
        # complainMenu.add_command(label="Submit Document Complaint",command=self.addDocComplaint)
        complainMenu.add_command(label="Submit User Complaint",command=self.addUserComplaint)
        self.mainMenu.add_cascade(label="Complaints",menu=complainMenu)
        # complainMenu.entryconfigure("Submit Document Complaint",state="disabled")

        # Document Options Menu
        optMenu = Menu(self.mainMenu)
        optMenu.add_command(label="Lock Document",command=self.lockDocument)#command = lockDocument 
        optMenu.add_command(label="Unlock Document",command=self.unlockDocument)#command = unLockDocument
        self.pastVerMenu = Menu(optMenu)
        num = 0
        #deltas = doc_cli.get_updates(self.currentDoc.doc_id,)
        #optMenu.add_command(label="Set Privacy Level")
        self.privMenu = Menu(optMenu)
        self.privMenu .add_command(label="Current Privacy Level: "+ self.currentDoc.privacyLevel)
        self.privMenu.add_command(label="Set Private",command=lambda i= "private" :self.setPriv(i))
        self.privMenu.add_command(label="Set Public",command=lambda i = "public" : self.setPriv(i))
        self.privMenu.add_command(label="Set Shared", command=lambda i= "shared" : self.setPriv(i))
        self.privMenu.add_command(label= "Set Restricted",command=lambda i ="restricted" : self.setPriv(i))
        optMenu.add_cascade(label="Set Privacy Level",menu=self.privMenu)
        optMenu.add_cascade(label="Load Past Versions", menu=self.pastVerMenu)#command = ???? Something to view previous docs
        
        self.mainMenu.add_cascade(label="Document Options", menu=optMenu)
        
        # Membership Options Menu

        #membOptMenu = Menu(self.mainMenu)
        #membOptMenu.add_command(label="Update Member(s)")

        self.updateMembersMenu = Menu(self.mainMenu)

        
        self.allMembersMenu = Menu(self.updateMembersMenu)
        self.allUserMenu = Menu(self.updateMembersMenu) #For Removing Members
        self.allMembersMenu.add_command(label="All Members Menu")

        for member in self.allMembers:
            self.allMembersMenu.add_command(label=member,command=lambda i= member: self.removeUser(i))
        self.allUserMenu = Menu(self.updateMembersMenu)
        self.allUserMenu.add_command(label="All Users Menu")
        for user in self.allUsers:
            self.allUserMenu.add_command(label=user,command=lambda j = user: self.addUser(j))
        self.updateMembersMenu.add_cascade(label="Remove/View Members", menu=self.allMembersMenu)
        self.updateMembersMenu.add_cascade(label="All Registered System Users",menu=self.allUserMenu)
        #membOptMenu.add_cascade(label="View All Members", menu=self.allMembersMenu)
        self.mainMenu.add_cascade(label="Membership Option",menu=self.updateMembersMenu)

        # Taboo Word Menu
        self.tabooMenu = Menu(self.mainMenu)
        self.tabooWords = TabooWords.TabooWord.getAllTaboo() 
        for tWord in self.tabooWords:
            if tWord.status==1:
                self.tabooMenu.add_command(label=tWord.text)
        self.tabooMenu.add_separator()
        self.tabooMenu.add_command(label="Add Taboo Word", command=self.addTabooWord)# command ~~ addTabooWord
        self.tabooMenu.add_separator()
        self.tabooMenu.add_command(label="Newly Added Taboos")
        
        self.mainMenu.add_cascade(label="TabooWords", menu=self.tabooMenu)

        # Document Complaints [ Against Document ] Menu
        docComplaintMenu = Menu(self.mainMenu)
        complaints = self.currentDoc.getComplaints()
        for complaint in complaints:
            docComplaintMenu.add_command(label=complaint.text)
        self.mainMenu.add_cascade(label="View Document Complaints",menu=docComplaintMenu)

        # Submit Menu
        self.changeMenu = Menu(self.mainMenu)
        self.changeMenu.add_command(label="Submit Changes",command= self.submitChanges)
        self.changeMenu.add_command(label="Pull Staged Changes",command = self.pullChanges)
        self.changeMenu.add_command(label="Create New Version",command=self.createNewVersion)
        self.changeMenu.add_command(label="Save as New Version",command=self.saveAsNew)
        self.mainMenu.add_cascade(label="Version Control",menu=self.changeMenu)


        # --Dynamic Buttons----------------------------------------------------------------------
        # These come from the user who opened this documentvIEW
        # These can also just be extra fields in the menu
        # Acomplished by Disabling buttons based on user Rank
        # TODO: Check if anymore must be added
        if(self.userRank=="SU"):
            print()
        elif(self.userRank=="OU"):
            #Lock Document
            print()
        elif(self.userRank=="GU"):
            optMenu.entryconfigure("Lock Document",state="disabled")
            optMenu.entryconfigure("Unlock Document",state="disabled")
            print()
        else:
            print("ERROR: USER RANK UNDIFINED")

        
        # --Text Fields--------------------------------------------------------------------------

        displayText = self.currentDoc.getWords() 
        # create a Text (widget)
        textFrame = Frame(self.root,width = DocWidth,height=DocHeight)
        textFrame.pack(fill="both",expand=True)
        textFrame.grid_propagate(False)
        textFrame.grid_rowconfigure(0,weight=1)
        textFrame.grid_columnconfigure(0,weight=1)
        self.txt = Text(textFrame, borderwidth=3, relief="sunken",width=200,height=DocHeight)
        self.txt.insert(END,self.currentDoc.words)
        self.txt.config(font=("consolas", 12), undo=True, wrap='word')
        self.txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2,)
        scrollb = Scrollbar(textFrame, command=self.txt.yview)
        scrollb.grid(row=0, column=2, sticky='nsew')
        self.txt['yscrollcommand'] = scrollb.set    
        self.root.config(menu=self.mainMenu)   
        # Get changes from server
        self.pullChanges() 
        self.root.mainloop()
#--- END MAKE SCREEN ------------------------------

    def setPriv(self,p):
        self.privMenu.entryconfigure("Current Privacy Level: "+ self.currentDoc.privacyLevel,label="Current Privacy Level: " + p)
        self.currentDoc.setPriv(p)
    def refreshText(self):
        self.txt.delete(1.0,END)
        self.txt.insert(END,self.currentDoc.words)
    def addUser(self,user):
        print("Add User To Document Function")
        print(user)
        print("SHOOOOOOOULD BE USER STRING:  " + user[0])
        #print("TYYYYYYYYYYYYYPE:   "+ str(type(user[0])))
        self.currentDoc.addMember(user)
        self.allMembersMenu.add_command(label=user, command=lambda i= user[0]: self.removeUser(i))

    def removeUser(self,uname):
       
        print("Remove User Function , uname: {}".format(uname))
        off = "disabled"
        self.currentDoc.removeMember(uname)
        self.allMembersMenu.entryconfigure(uname,state=off)
    #PostCond: The inputed Word is added to the DB of Taboo Words
    def addTabooWord(self):
        from DocumentDB import doc_cli

        uInput = tkSimpleDialog.askstring("Add Taboo Word","Word?")
        TabooWords.TabooWord.addTabooWord(uInput)

        #self.tabooMenu.pack()

    #TODO: Changing other GUI elements as well when its locked
    #  - submit button
    #  - adding member button
    def lockDocument(self):
        off="disabled"
        #self.txt.config(state=off)
        self.changeMenu.entryconfigure("Submit Changes",state=off)
        self.changeMenu.entryconfigure("Pull Staged Changes",state=off)
        self.updateMembersMenu.entryconfigure("Remove/View Members",state=off)
        self.updateMembersMenu.entryconfigure("All Registered System Users",state=off)
        self.currentDoc.lockDocument()
    def unlockDocument(self):
        on = "normal"
        #self.txt.config(state=on)
        self.changeMenu.entryconfigure("Submit Changes",state=on)
        self.changeMenu.entryconfigure("Pull Staged Changes",state=on)
        self.updateMembersMenu.entryconfigure("Remove/View Members",state=on)
        self.updateMembersMenu.entryconfigure("All Registered System Users",state=on)

        self.currentDoc.unlockDocument()
    def addDocComplaint(self):
        complaint=tkSimpleDialog.askstring("Enter Complaint against Document","Complaint:")
        self.currentDoc.addComplaint(complaint,self.currentUser)
    def addUserComplaint(self):
        from DocumentDB import doc_cli
        complaint=tkSimpleDialog.askstring("Enter Complain Against User","Complaint")
        doc_cli.add_complaint(self.currentUser.getUserName(),complaint)
        
    def undo(self):
        print("Go back one delta")
    
    def loadVersion(self, update):
        #self.pullChanges(update)
       #self.lastChange = -1
       # self.submitChanges()
        print("faf")
    
    def createNewVersion(self):
        from DocumentDB import doc_cli
        self.submitChanges()
        print("Create a New Version at "+str(self.lastChange))
        import datetime
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        doc_cli.create_version(self.currentDoc.doc_id, dt, self.lastChange)
        self.pastVerMenu.add_command(label = dt, command=lambda i=self.lastChange: self.loadVersion(i))
        
    def saveAsNew(self):
        print("Save as New Version")

    def submitChanges(self):
        from DocumentDB import doc_cli
        print("LISTENTO ME: "+self.currentDoc.docName+", "+self.currentUser.getUserName())
        doc = doc_cli.get_document(self.currentDoc.docName, self.currentDoc.owner, 0)
        if doc.owner!=self.currentUser.getUserName() and doc.locked==1:
            self.pullChanges()
            self.txt.config(state=off)
            return
        else:
            self.txt.config(state=on
        old = self.currentDoc.getWords()
        new = self.txt.get("1.0",'end-1c')
        
        
        import re
        tabooWords = TabooWords.TabooWord.getAllTaboo()
        for w in tabooWords:
            pattern = re.compile(w.text, re.IGNORECASE)
            new = pattern.sub("UNK", new)
        
        deltas = self.currentDoc.generateDeltas(old,new)
        self.currentDoc.words= new
        doc_cli.push_updates(self.currentDoc.doc_id, deltas, self.lastChange)
        
        
        self.pullChanges()

        # DEBUG CODE
        # deltaListServ = doc_cli.get_updates(self.currentDoc.doc_id,0)
        # print("DeltaList Server")
        # for i in deltaListServ:
            # i.show()
        # print("DeltaList Client")
        # deltaListClient = self.currentDoc.deltaLog
        # for j in deltaListClient:
            # j.show()
        # print("Old {} | New {} |Doc.words {}".format(old,new,self.currentDoc.words))

    def refreshText(self):
        self.txt.delete(1.0, END)
        self.txt.insert(END, self.currentDoc.words)

    def addDeltaToDisplay(self,oldDeltas,newDeltas):
        print("Add Delta To Display")
        for i in range(0,len(newDeltas)):
            if(i>len(oldDeltas)):
                self.pastVerMenu.add_command(label= newDeltas[i].show() + "NUM: " + str(i), 
                command = lambda k = i, d=self.currentDoc.deltaLog:self.currentDoc.sRec(k,d))
    def pullChanges(self):
        from DocumentDB import doc_cli
        oldDeltaList = self.currentDoc.deltaLog
        deltaList= doc_cli.get_updates(self.currentDoc.doc_id,0)
        for d in deltaList:
            d.show()
            
        self.currentDoc.reconstruct(5,deltaList)
        self.refreshText()
        if len(deltaList)>0:
            self.lastChange = deltaList[len(deltaList)-1].u_id
        else:
            self.lastChange = -1

        #self.addDeltaToDisplay(oldDeltaList,deltaList)

