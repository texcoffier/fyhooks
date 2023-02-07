"""
The reactor framework.
"""

from typing import Dict, List, Tuple, Callable, Any

EventType = str
EventHandler = Callable[[Tuple], Any] # pylint: disable=invalid-name
Priority = str

class Reactor:
    """Manage handlers"""
    M:Any = None
    def __init__(self):
        self.handlers: Dict[EventType, List[Tuple[Priority, int, EventHandler]]] = {}
        self.sorted_handlers: Dict[EventType, List[EventHandler]] = {}

    def add(self, event_type: EventType, handler: EventHandler, priority: Priority) -> None:
        """Add an handler"""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        handlers = self.handlers[event_type]
        handlers.append((priority, len(handlers), handler))
        handlers.sort()
        self.sorted_handlers[event_type] = [handler[2] for handler in handlers]

    def __call__(self, *args) -> Any:
        """Send event"""
        for handler in self.sorted_handlers.get(args[0], ()):
            result = handler(args)
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
                text.append(f'    {priority:7}{index:3} {filename:25}{fctname}')
        return '\n'.join(text)

R = Reactor()
