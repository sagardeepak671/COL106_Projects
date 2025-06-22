# from treasure import Treasure  


class Heap:
    def __init__(self, comparison_function, init_array=[]):
        self.heap = init_array[:]
        self.cmp = comparison_function

    def heapify_up(self, i):
        parent_index = (i - 1) // 2
        while i > 0 and self.cmp(self.heap[i], self.heap[parent_index]):
            self.heap[i], self.heap[parent_index] = self.heap[parent_index], self.heap[i]
            i = parent_index
            parent_index = (i - 1) // 2
            
    def heapify_down(self, i):
        left_child_index = 2 * i + 1

        right_child_index = 2 * i + 2
        smallest = i

        if left_child_index < len(self.heap) :
            if self.cmp(self.heap[left_child_index], self.heap[smallest]):
                smallest = left_child_index

        if right_child_index < len(self.heap):
            if self.cmp(self.heap[right_child_index], self.heap[smallest]):
                smallest = right_child_index

        if smallest != i:
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            self.heapify_down(smallest)

    #build heap in O(n)  sagar deepak
    def build_heap(self):
        for i in range(len(self.heap) // 2, -1, -1):
            self.heapify_down(i)

    def extract(self):
        if not self.heap:
            return None
        # sw ap
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        # pop la st one
        value = self.heap.pop()
        # heapi fy it 
        self.heapify_down(0)
        return value
    
    def insert(self, value):
        self.heap.append(value)
        self.heapify_up(len(self.heap) - 1)

    def top(self):
        if self.heap:
            return self.heap[0]
        else:
            return None
            
    #sagardeepak
    def defaultExcride(self, x):
        
        return self.heap[x]
    
    def left_child(self,index):
        if 2*index + 1 < len(self.heap):
            return self.heap[2*index + 1]
        else:
            return None
        
    def right_child(self,index):
        if 2*index + 2 < len(self.heap):
            return self.heap[2*index + 2]
        else:
            return None
    
    def is_heap_empty(self):
        if len(self.heap) == 0:
            return True
        else:
            return False
    def parent(self,index):
        if index == 0:
            return None
        return self.heap[(index-1)//2]
    
    def size_of_heap(self):
        if self.heap:
            return len(self.heap)
        else:
            return 0

    def _printHelper(self, index, indent, excride = defaultExcride):
        
        if index >= self.size:
            return
        print(indent[:-3]+"---", end="")
        print(excride(self, index))
        # print(1)
        self._printHelper(2*index + 1, indent + "|   ", excride)
        self._printHelper(2*index + 2, indent + "|   ", excride)

    #used to print the heap just for the degugging prpose
    def prettyPrint(self):
        self._printHelper(0, "    ")
        # print(self.size)
        print(f'Heap Size: {self.size}')
        print(f'Top: {self.top()}')

    def __str__(self):
        return str(self.heap)
    
    def __repr__(self):
        return str(self.heap)
    