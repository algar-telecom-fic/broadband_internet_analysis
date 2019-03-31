from tkinter import *
from tkinter import filedialog


class ChoseFileWindow:
    def __init__(self, master=None):
        self.file1 = ""
        self.file2 = ""

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

        self.endFrame = Frame(master)
        self.endFrame.pack()
        self.endButton = Button(self.endFrame)
        self.endButton["text"] = "Gerar relatórios"
        self.endButton["command"] = self.endFrame.quit
        self.endButton.pack()


    def choose_file1(self, event):
        self.file1 = filedialog.askopenfilename()
        self.choose1["text"] = "Escolhido"
        self.filemsg1['text'] = self.file1


    def choose_file2(self, event):
        self.file2 = filedialog.askopenfilename()
        self.choose2["text"] = "Escolhido"
        self.filemsg2["text"] = self.file2


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


class UIManager:
    def __init__(self):
        root = Tk()
        app = ChoseFileWindow(root)
        root.mainloop()
        try:
            print(app.file1)
            print(app.file2)

            self.cidade_filename = app.file1
            self.dados_filename  = app.file2
        except:
            warning = Tk()
            Wapp = myWarning(warning)
            warning.mainloop()

    def get_filenames(self):
        return (self.cidade_filename, self.dados_filename)
