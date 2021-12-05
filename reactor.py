from typing import *

EventType = str
Handler = Callable
Priority = str

class Reactor:
    def __init__(self):
        self.handlers:Dict[EventType,List[Tuple[Priority, Handler]]] = {}
        self.sorted_handlers:Dict[EventType, List[Handler]] = {}

    def add(self, event_type:EventType, handler:Handler, priority:Priority):
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        handlers = self.handlers[event_type]
        handlers.append((priority, len(handlers), handler))
        handlers.sort()
        self.sorted_handlers[event_type] = [handler[2] for handler in handlers]

    def __call__(self, *data):
        event = Event(data)
        for handler in self.sorted_handlers.get(data[0], []):
            result = handler(event)
            if result:
                return result

    def handler(self, event_type:EventType, priority:Priority = 'MMMMM'):
        def handler(function):
            if event_type:
                self.add(event_type, function, priority)
            else:
                for event in self.handlers:
                    self.add(event, function, priority)
            return function
        return handler

class Event:
    def __init__(self, data):
        self.data = data
    def __str__(self):
        return f'{self.data} {self.__dict__}'

R = Reactor()
