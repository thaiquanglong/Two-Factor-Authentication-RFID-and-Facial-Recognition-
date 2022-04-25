from asyncio.windows_events import NULL
import sqlite3
import hashlib
import hmac
class User:
    def __init__(self, db: sqlite3.Connection, id) -> None:
        self.db = db
        if id == NULL:
            self.make_user("NULL","NULL","NULL")
        else:
            if type(id) is int:
                if self.exist(id) == True:
                    self.get_user(id)
            elif type(id) is str:
                if self.exist_name(id) == True:
                    self.get_user_name(id)
            else:
                self.make_user_ID(id, "NULL","NULL","NULL")
    
    def get_user_name(self, name:str) -> None:
        cursor = self.db.cursor()
        temp = cursor.execute("SELECT * FROM PASSWORDS WHERE USER_NAME = '" +name+"';").fetchone()      
        self.ID = temp[0]
        self.name = temp[1]
        self.hash = temp[2]
        self.face_data = temp[3]
        self.db.commit()
        cursor.close()
    
    def exist(self,id: int) -> bool:
        cursor = self.db.cursor()
        temp = cursor.execute("SELECT * FROM PASSWORDS WHERE ID =" +str(id)+";").fetchone()
        self.db.commit()
        cursor.close()
        if (temp == None):
            return False
        return True
    
    def exist_name(self,name: str) -> bool:
        cursor = self.db.cursor()
        temp = cursor.execute("SELECT * FROM PASSWORDS WHERE USER_NAME = '" +name+"';").fetchone()      
        self.db.commit()
        cursor.close()
        if (temp == None):
            return False
        return True
        
    def make_user(self, name: str, hash: str, face_data: str) -> None:
        cursor = self.db.cursor()
        cursor.execute('INSERT INTO "PASSWORDS"("USER_NAME","HASH","FACE_DATA") VALUES (' + name+" ,"+hash+","+face_data+");")
        self.ID = cursor.execute('''SELECT seq FROM sqlite_sequence WHERE name = "PASSWORDS";''').fetchall()[0][0]
        self.name = name
        self.hash = hash
        self.face_data = face_data
        self.db.commit()
        cursor.close()


    def make_user_ID(self,id: int, name: str, hash: str, face_data: str) -> None:
        cursor = self.db.cursor()
        cursor.execute('INSERT INTO "PASSWORDS" VALUES ('+ str(id)+", " + name+" ,"+hash+","+face_data+");")
        self.ID = cursor.execute('''SELECT seq FROM sqlite_sequence WHERE name = "PASSWORDS";''').fetchall()[0][0]
        self.name = name
        self.hash = hash
        self.face_data = face_data
        self.db.commit()
        cursor.close()


    def get_user(self, id: int) -> None:
        cursor = self.db.cursor()
        temp = cursor.execute("SELECT * FROM PASSWORDS WHERE ID = " +str(id)+";").fetchone()
        self.ID = temp[0]
        self.name = temp[1]
        self.hash = temp[2]
        self.face_data = temp[3]
        self.db.commit()
        cursor.close()

    def set_name(self, name: str) -> None:
        cursor = self.db.cursor()
        cursor.execute('UPDATE PASSWORDS SET USER_NAME = \"'+name+'\" WHERE ID = '+str(self.ID)+';')
        self.db.commit()
        cursor.close()
        self.name = name

    def get_name(self) -> str:
        return self.name
    
    def set_hash(self, password: str) -> None:
        cursor = self.db.cursor()
        hash = hash_new_password(password,self.get_name())
        sqlite_insert_blob_query = 'UPDATE PASSWORDS SET HASH = ? WHERE ID = ?;'
        cursor.execute(sqlite_insert_blob_query,(hash, str(self.ID)))
        self.db.commit()
        cursor.close()
        self.hash = hash

    def get_hash(self) -> bytes:
        return self.hash

    def set_face_data(self, face_data: str) -> None:
        cursor = self.db.cursor()
        hash = hash_new_password(face_data,self.get_name())
        sqlite_insert_blob_query = 'UPDATE PASSWORDS SET FACE_DATA = ? WHERE ID = ?;'
        cursor.execute(sqlite_insert_blob_query,(hash, str(self.ID)))        
        self.db.commit()
        cursor.close()
        self.face_data = hash

    def get_face_data(self) -> str:
        return self.face_data

    def get_id(self) -> int:
        return self.ID

class Vault:
    def __init__(self) -> None:
        self.db = sqlite3.connect('Vault.db')
        cursor = self.db.cursor()
        if cursor.execute('''SELECT "PASSWORDS" FROM sqlite_master WHERE type='table';''').fetchall() != []:
            return
        else:
            cursor.execute('''CREATE TABLE IF NOT EXISTS "PASSWORDS" (
                "ID"	INTEGER,
                "USER_NAME"	NVARCHAR(200) UNIQUE,
                "HASH"	BLOB,
                "FACE_DATA"	BLOB,
                PRIMARY KEY("ID" AUTOINCREMENT)
                );''')
        self.db.commit()
        
    def new_user(self) -> User:
        return User(self.db, NULL)
    
    def exist(self,id: int) -> bool:
        cursor = self.db.cursor()
        temp = cursor.execute("SELECT * FROM PASSWORDS WHERE id = " +str(id)+";").fetchone()      
        self.db.commit()
        cursor.close()
        if (temp == None):
            return False
        return True

    def exist_name(self,name: str) -> bool:
        cursor = self.db.cursor()
        temp = cursor.execute("SELECT * FROM PASSWORDS WHERE USER_NAME = '" +name+"';").fetchone()      
        self.db.commit()
        cursor.close()
        if (temp == None):
            return False
        return True

    def get_user(self, id) -> User:
        if type(id) is int:
            if self.exist(id) == False:
                return NULL
        if type(id) is str:
            if self.exist_name(id) == False:
                return NULL
        return User(self.db,id)
        
    def new_user_ID(self,id: int) -> User:
        if (self.exist(id) == True):
            return self.get_user(id)
        return User(self.db, id)
    
    def verify_rfid(self, user: User, password: str) -> bool:
        return is_correct_password(password,user.get_name(),user.get_hash())

    def close(self) -> None:
        self.db.close()

def hash_new_password(password: str, salt: str) -> bytes:
    pw_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return pw_hash

def is_correct_password(password: str, salt: str, pw_hash: bytes) -> bool:
    return hmac.compare_digest(
        pw_hash,
        hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    )


