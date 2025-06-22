from prime_generator import get_next_size

class HashTable:
    def __init__(self, collision_type, params): 
        pass  
    def insert(self, x):      
        pass   
    def find(self, key):
        pass   
    def get_slot(self, key):
        pass   
    def get_load(self):
        pass
    def __str__(self):
        pass
    def rehash(self):
        pass
    
class HashSet(HashTable):

    def __init__(self, collision_type, params):
        self.collision_type = collision_type
        self.params = params
        if collision_type == "Chain" or collision_type == "Linear":
            self.table_size = params[1]
            self.z = params[0]
        else:
            self.table_size = params[3]
            self.z, self.z2, self.c2 = params[0], params[1], params[2]

        self.table = [None] * self.table_size
        self.num_of_elements = 0
    
    def insert(self, key):
        slot = self.get_slot(key)
        if self.collision_type == "Chain":
            if self.table[slot] == None:
                self.table[slot] = []
            if key not in self.table[slot]:
                self.table[slot].append(key)
            else:
                return
        elif self.collision_type == "Linear": 
            if self.num_of_elements == self.table_size:
                raise Exception("Table Is FULL - CANNOT INSERT")
            while self.table[slot] != None :
                if self.table[slot] == key:
                    return
                slot = (slot + 1) % self.table_size
            self.table[slot] = key
        else:
            if self.num_of_elements == self.table_size:
                raise Exception("Table Is FULL - CANNOT INSERT") 
            h2 = self.h2_fxn(key,self.z2,self.c2) 
            while(self.table[slot]!=None):
                if(self.table[slot]==key):
                    return 
                slot =(slot+ (h2)%self.table_size)%self.table_size 
            self.table[slot] = key
        self.num_of_elements += 1
    
    def find(self, key): 
        slot = self.get_slot(key)
        if self.collision_type == "Chain":
            if self.table[slot] == None :
                return False
            return key in self.table[slot]
        elif self.collision_type == "Linear": 
            while(self.table[slot] != None):
                if(self.table[slot] == key):
                    return True
                slot = (slot + 1) % self.table_size
            return False
        else:  
            h2 = self.h2_fxn(key,self.z2,self.c2)  
            while(self.table[slot]!=None):
                if(self.table[slot] == key):
                    return True 
                slot =(slot+ (h2)%self.table_size)%self.table_size
            return False  
    
    def get_slot(self, key):
        return self.h_fxn(key, self.z, self.table_size)
    
    def get_load(self):
        return self.num_of_elements/self.table_size  
    
    def __str__(self):
        parts = []
        
        if self.collision_type == "Chain":
            for i in range(self.table_size):
                if self.table[i] is None:
                    parts.append("<EMPTY>")
                else:
                    parts.append(" ; ".join(self.table[i]))
                if i != self.table_size - 1:
                    parts.append(" | ")
        
        else:   
            for i in range(self.table_size):
                if self.table[i] is None:
                    parts.append("<EMPTY>")
                else:
                    parts.append(self.table[i])
                if i != self.table_size - 1:
                    parts.append(" | ")
        
        return "".join(parts)
    
    def h_fxn(self, name, z, table_size):
        cum = 0
        poww = 1
        for char in name:
            char_val = ord(char) - ord('a') if 'a' <= char <= 'z' else ord(char) - ord('A') + 26
            cum = (cum + char_val * poww) % table_size
            poww = (poww * z) % table_size
        return cum
        
    def h2_fxn(self,name,z2,c2):
        return c2-self.h_fxn(name,z2,c2) 
    
class HashMap(HashTable):
    def __init__(self, collision_type, params):
        self.collision_type = collision_type
        self.params = params
        if collision_type == "Chain" or collision_type == "Linear":
            self.table_size = params[1]
            self.z = params[0]
        elif(collision_type == "Double"):
            self.table_size = params[3]
            self.z, self.z2, self.c2 = params[0], params[1], params[2]

        self.table = [None] * self.table_size
        self.num_of_elements = 0 
    
    def insert(self, x): 
        key = x[0]
        value = x[1] 
        if self.collision_type == "Chain":
            slot = self.get_slot(key)
            if self.table[slot] is None:
                self.table[slot] = [] 
            for i in range(len(self.table[slot])):
                if self.table[slot][i][0] == key:
                    self.table[slot][i][1] = value
                    return   
            self.table[slot].append([key, value])
        elif self.collision_type == "Linear":
            if self.num_of_elements == self.table_size:
                raise Exception("Table Is FULL - CANNOT INSERT")
            slot = self.get_slot(key)
            while self.table[slot] is not None:
                if self.table[slot][0] == key: 
                    self.table[slot][1] = value
                    return
                slot = (slot + 1) % self.table_size
            self.table[slot] = [key, value]
        else:
            if self.num_of_elements == self.table_size:
                raise Exception("Table Is FULL - CANNOT INSERT")
            slot = self.get_slot(key) 
            h2 = self.h2_fxn(key, self.z2, self.c2) 
            while self.table[slot] is not None:
                if self.table[slot][0] == key: 
                    self.table[slot][1] =  value
                    return 
                slot =(slot+ (h2)%self.table_size)%self.table_size 
            self.table[slot] = [key, value]
        self.num_of_elements += 1 
    
    def find(self, key):
        slot = self.get_slot(key)
        if self.collision_type == "Chain":
            if self.table[slot]==None:
                return None 
            for i in self.table[slot]:
                if i[0]==key:
                    return i[1]
            return None
        elif self.collision_type == "Linear": 
            while self.table[slot] != None:
                if self.table[slot][0] == key:
                    return self.table[slot][1]
                slot = (slot+1)%self.table_size
            return None
        else:  
            h2 = self.h2_fxn(key,self.z2,self.c2)  
            while self.table[slot]!=None:
                if self.table[slot][0]==key:
                    return self.table[slot][1]
                slot =( slot+ (h2)%self.table_size)%self.table_size 
            return None
    
    def get_slot(self, key):
        return self.h_fxn(key, self.z, self.table_size)
    
    def get_load(self):
        return self.num_of_elements/self.table_size 
    
    '''Probing HashMap: (Stack, 1) | (AVL, 2) | <EMPTY> | (Heap, 3) | (Hash,4)'''
    '''Chaining HashMap: (Stack, 1) ; (AVL, 2) | <EMPTY> | (Heap, 3) | (Hash,4)'''
    def __str__(self):
        parts = []
        
        if self.collision_type == "Chain":
            for i in range(self.table_size):
                if self.table[i] is None:
                    parts.append("<EMPTY>")
                else:
                    parts.append(" ; ".join(f"({k}, {v})" for k, v in self.table[i]))
                if i != self.table_size - 1:
                    parts.append(" | ")
        
        else:   
            for i in range(self.table_size):
                if self.table[i] is None:
                    parts.append("<EMPTY>")
                else:
                    parts.append(f"({self.table[i][0]}, {self.table[i][1]})")
                if i != self.table_size - 1:
                    parts.append(" | ")
        
        return "".join(parts)

    def h_fxn(self, name, z, table_size):
        cum = 0
        poww = 1
        for char in name:
            char_val = ord(char) - ord('a') if 'a' <= char <= 'z' else ord(char) - ord('A') + 26
            cum = (cum + char_val * poww) % table_size
            poww = (poww * z) % table_size
        return cum

        
    def h2_fxn(self,name,z2,c2):
        return c2-self.h_fxn(name,z2,c2)