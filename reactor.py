"""
The reactor framework.
"""

import collections
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
                item = item.__class__.__name__
            clean.append(f'{key}={item}')
        return ' '.join(clean)

EventType = str
EventHandler = Callable[[State], Any]
Priority = str

class Reactor:
    """Manage handlers"""
    M:Any = None
    priority = 0
    generic_handler:List[Tuple[EventHandler, Priority]] = []
    def __init__(self):
        self.handlers: Dict[EventType, List[Tuple[Priority, int, EventHandler]]] = {}
        self.sorted_handlers: Dict[EventType, List[EventHandler]] = {}
        self.handler_descriptions: Dict[EventType, str] = collections.defaultdict(str)

    def add(self, event_type: EventType, handler: EventHandler, priority: Priority) -> None:
        """Add an handler"""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        handlers = self.handlers[event_type]
        # Reactor.priority is here only to never compare 2 handler (sorting will fail)
        handlers.append((priority, Reactor.priority, handler))
        Reactor.priority += 1            

        # Apply previously defined generic handlers
        for handler, priority in self.generic_handler:
            handlers.append((priority, Reactor.priority, handler))
            Reactor.priority += 1            

        handlers.sort()
        self.sorted_handlers[event_type] = [handler[2] for handler in handlers]

    def update_handlers(self):
        """Update all handlers"""
        for event_type, handlers in self.handlers.items():
            handlers.sort()
            self.sorted_handlers[event_type] = [handler[2] for handler in handlers]

    def __call__(self, event_type: EventType, **kargs) -> Any:
        """Send event"""
        state = State(event_type, kargs)
        for handler in self.sorted_handlers.get(event_type, ()):
            result = handler(state)
            if result is not None:
                return result
        return None

    def description(self, event_type: EventType, description:str) -> None:
        """Add a handler description"""
        self.handler_descriptions[event_type] += description

    def handler(self, event_type: EventType, priority: Priority = 'MEDIUM',
               ) -> Callable[[EventHandler], EventHandler]:
        """Add a handler decorator.
        Event type '' match all existing events.
        """
        def handler(function:EventHandler) -> EventHandler:
            if event_type:
                self.add(event_type, function, priority)
            else:
                self.generic_handler.append((function, priority))
                for event in self.handlers:
                    self.add(event, function, priority)
            return function
        return handler

    def __str__(self):
        """State"""
        text = []
        for key, handlers in sorted(self.handlers.items()):
            text.append('='*79)
            label = key + ' # '
            indent = ' ' * (len(label) - 2) + '# '
            description = self.handler_descriptions.get(key, '').split('\n')
            text.append(label + description[0])
            for line in description[1:]:
                text.append(indent + line.strip())
            text.append('  PRIORITY   FILE                     FUNCTION')
            for priority, index, fct in handlers:
                filename = fct.__code__.co_filename.split("/")[-1]
                fctname = fct.__code__.co_name
                text.append(f'  {priority+"."+str(index):<10} {filename:25}{fctname}')
        return '\n'.join(text)

R = Reactor()
