'''
    This file contains the class definition for the StrawHat class.
'''
import crewmate
import heap
import treasure

class StrawHatTreasury:
    '''
    Class to implement the StrawHat Crew Treasury
    '''
    def comp1(self,a,b):
        if (-a[1].arrival_time-a[0]) == (-b[1].arrival_time-b[0]):
            return a[1].id < b[1].id
        return (-a[1].arrival_time-a[0]) > (-b[1].arrival_time-b[0])
    def comp2(self,a,b):
        return a.load+a.lastest_entry < b.load+b.lastest_entry

    def __init__(self, m):
        self.crew = heap.Heap(self.comp2)
        for i in range(m):
            c = crewmate.CrewMate()
            self.crew.insert(c)
        self.completed = []
        self.filledmates = []

    def add_treasure(self, treasure):

        least_load_crew = self.crew.extract()
        # print(least_load_crew.load)
        # print(least_load_crew.load)
        if not least_load_crew.treasures:
            self.filledmates.append(least_load_crew)
        least_load_crew.addtreasure(treasure)
        self.crew.insert(least_load_crew)


    def get_completion_time(self):
        self.completed = []
        for i in range(len(self.filledmates)):
            c = self.filledmates[i]
            r = []
            j = 0
            while j < len(c.treasures):
                r.append([c.treasures[j].size, c.treasures[j]])
                j += 1
            count = 0
            h = heap.Heap(self.comp1)
            k = 0
            while k < len(r):
                i = r[k]
                count = 0
                if len(h.heap) > 0:
                    total = i[1].arrival_time
                    for l in range(len(h.heap)):
                        if total >= 0:
                            if h.top()[0] <= total - h.top()[1].top:
                                d = h.extract()
                                d[1].completion_time = d[1].top + d[0]
                                self.completed.append(d[1])
                                if len(h.heap)>0:
                                    h.top()[1].top = d[1].top + d[0]
                                total -= d[0]
                                d[0] = 0
                            else:
                                d = h.extract()
                                d[0] = d[0] - (i[1].arrival_time - d[1].top)
                                h.insert(d)
                                total = 0
                                break
                    if total > 0:
                        if len(h.heap) > 0:
                            f = h.top()
                            h.insert(i)
                            s = h.top()
                            if f == s:
                                h.top()[1].top = i[1].arrival_time - total
                            else:
                                h.top()[1].top = i[1].arrival_time
                        else:
                            h.insert(i)
                            h.top()[1].top = i[1].arrival_time
                    else:
                        h.insert(i)
                        h.top()[1].top = i[1].arrival_time
                else:
                    h.insert(i)
                    h.top()[1].top = i[1].arrival_time
                k += 1

            count = r[-1][1].arrival_time
            for m in range(len(h.heap)):
                t = h.extract()
                t[1].completion_time = t[0] + count
                count += t[0]
                t[0] = 0
                self.completed.append(t[1])
            
        self.completed.sort(key=lambda x: x.id)
        return self.completed
