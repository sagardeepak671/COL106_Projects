from flight import Flight
import Que as q
import heap as h 
class Node:
    def __init__(self, flight, parent=None, fare=float('inf'), distance = -1):
        self.flight = flight
        self.parent = parent       #came by this flight_no
        self.fare   = fare
        self.distance = distance   #bfs distance from start city
    
def comp(node1,node2):
    return node1.fare < node2.fare

def backtrack_path(nodes_list, start_city, last_node):
    path = []
    while last_node is not None:
        path.append(last_node.flight)
        if last_node.flight.start_city == start_city:
            break
        last_node = nodes_list[last_node.parent]
    return path[::-1]

class Planner:
    def __init__(self, flights): 
        self.no_of_flights = len(flights)

        self.max_city = 0
        self.max_city = max(max(flight.start_city, flight.end_city) for flight in flights)

        self.adj = [[] for _ in range(self.max_city + 1)] 
        for flight in flights:
            self.adj[flight.start_city].append(flight)
            
    def least_flights_ealiest_route(self, start_city, end_city, t1, t2):
        if start_city == end_city or t1 > t2: return []
        
        queue = q.Queue()
        nodes_list = [None]*(self.no_of_flights+1)
        path = []
        MinTime = t2
        MinDis = None
        for flight in self.adj[start_city]:
            if flight.departure_time >= t1 and flight.arrival_time <= t2:
                temp = nodes_list[flight.flight_no]
                if temp is None:
                    nodes_list[flight.flight_no] = Node(flight, distance=1)
                    temp = nodes_list[flight.flight_no]
                temp.parent = flight.flight_no
                queue.push(temp)
                if flight.end_city == end_city and flight.arrival_time <= MinTime:
                    MinTime = flight.arrival_time
                    MinDis = 1
                    path = [flight]
        if MinDis is not None:
            return path
        last_node = None
        while not queue.is_empty():
            node = queue.popp()
            last_city = node.flight.end_city
            last_time = node.flight.arrival_time
            last_dis = node.distance
            if last_city == end_city and node.distance == MinDis and last_time <= MinTime:
                MinTime = last_time
                MinDis = last_dis
                last_node = node
                continue
            if MinDis is not None and node.distance == MinDis:
                continue
            for flight in self.adj[last_city]:
                if flight.departure_time >= last_time +20 and flight.arrival_time <= t2:
                    temp = nodes_list[flight.flight_no]
                    if temp is None:
                        nodes_list[flight.flight_no] = Node(flight)
                        temp = nodes_list[flight.flight_no]
                    if temp.distance == -1:
                        temp.distance = last_dis + 1
                        temp.parent = node.flight.flight_no
                        queue.push(temp)
                        if flight.end_city == end_city:
                            if MinDis is None:
                                MinDis = temp.distance
        return backtrack_path(nodes_list, start_city, last_node) 
    
    def cheapest_route(self, start_city, end_city, t1, t2):
        if start_city==end_city or t1>t2: return [] 

        pq = h.Heap(comp)
        nodes_list = [None]*(self.no_of_flights+1)
        MinFare = float('inf')   
        last_node = None
        for flight in self.adj[start_city]:
            if flight.departure_time>=t1 and flight.arrival_time<=t2:
                temp = nodes_list[flight.flight_no]
                if temp is None:
                    nodes_list[flight.flight_no] = Node(flight)
                    temp = nodes_list[flight.flight_no]
                temp.parent = flight.flight_no
                temp.fare = flight.fare
                pq.insert(temp)
                if flight.end_city == end_city and flight.fare <= MinFare:
                    MinFare = flight.fare
                    last_node = temp

        while not pq.is_heap_empty():
            node = pq.extract()
            last_city = node.flight.end_city
            last_time = node.flight.arrival_time
            last_fare = node.fare

            if last_city == end_city and node.fare <= MinFare:        
                last_node = node
                MinFare = node.fare
                break

            for flight in self.adj[last_city]:
                if flight.departure_time >= last_time+20 and flight.arrival_time <= t2 :
                    new_fare = last_fare + flight.fare 
                    new_node = nodes_list[flight.flight_no]
                    if new_node is None:
                        nodes_list[flight.flight_no] = Node(flight)
                        new_node = nodes_list[flight.flight_no]
                    if new_fare <= new_node.fare:
                        new_node.fare = new_fare
                        new_node.parent = node.flight.flight_no
                        pq.insert(new_node)
        return backtrack_path(nodes_list, start_city, last_node)
 
    def least_flights_cheapest_route(self, start_city, end_city, t1, t2): 
        if start_city==end_city or t1>t2: return []

        pq = h.Heap(comp)
        nodes_list = [None]*(self.no_of_flights+1)
        path = []
        mini=(float('inf'),float('inf')) 
        last_node = None
        for flight in self.adj[start_city]:
            if flight.departure_time>=t1 and flight.arrival_time<=t2:
                temp = nodes_list[flight.flight_no]
                if temp is None:
                    nodes_list[flight.flight_no] = Node(flight,fare = (float('inf'),float('inf')))
                    temp = nodes_list[flight.flight_no]
                temp.parent = flight.flight_no
                temp.fare = (1,flight.fare)
                pq.insert(temp)
                if flight.end_city == end_city and temp.fare<=mini :
                    path = [flight]
                    mini=temp.fare
                    last_node = temp
        if last_node is not None:
            return path
        while not pq.is_heap_empty():
            node = pq.extract()
            last_city = node.flight.end_city
            last_time = node.flight.arrival_time
            num,last_fare = node.fare                          # num is bfs distance
            if last_city == end_city and node.fare <= mini:
                last_node = node
                mini=node.fare
                break
            for flight in self.adj[last_city]:
                if flight.departure_time >= last_time+20 and flight.arrival_time <= t2 :
                    new_fare =(num+1, last_fare + flight.fare)
                    new_node = nodes_list[flight.flight_no]
                    if new_node is None:
                        nodes_list[flight.flight_no] = Node(flight,fare = (float('inf'),float('inf')))
                        new_node = nodes_list[flight.flight_no]
                    if new_fare <= new_node.fare:
                        new_node.parent = node.flight.flight_no
                        new_node.fare = new_fare
                        pq.insert(new_node)
        return backtrack_path(nodes_list, start_city, last_node) 
#sagardeepak