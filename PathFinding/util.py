import heapq
from typing import _T, List, Tuple


class PriorityQueue(object):
    def __init__(self):
        super(PriorityQueue, self).__init__()
        self.elements: List[Tuple[float, _T]] = []
    
    def empty(self) -> bool:
        return not self.elements

    def put(self, item: _T, priority: float):
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> _T:
        return heapq.heappop(self.elements)[1]

class Location(object):
    def __init__(self):
        super(Location, self).__init__()
        