
from Package import Package
from LinkedList import *
import csv
from datetime import datetime

# Hash Table implementation with chaining
# Array w/ each index holding a linked list
class PackageTable:

    def __init__(self, packages_filepath, initial_capacity = 10):
        
        self.packages_filepath = packages_filepath
        
        # All packages
        self.table = []

        # Packages with constraints
        self.with_special_notes = []
        self.with_delivery_deadlines = []

        # packages without constraints
        self.with_no_constraints = []

        # initialize linked list at each index for ease of use
        for i in range(initial_capacity):
            self.table.append(LinkedList())
        
        self.import_package_table()

    
    def get_key(self, package_id):
        return int(package_id) % len(self.table)

    
    def import_package_table(self):
        
        with open(self.packages_filepath) as csv_input:
            # open the csv
            input_table = csv.reader(csv_input, delimiter=',')
            # initialize line index 
            line_idx = 0
            # read in rows line by line
            # skip first line, then add rest to out packages 
            for row in input_table:
                if line_idx == 0:
                    pass
                else:
                    # Package constructor parses list and sets all fields for each package
                    package = Package(row)
                    self.insert_package(package)
                    
                    # collect id's for packages with special notes
                    if package.special_notes != '':
                        self.with_special_notes.append(package.id)
                    # collect id's for ackages without special notes
                    # and with delivery deadlines before EOD
                    elif package.delivery_deadline != 'EOD':
                        self.with_delivery_deadlines.append(package.id)
                    # the rest of the packages have no constraints
                    # the program will draw from this list when 
                    # loading the truck and searching for the nearest neighboring address
                    # after all priority packages are dealt with
                    else:
                        self.with_no_constraints.append(package.id)
                    
                line_idx += 1             
        
    
    def insert_package(self, item):
        bucket_idx = self.get_key(item.id)
        self.table[bucket_idx].insert_element(item)


    def search(self, id):
        bucket_idx = self.get_key(id)
        return self.table[bucket_idx].search_by_id(id)


    def lookup_package(self, id):
        print(str(self.search(id).__str__()))

 
    def get_package_delivery_status(self, id, time):
        # checks user specified time against scheduled load and delivery time
        # print package status based on user specified time
        
        package = self.search(id)
        
        load_time = package.load_to_truck_time
        delivery_time= package.delivery_time

        current_status = "at hub"

        if time > delivery_time:
            current_status = "delivered"
        elif time < delivery_time and time > load_time:
            current_status = "en route"

        
        
        print ('{0:3} {1:8} {2:10} {3:10} {4:9} {5:6} {6:7} {7:} {8:} {9:} {10:}'
               .format(str(id), str(time),current_status,str(package.delivery_time), 
                       str(package.delivery_deadline), str(package.truck_id), 
                       str(package.package_weight), str(package.delivery_address),
                       str(package.delivery_city), str(package.delivery_state), package.delivery_zip))
     

    def remove_package(self, id):
        # get the bucket list where this item will be removed from.
        bucket_idx = self.get_key(id)
        return self.table[bucket_idx].remove_by_id(id)


    def get_packages_without_constraints(self):
        unconstrained = []
        for id in self.with_no_constraints:
            package = self.search(id)
            if package.delivery_status == "at hub":
                unconstrained.append(package)

        return unconstrained
    
    
    def insertion_sort_by_time(self, high_priority = []):
        # used to sort by delivery deadline
        if len(high_priority) == 0:
            return False
        
        high_priority[0].delivery_priority = 0
        
        # insertion sort algo
        for i in range(1,len(high_priority)):
            temp = high_priority[i]
            compare_value = datetime.strptime(high_priority[i].delivery_deadline, '%I:%M %p')            
            sorted_from_idx= i - 1
            sorted_from_idx_value = datetime.strptime(high_priority[sorted_from_idx].delivery_deadline, '%I:%M %p') 

            while sorted_from_idx >= 0:
                
                if sorted_from_idx_value > compare_value:
                    high_priority[sorted_from_idx + 1] = high_priority[sorted_from_idx]
                    high_priority[sorted_from_idx] = temp
                    sorted_from_idx -= 1 
                else:
                    break
    
    
    def determine_time_priority(self, priority, high_priority, eod_priority):
        # determines priority by delivery deadline: 
        # if not EOD, then pacage has a higher priority
        
        for p_id in priority:
            
            p = self.search(p_id)
            
            if p.delivery_deadline != 'EOD':
                high_priority.append(p)
            else:
                eod_priority.append(p)

    
    def set_package_priority_levels(self, high_priority, eod_priority):

        # assign priority
        # Items with same delivery deadline have equal priority
        # Ie if multiple items need to be delivered at 10:30am, they will have the same priority
        
        # if no packages with high priority, then it's all eod priority
        # and they're all the same priority level
        if len(high_priority) == 0:
            for p in eod_priority:
                p.delivery_priority = 0
            return

        high_priority[0].delivery_priority = 0
        for i in range(1,len(high_priority)):
            
            curr_time = datetime.strptime(high_priority[i].delivery_deadline, '%I:%M %p')            
            prev_time = datetime.strptime(high_priority[i-1].delivery_deadline, '%I:%M %p')
            
            if curr_time > prev_time:
                high_priority[i].delivery_priority = high_priority[i-1].delivery_priority + 1
            else:
                high_priority[i].delivery_priority = high_priority[i-1].delivery_priority    
    
        # get lowest priority in the high_priority list
        # Then set the eod package priorities to that + 1
        max_priority_level = high_priority[len(high_priority)-1].delivery_priority
        eod_priority_level = max_priority_level + 1

        for p in eod_priority:
            p.delivery_priority = eod_priority_level

    
    def sort_packages_by_deadline(self, priority = []):

        if len(priority) == 0:
            return False

        high_priority = []
        eod_priority = []
        self.determine_time_priority(priority, high_priority, eod_priority)
        
        # sort the high priority list by delivery deadline    
        self.insertion_sort_by_time(high_priority)   
        
        # Assign priority level to each package
        self.set_package_priority_levels(high_priority, eod_priority)
        
        # write to priority list, but now we're sorted by deadline
        priority = high_priority
        priority.extend(eod_priority)
        
        return priority
          





    


