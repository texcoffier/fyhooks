from typing import *

EventType = str
Handler = Callable
Priority = str

class Reactor:
    def __init__(self):
        self.handlers:Dict[EventType,List[Tuple[Priority, Handler]]] = {}

    def add(self, event_type:EventType, handler:Handler, priority:Priority):
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append((priority, handler))
        self.handlers[event_type].sort()

    def __call__(self, *data):
        event = Event(data)
        for _, handler in self.handlers.get(data[0], []):
            if handler(event):
                break

class Event:
    def __init__(self, data):
        self.data = data
    def __str__(self):
        return f'{self.data} {self.__dict__}'

