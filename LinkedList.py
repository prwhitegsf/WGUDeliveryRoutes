class Node:

    def __init__(self, package):
        self.package = package
        self.next_address = None

class LinkedList:

    def __init__(self, head=None):
        self.head = head


    def insert_element(self, package):
         
        new_node = Node(package)

        if self.head == None:
            self.head = new_node
            return
        
        current_node = self.head

        # iterate to end, which we identify by next_address == None
        while current_node.next_address is not None:
            if current_node.package.id != new_node.package.id:
                current_node = current_node.next_address
            else:
                print("Package id: "+ new_node.package.id + " is already in table")
                return

        # At this point we're on the current last element, 
        # we simply point it's next_address to our new node
        current_node.next_address = new_node
        return


    def search_by_id(self, id):

        current_node = self.head
       
        while current_node != None:
       
            if current_node.package.id == id:
                return current_node.package
            else:
                current_node = current_node.next_address    
        
        return None

    def remove_by_id(self, id):

        if self.head is None:
            print("no elements in list")
            return False

        # if the value is the head
        # set the head to the next pointer
        current_node = self.head
        if current_node.package.id == id:
            self.head = current_node.next_address
            return True
        
        # otherwise, loop through searching for it on the next node
        # we'll want to be able to access the node before the id to 
        # change the pointer
        while current_node.next_address != None:
            
            if current_node.next_address.package.id == id:
                temp = current_node
                current_node = current_node.next_address
                next_node_after_removal = current_node.next_address
                temp.next_address = next_node_after_removal
                return True
        print("removal value not found")
        return False



    def get_last_element(self):

        current_node = self.head()

        while current_node.next_address is not None:
            current_node = current_node.next_address

        return current_node.package


    def print_elements(self):
        # start wuth the head
        current_node = self.head
        element_list = []
        while current_node is not None:
            element_list.append(current_node.package)
            #print(current_node.package,", ")
            # increment to next node
            current_node = current_node.next_address
        
        print(element_list)

    
