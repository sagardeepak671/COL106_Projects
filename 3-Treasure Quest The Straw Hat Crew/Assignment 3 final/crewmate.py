import heap
import treasure
class CrewMate:
    '''
    Class to implement a crewmate
    '''
    # def comp1(self,a,b):
    #     if (-a.arrival_time-a.remaining) == (-b.arrival_time-b.remaining):
    #         return a.id < b.id
    #     return (-a.arrival_time-a.remaining) > (-b.arrival_time-b.remaining)
    
    def __init__(self):

        self.load = 0
        self.treasures = []
        self.lastest_entry = 0

    def addtreasure(self,treasure):
        # print(treasure.arrival_time)
        treasure.top = None
        treasure.remaining = treasure.size
        self.treasures.append(treasure)
        self.load =  max(0, self.load - (treasure.arrival_time - self.lastest_entry))
        self.load += treasure.size
        self.lastest_entry  = treasure.arrival_time

        
