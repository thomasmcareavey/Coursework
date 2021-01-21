import tkinter as tk
from tkinter import ttk
from MainDB import DataBase as db
from Widgets import BasicWidget

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page")
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="Accounts",
                           command=lambda: controller.show_frame(Accounts))
        button.pack()

class Accounts(tk.Frame):
    def __init__(self, parent, controller):
        self.accountFields = None
        self.Addwindow = None
        self.controller = controller
        self.row = 0
        self.column = 0

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Accounts")
        label.grid(row= self.row, column= self.column,
                    columnspan=2, pady=10, padx=10)
        self.row +=1

        self.myDB = db("shop.db")
        accountFields = self.myDB.get_fields("accounts")

        for f in accountFields:
            wid = BasicWidget(self,f, self.row, self.column+1)
            self.row +=1

        button = tk.Button(self, text="Home",
                           command=lambda: controller.show_frame(HomePage))
        button.grid(row=self.row, column=self.column+1)

        #treeview
        self.tree = ttk.Treeview(self, column=(accountFields))
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        vsb.grid(row=self.row, column=11, sticky='nsew')
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=self.row, column=1, columnspan=10, sticky='nsew')

        self.myDB = db("shop.db")
        accountFields = self.myDB.get_fields("accounts")

        for field in range(0, len(accountFields)):
            self.tree.heading(f'#{field}', text=accountFields[field])
            self.tree.column(f'#{field}', stretch=tk.FALSE,
                             minwidth=75, width=100)
        self.populateTree(self.myDB.fetch_all("accounts"))
        self.row +=1

        self.tree.bind('<ButtonRelease-1>', self.populateWidgets)


        self.buttonNames = ["Search", "Add",
                            "Update", "Delete",
                            "Close"]

        self.searchBox = ttk.Entry(self)
        self.searchBox.insert(0, "Enter Name:")
        self.searchBox.grid(row=self.row, column = self.column, padx=5,
                            pady=5, sticky='we')
        self.searchBox.bind('<Button-1>', self.clear)
        self.column +=1

        for i in range(0, len(self.buttonNames)):
            self.navButton = ttk.Button(self, text = self.buttonNames[i],
                                        command= lambda x=self.buttonNames[i]:self.crud(x))
            self.navButton.grid(row = self.row, column = self.column,
                                padx=5, pady=5, sticky='we')
            self.column +=1

    def crud(self, txt):
        if txt == "Close":
            self.controller.show_frame(HomePage)
        if txt == "Search":
            self.Search()
        if txt == "Add":
            self.AddWindow = tk.Toplevel()
            for i in range(1, len(self.accountFields)):
                BasicWidget(self.AddWindow, self.accountFields[i], i, 0)
            self.addButton = ttk.Button(self.AddWindow, text="Add",
                                        command=self.AddRecord)
            self.addButton.grid(row=len(self.accountFields) + 1, column=0, padx=5,
                                pady=5, sticky="we")
            self.closeButton = ttk.Button(self.AddWindow, text="Close",
                                          command=self.AddWindow.destroy)
            self.closeButton.grid(row=len(self.accountFields) + 1, column=1,
                                  padx=5, pady=5, sticky='we')

        if txt == "Update":
            self.update()
        if txt == "Delete":
            self.delete()

    def Search(self):
        self.myDB = db("shop.db")
        searchCriteria = self.searchBox.get()
        results = self.myDB.retrieve_data("accounts", "Username", searchCriteria)
        self.populateTree(results)
        self.myDB.close()

    def update(self):
        self.myDB = db("shop.db")
        fields = self.myDB.get_fields("accounts")
        wids = self.winfo_children()
        data = [wid.get() for wid in wids if type(wid) == tk.Entry]
        for i in range(1, len(fields)):
            self.myDB.update_data("accounts", fields[i], data[i],
                                  fields[0], data[0])
        self.populateTree(self.myDB.fetch_all("accounts"))
        self.myDB.close()

    def delete(self):
        curItem = self.tree.focus()
        id = self.tree.item(curItem)['text']
        self.myDB = db("shop.db")
        self.myDB.delete_record("Username", "accounts", id)
        self.populateTree(self.myDB.fetch_all("accounts"))
        self.myDB.close()

    def AddRecord(self):
        self.wids = self.AddWindow.winfo_children()
        data = [wid for wid in self.wids if type(wid)==tk.Entry]
        self.myDB = db("shop.db")
        self.myDB.create_data("accounts", data)
        self.populateTree(self.myDB.fetch_all("accounts"))
        self.myDB.close()
        entryWids = [wid for wid in self.wids if type (wid)==tk.Entry]
        for wid in entryWids:
            wid.delete(0,"end")
            self.Addwindow.destroy()

    def populateTree(self, data):
        self.tree.delete(*self.tree.get_children())
        accounts = self.myDB.fetch_all("accounts")
        for record in data:
            self.tree.insert("", "end", text=str(record[0]),
                             values=(record[1], record[2], record[3], record[4]))
        self.myDB.close()

    def populateWidgets(self, evt):
        self.wids = self.winfo_children()
        EntryWidgets = [wid for wid in self.wids if type(wid)==tk.Entry]
        for widget in EntryWidgets:
            widget.delete(0,"end")
        curItem = self.tree.focus()
        id = self.tree.item(curItem)['text']
        record = self.tree.item(curItem)['values']
        EntryWidgets[0].insert(0,id)
        for i in range(0, len(EntryWidgets)-1):
            EntryWidgets[i+1].insert(0,record[i])

    def clear(self, evt):
        self.searchBox.delete(0, "end")
