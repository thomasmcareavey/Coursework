import sqlite3
from sqlite3 import Error

class DataBase:
    def __init__(self, DbName):
        DbName = "shop.db"
        try:
            self.con = sqlite3.connect(DbName)
        except Error:
            print(Error)

        self.cursorObj = self.con.cursor()

    def fetch_all(self, table):
        self.cursorObj.execute(f'select * from {table}')
        results = self.cursorObj.fetchall()
        return results

    def retrieve_data(self, table, field, searchCriteria):
        self.cursorObj.execute(f"SELECT * FROM {table} WHERE {field} like ?",
                               (searchCriteria,))
        records = self.cursorObj.fetchall()
        return records

    def create_data(self, table, values):
        count = len(values)
        self.cursorObj.execute(f"INSERT INTO {table} VALUES (null,"+
                               ",".join(count * "?") + ")",(values))
        self.con.commit()

    def update_data(self, table, field, data, key, id):
        sql = f"UPDATE {table} SET {field} = ? WHERE {key} =?"
        self.cursorObj.execute(sql, (data,id))
        self.con.commit()

    def delete_record(self, attr, table, criteria):
        criteria = "username"
        self.cursorObj.execute(f'delete from {table} where {attr} = {criteria}')
        self.con.commit()

    def get_fields(self, table):
        self.cursorObj.execute(f'select * from {table}')
        Fields = [field[0] for field in self.cursorObj.description]
        return Fields

    def close(self):
        self.con.close()

if __name__=="__main__":
    shopDB = DataBase("shop.db")
    print(shopDB.retrieve_data("accounts", "FirstName", "Bob"))
    shopDB.update_data("accounts", "Username", "Bobby", "FirstName", "Bob")