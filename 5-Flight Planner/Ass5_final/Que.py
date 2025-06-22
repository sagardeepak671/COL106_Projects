class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
class Queue:
    def __init__(self):
        self.front = None
        self.rear = None


    def push(self, data):
        new_node = Node(data)
        if self.rear is None or self.is_empty() is True or self.front is None:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
            
    def is_empty(self):
        if self.front is None:
            return True
        return False

    def popp(self):
        if not self.is_empty():
            removed_data = self.front.data
            self.front = self.front.next
            if self.front is None:
                self.rear = None
            return removed_data
        else:
            print("Given Queue is empty")
            return None
    
    def front(self):
        if not self.is_empty():
                return self.front.data
        print("Given Queue is empty")
        return None

    def display(self):
        if self.is_empty():
            print("Given Queue is empty")
            return
        temp = self.front
        while temp:
            print(temp.data, end=" => ")
            temp = temp.next
        print("None")
    
    def size(self):
        if self.is_empty():
            return 0
        temp = self.front
        cnt = 0
        while temp is not None:
            cnt += 1
            temp = temp.next
        return cnt
    
    #sagar deepak
    def __str__(self):
        if self.is_empty():
            return "Given Queue is empty"
        temp = self.front
        result = ""
        while temp:
            result += str(temp.data) + " => "
            temp = temp.next
        return result + "None"
    
    def __repr__(self):
        return self.__str__()
    
    #print the queue just for the debugging prpose
    def bettr_print(self):
        if self.is_empty():
            print("Given Queue is empty")
            return
        temp = self.front
        while temp:
            print(temp.data)
            temp = temp.next
        print("None")
     