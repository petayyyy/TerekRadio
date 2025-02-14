from configs import *
from sheetEditor import *
from aiogram import Bot
from aiogram import types
from buttons import HomeButton, EmptyBut, ClearBut, CancelBut, buttons_labels, buttons_comand, mapsGetB, adminButInLine, servBut, servHBut, questionsBut, questionsAdminBut, mapBut
from maps import CreateMapP, GetMapP

class User:
    def __init__(self, userID: str, userName: str):
        # 0 - none, 1 - questions first, 2 - question second, 3 - Rewies, 4 - Make offers, 5 - Start Serv, 6 - Serv 2, 7 - Map 1, 8 - Map by mes data
        self.state = 0
        self.user_id = userID
        self.user_name = userName

        self.lastMessage = ""
        self.lastMessageId = -1
        self.listMessage = []

        self.listmap = []
    def UpdateState(self, newState):
        self.state = newState
        return self.state
    def ResetState(self):
        self.state = 0
    def UpdateMessage(self, newMessage):
        self.lastMessage = newMessage
        self.listMessage.append(newMessage)
    def UpdateMessageId(self, newMessage):
        self.lastMessageId = newMessage.message_id
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

    def UpdateMap(self, map1, map2, map3):
        self.listmap = [map1, map2, map3]
class UserList:
    def __init__(self, botM: Bot):
        self.listUser = []
        self.sh = SheetEditor()
        # Init list Dillers
        self.sh.ReadDataDillers()
        self.botMaster = botM
        # self.adminsLastM = ""
        # 90 - wait message, 91 - get question, 92 - write answer, 93 - send answer, wait user ok, 94 - get update questions
        self.adminState = 90
        self.adminLastState = 0
        self.lastWorkingQuestionsId = -1
        # id user, [questions]  
        self.dictQuestions = {}
        # user_id, chat_id
        self.listmapUser = []
        # self.lastUserWork = ""
    """
        Провека оставшихся senderov

        :param messageU: Message from user
        :param state:  1 - all message, 2 - answerB2, 3 - Вопрос, 4 - Сервисный центр (Start), 
        5 - Сервисный центр (Все ещё остались вопросы), 6 - Сервисный центр (Помогло), 
        7 - Сервисный центр (Вопросов больше нет), 8 - Отзыв, 9 - Предложение
        10 - answerG, 11 - answerB1,
        12 - mapG2(map init), 13 - map 1, 14 - map 2, 15 - map 3б
        16 - Вопрос тех. поддержки,
        17 - map start init, 18 - mapG2(map by message), 19 - cancel
        :return: None
    """
    async def CheckMessage(self, messageU: types.Message, state: int):
        userID = messageU.from_user.id
        text = messageU.text
        if (self.CheckIsAdmin(message=messageU)):
            if (self.adminState == 92):
                msg = await self.botMaster.send_message(self.lastWorkingQuestionsId,  text=text, reply_markup=questionsBut)
                self.adminState = 93
                userIdList = self.GetUser(userID=self.lastWorkingQuestionsId, userName="")
                self.listUser[userIdList].UpdateMessageId(msg)
            self.adminLastState = self.adminState     
            self.adminState = state
        else:
            userIdList = self.GetUser(userID=messageU.from_user.id, userName=messageU.from_user.full_name)
            self.listUser[userIdList].UpdateMessage(messageU.text)
            if (state == 1):
                if (self.adminState == 90 and self.listUser[userIdList].state == 1):
                    # Отправка первого вопроса
                    self.dictQuestions = { userID : [text] }
                    self.lastWorkingQuestionsId = userID
                    await self.botMaster.send_message(chatId,  text=text, reply_markup= adminButInLine.as_markup())
                    print("New Question")
                    await messageU.answer( text="Ожидайте ответа", 
                        reply_markup=EmptyBut.as_markup(resize_keyboard=True)
                    )
                    self.listUser[userIdList].UpdateState(2)
                    self.adminState = 91
                elif (self.adminState != 90 and self.listUser[userIdList].state == 1):
                    # Отправка первого вопроса в очередь
                    self.dictQuestions.update({ userID : [text] })
                    print(self.dictQuestions)
                    await self.botMaster.send_message(chatId,  text="Ещё один вопрос в очереди")
                    print("New Question in list")
                    await messageU.answer( text="Ожидайте ответа", 
                        reply_markup=EmptyBut.as_markup(resize_keyboard=True)
                    )
                    self.listUser[userIdList].UpdateState(2)
                elif (self.listUser[userIdList].state == 2):
                    # Отправка второго вопроса
                    self.dictQuestions[self.lastWorkingQuestionsId] = self.dictQuestions[self.lastWorkingQuestionsId].append(text)
                    print("Update Question")
                    await self.botMaster.send_message(chatId,  text=text, reply_markup= questionsAdminBut.as_markup())
                    await messageU.answer( text="Ожидайте ответа", 
                        reply_markup=EmptyBut.as_markup(resize_keyboard=True)
                    )
                    self.listUser[userIdList].UpdateState(1)
                    self.adminState = 91

                elif (self.listUser[userIdList].state == 3):
                    # Отправка отзыва
                    print("Rewies")
                    await self.listUser[userIdList].SetAction(7, messageU, self.sh, self.botMaster, True)
                elif (self.listUser[userIdList].state == 4):
                    print("MakeOffer")
                    await self.listUser[userIdList].SetAction(8, messageU, self.sh, self.botMaster, True)
                elif (self.listUser[userIdList].state == 7):
                    print("Check map")
                    lat, lon, addStr = GetMapP(messageU.text)
                    if (lat != 0 and lon != 0):
                        min1, min2, min3 = self.sh.CheckDillers(lat=lat, lon=lon)
                        self.listUser[userIdList].UpdateMap(min1, min2, min3)
                        mesOut = "Мы нашли самых близких к Вам дилеров.\nВыберите наиболее подходящий для Вас вариант:\n\n"
                        mesOut += "1⃣ " + self.GetStrOut(min1[6:8]) + "\n" + "2⃣ " +  self.GetStrOut(min2[6:8]) + "\n" + "3⃣ " + self.GetStrOut(min3[6:8]) + "\n"
                        await messageU.answer( text= mesOut, 
                            reply_markup=mapBut
                        )
                        self.listmapUser.append([self.listUser[userIdList].user_id, messageU.chat.id])
                    else:
                        await messageU.answer( text="Вы допустили ошибку в написании адреса.\nПовторно напишите Ваш аддрес для подбора \nдля Вас наиближайшего диллера в формате \nГород улица, пример \nг. Москва ул. Пионеров", 
                            reply_markup=EmptyBut.as_markup(resize_keyboard=True)
                        )
            elif (state == 2):
                await messageU.answer(
                    "Дополните вопрос и оправте его в одном сообщении",
                    reply_markup=ClearBut,
                    parse_mode="MarkdownV2"
                )
                self.listUser[userIdList].UpdateState(2)
            elif (state == 3):
                await messageU.answer(
                    "Напишите Ваш вопрос",
                    reply_markup=CancelBut.as_markup(resize_keyboard=True)
                )
                self.listUser[userIdList].UpdateState(1)
            elif (state == 4):
                await messageU.answer(
                    "Ссылка на ютуб канал Терек-Радио с инструкциями: https://youtube.com/@terek-radio?si=FWB7JgVCcBpp4Ws- . Остались еще вопросы?",
                    reply_markup=servBut.as_markup(resize_keyboard=True)
                )
                self.listUser[userIdList].UpdateState(5)
            elif (state == 5):
                await messageU.answer(
                    "Контакт СЦ: моб: 8 (988) 243-16-97",
                    reply_markup=servHBut.as_markup(resize_keyboard=True),
                )
                self.listUser[userIdList].UpdateState(6)
            elif (state == 6):
                await messageU.answer(
                        "Отлично!",
                        reply_markup=HomeButton.as_markup(resize_keyboard=True)
                )
                self.listUser[userIdList].ResetState()
            elif (state == 7):
                await messageU.answer(
                    "Попробуйте задать вопрос, наша тех поддержка найдет ответ на любой интересующий Вас вопрос",
                    reply_markup=HomeButton.as_markup(resize_keyboard=True)
                )
                self.listUser[userIdList].ResetState()
            elif (state == 8):
                await messageU.answer(
                    "Напишите и отправьте отзыв в одном сообщении",
                    reply_markup=ClearBut,
                    parse_mode="MarkdownV2"
                )
                self.listUser[userIdList].UpdateState(3)
            elif (state == 9):
                await messageU.answer(
                    "Напишите и отправьте предложение в одном сообщении",
                    reply_markup=ClearBut,
                    parse_mode="MarkdownV2"
                )
                self.listUser[userIdList].UpdateState(4)
            elif (state == 10):
                await self.botMaster.send_message(chatId,  text="Ответ устроил пользователя")
                await messageU.answer(
                    "Были рады ответить на Ваш вопрос, пишите ещё!",
                    reply_markup=HomeButton.as_markup(resize_keyboard=True),
                )
                self.listUser[userIdList].ResetState()

                if self.lastWorkingQuestionsId in self.dictQuestions: del self.dictQuestions[self.lastWorkingQuestionsId]
                self.lastSendMesId = -1
                self.lastWorkingQuestionsId = -1
                self.adminState = 90
                if (len(self.dictQuestions) != 0):
                    # Выполняем следующий вопрос по ожиданию
                    for key, values in self.dictQuestions.items():
                        self.lastWorkingQuestionsId = key
                        self.adminState = 91
                        await self.botMaster.send_message(chatId,  text=values[0], reply_markup= adminButInLine.as_markup())
                        print("New Question")
                        break
            elif (state == 11):
                await messageU.answer( text="Ожидайте ответа тех. поддержки", 
                    reply_markup=EmptyBut.as_markup(resize_keyboard=True)
                )
                await self.botMaster.send_message(chatId,  text="Ответ не устроил пользователя, разверните его", reply_markup= adminButInLine.as_markup())
                self.adminState = 91
                self.listUser[userIdList].UpdateState(2)
            elif (state == 12):
                await messageU.answer(
                    "Напишите свой адрес и мы подберем\nближайшего к Вам дилера\.\nФормат: Город и улица\nПример: г\. Москва ул\. Пионеров",
                    reply_markup=ClearBut,
                    parse_mode="MarkdownV2"
                )
                self.listUser[userIdList].UpdateState(7)
            elif (state == 13):
                idCurrentU = -1
                for ii in range(len(self.listmapUser)):
                    if (self.listmapUser[ii][1] == messageU.chat.id):
                        idCurrentU = ii
                        break
                if (idCurrentU != -1):
                    uuuId = self.GetUserById(self.listmapUser[idCurrentU][0])
                    await messageU.answer(
                        self.GetStrOut(self.listUser[uuuId].listmap[0][:8], "\n", isOut = True),
                        reply_markup=HomeButton.as_markup(resize_keyboard=True)
                    )
                    self.listUser[uuuId].ResetState()
                    del self.listmapUser[idCurrentU]
            elif (state == 14):
                idCurrentU = -1
                for ii in range(len(self.listmapUser)):
                    if (self.listmapUser[ii][1] == messageU.chat.id):
                        idCurrentU = ii
                        break
                if (idCurrentU != -1):
                    uuuId = self.GetUserById(self.listmapUser[idCurrentU][0])
                    await messageU.answer(
                        self.GetStrOut(self.listUser[uuuId].listmap[1][:8], "\n", isOut = True),
                        reply_markup=HomeButton.as_markup(resize_keyboard=True)
                    )
                    self.listUser[uuuId].ResetState()
                    del self.listmapUser[idCurrentU]
            elif (state == 15):
                idCurrentU = -1
                for ii in range(len(self.listmapUser)):
                    if (self.listmapUser[ii][1] == messageU.chat.id):
                        idCurrentU = ii
                        break
                if (idCurrentU != -1):
                    uuuId = self.GetUserById(self.listmapUser[idCurrentU][0])
                    await messageU.answer(
                        self.GetStrOut(self.listUser[uuuId].listmap[2][:8], "\n", isOut = True),
                        reply_markup=HomeButton.as_markup(resize_keyboard=True)
                    )
                    self.listUser[uuuId].ResetState()
                    del self.listmapUser[idCurrentU]
            elif (state == 15):
                await messageU.answer(
                    "Напишите Ваш вопрос",
                    reply_markup=ClearBut,
                    parse_mode="MarkdownV2"
                )
                self.listUser[userIdList].UpdateState(1)
            elif (state == 17):
                await messageU.answer(
                    "Выберите метод нахождения ближайшей точки продажи,\nесли Вас не устраивает не один из методов отправте точку на карте через Геопозицию",
                    reply_markup=mapsGetB.as_markup(resize_keyboard=True,  one_time_keyboard=True)
                )
            elif (state == 18):
                await messageU.answer(
                    "Ваша локация обрабатывается",
                    reply_markup=ClearBut,
                    parse_mode="MarkdownV2"
                )
                print("Get map by mess")
                location = messageU.location
                lat = location.latitude
                lon = location.longitude
                print(location)
                if (lat != 0 and lon != 0):
                    min1, min2, min3 = self.sh.CheckDillers(lat=lat, lon=lon)
                    self.listUser[userIdList].UpdateMap(min1, min2, min3)
                    mesOut = "1 => " + self.GetStrOut(min1[6:8]) + "\n" + "2 => " +  self.GetStrOut(min2[6:8]) + "\n" + "3 => " + self.GetStrOut(min3[6:8]) + "\n"
                    await messageU.answer( text= mesOut, 
                        reply_markup=mapBut
                    )
                    self.listmapUser.append([self.listUser[userIdList].user_id, messageU.chat.id])
                else:
                    await messageU.answer( text="Ваш адрес не передается попробуйте ввести в ручную или попробовать заново", 
                        reply_markup=mapsGetB.as_markup(resize_keyboard=True)
                    )
            elif (state == 19):
                await messageU.answer(
                    text="Вы не задали вопрос, но мы с радостью на него ответим!",
                    reply_markup=HomeButton.as_markup(resize_keyboard=True)
                )
                self.listUser[userIdList].ResetState()
    def GetStrOut(self, array, step:str = " ", isOut = False):
        if (not isOut): outStr = ""
        else: outStr = "Контактные данные дилера:\n"
        for i in array:
            if (str(i) != "" and str(i) != "-"): outStr += str(i) + step
        return outStr   
    def GetStrMapOut(self, array):
        outStr = ""
        outStr += str(array[0]) + "\n"
        outStr += "\n"
        if (str(array[2]) != "-"): outStr += "сайт: " + str(array[2]) + "\n"
        if (str(array[3]) != "-"): outStr += "email: " + str(array[3]) + "\n"
        if (str(array[4]) != "-"): outStr += "осн.тел: " + str(array[4]) + "\n"
        if (str(array[5]) != "-"): outStr += "доп.тел: " + str(array[5]) + "\n"
        outStr += "адрес: " + str(array[6]) + " " + str(array[7]) + "\n"
        return outStr   
    # Проверка админовских senderov
    # 92 - answerM, 93 - updateDillers, 99 - clear last list question
    async def CheckAdmMessage(self, messageU: types.Message, state: int):
        if (self.CheckIsAdmin(message=messageU)):
            if (state == 92):
                await messageU.answer("Пишите ответ")
                await self.botMaster.edit_message_reply_markup(
                    chat_id=chatId,
                    message_id=messageU.message_id, 
                    reply_markup=None
                )  
            elif(state == 93):
                self.sh.ReadDataDillers()
            elif(state == 99):
                userIdList = self.GetUser(userID=self.lastWorkingQuestionsId, userName="")
                await self.botMaster.send_message(chatId,  text="Ответ сброшен пользователя")
                print("lastMessageId :", self.listUser[userIdList].lastMessageId)
                print("lastWorkingQuestionsId :", self.lastWorkingQuestionsId)

                await self.botMaster.edit_message_reply_markup(
                    chat_id=self.lastWorkingQuestionsId,
                    message_id=self.listUser[userIdList].lastMessageId, 
                    reply_markup=None,
                )
                await self.botMaster.send_message(
                    text="Время ожидания вашего ответа закончилось. Диалог автоматически завершился. Если у Вас ещё остались вопросы, задавайте, мы с радостью на них ответим!",
                    chat_id=self.lastWorkingQuestionsId,
                    reply_markup=HomeButton.as_markup(resize_keyboard=True)
                )
                self.listUser[userIdList].ResetState()
                if self.lastWorkingQuestionsId in self.dictQuestions: del self.dictQuestions[self.lastWorkingQuestionsId]
                self.lastSendMesId = -1
                self.lastWorkingQuestionsId = -1
                state = 90
                print(self.dictQuestions)
                if (len(self.dictQuestions) != 0):
                    # Выполняем следующий вопрос по ожиданию
                    for key, values in self.dictQuestions.items():
                        self.lastWorkingQuestionsId = key
                        state = 91
                        await self.botMaster.send_message(chatId,  text=values[0], reply_markup= adminButInLine.as_markup())
                        print("New Question")
                        break
            self.adminLastState = self.adminState     
            self.adminState = state           
    def CheckIsAdmin(self, message: types.Message):
        if (message.from_user.id in listAdmins):
            print("is admin")
            return True
        if (message.chat.id  == chatId):
            print("is admin")
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
    def GetUserById(self, userID):
        if (userID in listAdmins): return -2
        useridInListSel = -1
        for i in range(len(self.listUser)):
            if (self.listUser[i].user_id == userID):
                useridInListSel = i
                break
        if (useridInListSel != -1):
           return useridInListSel
    def AddUser(self, userId, userName):
        self.listUser.append(User(userId, userName))
    def PrintData(self):
        outStr = ""
        outStr += "Admin data => state:{0}, work question:{1}, dict:[".format(self.adminState, self.lastWorkingQuestionsId)
        for key, values in self.dictQuestions.items():
            outStr +="user id: {0}, user text array {1}".format(key, values)
        outStr += "]\n"
        outStr += "////////////////////////////////////////////\n"
        for i in self.listUser:
            outStr += "User id: {0}, name: {1}, last message '{2}', state {3}\n".format(i.user_id, i.user_name, i.lastMessage, i.state)
        outStr = outStr.replace("-", "\-")
        outStr = outStr.replace(">", "\>")
        outStr = outStr.replace("=", "\=")
        outStr = outStr.replace("[", "\[")
        outStr = outStr.replace("]", "\]")
        return outStr
