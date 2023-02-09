"""
The reactor framework.
"""

from typing import Dict, List, Tuple, Callable, Any

class State: # pylint: disable=too-few-public-methods
    """The state given to handlers"""
    def __init__(self, event, kargs):
        self.__dict__.update(kargs)
        self.event = event
    def __str__(self):
        clean = [self.event]
        for key, item in sorted(self.__dict__.items()):
            if key == 'event':
                continue
            if not isinstance(item, (str, int)):
                item = '<' + item.__class__.__name__ + '>'
            clean.append(f'{key}={item}')
        return ' '.join(clean)

EventType = str
EventHandler = Callable[[State], Any]
Priority = str

class Reactor:
    """Manage handlers"""
    M:Any = None
    priority = 0
    def __init__(self):
        self.handlers: Dict[EventType, List[Tuple[Priority, int, EventHandler]]] = {}
        self.sorted_handlers: Dict[EventType, List[EventHandler]] = {}

    def add(self, event_type: EventType, handler: EventHandler, priority: Priority) -> None:
        """Add an handler"""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        handlers = self.handlers[event_type]
        # Reactor.priority is here only to never compare 2 handler (sorting will fail)
        handlers.append((priority, Reactor.priority, handler))
        handlers.sort()
        Reactor.priority += 1
        self.sorted_handlers[event_type] = [handler[2] for handler in handlers]

    def __call__(self, event, **kargs) -> Any:
        """Send event"""
        state = State(event, kargs)
        for handler in self.sorted_handlers.get(event, ()):
            result = handler(state)
            if result is not None:
                return result
        return None

    def handler(self, event_type: EventType, priority: Priority = 'MEDIUM'
               ) -> Callable[[EventHandler], EventHandler]:
        """Add a hander decorator.
        Event type '' match all existing events.
        """
        def handler(function:EventHandler):
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
                text.append(f'    {priority+"."+str(index):<10} {filename:25}{fctname}')
        return '\n'.join(text)

R = Reactor()
