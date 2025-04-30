import sqlite3
import json

class Db:
    def __init__(self, bank_name:str = None, table:str = None):
        if bank_name:
            if self.check_db(bank_name):
                self.bank_name = bank_name
                self.table = table
                self.connect(bank_name, table)
            else:
                raise Exception(f"Database {bank_name} does not exist.")
        pass
    
    def check_db(self, bank_name:str):
        try:
            with open(bank_name, "r") as file:
                return True
        except Exception as ERROR:
            print(ERROR)
            return False
    
    def connect(self, bank_name:str, table:str):
        try:
            self.bank = sqlite3.connect(bank_name)
            self.cursor = self.bank.cursor()
            self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if not self.cursor.fetchone():
                raise Exception(f"Table {table} does not exist in {bank_name}.")
        except Exception as ERROR:
            print(ERROR)
            pass
    
    def createBank(self, bank_name:str, table:str,columns:list):
        try:
            self.bank = sqlite3.connect(bank_name)
            self.cursor = self.bank.cursor()
            columnsName = columns
            temp =""
            for i in columns:
                type_ = " json_data," if "json" in i.lower() else " text,"
                temp += i + type_
            columns = temp[:-1]
            temp=""
            columns ="id integer primary key autoincrement, " + columns
            self.cursor.execute(f"create table if not exists {table} ({columns}) ")
            self.bank.commit()
            for index,i in enumerate(columnsName):
                if (index+1) != len(columnsName):
                    temp += i + ", "
                else:
                    temp += i 
            columnsName = temp
            if len(self.consultDB(table)) == 0:
                values = ("Null, " * len(columnsName.split(",")))[:-2]
                self.cursor.execute(f"INSERT INTO {table} ({columnsName}) VALUES ({values})")
                self.bank.commit()
                
        except Exception as ERROR: 
            print(ERROR)
            return ERROR

    def consultDB(self,table: str=None):
        if not table: table = self.table
        try:
            self.cursor.execute(f"SELECT * FROM {table}")
            return self.cursor.fetchall()
        except Exception as ERROR: return ERROR
        
    def Insert(self, columns:list, values:list, table:str=None):
        try:
            _list = []
            if not table: table = self.table
            for index,column in enumerate(columns):
                if len(columns) != (index + 1):
                    _list.append( column + ",")
                    #_list_values.append( values + ",")
                else:
                    _list.append( column)
                    #_list_values.append( values)
            columns = ""
            for i in _list: columns+=i
            #print(columns)
            self.cursor.execute(f"INSERT INTO {table} ({columns}) VALUES ({values})")
            self.bank.commit()
            return True
        except Exception as ERROR: return ERROR
                
    def Update(self,columns:list, values:list, whereID:int,table:str=None):
        if not table: table = self.table
        try:
            _list = []
            
            for index,column in enumerate(columns):
                if len(columns) != (index + 1):
                    _list.append( column + "=" + (f"'{values[index]}'") + ",")
                else:
                    _list.append( column + "=" + (f"'{values[index]}'"))
            columns = ""
            for i in _list: 
                columns +=i
                
            
            self.cursor.execute(f"UPDATE {table} SET {columns} WHERE id = {whereID}")
            self.bank.commit()
        except Exception as ERROR:
            print(ERROR)
            return ERROR
            
    def Delete(self,table:str,where:str):
        if not "=" in str(where): return False  
        self.cursor.execute(f"DELETE FROM {table} WHERE {where}")
        self.bank.commit()
    
    def closeDB(self):
        self.bank.close()

class app():
    
    def __init__(self, *args, **kwargs):
        db = Db()
        db.createBank("teste.sql", "data", ["chave_nfe","json_data"])
        valueDic = {"dev":"Felipe","contato":"felipesgs@proton.me"}
        valueDic = json.dumps(valueDic)
        chave, xml = "151684646546", valueDic
        print(db.Insert("data", ["chave_nfe","json_data"], f"'{chave}','{xml}'"))
        #db.Update("data", ["json_data"], [valueDic], 1)
        data = db.consultDB("data")
        print(data)
        db.closeDB()
        
if __name__ == "__main__":
    app()
        
