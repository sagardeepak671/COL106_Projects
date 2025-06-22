from hash_table import HashSet, HashMap
from prime_generator import get_next_size

class DynamicHashSet(HashSet):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        
    def rehash(self):
        # IMPLEMENT THIS FUNCTION
        big_size = get_next_size()
        old_table = self.table 
        self.table_size = big_size
        self.num_of_elements = 0
        self.table = [None] * self.table_size
        if self.collision_type == "Chain":
            for i in range(len(old_table)):
                if old_table[i] != None:
                    for j in range(len(old_table[i])):
                        self.insert(old_table[i][j])
        else:
            for i in range(len(old_table)):
                if old_table[i]!=None:
                    self.insert(old_table[i])
        
    def insert(self, key):
        # YOU DO NOT NEED TO MODIFY THIS
        super().insert(key)
        
        if self.get_load() >= 0.5:
            self.rehash()
            
            
class DynamicHashMap(HashMap):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        
    def rehash(self):
        # IMPLEMENT THIS FUNCTION\
        big_size = get_next_size()
        old_table = self.table  
        self.table_size = big_size
        self.num_of_elements = 0  
        self.table = [None] * self.table_size
        if  self.collision_type == "Chain":
            for i in range(len(old_table)):
                if old_table[i]!=None:
                    for j in range(len(old_table[i])):
                        self.insert(old_table[i][j]) 
        else:
            for i in range(len(old_table)):
                if old_table[i]!=None:
                    self.insert(old_table[i])



        
    def insert(self, key):
        # YOU DO NOT NEED TO MODIFY THIS
        super().insert(key)
        
        if self.get_load() >= 0.5:
            self.rehash()