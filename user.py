from  configs import *
from sheetEditor import *

class User:
    def __init__(self, userID, userName):
        # 0 - none, 1 - rewies, 2 - 
        self.state = 0
        self.user_id = userID
        self.user_name = userName

        self.lastMessage = ""
        self.listMessage = []
    def UpdateState(self, newState):
        self.state = newState
        return self.state
    def UpdateMessage(self, newMessage):
        self.lastMessage = newMessage
        self.listMessage.append(newMessage)
    def SetAction(self, state, sheets):
        if (state == 0):
            pass
        if (state == 1):
            print("Rewies")
            sheets.SendReviews(self.user_id, self.user_name, self.lastMessage)
        

class UserList:
    def __init__(self):
        self.listUser = []
        self.sh = SheetEditor()
    def CheckMessage(self, userID, userName, message, state):
        userIdList = self.GetUser(userID=userID, userName=userName)
        stateDo = self.listUser[userIdList].UpdateState(state)
        self.listUser[userIdList].UpdateMessage(message)
        return stateDo
    def GetUser(self, userID, userName):
        useridInListSel = -1
        for i in range(len(self.listUser)):
            if (self.listUser[i].user_id == userID):
                useridInListSel = i
                break
        if (useridInListSel != -1):
           return useridInListSel
        else:
            self.AddUser(userID, userName)
            return len(self.listUser) - 1
    def AddUser(self, userId, userName):
        self.listUser.append(User(userId, userName))

