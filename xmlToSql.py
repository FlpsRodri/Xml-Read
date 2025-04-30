import xml.etree.ElementTree as ET
import os
import json
from Banco_de_Dados import Db
from time import time

class XmlToDatabase:
    
    def __init__(self, bank_name:str, table:str):
        self.bank_name = bank_name
        self.table = table
        self.dir = "NFE"
        self.dir_arq = "Arq"
        self.chave_list = []
        self.xml = []
        self.key_nfe = None
        
        self.connect_bank()
        xmlList = self.get_filesName()
        for xml in xmlList:
            self.key_nfe = None
            json_data = self.xmlToJson(xml)
            json_dict = json.loads(json_data)
            json_data = json.dumps(json_dict, ensure_ascii=False)
            json_data = json_data.replace("'"," ")
            json_data = json_data.replace("{http://www.portalfiscal.inf.br/nfe}","")
            json_dict = json.loads(json_data)
            json_dict = self.get_only_xml(json_dict)
            if json_dict:
                self.creat_resumed_xml_dict(json_dict)
                self.move_file_to_arq(xml)
        
        self.db.closeDB()
        print("Importação finalizada")
        return self.chave_list
            
    def move_file_to_arq(self, file_name:str):
        try:
            os.makedirs("arq", exist_ok=True)
            if self.key_nfe in self.chave_list:
                print("File on the list")
                os.remove(f"{self.dir}\\{file_name}")
                print("removed file ", file_name)
                return False
            os.rename(f"{self.dir}/{file_name}", f"{self.dir_arq}/{file_name}")
            print("moveu")
        except Exception as ERROR:
            return ERROR
        
    def creat_resumed_xml_dict(self, json_dict:dict):
        try:
            if json_dict:
                ide = self.get_only_xml(xmlDict=json_dict, keyArg="ide")
                emit = self.get_only_xml(xmlDict=json_dict, keyArg="emit")
                det = self.get_only_xml(xmlDict=json_dict, keyArg="det")
                total = self.get_only_xml(xmlDict=json_dict, keyArg="total")
                xml =  {"ide":ide, "emit":emit, "det":det, "total":total}
                self.insert_xml_in_db(self.key_nfe, xml)
                
        except Exception as ERROR:
            print(ERROR,"1")
            return ERROR
    
    def insert_xml_in_db(self, chave_nfe:str, xml_dict:dict):
        try:
            json_data = json.dumps(xml_dict, ensure_ascii=False)
            if not chave_nfe in self.chave_list:
                if self.db.Insert(table=self.table,columns= ["chave_nfe","json_data"],values= f"'{chave_nfe}','{json_data}'"):
                    print("inserido "+chave_nfe)
            #print(len(self.db.consultDB(self.table)))
            
        except Exception as ERROR:
            print(ERROR,"2")
            return ERROR
        
    def get_only_xml(self, xmlDict:dict, keyArg:str=None):
        try:
            if keyArg:
                if keyArg in xmlDict.keys():
                    for i in xmlDict.keys():
                        if keyArg in i:
                            return xmlDict[i]
                else:
                    k = list(xmlDict.keys())[0]
                    return self.get_only_xml(xmlDict=xmlDict[k],keyArg=keyArg)
                        
            if list(xmlDict.keys())[0] == "nfeProc":
                self.key_nfe = xmlDict["nfeProc"]["protNFe"]["infProt"]["chNFe"]["text"]
                return self.get_only_xml(xmlDict["nfeProc"])
            
            return xmlDict["NFe"]
            
            
        except Exception as ERROR:
            #print(keyArg)
            #print(xmlDict)
            print(ERROR,"#")
            return False
    
    def connect_bank(self):
        
        self.db = Db()
        self.db.createBank(bank_name=self.bank_name, table=self.table, columns=["chave_nfe","json_data"])
        self.db.Update(table=self.table, columns= ["chave_nfe","json_data"], values=["Dev:FelipeRodrigues", "Contato:felipesgs@proton.me"],whereID=1)
        #self.db.Delete(self.table,"id=2")
        data_base_value = self.db.consultDB("data")

        for value in data_base_value:
            id = value[0]
            if int(id) > 1:
                
                xml = value[2]
                #self.db.Update(table=self.table, columns=["json_data"], values=[xml], whereID=id)
                #print("update", id, "\n")
                
                xml = json.loads(xml)
                chave = value[1]
                if chave == "None":
                    chave = xml["ide"]["chNFe"]["text"]
                    self.db.Update(table=self.table, columns=["chave_nfe"],values=[chave],whereID=id)
                    print(chave)
                    print("Update #2")
                self.chave_list.append(chave)
                self.xml.append(xml)
            
    def get_filesName(self):
        try:
            xmlList = os.listdir(self.dir)
            xmlList = [file for file in xmlList if (file.endswith('.xml') or file.endswith('.XML'))]
            return xmlList
        except Exception as ERROR:
            print(ERROR,"4")
            return ERROR

    def xmlToJson(self, xml:str):
        try:
            tree = ET.parse(f'{self.dir}/{xml}')
            root = tree.getroot()
            xml_dict = {root.tag: self._element_to_dict(root)}
            json_data = json.dumps(xml_dict, ensure_ascii=False)
            return json_data
        except Exception as ERROR:
            print(ERROR,"5")
            return ERROR

    def _element_to_dict(self, element):
        node = {}
        if element.text:
            node['text'] = element.text.strip()
        for child in element:
            child_dict = self._element_to_dict(child)
            if child.tag not in node:
                node[child.tag] = child_dict
            else:
                if not isinstance(node[child.tag], list):
                    node[child.tag] = [node[child.tag]]
                node[child.tag].append(child_dict)
        return node


if __name__ == '__main__':
    Time = time()
    XmlToDatabase("Xml_DB.sql", "data")
    print(time()-Time)
    