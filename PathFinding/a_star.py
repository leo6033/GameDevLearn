from typing import Dict, Optional
import PathFinding.util as util 


def heuristic(a: util.Location, b: util.Location) -> float:
    return 0


def a_star_search(graph, start: util.Location, goal: util.Location):
    frontier = util.PriorityQueue()
    frontier.put(start, 0)
    come_from: Dict[util.Location, Optional[util.Location]] = {}
    costs: Dict[util.Location, float] = {}
    
    come_from[start] = None
    costs[start] = 0

    while not frontier.empty():
        current: util.Location = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            cost = costs[current] + graph.cost(current, next)
            if next not in costs or cost < costs[next]:
                costs[next] = cost
                priority = cost + heuristic(next, goal)
                frontier.put(next, priority)
                come_from[next] = current
    return come_from, costs
