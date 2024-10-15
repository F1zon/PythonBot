from typing import Any


class User:
    chatId = 0
    events = []

    def __init__(self, UserId) -> None:
        User.chatId = UserId
    
    def setDate(self, dates, desc):
        User.events.append(Events(dates, desc))
    
    def setDesc(self, dateEvent, descEvent):
        if User.isEmptyDate(dateEvent):
            return []

        for i in User.events:
            if i.dates == dateEvent:
                i.desc.append(descEvent)

    def getDescDate(self, dateEvent, descEvent):
        if User.isEmptyDate(dateEvent):
            return []

        for i in User.events:
            if i.dates == dateEvent:
                return i.desc

    def isEmptyDate(self, dateEvent):
        for i in User.events:
            if i.getDate() == dateEvent:
                return False
        return True


class Events:
    dates = ""
    desc = []
    
    def __init__(self, d, e) -> None:
        Events.dates = d
        Events.desc.append(e)
    
    def setDesc(self, e) -> None:
        Events.desc.append(e)
    