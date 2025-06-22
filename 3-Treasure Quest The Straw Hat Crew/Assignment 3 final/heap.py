'''
Python Code to implement a heap with general comparison function
'''

class Heap:
    '''
    Class to implement a heap with general comparison function
    '''

    def __init__(self,comparison_function,data=None):
        # If data is provided, use heapify to turn it into a heap
        self.compare = comparison_function
        if data is None:
            self.heap = []
        else:
            self.heap = data
            self.heapify()

    def heapify(self):
        # Get the index of the last non-leaf node
        n = len(self.heap)
        # Start from the last non-leaf node and move upwards to the root (index 0)
        for i in range(n // 2 - 1, -1, -1):
            self.sift_down(i, n)

    def sift_down(self, i, n):
        # Sifting down to maintain the heap property
        smallest = i
        left = 2 * i + 1  # Left child index
        right = 2 * i + 2  # Right child index

        # Check if left child exists and is smaller than the current node
        if left < n and self.compare(self.heap[left] ,self.heap[smallest]):
            smallest = left

        # Check if right child exists and is smaller than the current smallest
            if right < n and self.compare(self.heap[right] ,self.heap[smallest]):
                smallest = right

        # If the smallest value is not the parent node, swap and continue sifting down
        if smallest != i:
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            self.sift_down(smallest, n)


    def parent(self,r):
        return  (r-1)//2
    
    def left_child(self,r):
        return 2*r+1
    
    def right_child(self,r):
        return 2*r +2
    
    def has_left(self,r):
        return  self.left_child(r) < len(self.heap)
    
    def has_right(self,r):
        return self.right_child(r) < len(self.heap)
    
    def swap(self,i,j):
        self.heap[i],self.heap[j] = self.heap[j],self.heap[i]

    def upheap(self,j):
        parent = self.parent(j)
        if self.compare(self.heap[j],self.heap[parent]) and j > 0:
            self.swap(j,parent)
            self.upheap(parent)

    def  downheap(self,j):
        if self.has_left(j):
            left = self.left_child(j)
            mini = left
            if self.has_right(j):
                right = self.right_child(j)
                if self.compare(self.heap[right],self.heap[left]):
                    mini = right
            if self.compare(self.heap[mini],self.heap[j]):
                self.swap(j,mini)
                self.downheap(mini)

    def insert(self, value):
        '''
        Arguments:
            value : Any : The value to be inserted into the heap
        Returns:
            None
        Description:
            Inserts a value into the heap
        Time Complexity:
            O(log(n)) where n is the number of elements currently in the heap
        '''
        
        # Write your code here
        self.heap.append(value)
        self.upheap(len(self.heap)-1)

    # def heapify(self):
    #     for i in range(len(self.heap)-1,-1):
    #         self.upheap(i)
    
    def extract(self):
        
        # Write your code here
        if len(self.heap) == 0:
            return None
        self.swap(0,len(self.heap)-1)
        item = self.heap.pop()
        self.downheap(0)
        return item

    def top(self):
        # Write your code here
        return self.heap[0]
    
