from node import Node

def comp_1(node_1, node_2):
    if node_1.capacity == node_2.capacity:
        return node_1.id < node_2.id
    return node_1.capacity < node_2.capacity

class AVLTree:
    def __init__(self, compare_function=comp_1):
        self.root = None
        self.comparator = compare_function
    
    def height(self, node):
        if node is None:
            return 0
        return node.height
    
    def balance(self, node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)
    
    def left_rotate(self, node):
        y = node.right
        T2 = y.left
        y.left = node
        node.right = T2
        node.height = 1 + max(self.height(node.left), self.height(node.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))
        return y

    def right_rotate(self, node):
        y = node.left
        T3 = y.right
        y.right = node
        node.left = T3
        node.height = 1 + max(self.height(node.left), self.height(node.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))
        return y
   
    def insert(self, root, node):
        if root is None:
            return node
        if self.comparator(node, root):
            root.left = self.insert(root.left, node)
            root.left.parent = root
        else:
            root.right = self.insert(root.right, node)
            root.right.parent = root
        root.height = 1 + max(self.height(root.left), self.height(root.right))
        balance_factor = self.balance(root)
        if balance_factor > 1 and self.comparator(node, root.left):
            return self.right_rotate(root)
        if balance_factor < -1 and not self.comparator(node, root.right):
            return self.left_rotate(root)
        if balance_factor > 1 and not self.comparator(node, root.left):
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance_factor < -1 and self.comparator(node, root.right):
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)
        return root

    def delete(self, root, node_to_delete):
        if root is None:
            return root
        if self.comparator(node_to_delete, root):
            root.left = self.delete(root.left, node_to_delete)
        elif self.comparator(root, node_to_delete):
            root.right = self.delete(root.right, node_to_delete)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp

            temp = self.get_minimum_node(root.right)
            root.id = temp.id
            root.capacity = temp.capacity
            root.right = self.delete(root.right, temp)
        if root is None:
            return root
        root.height = 1 + max(self.height(root.left), self.height(root.right))
        balance_factor = self.balance(root)
        if balance_factor > 1 and self.balance(root.left) >= 0:
            return self.right_rotate(root)
        if balance_factor < -1 and self.balance(root.right) <= 0:
            return self.left_rotate(root)
        if balance_factor > 1 and self.balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance_factor < -1 and self.balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)
        return root 
    
    def get_minimum_node(self, root):
        temp = root
        if temp is None:
            return None
        while temp.left is not None:
            temp = temp.left
        return temp
    
    def get_maximum_node(self, root):
        temp = root
        if temp is None:
            return None
        while temp.right is not None:
            temp = temp.right
        return temp
    
    def get_minimum_id_node(self, capacity):
        temp = self.search(self.root, capacity)
        result = temp
        while temp:
            while temp and temp.left and temp.left.capacity == capacity:
                temp = temp.left
                result = temp
            temp = temp.left
            while temp and temp.right:
                temp = temp.right
                if temp.capacity == capacity:
                    result = temp
                    break
        return result
    
    def get_maximum_id_node(self, capacity):
        temp = self.search(self.root, capacity)
        result = temp
        while temp:
            while temp and temp.right and temp.right.capacity == capacity:
                temp = temp.right
                result = temp
            temp = temp.right
            while temp and temp.left:
                temp = temp.left
                if temp.capacity == capacity:
                    result = temp
                    break

        return result
    
    def insert_value(self, id, capacity):  #insert by value
        temp_node = Node(id, capacity)
        if self.root is None:
            self.root = temp_node
        else:
            self.root = self.insert(self.root, temp_node)

    def delete_value(self, id, capacity):  #delete by value
        temp_node = Node(id, capacity)
        if self.root is None:
            return
        self.root = self.delete(self.root, temp_node)

    # left left
    def BlueCargo(self, root, capacity):  
        if(root is None):
            return None
        temp_node = self.lower_bound_node(root,capacity)
        if(temp_node is None):
            return None
        return self.get_minimum_id_node(temp_node.capacity)

    # right right
    def GreenCargo(self, root):
        return self.get_maximum_node(root)

    # left right
    def YellowCargo(self, root, capacity):
        temp_node = self.lower_bound_node(root, capacity)
        if temp_node is None:
            return None
        return self.get_maximum_id_node(temp_node.capacity)

    # right left
    def RedCargo(self, root):
        temp_node = self.get_maximum_node(root)
        if temp_node is None:
            return None
        return self.get_minimum_id_node(temp_node.capacity)

    def lower_bound_node(self, root, capacity):
        temp = root
        result = None
        while temp:
            if temp.capacity >= capacity:
                if result is None:
                    result = temp
                else:
                    if temp.capacity < result.capacity:
                        result = temp
                temp = temp.left
            else:
                temp = temp.right
        return result

    def search(self, root, capacity):  # search by capacity value (not node)
        if root is None or (root.capacity == capacity):
            return root
        if root.capacity > capacity:
            return self.search(root.left, capacity)
        return self.search(root.right, capacity)
    
    #debugging
    def pre_order(self, root):
        if root is None:
            return []
        return [root.capacity] + [self.pre_order(root.left) , self.pre_order(root.right)]
   