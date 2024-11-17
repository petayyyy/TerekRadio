from configs import *
from sheetEditor import *
from aiogram import Bot
from aiogram import types
from buttons import HomeButton, EmptyBut, ClearBut, buttons_labels, buttons_comand, adminButInLine, servBut, servHBut, questionsBut, questionsAdminBut

class User:
    def __init__(self, userID: str, userName: str):
        # 0 - none, 1 - questions first, 2 - question second
        self.state = 0
        self.user_id = userID
        self.user_name = userName

        self.lastMessage = ""
        self.listMessage = []
    def UpdateState(self, newState):
        self.state = newState
        return self.state
    def ResetState(self):
        self.state = 0
    def UpdateMessage(self, newMessage):
        self.lastMessage = newMessage
        self.listMessage.append(newMessage)
    # 0 - pass, 7 - Rewies, 8 - Offer
    async def SetAction(self, state, messageFromU: types.Message, sheets: SheetEditor, botM: Bot, isReset: bool = False):
        if (state == 0):
            pass
        elif (state == 7):
            print("Rewies")
            sheets.SendReviews(self.user_id, self.user_name, self.lastMessage)
            await messageFromU.answer(
                "Ваш отзыв успешно создан",
                reply_markup=HomeButton.as_markup(resize_keyboard=True)
            )
        elif (state == 8):
            print("MakeOffer")
            await messageFromU.answer(
                "Ваше предложение успешно создано",
                reply_markup=HomeButton.as_markup(resize_keyboard=True)
            )
            sheets.SendOffer(self.user_id, self.user_name, self.lastMessage)
        if (isReset): self.ResetState()      
        

class UserList:
    def __init__(self, botM: Bot):
        self.listUser = []
        self.sh = SheetEditor()
        self.botMaster = botM
        self.adminsLastM = ""
        # 90 - wait message, 91 - get question, 92 - write answer, 93 - send answer, wait user ok, 94 - get update questions
        self.adminState = 90
        self.adminLastState = 0
        self.lastWorkingQuestionsId = -1
        # id user, [questions]  
        self.dictQuestions = {}
        self.lastUserWork = ""
    # Провека оставшихся senderov
    async def CheckMessage(self, messageU: types.Message, state: int):
        userID = messageU.from_user.id
        text = messageU.text
        if (self.CheckIsAdmin(message=messageU)):
            if (self.adminState == 92):
                await self.botMaster.send_message(self.lastWorkingQuestionsId,  text=text, reply_markup=questionsBut)
                self.adminState = 93
            elif (self.adminState == 93 and self):
                pass
            self.adminLastState = self.adminState     
            self.adminState = state
        else:
            userIdList = self.GetUser(userID=messageU.from_user.id, userName=messageU.from_user.full_name)
            self.listUser[userIdList].UpdateMessage(messageU.text)
            if (state == 1 and self.adminState == 90 and self.listUser[userIdList].state == 1):
                # Отправка первого вопроса
                self.dictQuestions = { userID : [text] }
                self.lastWorkingQuestionsId = userID
                await self.botMaster.send_message(chatId,  text=text, reply_markup= adminButInLine.as_markup())
                print("New Question")
                await messageU.answer( text="Ожидайте ответа тех. поддержки", 
                    reply_markup=EmptyBut.as_markup(resize_keyboard=True)
                )
                self.listUser[userIdList].UpdateState(2)

            elif (state == 1 and self.adminState != 90 and self.listUser[userIdList].state == 1):
                # Отправка первого вопроса в очередь
                self.dictQuestions.update({ userID : [text] })
                await self.botMaster.send_message(chatId,  text="Ещё один вопрос в очереди")
                print("New Question in list")
                await messageU.answer( text="Ожидайте ответа тех. поддержки", 
                    reply_markup=EmptyBut.as_markup(resize_keyboard=True)
                )
                self.listUser[userIdList].UpdateState(2)

            elif (state == 1 and self.listUser[userIdList].state == 2):
                # Отправка второго вопроса
                self.dictQuestions[self.lastWorkingQuestionsId] = self.dictQuestions[self.lastWorkingQuestionsId].append(text)
                print("Update Question")
                await self.botMaster.send_message(chatId,  text=text, reply_markup= questionsAdminBut.as_markup())
                await messageU.answer( text="Ожидайте ответа тех. поддержки", 
                    reply_markup=EmptyBut.as_markup(resize_keyboard=True)
                )
                self.listUser[userIdList].UpdateState(1)

            elif (state == 1 and self.listUser[userIdList].state == 3):
                # Отправка отзыва
                print("Rewies")
                self.listUser[userIdList].SetAction(7, messageU, self.sh, self.botMaster, True)
            elif (state == 1 and self.listUser[userIdList].state == 3):
                print("MakeOffer")
                self.listUser[userIdList].SetAction(8, messageU, self.sh, self.botMaster, True)
    # Проверка админовских senderov
    async def CheckAdmMessage(self, messageU: types.Message, state: int):
        if (self.CheckIsAdmin(message=messageU)):
            if (state == 92):
                await messageU.answer("Пишите ответ")
                await self.botMaster.edit_message_reply_markup(
                    chat_id=chatId,
                    message_id=messageU.message_id, 
                    reply_markup=None
                )  
            self.adminLastState = self.adminState     
            self.adminState = state 
            
    def CheckIsAdmin(self, message: types.Message):
        print("Chat id is " + str(message.chat.id))
        if (message.from_user.id in listAdmins):
            return True
        if (message.chat.id  == chatId):
            return True
        return False
    def GetUser(self, userID, userName):
        if (userID in listAdmins): return -2
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

