from bin import Bin
from avl import AVLTree
from object import Object, Color
from exceptions import NoBinFoundException

class GCMS:
    def __init__(self):
        self.bintree = AVLTree()                              # main avl tree by (sort by capacity)
        self.bin_address_tree = AVLTree()                     # to find the remainig capacity and objects in this address bin
        self.object_address_tree = AVLTree()                  # to find in which address bin is the this address object

    def add_bin(self, bin_id, capacity):
        temp = AVLTree()
        self.bintree.insert_value(bin_id, capacity)                                       # sorted by capacity
        self.bin_address_tree.insert_value(capacity, bin_id)                              # sorted by bin_id    
        self.bin_address_tree.search(self.bin_address_tree.root, bin_id).value = temp    

    def add_object(self, object_id, size, color):
        
        temp_node = None
        if color == Color.GREEN:  
            temp_node = self.bintree.GreenCargo(self.bintree.root)
        elif color == Color.RED:
            temp_node = self.bintree.RedCargo(self.bintree.root)
        elif color == Color.YELLOW:  
            temp_node = self.bintree.YellowCargo(self.bintree.root,size)
        elif color == Color.BLUE:
            temp_node = self.bintree.BlueCargo(self.bintree.root,size)

        if temp_node is None:
            raise NoBinFoundException
        
        if temp_node.capacity >= size:
            remaining_capacity = temp_node.capacity - size
            curr_id = temp_node.id
            self.bintree.delete_value(curr_id, temp_node.capacity)
            self.bintree.insert_value(curr_id, remaining_capacity)
            bin_node = self.bin_address_tree.search(self.bin_address_tree.root, curr_id)
            bin_node.value.insert_value(curr_id,object_id)
            bin_node.id = remaining_capacity
            self.object_address_tree.insert_value(curr_id, object_id)
            self.object_address_tree.search(self.object_address_tree.root, object_id).value = size     # .value store the size of the object in the object tree to use it while deleting the object
        else :
            raise NoBinFoundException
    
    def delete_object(self, object_id):
        bin_id = self.object_address_tree.search(self.object_address_tree.root, object_id)
        if bin_id is None:
            return None
        bin_node = self.bin_address_tree.search(self.bin_address_tree.root, bin_id.id)
        initail_capacity = bin_node.id
        bin_node.id += bin_id.value
        final_capacity = bin_node.id
        self.bintree.delete_value(bin_id.id, initail_capacity)
        self.bintree.insert_value(bin_id.id, final_capacity)
        
        bin_node.value.delete_value(bin_id.id, object_id)
        self.object_address_tree.delete_value(bin_id.id, object_id)
        
    def bin_info(self, bin_id):
        temp = self.bin_address_tree.search(self.bin_address_tree.root,bin_id)  # temp id is the bin capacity remaining
        if temp is None:
            return None , []
        return temp.id, self.inorder(temp.value.root)
        
    def in_helper(self, root, result):
        if root is None:
            return
        self.in_helper(root.left, result)
        result.append(root.capacity)
        self.in_helper(root.right, result)

    def inorder(self, root):
        if root is None:
            return []
        result = []
        self.in_helper(root, result)
        return result

    def object_info(self, object_id):
        temp =  self.object_address_tree.search(self.object_address_tree.root,object_id)
        if temp is None:
            return None
        return temp.id
    