import FacialRecognition, Vault
# create_face.create_new_face("test_user_2")                                               
# print(create_face.recognize("test_user"))
# print(create_face.recognize("test_user_2"))

def input_is_int(input):
    try:
        val = int(input)
        return val
    except ValueError:
        return None
def main_menu() -> int:
    print("Functions:")
    print("1 - Create New User")
    print("2 - Authenticate User")
    return input_is_int(input("Enter the Function (single number): "))

def check_go_back() -> bool:
    print("Do you want to go back ?")
    temp = input("(y/n), n will terminate to program: ")
    if(temp == "y" or temp == "n" or temp == "Y" or temp == "N"):
        if (temp == "y" or temp == "Y"):
            return True
        else:
            return False
    else: 
        temp = input("(y/n), n will terminate to program: ")

database = Vault.Vault()
face_database = FacialRecognition.Facial_Model()
def main():
    running = True
    while running:
        inputs = main_menu() 
        if(inputs == None or inputs > 2 or inputs < 1):
            if(check_go_back()):
                continue
            else:
                break
        if(inputs == 1):
            new_user = database.new_user()
            name = input("Input user's name: ")
            new_user.set_name(name)
            password = input("Input user's RFID: ")
            new_user.set_hash(password)
            face_database.create_new_face(new_user.get_name())
            print("New user ID : " + str(new_user.get_id()))
            print("Name: "+ new_user.get_name())
            print("Hash: "+ str(new_user.get_hash()))
            if(check_go_back()):
                continue
            else:
                break
        if(inputs == 2):
            name = input("Input user's name: ")
            if(database.exist_name(name) == False):
                print("No user name exist that matches the input.")
                if(check_go_back()):
                    continue
                else:
                    running = False
                    break
            user = database.get_user(name)
            password = input("Input user's RFID: ")
            check_rfid = check_rfid = database.verify_rfid(user,password)
            if(check_rfid):
                while(check_rfid):
                    print("RFID Authenticated.")
                    print("Scanning Face............")
                    if(face_database.recognize(user.get_name()) == True):
                        print("Authenticated!!!!!")
                        print("Welcome!!! "+user.get_name())
                        check_rfid = False
                        if(check_go_back()):
                            continue
                        else:
                            running = False
                            break
                    else:
                        print("Authentication Failed!!!")
                        print("Access Denied!!!")
                        if(check_go_back()):
                            continue
                        else:
                            running = False
                            break
            else:
                print("Authentication Failed!!!")
                print("Access Denied!!!")
                if(check_go_back()):
                    continue
                else:
                    running = False
                    break
if __name__=="__main__":
    main()