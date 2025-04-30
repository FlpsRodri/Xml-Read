import os
from tkinter import *
import unicodedata
from tkinter import ttk,messagebox
from datetime import datetime
import pyperclip
import keyboard
import json
from xmlToSql import XmlToDatabase
from Banco_de_Dados import Db
import threading


class relogio(object):
    
    def run_clock(self,master,time=(False,0,0), date=(False,0,0), font=None, bg="white", fg="black"):
        time,timex,timey = time[0], time[1], time[2]
        date,datex,datey = date[0], date[1], date[2]
        if time:
            self.time = Label(master, text="", font=font, bg=bg, fg=fg)
            self.time.place(relx=timex, rely=timey)
        if date:
            self.date = Label(master,  font=font, bg=bg, fg=fg)
            self.date.place(relx=datex,rely=datey)    
        self.relogio(time=time,date=date)
    
    def relogio(self,time=False,date=False):
        self.tempo = datetime.now()
        if time:
            
            hora = self.tempo.strftime("%H:%M:%S")
            self.time.config(text=hora)
            self.time.after(500, lambda:self.relogio(time=True))
            
        if date:
            self.get_time()
    
    def get_time(self):
        dia = self.tempo.day
        mes = (f"0{str(self.tempo.month)}" if self.tempo.month < 10 else str(self.tempo.month))
        ano = self.tempo.strftime("%Y")
        self.date.config(text=f" {str(dia)}/{str(mes)}/{ano}")
        if not self.time:
            self.date.after(500, lambda:self.relogio(date=True))
            
class Table(object):
        
    def filter_num(self,key):
        kargs = "1234567890"
        return "".join(i for i in key if i in kargs)
    
    def window(self, master):
        def set_table_geometry():
            self.width = int(master.winfo_width() * 0.95)
            self.height = int(master.winfo_height() * 0.8)
            self.width = str(self.width)
            self.height = str(self.height)
            table_Frame.config(width=self.width, height=self.height)
            geometry.after(500, set_table_geometry)
        
        geometry = Label(master, text="", bg=self.main_bg)
        geometry.grid(column=6, row=0)
        
        entry_values_frame = LabelFrame(master, text="Entrada de Busca", bg=self.main_bg, fg=self.main_fg, font=self.main_font, width=600, height=150)
        entry_values_frame.grid(row=0, column=0,padx=20, sticky="w")
        info_add_frame = LabelFrame(master, text="Informações Adicionais", bg=self.main_bg, fg=self.main_fg, font=self.main_font)
        info_add_frame.grid(row=0, column=1, sticky="w")
        table_Frame = LabelFrame(master, text="Tabela de Produtos", bg=self.main_bg, fg=self.main_fg, font=self.main_font, width=2300, height=500)
        table_Frame.grid(row=1, column=0, columnspan=3, padx=20,sticky="w")
        set_table_geometry()
        
        Style = ttk.Style()
        Style.configure("Treeview",font=("Times",11))
        self.cb_descriptionVar = IntVar(master=entry_values_frame,value=0)
        self.cb_description = Checkbutton(master=entry_values_frame, text="Descrição exata", variable=self.cb_descriptionVar, bg=self.main_bg,fg=self.main_fg, command=lambda:print(self.cb_descriptionVar.get()))
        #self.cb_description.place(relx=0.06,rely=0.08)
        self.cb_description.grid(row=2, column=0,sticky="w")
        
        def select(*args):
            item = self.tabela.selection()[0]
            prod = self.ProdsList[(self.tabela.get_children()).index(item)]
            pyperclip.copy(prod["xProd"])
        
        def labels():
            self.value_items = StringVar(master)
            
            Label(entry_values_frame, text="GTIN / Descrição do produto",font=self.main_font,bg=self.main_bg,fg=self.main_fg).grid(row=0, column=0, sticky="nsew")
            Label(entry_values_frame, text="N° NF-e", font=self.main_font,bg=self.main_bg,fg=self.main_fg).grid(row=0, column=1, padx=5)
            Label(entry_values_frame, text="Chave de Acesso (44 digitos)", font=self.main_font,bg=self.main_bg,fg=self.main_fg).grid(row=3, column=0, columnspan=2, sticky="nsew")
            Label(info_add_frame, text="Items: ", font=self.main_font,bg=self.main_bg,fg=self.main_fg).grid(row=0, column=0, sticky="nsew")
            Label(info_add_frame, text="Maior Valor: ", font=self.main_font,bg=self.main_bg,fg=self.main_fg).grid(row=1, column=0, sticky="nsew")
            Label(info_add_frame, text="Menor Valor: ", font=self.main_font,bg=self.main_bg,fg=self.main_fg).grid(row=2, column=0, sticky="nsew")
            Label(info_add_frame, text="Res. p/ Busca", font=self.main_font, width=8,anchor=W, bg="white",fg=self.main_fg).grid(row=3, column=0, sticky="nsew")
            
            self.value_items = Label(info_add_frame, text="0", font=self.main_font,bg=self.main_bg,fg=self.main_fg)
            self.value_items.grid(row=0, column=1, sticky="nsew")
            self.value_MaxValue = Label(info_add_frame, text="0,00", font=self.main_font,bg=self.main_bg,fg=self.main_fg) 
            self.value_MaxValue.grid(row=1, column=1, sticky="nsew")
            self.value_MinValue = Label(info_add_frame, text="0,00", font=self.main_font,bg=self.main_bg,fg=self.main_fg) 
            self.value_MinValue.grid(row=2, column=1, sticky="nsew")
            
        def entrys():
            
            def filter_nnfe(*args):
                key = self.variable_nnfe.get()
                self.variable_nnfe.set(self.filter_num(key))
            def filter_keynfe(*arg):
                key = self.variable_keynfe.get()
                if len(key) < 44: self.variable_keynfe.set(self.filter_num(key=key))
                else:self.variable_keynfe.set(self.filter_num(key=key)[:44])
                
            self.variable_nnfe = StringVar(master=entry_values_frame)
            self.variable_nnfe.trace("w",filter_nnfe)
            self.variable_keynfe = StringVar(master=entry_values_frame)
            self.variable_keynfe.trace("w",filter_keynfe)
            self.variable_lim_result = StringVar(master,value="")
            
            self.prodDescription = Entry(entry_values_frame, bg=self.main_bg_entry, width=60)
            self.entry_nnfe = Entry(entry_values_frame, bg=self.main_bg_entry, textvariable=self.variable_nnfe)
            self.entry_keynfe = Entry(entry_values_frame, bg=self.main_bg_entry, textvariable=self.variable_keynfe, width=50, font="times 12 bold")
            self.entry_lim_result = Entry(info_add_frame, bg="#fff",bd=1, relief="groove", font=self.main_font, textvariable=self.variable_lim_result, width=5)
            
            self.prodDescription.focus()
            self.prodDescription.grid(row=1, column=0, sticky="nsew")
            self.entry_keynfe.grid(row=4, column=0,columnspan=2, sticky="nsew")
            self.entry_nnfe.grid(row=1, column=1, padx=5)
            self.entry_lim_result.grid(row=3, column=1, sticky="nsew")
            
            
        def table():
            colunas = ["EAN", "PRODUTO","CD", "V. UNIT", "V.DESC","QTD", "U TRIB", "V. TRIB", "QTN. TRIB", "V. TOTAL", "ICMS", "FORNECEDOR", "DATA", "NCM", "N° NFE", "C. NFE"]
            columns_geo = {"EAN":[100], "PRODUTO":[360],"CD":[30], "V. UNIT":[60], "V.DESC":[60],"QTD":[40] , "U TRIB":[35], "V. TRIB":[60], "QTN. TRIB":[40],"V. TOTAL":[90], "ICMS":[60], "FORNECEDOR":[200], "DATA":[100], "NCM":[100], "N° NFE":[100], "C. NFE":[100]}
            self.tabela = ttk.Treeview(table_Frame, columns=colunas, show="headings", style="Treeview")
            self.tabela.place(relx=0.001, rely=0.002, relwidth=0.97, relheight=0.9)
            
            vs = Scrollbar(master=table_Frame, orient="vertical", command=self.tabela.yview, width=15)
            self.tabela.configure(yscrollcommand=vs.set)
            vs.place(rely=0.002, relx=0.97, relheight=0.9)
            hs = Scrollbar(master=table_Frame, orient="horizontal", command=self.tabela.xview)
            self.tabela.configure(xscrollcommand=hs.set)
            hs.place(rely=0.9, relx=0.001, relwidth=0.97)
            
            for coluna in colunas:
                self.tabela.heading(coluna, text=coluna)
                tamanho = columns_geo[coluna][0]
                
                self.tabela.column(coluna, width=tamanho, minwidth=tamanho)
        
        labels(), entrys(), table()
        self.tabela.bind("<Double-Button-1>",select)
        self.tabela.bind("<Return>",select)
        self.prodDescription.bind("<Shift-Return>", self.shift_return)
        self.prodDescription.bind("<Return>",self.get_key)
        self.entry_nnfe.bind("<Shift-Return>", self.shift_return)
        self.entry_nnfe.bind("<Return>",self.get_key)
        self.entry_keynfe.bind("<Shift-Return>", self.shift_return)
        self.entry_keynfe.bind("<Return>",self.get_key)
        self.entry_lim_result.bind("<Shift-Return>", self.shift_return)
        self.entry_lim_result.bind("<Return>",self.get_key)

    def shift_return(self,event):
        event.widget.tk_focusPrev().focus_set()
        return "break"
    
    def table2(self,master):
        #["file_name","emitente","CNPJ|CPF","@Id","Cliente", "dhEmi","nNFe","cNFe","nNF","vTotProd", "vNF","fat",{"fat","dup"},"vTotDesc"]
        def select(*args):
            
            item = self.tabela2.selection()[0]
            nfe = self.nfeInTable[(self.tabela2.get_children()).index(item)]
            self.viewResultTable2(nfe)
            
        colunas = ["FORNECEDOR","DT. EMISSAO","N° NFE","V. TOTAL"]
        columns_geo = {"FORNECEDOR":[320],"DT. EMISSAO":[90],"N° NFE":[90],"V. TOTAL":[120]}
        self.tabela2 = ttk.Treeview(master, columns=colunas, show="headings")
        self.tabela2.place(relx=0.1, rely=0.5, relheight=0.48)
        self.tabela2.bind("<Double-Button-1>",select)
        self.tabela2.bind("<Return>",select)
        vs = Scrollbar(master=master, orient="vertical", command=self.tabela2.yview, width=15)
        self.tabela2.configure(yscrollcommand=vs.set)
        #vs.place(rely=0.5, relx=0.8 ,relheight=0.48)
        vs.place(rely=0.5, x=705, relheight=0.48)
        for coluna in colunas:
            self.tabela2.heading(coluna, text=coluna)
            tamanho = columns_geo[coluna][0]
            self.tabela2.column(coluna, width=tamanho, minwidth=tamanho)
    
    def InsertOnTable2(self,keyAgr,key):
        
        #columns : "FORNECEDOR","DT. EMISSAO","N° NFE","V. TOTAL"
        try: self.tabela2.delete(*self.tabela2.get_children())
        except Exception: pass
        
        amount = 0
        self.nfeInTable = []
        for nfe in self.list_nfe:
            if keyAgr.upper() == nfe[key]:
                amount += 1
                self.nfeInTable.append(nfe)
                dicNfe = nfe
                nfe["dhEmi"] = nfe["dhEmi"][:10]
                values = [nfe["emitente"],nfe["dhEmi"],nfe["nNFe"],nfe["vNF"]]
                self.tabela2.insert("",END,values=values)
        if amount == 1:
            self.viewResultTable2(dicNfe)
        else: dicNfe = None
        
    def viewResultTable2(self,nfe):
        #nfe = {"emitente":emitente["nome"],"CNPJ|CPF":emitente["CNPJ|CPF"],"Cliente":cliente["nome"], 
        # "dhEmi":dtEmissao,"nNFe":nNFE,"cNFe":cNFe,"nNF":nNFe,"vTotProd":vTotProd, "vNF":vTotNf,
        # "fat":{"fat":fat,"dup":dup},"vTotDesc":vTotDesc}
        pyperclip.copy(nfe["nNF"])
        self.lblFornecedor["text"] = nfe["emitente"]
        self.lblDest["text"] = nfe["Cliente"]
        self.lblNatOp["text"] = nfe["natOp"]
        
        self.lblNNf["text"] = nfe["nNFe"]
        self.lblCdNf["text"] = nfe["cNFe"]
        self.lblDtEmi["text"] = nfe["dhEmi"][:10]
        
        self.lblKeyAcess["text"] = nfe["nNF"]
        self.lblVlProd["text"] = nfe["vTotProd"]
        self.VlNf["text"] = nfe["vNF"]
        
        #fatFrame = LabelFrame(nfe_master, text="Fatura ",width=260, height=80, bg=self.main_bg, bd=1)
        #fatFrame.place(rely=0.17,relx=0.1, width=640, height=122)
    
    def Frmt(self, num):
        num = float(num)
        return format(num,".2f")
        
class app(Table,relogio):
    
    def __init__(self):
        
        
        self.root = Tk()
        self.config(self.root)
        self.menuBar()
        nb = ttk.Notebook(self.root)
        nb.place(relx=0, rely=0, relheight=1, relwidth=1)
        aba1 = Frame(nb, bg=self.main_bg)
        aba2 = Frame(nb, bg=self.main_bg)
        
        load_thread = threading.Thread(target=self._load_data_background, daemon=True)
        load_thread.start()
        nb.add(aba1, text="Buscar Produtos" )
        nb.add(aba2, text="Buscar Nota Fiscal Eletrônica")
        self.window(aba1)
        self.window_search_nfe(master=aba2)
        self.run_clock(master=aba1,time=(True,0.8,0.96),date=(True,0.85,0.96), bg=self.main_bg, font="times 12 bold")
        self.hotkeys()
        
        self.root.mainloop()
    
    def menuBar(self):
        def sobre():
            messagebox.showinfo("Sobre", "Sistema de consulta de produtos e NFe extraidps de XML\nDesenvolvido por: FelipeRodrigues\n Contato: Felipesgs@proton.me\nVersão 1.1")
        def instrucoes():
            topLevel_Info = Toplevel(self.root)
            topLevel_Info.title("Instruções")
            topLevel_Info.resizable(False,False)
            text = ('''
                    Para buscar um produto, digite o GTIN(Condigo EAN) ou parte da descrição.\n
                    Para busca extata de um produto, marque o Check Box\n
                    Para buscar uma NFe, digite o número da NFe ou a chave de acesso em seus respectivos campos de entrada.\n
                    Extras:\n
                    - Estando o checkBox desativado, o programa busca a palavra inserida em qualquer parte do nome do produto\n
                    - Adicionar o numero na nota fiscal e buscar por nome ou GTIN \n
                      a busca se dará somente na nota com o numero de NFe inerido \n
                    - Dois Cliques na tabela de produtos, copia o nome do produto para a área de transferência\n
                    - Dois cliques na tabela de NFe, copia a chave de acesso da NFe para a área de transferência\n
                    ''')
            Label(topLevel_Info, text=text, font="times 12", justify=LEFT).pack(pady=10, padx=30)
        menu_bar = Menu(self.root)
        
        help = Menu(menu_bar, tearoff=0)
        option = Menu(menu_bar, tearoff=0)
        option.add_command(label="Atualizar Dados", command=self._load_data_background)
        option.add_separator()
        option.add_command(label="Sair", command=self.root.quit)
        help.add_command(label="Sobre", command=sobre)
        help.add_command(label="Instruções", command=instrucoes)
        
        menu_bar.add_cascade(label="Opções", menu=option)
        menu_bar.add_cascade(label="Ajuda", menu=help)
        self.root.config(menu=menu_bar)
        
    def _load_data_background(self):
        print("Iniciando carregamento de dados em background...")
        self.chave_list = []
        try:
            # A lógica original de DataBase e update_values
            self.DataBase() # Esta função agora faz todo o trabalho pesado
            print("Carregamento de dados concluído.")
            # Habilitar widgets após carregar
            self.root.after(0, self._enable_widgets) # Usa after para garantir que seja executado na thread principal da GUI
        except Exception as e:
            print(f"Erro ao carregar dados em background: {e}")
            # Talvez mostrar um erro para o usuário
    
    def _enable_widgets(self):
        messagebox.showinfo("Concluido", "Dados atualizados com sucesso!")

    def update_values(self):
        
        def get_prod(prod_dict:dict):
            #print(prod_dict.keys())
            cEAN = prod_dict['cEAN']['text'] if 'cEAN' in prod_dict.keys() else "Sem Gtin"
            vDesc = prod_dict['vDesc']['text'] if 'vDesc' in prod_dict.keys() else 0
            
            prod = {'cEAN':cEAN, 'xProd':prod_dict['xProd']['text'], 'uCom':prod_dict['uCom']['text'], 'vUnCom':prod_dict['vUnCom']['text'],
                    'vDesc':vDesc, 'qntd':prod_dict['qCom']['text'], 'uTrib':prod_dict['uTrib']['text'], 
                    'vUnTrib':prod_dict['vUnTrib']['text'], 'qTrib':prod_dict['qTrib']['text'], 'vProd':prod_dict['vProd']['text'],
                    'ICMS':prod_dict['ICMS']['ICMS00']['pICMS']['text'] if "ICMS" in prod_dict.keys() else 0,
                    'emitente':self.list_nfe[-1]['emitente'], 'dtEmissao':self.list_nfe[-1]['dhEmi'],
                    'NCM':prod_dict['NCM']['text'] if "NCM" in prod_dict.keys() else "Sem NCM",
                    'nNF':self.list_nfe[-1]['nNFe'], 'cNF':self.list_nfe[-1]['cNFe']}
            return prod
        
        if len(os.listdir("NFE")) > 0:
            print("Encontrado Arquivos para adionar")
            XmlToDatabase("Xml_DB.sql", "data")
            print("Inserção de arquivos Conluida")
        
        for ind, nNf, data in self.data_master:
            if nNf in self.chave_list: continue
            nfe={}
            self.chave_list.append(nNf)
            data = json.loads(data)
            
            ide = data['ide']
            emit = data['emit']
            det = data['det']
            total = data['total']
            CNPJ = emit['CNPJ']['text'] if 'CNPJ' in emit.keys() else emit['CPF']['text']
            date = (ide['dhEmi']['text'][:10]).split("-")
            date = f"{date[2]}-{date[1]}-{date[0]}"
            nfe = {'emitente':(emit['xNome']['text']).upper(), 'nNF':nNf, 'natOp':ide['natOp']['text'],'nNFe':ide['nNF']['text'],'cNFe':ide['cNF']['text'],
                    'dhEmi':date, 'CNPJ|CPF':CNPJ, 'vNF':total['ICMSTot']['vNF']['text'], 'vTotProd':total['ICMSTot']['vProd']['text'],
                    'vTotDesc':total['ICMSTot']['vDesc']['text'],'fat':{'fat':'None','dup':'None'},'Cliente':"Not Found"}
            self.list_nfe.append(nfe)
            
            if type(det) == list:
                for i in det:
                    i = i['prod']
                    self.produtos.append(get_prod(i))
            else:
                self.produtos.append(get_prod(det['prod']))
        self.list_nfe.sort(key=lambda x: datetime.strptime(x['dhEmi'],'%d-%m-%Y'), reverse=True)
        self.filter_combobox_emitent(None)
        
        return True
    
    def DataBase(self):
        
        self.list_nfe = []
        self.produtos = []
        print("Conectando ao banco de dados...")
        self.db = Db(bank_name="Xml_DB.sql", table="data")
        print("Carregando dados...")
        self.data_master = (self.db.consultDB())
        self.data_master = self.data_master[1:]
        print("Dados carregados com sucesso!")
        self.update_values()
    
    def hotkeys(self):
        def F11():
            self.screenSet = False if self.screenSet == True else True
            self.root.attributes("-fullscreen",self.screenSet)
        self.screenSet = False
        keyboard.add_hotkey("F11",F11)
    
    def config(self, master):
        self.main_bg = "#ddd"
        self.main_fg = "#000000"
        self.main_geometry = {"height":"720","width":"1300"}
        self.main_title = "Tabela Produtos"
        #self.main_icon = "icon.ico"
        self.main_title_font = "times 18 bold"
        self.main_font = "consolas 12"
        self.main_bg_entry = "#F3FCA1"
        
        master.state("zoomed")
        master["bg"] = self.main_bg
        master.title(self.main_title)
        master.geometry(f"{self.main_geometry['width']}x{self.main_geometry['height']}")
        master.minsize(800,600)
        #master.minsize(self.main_geometry['width'],self.main_geometry['height'])
        #master.resizable(False,False)
        
    def normalize_text(self, text):
        # Remove acentos e substitui ç por c
        text = unicodedata.normalize('NFD', text)
        text = text.encode('ascii', 'ignore').decode('utf-8')
        text = text.upper()
        return text.replace('Ç', 'C')
        
    def filter_combobox_emitent(self, event):
        typed = self.normalize_text(self.cbb_emitent.get())
        all_values = sorted(set(map(lambda x: x["emitente"], self.list_nfe)), key=str.upper)

        if typed == "":
            self.cbb_emitent['values'] = all_values
        else:
            filtered = [item for item in all_values if typed in self.normalize_text(item)]
            self.cbb_emitent['values'] = filtered
            #if filtered:
            #    self.cbb_emitent.event_generate('<Down>')
        
    def window_search_nfe(self, master):
        master = LabelFrame(master, width=800)
        master.pack(anchor=CENTER,fill=Y,expand=Y)
        master_widgets = Frame(master, bg=self.main_bg)
        master_widgets.place(relx=0, rely=0, relwidth=1, relheight=0.55)
        
        def labels():
            Label(master_widgets, text="N° Nota Fiscal",  font=self.main_font, bg=self.main_bg, fg=self.main_fg).place(relx=0.1, rely=0.05)
            Label(master_widgets, text="Cd Nota Fiscal",  font=self.main_font, bg=self.main_bg, fg=self.main_fg).place(relx=0.5, rely=0.05)
            Label(master_widgets, text="Fornecedor",      font=self.main_font, bg=self.main_bg, fg=self.main_fg).place(relx=0.1, rely=0.18)
            Label(master_widgets, text="Chave de acesso", font=self.main_font, bg=self.main_bg, fg=self.main_fg).place(relx=0.1, rely=0.32)
             
        def entrys():
            
            font = "times 12 bold"
            self.entry_Nnf = Entry(master_widgets, bg="#F3FCA1", width=25, font=font)
            self.entry_Cnf = Entry(master_widgets, bg="#F3FCA1", width=25, font=font)
            values = list(map(lambda x: x["emitente"], self.list_nfe))
            values = sorted(set(values), key=str.upper)
            self.cbb_emitent = ttk.Combobox(master_widgets,values=values, width=68, font=font)
            self.keyAcessVar = StringVar()
            self.entry_KeyAcess = Entry(master_widgets,textvariable=self.keyAcessVar, bg="#F3FCA1", width=70, font=font)
            self.entry_Nnf.place(relx=0.1, rely=0.12)
            self.entry_Cnf.place(relx=0.5, rely=0.12)
            self.cbb_emitent.place(relx=0.1, rely=0.25)
            self.entry_KeyAcess.place(relx=0.1, rely=0.39)
            self.entry_Nnf.bind("<Return>",self.get_key)
            self.entry_Cnf.bind("<Return>",self.get_key)
            self.cbb_emitent.bind("<Return>",self.get_key)
            self.entry_KeyAcess.bind("<Return>",self.get_key)
            
            self.cbb_emitent.bind("<KeyRelease>",self.filter_combobox_emitent)
        
        def nfe():
            
            font = "consolas 10 bold"
            nfe_master = Frame(master, bg=self.main_bg)
            nfe_master.place(relx=0, rely=0.55, relwidth=1, relheight=1)
            
            titleFrame = LabelFrame(nfe_master, width=290, height=80, bg=self.main_bg, bd=1)
            #titleFrame.place(rely=0, relx=0.05, width=260, height=122)
            titleFrame.grid(row=0, column=0, sticky="nsew")
            
            Label(titleFrame,text="Fornecedor", bg=self.main_bg, fg=self.main_fg, font=font,anchor=W).pack(anchor=W)
            self.lblFornecedor = Label(titleFrame,text="", bg=self.main_bg, fg=self.main_fg, font=font)
            self.lblFornecedor.pack(anchor=W)
            Label(titleFrame,text="Destinatario", bg=self.main_bg, fg=self.main_fg, font=font).pack(anchor=W)
            self.lblDest = Label(titleFrame,text="", bg=self.main_bg, fg=self.main_fg, font=font)
            self.lblDest.pack(anchor=W)
            Label(titleFrame,text="Nat. da Operação", bg=self.main_bg, fg=self.main_fg, font=font).pack(anchor=W)
            self.lblNatOp = Label(titleFrame,text="", bg=self.main_bg, fg=self.main_fg, font=font)
            self.lblNatOp.pack(anchor=W)
            
            infoFrame = LabelFrame(nfe_master, width=120, height=80, bg=self.main_bg, bd=1)
            #infoFrame.place(rely=0,relx=0.34, width=120, height=122)
            infoFrame.grid(row=0, column=1, sticky="nsew")
            
            Label(infoFrame,text="N° NF-e", bg=self.main_bg, fg=self.main_fg, font=font).pack(anchor=W)
            self.lblNNf = Label(infoFrame,text="", bg=self.main_bg, fg=self.main_fg, font=font)
            self.lblNNf.pack(anchor=W)
            Label(infoFrame,text="Cd. NF-e", bg=self.main_bg, fg=self.main_fg, font=font).pack(anchor=W)
            self.lblCdNf = Label(infoFrame,text="", bg=self.main_bg, fg=self.main_fg, font=font)
            self.lblCdNf.pack(anchor=W)
            Label(infoFrame,text="Dt. Emis.", bg=self.main_bg, fg=self.main_fg, font=font).pack(anchor=W)
            self.lblDtEmi = Label(infoFrame,text="", bg=self.main_bg, fg=self.main_fg, font=font)
            self.lblDtEmi.pack(anchor=W)
            
            indFrame = LabelFrame(nfe_master, width=260, height=80, bg=self.main_bg, bd=1)
            #indFrame.place(rely=0,relx=0.475, width=340, height=122)
            indFrame.grid(row=0, column=2, sticky="nsew")
            
            Label(indFrame,text="Chave de Acesso", bg=self.main_bg, fg=self.main_fg, font=font).pack(anchor=W)
            self.lblKeyAcess = Label(indFrame,text="", bg=self.main_bg, fg=self.main_fg, font=font)
            self.lblKeyAcess.pack(anchor=W)
            Label(indFrame,text="Valor dos Produtos", bg=self.main_bg, fg=self.main_fg, font=font).pack(anchor=W)
            self.lblVlProd = Label(indFrame,text="", bg=self.main_bg, fg=self.main_fg, font=font)
            self.lblVlProd.pack(anchor=W)
            Label(indFrame,text="Valor da Nota", bg=self.main_bg, fg=self.main_fg, font=font).pack(anchor=W)
            self.VlNf = Label(indFrame,text="", bg=self.main_bg, fg=self.main_fg, font=font)
            self.VlNf.pack(anchor=W)
            
            fatFrame = LabelFrame(nfe_master, text="Fatura ",width=800, height=120, bg=self.main_bg, bd=1)
            #fatFrame.place(relx=0.05, rely=0.2, width=722, height=122)
            fatFrame.grid(row=1, column=0, columnspan=3, sticky="nsew")

        self.table2(master=master_widgets)
        labels(), entrys(), nfe()
        
    def searchProd(self, prod, manage=None, per_result="ALL", filter=None):
        
        self.ProdsList = []
        self.value_items["text"] = "0"
        self.value_MaxValue["text"] = "0,00"
        self.value_MinValue ["text"] = "0,00"
        self.tabela.delete(*self.tabela.get_children())
        self.count,self.max,self.min = 0,0,0
        def calc_info(value):
            value = float(self.Frmt(value))
            self.count +=1
            self.max = value if value > self.max else self.max
            if self.min == 0: self.min = value
            elif value < self.min: self.min = value 
        def insertOnTable():
            
            def sorted_prod():
                
                value = []
                newList = []
                for ind,i in enumerate(self.ProdsList):
                    if type(i["dtEmissao"]) == str and "T" in i["dtEmissao"]:
                        i["dtEmissao"] = ((i["dtEmissao"]).split("T"))[0]
                        i['dtEmissao'] = datetime.strptime(i['dtEmissao'], "%Y-%m-%d")
                        i['dtEmissao'] = i['dtEmissao'].strftime("%d-%m-%Y")
                    
                    date = i["dtEmissao"].split("-")
                    date = reversed(date)
                    date = "".join(date)
                    date = int(date)
                    value.append((ind,date))
                value = sorted(value, key=lambda x: x[1], reverse=True)
                for ind,date in value:
                    newList.append(self.ProdsList[ind])
                self.ProdsList = newList
                
                return value
            sorted_prod()
            
            for amount, i in enumerate(self.ProdsList):
                if not per_result == "ALL":
                    if amount == int(per_result): break
                
                self.tabela.insert("",END,values=list(i.values()))
                calc_info(i["vUnCom"])
            
        if not self.cb_descriptionVar.get() and manage!="NNFe":
            values = prod.split(" ")
            def check_and(keys,words):
                for key in keys:
                    if key.lower() not in words.lower():
                        return False
                return True
            for i in self.produtos:
                xProd = i["xProd"]
                if filter:
                    if check_and(keys=values, words=xProd) and filter == str(i["nNF"]):
                        self.ProdsList.append(i)
                    else:
                        if prod in str(i["cEAN"]) and filter == str(i["nNF"]):
                            self.ProdsList.append(i)
                else:
                        if check_and(keys=values, words=xProd):
                            self.ProdsList.append(i)
                        else:
                            if prod in str(i["cEAN"]):
                                self.ProdsList.append(i)
                    
            insertOnTable()
                             
        elif manage == "NNFe":
            for i in self.produtos:
                if prod == i["nNF"]:
                    self.ProdsList.append(i)
            insertOnTable()
        
        else:
            for i in self.produtos:
                if ((prod.lower() in str(i["xProd"]).lower()) or (prod in str(i["cEAN"]))):
                    if filter:
                        if filter == i["nNF"]:
                            self.ProdsList.append(i)
                    else:
                        self.ProdsList.append(i)
                        
            insertOnTable()
            
        self.value_items["text"], self.value_MaxValue["text"], self.value_MinValue ["text"] = self.count, self.max, self.min
                    
    def searcheNFe(self,key_nfe):
        try: self.tabela.delete(*self.tabela.get_children())
        except Exception: pass
        not_s = True
        for index,NFe in enumerate(self.list_nfe):
            
            if key_nfe in NFe["nNF"]:
                not_s = False
                self.searchProd(prod=NFe["nNFe"],manage="NNFe")
            elif ((index + 1) == len(self.list_nfe)) and not_s:
                messagebox.showinfo("Sem Registro", "Chave de acesso não encontrada no banco de dados")
    
    def get_key(self,event):
        if not event.widget.get():
            event.widget.tk_focusNext().focus()
        elif event.widget in (self.prodDescription, self.entry_nnfe, self.entry_keynfe):
            pyperclip.copy(event.widget.get())
            if event.widget == self.prodDescription :
                try:
                    per_result = self.variable_lim_result.get() if int(self.variable_lim_result.get())>0 else "ALL"
                except Exception :
                    self.variable_lim_result.set("")
                    per_result = "ALL"
                if self.entry_nnfe.get() or self.entry_keynfe.get():
                    self.searchProd(event.widget.get(),per_result=per_result, filter=self.entry_nnfe.get())
                else:
                    self.searchProd(event.widget.get(),per_result=per_result)
                self.prodDescription.delete(0,END)
                
            elif self.entry_nnfe.get() and (event.widget == self.entry_nnfe):
                self.searchProd(prod=self.entry_nnfe.get(), manage="NNFe")
                self.entry_nnfe.delete(0,END)
                
            elif self.entry_keynfe.get() and (event.widget == self.entry_keynfe):
                if len(self.entry_keynfe.get()) == 44:
                    self.searcheNFe(key_nfe=self.entry_keynfe.get())
                    self.entry_keynfe.delete(0,END)
                else: messagebox.showerror("Chave Inválida", "CHAVE INVÁLIDA\n Verifique o codigo e tente novamente.")
                self.entry_nnfe.delete(0,END)
           
                  # Mudar o foco para o segundo campo de entrada
        elif event.widget in (self.entry_Nnf, self.entry_Cnf, self.cbb_emitent, self.entry_KeyAcess):
            pyperclip.copy(event.widget.get())
            if event.widget.get():
                value = event.widget.get()
                if event.widget == self.entry_Nnf: 
                    self.entry_Nnf.delete(0,END)
                    key = "nNFe"
                elif event.widget == self.entry_Cnf: 
                    self.entry_Cnf.delete(0,END)
                    key = "cNFe"
                elif event.widget == self.cbb_emitent:
                    key = "emitente"
                    self.cbb_emitent.set("")
                else:
                    self.entry_KeyAcess.delete(0,END)
                    key = "nNF"
                self.InsertOnTable2(keyAgr=value,key=key)
    
if __name__ == "__main__":
    run=app()   
