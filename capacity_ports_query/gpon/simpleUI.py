from tkinter import *
from tkinter import filedialog
class Application:
    def __init__(self, master=None):
        self.widget1 = Frame(master)
        self.widget1.pack()       
        self.msg1 = Label(self.widget1, text="PRIMEIRO ESCOLHA A PLANILHA COM A RELAÇÃO CONCESSÃO/EXPANSÃO")
        self.msg1.pack()
        
        self.choose1 = Button(self.widget1)
        self.choose1["text"] = "Escolha"
        self.choose1["width"] = 5
        self.choose1.bind("<Button-1>", self.choose_file1)
        self.choose1.pack(side=LEFT)
        
        self.filemsg1 = Label(self.widget1, text="")
        self.filemsg1.pack(side=RIGHT)
        
        
        self.widget2 = Frame(master)
        self.widget2.pack()
        self.msg2 = Label(self.widget2, text="ESCOLHA O ARQUIVO .CSV COM TODOS OS DADOS PARA A ANÁLISE")
        self.msg2.pack()
        
        self.choose2 = Button(self.widget2)
        self.choose2["text"] = "Escolha"
        self.choose2["width"] = 5
        self.choose2.bind("<Button-1>", self.choose_file2)
        self.choose2.pack(side=LEFT)
        
        self.filemsg2 = Label(self.widget2, text="")
        self.filemsg2.pack(side=RIGHT)
        
        
        self.widget3 = Frame(master)
        self.widget3.pack()
        self.msg3 = Label(self.widget3, text="ESCOLHA O ARQUIVO .xlsx COM OS DADOS DA CONCESSÃO DA ÚLTIMA ANÁLISE")
        self.msg3.pack()
        
        self.choose3 = Button(self.widget3)
        self.choose3["text"] = "Escolha"
        self.choose3["width"] = 5
        self.choose3.bind("<Button-1>", self.choose_file3)
        self.choose3.pack(side=LEFT)
        
        self.filemsg3 = Label(self.widget3, text="")
        self.filemsg3.pack(side=RIGHT)
         
        
        self.widget4 = Frame(master)
        self.widget4.pack()
        self.msg4 = Label(self.widget4, text="ESCOLHA O ARQUIVO .xlsx COM OS DADOS DA EXPANSÃO DA ÚLTIMA ANÁLISE")
        self.msg4.pack()
        
        self.choose4 = Button(self.widget4)
        self.choose4["text"] = "Escolha"
        self.choose4["width"] = 5
        self.choose4.bind("<Button-1>", self.choose_file4)
        self.choose4.pack(side=LEFT)
        
        self.filemsg4 = Label(self.widget4, text="")
        self.filemsg4.pack(side=RIGHT)
        
        
        self.endFrame = Frame(master)
        self.endFrame.pack()
        self.endButton = Button(self.endFrame)
        self.endButton["text"] = "Gerar relatórios"
        self.endButton["command"] = self.endFrame.quit
        self.endButton.pack()
        
        
    def choose_file1(self, event):
        self.file1 = filedialog.askopenfilename()
        self.choose1["text"] = "Escolhido"
        self.filemsg1['text'] = text=self.file1
    
            
    def choose_file2(self, event):
        self.file2 = filedialog.askopenfilename()
        self.choose2["text"] = "Escolhido"
        self.filemsg2["text"] = self.file2
    
    
    def choose_file3(self, event):
        self.file3 = filedialog.askopenfilename()
        self.choose3["text"] = "Escolhido"
        self.filemsg3["text"] = self.file3
    
    def choose_file4(self, event):
        self.file4 = filedialog.askopenfilename()
        self.choose4["text"] = "Escolhido"
        self.filemsg4["text"] = self.file4
    

class myWarning:
    def __init__(self, master=None):
        self.widget1 = Frame(master)
        self.widget1.pack()       
        self.msg1 = Label(self.widget1, text="Algo deu errado, tente novamente e certifique-se de que todos os arquivos foram escolhidos corretamente.")
        self.msg1.pack()
        
        self.endFrame = Frame(master)
        self.endFrame.pack()
        self.endButton = Button(self.endFrame)
        self.endButton["text"] = "OK"
        self.endButton["command"] = self.endFrame.quit
        self.endButton.pack()
        


def configs():
    root = Tk()
    app = Application(root)
    root.mainloop()
    
    
    
    try:
        print(app.file1)
        print(app.file2)
        print(app.file3)
        print(app.file4)
        root.fileCn = filedialog.asksaveasfilename(initialdir = ".",title = "Selecione como salvar o arquivo das concessões",filetypes = (("Microsoft Excel Format","*.xlsx"),("all files","*.*")))
        print(root.fileCn)
        root.fileEx = filedialog.asksaveasfilename(initialdir = ".",title = "Selecione como salvar o arquivo das expansões",filetypes = (("Microsoft Excel Format","*.xlsx"),("all files","*.*")))
        print(root.fileEx)
        
        return (app.file1, app.file2, app.file3, app.file4, root.fileCn, root.fileEx)
    except:
        warning = Tk()
        Wapp = myWarning(warning)
        warning.mainloop()
        



