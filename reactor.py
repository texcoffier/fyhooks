"""
The reactor framework.
"""

from typing import Dict, List, Tuple, Callable

EventType = str
EventHandler = Callable # pylint: disable=invalid-name
Priority = str

class Reactor:
    """Manage handlers"""
    M = None
    def __init__(self):
        self.handlers: Dict[EventType, List[Tuple[Priority, EventHandler]]] = {}
        self.sorted_handlers: Dict[EventType, List[EventHandler]] = {}

    def add(self, event_type: EventType, handler: EventHandler, priority: Priority):
        """Add an handler"""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        handlers = self.handlers[event_type]
        handlers.append((priority, len(handlers), handler))
        handlers.sort()
        self.sorted_handlers[event_type] = [handler[2] for handler in handlers]

    def __call__(self, *data):
        """Send event"""
        event = Event(data)
        for handler in self.sorted_handlers.get(data[0], []):
            result = handler(event)
            if result is not None:
                return result
        return None

    def handler(self, event_type: EventType, priority: Priority = 'MEDIUM'):
        """Add a hander decorator"""
        def handler(function):
            if event_type:
                self.add(event_type, function, priority)
            else:
                for event in self.handlers:
                    self.add(event, function, priority)
            return function
        return handler

    def __str__(self):
        """State"""
        text = []
        for key, handlers in self.handlers.items():
            text.append(key)
            for priority, index, fct in handlers:
                filename = fct.__code__.co_filename.split("/")[-1]
                fctname = fct.__code__.co_name
                text.append(f'    {priority:7}{index:3} {filename:25}{fctname}')
        return '\n'.join(text)

class Event: # pylint: disable=too-few-public-methods
    """Event"""
    def __init__(self, data):
        self.data = data
    def __str__(self):
        return f'{self.data} {self.__dict__}'

R = Reactor()
