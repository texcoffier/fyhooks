"""
Manage threading
"""

import collections
import threading
from typing import Dict, List, Callable
from reactor import R

R.description('start_thread', 'Arguments: state.function\nThe function to start.')

running:Dict[str,List[Callable]] = collections.defaultdict(list)

@R.handler('start_thread')
def start(state):
    class Thread(threading.Thread):
        """Start a thread"""
        def run(self):
            """Run the function in the thread"""
            thread_list = running[state.function.__module__]
            thread_list.append(state.function)
            try:
                state.function(thread_list)
            finally:
                if state.function in thread_list:
                    thread_list.remove(state.function)
    Thread().start()

@R.handler('BEFORE_RELOAD')
@R.handler('BEFORE_DISABLE')
def stop_thread(state):
    """Stop the threads."""
    if state.functionality in running:
        running[state.functionality].clear()
