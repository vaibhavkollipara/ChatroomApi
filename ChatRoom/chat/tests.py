from django.test import TestCase, SimpleTestCase, TransactionTestCase, Client
from .models import ChatRoom, ChatRoomMembership
from django.contrib.auth.models import User


class ChatroomUnitTests(SimpleTestCase):

    def setUp(self):
        self.chatroom = ChatRoom(name="testroom", slug="testroom")

    def test_chatroom_name(self):
        self.assertEqual(self.chatroom.name, 'testroom')


class ChatroomTestCase(TransactionTestCase, Client):

    def setUp(self):
        user1 = User(username="testuser1")
        user1.set_password('password')
        user1.save()
        user2 = User(username="testuser2")
        user2.set_password('password')
        user2.save()
        user3 = User(username="testuser3")
        user3.set_password('password')
        user3.save()
        chatroom1 = ChatRoom(name="testroom1", admin=user1)
        chatroom1.save()
        chatroom2 = ChatRoom(name="testroom2", admin=user2)
        chatroom2.save()
        ChatRoomMembership(user=user3, chat_room=chatroom2).save()
        chatroom3 = ChatRoom(name="testroom3", admin=user3)
        chatroom3.save()
        ChatRoomMembership(user=user1, chat_room=chatroom3).save()
        ChatRoomMembership(user=user2, chat_room=chatroom3).save()
        self.chatroom1 = chatroom1
        self.chatroom2 = chatroom2
        self.chatroom3 = chatroom3

    def auth_fail_test(self):
        """
        Testcase to authenticate with invalid credentials
        """
        url = '/auth/obtaintoken/'
        data = {'username': 'testuser3', 'password': 'password3'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    def auth_test(self):
        """
        Testcase to authenticate with valid credentials
        """
        url = '/auth/obtaintoken/'
        data = {'username': 'testuser1', 'password': 'password'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.client.defaults['HTTP_AUTHORIZATION'] = 'JWT {}'.format(response.json()['token'])

    def test_chatroom_members_count(self):
        """
        Testcase to verify chatroom members count
        """
        self.assertEqual(self.chatroom1.members.count(), 1)
        self.assertEqual(self.chatroom2.members.count(), 2)
        self.assertEqual(self.chatroom3.members.count(), 3)

    def user_chatrooms_test(self):
        """
        Testcase to verify user's chatrooms list
        """
        url = '/mychatrooms/'
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def new_chatroom_test(self):
        """
        Testcase to create new chatroom
        """
        url = '/newchatroom/'
        data = {'name': 'extraroom'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        url = '/mychatrooms/'
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def add_member_test(self):
        """
        Testcase to add member to chatroom
        """
        url = '/chatroom/extraroom/newmember/'
        data = {'username': 'testuser3'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        url = '/chatroom/extraroom/memberslist/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def send_message_fail_test(self):
        """
        Testcase to send message to a chatroom in which user is not a member
        """
        url = '/chatroom/testroom2/newmessage/'
        data = {'message': 'hello from user1'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)

    def send_message_test(self):
        """
        Testcase to send message to a chatroom in which user is a member
        """
        url = '/chatroom/extraroom/newmessage/'
        data = {'message': 'hello from user1'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def delete_chatroom_test(self):
        """
        Testcase to delete chatroom
        """
        url = '/deletechatroom/extraroom/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        url = '/mychatrooms/'
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def invalid_chatroom_test(self):
        """
        Testcase to access invalid chatroom
        """
        url = '/deletechatroom/extraroom/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 500)

    def test_flow(self):
        self.auth_fail_test()
        self.auth_test()
        self.user_chatrooms_test()
        self.new_chatroom_test()
        self.add_member_test()
        self.send_message_fail_test()
        self.send_message_test()
        self.delete_chatroom_test()
        self.invalid_chatroom_test()
