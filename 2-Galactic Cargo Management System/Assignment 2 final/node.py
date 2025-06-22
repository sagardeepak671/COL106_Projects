class Node:
    def __init__(self, bin_id, capacity,value = None, left=None, right=None):   
        self.id = bin_id
        self.capacity = capacity             # tree sorted by .capacity first than by .id
        self.left = left
        self.right = right
        self.value = value                  # for storing object id in bin
        self.size =None
        self.height = 1


