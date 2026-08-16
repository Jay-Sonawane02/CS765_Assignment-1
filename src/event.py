"""
Event queue and event types for discrete-event simulation
"""
import heapq
from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class Event:
    timestamp: float
    event_type: str
    data: Any=field(compare=False)

class EventQueue:
    def __init__(self):
        self._queue = []
    def push(self, event: Event):
        heapq.heappush(self._queue, event)
    def pop(self) -> Event:
        return heapq.heappop(self._queue)
    def is_empty(self) -> bool:
        return len(self._queue) == 0
