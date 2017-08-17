import requests


class ChatRoomApiClient:
    username = None
    password = None
    token = None

    def __init__(self):
        pass

    def start(self):
        choice = str(input("[1] Login\t"
                           "[2] SignUp\t"
                           "[3] View your details\t"
                           "[4] View ChatRoomsList\t"
                           "[5] RoomMessages\t"
                           "[6] Send Message\n"
                           "[7] Add New member to ChatRoom\t"
                           "[8] Create new ChatRoom\t"
                           "[9] Delete ChatRoom\t"
                           "[10] Rename ChatRoom\n"
                           "[11] View Members in ChatRoom\t"
                           "[12] Logout\t"
                           "[13] ExitChatroom\t"
                           "[ ] Any other key to exit : \n"))
        if choice == str(1):
            self.login()
            self.start()
        elif choice == str(2):
            self.register()
            self.start()
        elif choice == str(3):
            self.view_my_details()
            self.start()
        elif choice == str(4):
            self.get_my_chatrooms()
            self.start()
        elif choice == str(5):
            self.get_room_messages()
            self.start()
        elif choice == str(6):
            self.send_message()
            self.start()
        elif choice == str(7):
            self.add_member()
            self.start()
        elif choice == str(8):
            self.new_chatroom()
            self.start()
        elif choice == str(9):
            self.delete_chatroom()
            self.start()
        elif choice == str(10):
            self.rename_chatroom()
            self.start()
        elif choice == str(11):
            self.get_chatroom_members()
            self.start()
        elif choice == str(12):
            self.logout()
            self.start()
        elif choice == str(13):
            self.exit_chatroom()
            self.start()
        else:
            return None

    def login(self):
        if self.token is not None:
            print("Already Logged In..")
            print("Logout to Re-login")
            return None
        if self.username is None:
            self.username = str(input("Enter username : "))
        if self.password is None:
            self.password = str(input("Enter Password : "))
        if self.username is None or self.password is None:
            print("Username and Password required")
            self.login()
        else:
            url = 'http://127.0.0.1:8000/auth/obtaintoken/'
            data = {'username': self.username, 'password': self.password}
            try:
                response = requests.post(url=url, data=data)
                if response.status_code == 200:
                    self.token = response.json()['token']
                    print("Logged in as {}".format(self.username))
                else:
                    print("Invalid login credentials")
                    self.username = None
                    self.password = None
                print(response.json())
            except:
                print("Problem connecting to server")

    def view_my_details(self):
        if self.verify_token():
            url = 'http://127.0.0.1:8000/accounts/mydetails/'
            headers = {'Authorization': 'JWT {}'.format(self.token)}
            try:
                response = requests.get(url=url, headers=headers)
                if response.status_code != 200:
                    print("Problem viewing details")
                print(response.json())
            except:
                print("Problem connecting to server")

    def get_my_chatrooms(self):
        if self.verify_token():
            url = 'http://127.0.0.1:8000/mychatrooms/'
            headers = {'Authorization': 'JWT {}'.format(self.token)}
            try:
                response = requests.get(url=url, headers=headers)
                if response.status_code == 200:
                    print("ChatroomsList Retrieved")
                else:
                    print("Something wrong...")
                print(response.json())
            except:
                print("Problem connecting to server")

    def get_chatroom_members(self):
        if self.verify_token():
            chatroom_slug = str(input("Enter chatroom slug : "))
            url = 'http://127.0.0.1:8000/chatroom/{}/memberslist/'.format(chatroom_slug)
            headers = {'Authorization': 'JWT {}'.format(self.token)}
            try:
                response = requests.get(url=url, headers=headers)
                if response.status_code == 200:
                    print("Members List Retrieved")
                else:
                    print("Problem Retrieving Members List")
                print(response.json())
            except:
                print("Problem connecting to server")

    def new_chatroom(self):
        if self.verify_token():
            chatroom_name = str(input("Enter ChatRoom Name : "))
            url = 'http://127.0.0.1:8000/newchatroom/'
            headers = {'Authorization': 'JWT {}'.format(self.token)}
            data = {'name': chatroom_name}
            try:
                response = requests.post(url=url, headers=headers, data=data)
                if response.status_code == 201:
                    print("Chatroom Created")
                else:
                    print("Problem Creating Chatroom")
                print(response.json())
            except:
                print("Problem connecting to server")

    def delete_chatroom(self):
        if self.verify_token():
            chatroom_slug = str(input("Enter ChatRoom slug : "))
            url = 'http://127.0.0.1:8000/deletechatroom/{}/'.format(chatroom_slug)
            headers = {'Authorization': 'JWT {}'.format(self.token)}
            try:
                response = requests.delete(url=url, headers=headers)
                if response.status_code == 204:
                    print("Chatroom Deleted")
                else:
                    print("Problem Deleting Chatroom")
                    print(response.json())
            except:
                print("Problem connecting to server")

    def exit_chatroom(self):
        if self.verify_token():
            chatroom_slug = str(input("Enter ChatRoom slug : "))
            url = 'http://127.0.0.1:8000/chatroom/{}/exit/'.format(chatroom_slug)
            headers = {'Authorization': 'JWT {}'.format(self.token)}
            try:
                response = requests.delete(url=url, headers=headers)
                if response.status_code == 204:
                    print("Exited from Deleted")
                else:
                    print("Problem Exiting Chatroom")
                    print(response.json())
            except:
                print("Problem connecting to server")

    def rename_chatroom(self):
        if self.verify_token():
            chatroom_slug = str(input("Enter chatroom-slug : "))
            chatroom_name = str(input("Enter ChatRoom new name : "))
            url = 'http://127.0.0.1:8000/renamechatroom/{}/'.format(chatroom_slug)
            headers = {'Authorization': 'JWT {}'.format(self.token)}
            data = {'name': chatroom_name}
            try:
                response = requests.patch(url=url, headers=headers, data=data)
                if response.status_code == 200:
                    print("ChatRoom Renamed")
                else:
                    print("Problem Renaming Chatroom")
                print(response.json())
            except:
                print("Problem connecting to server")

    def get_room_messages(self):
        if self.verify_token():
            chatroom_slug = str(input("Enter chatroom-slug : "))
            url = 'http://127.0.0.1:8000/chatroom/{}/'.format(chatroom_slug)
            headers = {'Authorization': 'JWT {}'.format(self.token)}
            try:
                response = requests.get(url=url, headers=headers)
                if response.status_code == 200:
                    print("Messaged Retrieved")
                else:
                    print("Problem Viewing Messages")
                print(response.json())
            except:
                print("Problem connecting to server")

    def send_message(self):
        if self.verify_token():
            chatroom_slug = str(input("Enter Chatroom slug : "))
            message = str(input("Enter Message : "))
            url = 'http://127.0.0.1:8000/chatroom/{}/newmessage/'.format(chatroom_slug)
            headers = {'Authorization': 'JWT {}'.format(self.token)}
            data = {'message': message}
            try:
                response = requests.post(url=url, headers=headers, data=data)
                if response.status_code == 201:
                    print("Message sent")
                else:
                    print("Failed to send message")
                print(response.json())
            except:
                print("Problem connecting to server")

    def add_member(self):
        if self.verify_token():
            chatroom_slug = str(input("Enter Chatroom slug :"))
            username = str(input("Enter new member username : "))
            url = 'http://127.0.0.1:8000/chatroom/{}/newmember/'.format(chatroom_slug)
            data = {'username': username}
            headers = {'Authorization': 'JWT {}'.format(self.token)}
            try:
                response = requests.post(url=url, headers=headers, data=data)
                if response.status_code == 201:
                    print("New Member Added")
                else:
                    print("Problem adding new member")
                print(response.json())
            except:
                print("Problem connecting to server")

    def register(self):
        first_name = str(input("Enter First Name : "))
        last_name = str(input("Enter Last Name : "))
        email = str(input("Enter Email : "))
        username = str(input("Enter Username : "))
        password = str(input("Enter Password : "))
        url = 'http://127.0.0.1:8000/accounts/signup/'
        data = {'first_name': first_name, 'last_name': last_name, 'email': email, 'username': username,
                'password': password}
        try:
            response = requests.post(url=url, data=data)
            if response.status_code == 201:
                print("Account Created")
            else:
                print("Problem SigningUp")
            print(response.json())
        except:
            print("Problem connecting to server")

    def verify_token(self):
        if self.token is not None:
            url = 'http://127.0.0.1:8000/auth/verifytoken/'
            data = {'token': self.token}
            try:
                response = requests.post(url=url, data=data)
                if response.status_code == 200:
                    return True
                else:
                    print("Token Expired.. Trying to fetch new token")
                    self.token = None
                    self.login()
                    self.verify_token()
            except:
                print("Problem connecting to server")
        else:
            print("Need to login")
            return False

    def logout(self):
        self.username = None
        self.password = None
        self.token = None


def main():
    client = ChatRoomApiClient()
    client.start()


if __name__ == '__main__':
    main()
