import datetime
import sys

# convenience class edit the defaults for trucks in other cities here
class LocalTruck:

    def __init__(self):
        self.speed = 18
        self.capacity = 16
        self.start_address = '4001 South 700 East'

# Delivery class holds info about each delivery
# The route is made up of delivery objects
# Current usage is useful for visibility into individual truck routes
# Could be extended to allow real time tracking
class Delivery:

    cumulative_distance = 0

    def __init__(self, package_id, address, delivery_time, distance):
        self.package_id = package_id
        self.address = address
        self.delivery_time = delivery_time
        self.distance = distance
        Delivery.cumulative_distance += distance       

    def __str__(self):
        return f'{self.package_id} - dist: {self.distance} :: {round(self.cumulative_distance,2)} time : {self.delivery_time} address {self.address}'



class Truck:

    def __init__(self, departure_time, truck_id, priority_package_list = []):
        # fields specific to WGU location
        local_truck = LocalTruck()
        self.speed = local_truck.speed
        self.capacity = local_truck.capacity
        self.start_address = local_truck.start_address

        # Holds the route and deliveries for each truck
        self.route = []

        self.miles = 0
        self._departure_time = self.parse_departure_time(departure_time) 
        self.excursion_duration = 0
        
        # all the packages that go onto the truck
        self.package_count = 0
        self.package_list = []
        
        self.truck_id = truck_id
        
        # check that we don't have too many packages in our priority list
        # then add them
        if (len(priority_package_list) > self.capacity):
            print("Too many packages in priority package list")
            return
        else:
            self.package_count = len(priority_package_list)
            self.package_list = priority_package_list


    def parse_departure_time(self, depart_time):
        hour = depart_time.split(':')[0]
        minute = depart_time.split(':')[1]
        return datetime.timedelta(hours=int(hour), minutes=int(minute))
    
    
    def get_nearest_neighbor(self, package_list, distance_table, route_idx):
    
        prev_stop = self.start_address
        min_distance = sys.maxsize
        next_package_id = sys.maxsize

        if len(self.route) > 0:
            prev_stop = self.route[route_idx].address

        # find the nearest neighbor
        for package in package_list:

            dist = distance_table.get_distance(prev_stop, package.delivery_address)

            if (dist < min_distance):
                next_package_id = package.id
                min_distance = dist        

        return min_distance, next_package_id


    def update_route(self, package, min_distance):
        # add delivery to route
        self.route.append(Delivery(package.id, package.delivery_address, package.delivery_time, min_distance))
        
       
    def update_package(self, package):
        # update package info now that's it's loaded and routed
        duration_in_seconds = round(self.excursion_duration * 3600)
        package.delivery_time = datetime.timedelta(seconds=duration_in_seconds) + self._departure_time
        package.load_to_truck_time = self._departure_time
        package.delivery_status = "en route"
        package.truck_id = self.truck_id


    def go_home(self, distance_table):
        # After delivering last package, return to WGU hub

        if len(self.route) > 0:
            
            home_distance = distance_table.get_distance(self.route[len(self.route)-1].address, 
                                                       self.start_address)
            
            self.excursion_duration += home_distance / self.speed
            duration_in_seconds = round(self.excursion_duration * 3600)
            home_time = datetime.timedelta(seconds=duration_in_seconds) + self._departure_time
            self.route.append(Delivery(-1, self.start_address, home_time, home_distance))
            
            self.miles += home_distance

    def format_priority_table(self, priority_count):

        # initialize and set rows
        priority_table = [[]]
        for i in range(priority_count):
            priority_table.append([])
        
        # place package in apporiate priority list
        for p in self.package_list:
            priority_table[p.delivery_priority].append(p)

        return priority_table

    # when determining the route, we first map the priority packages
    # they are delivered by delivery_deadline, then by nearest neighbor
    # Ex: if there are 3 packages with 10:30am delivery deadlines
    # the algo will select the closest to it's current address for the next delivery
    def set_priority_route(self, distance_table):
        
        # check that we have any priority deliveries
        if self.package_count == 0:
            return
        
        # get the lowest priority by looking at the last package added
        priority_count = self.package_list[self.package_count-1].delivery_priority + 1
        
        # organize priority list into columns of equal priorities
        priority_table = self.format_priority_table(priority_count)
        curr_address = self.start_address # defaults to the WGU hub
        
        i = 0
        while i < priority_count:
            
            # if this is not the first stop on our route, replace our starting address with the last delivery address
            if len(self.route) > 0:
                curr_address = self.route[len(self.route)-1].address
            
            # this is the last package with the current time priority
            if len(priority_table[i]) == 1: 
                
                # we don't select nearest neighbor here
                # because this package has higher time priority than all the others
                package = priority_table[i][0]
                min_distance = distance_table.get_distance(curr_address, package.delivery_address)
                
                self.miles += min_distance
                self.excursion_duration += min_distance / self.speed
                self.update_package(package)
                self.update_route(package, min_distance)
                
                i += 1
               
            else:
                # get nearest negihbor
                min_distance, next_package_id = self.get_nearest_neighbor(
                    priority_table[i], distance_table, len(self.route)-1)
                
                # create the delivery and update package info
                for package in priority_table[i]:
                    if package.id == next_package_id:
                        
                        # set package expected delivery time
                        self.excursion_duration += min_distance / self.speed
                        self.miles += min_distance

                        self.update_package(package)
                        self.update_route(package, min_distance)
                        
                         # remove package from priority table
                        priority_table[i].remove(package)

                    
    def load_truck(self, unconstrained_packages, distance_table):
        
        # first route the priority packages
        self.set_priority_route(distance_table)
        
        # check that we have enough room left on the truck
        remaining_capacity = self.capacity - self.package_count
         
        # set so we stop loading if we run out of packages
        if remaining_capacity > len(unconstrained_packages):
            remaining_capacity = len(unconstrained_packages)
       
        if remaining_capacity < 1:
            return
      
        while remaining_capacity > 0:
             
            min_distance, next_package_id = self.get_nearest_neighbor(
                unconstrained_packages, distance_table, len(self.route)-1)
          
            for package in unconstrained_packages:
                    if package.id == next_package_id:
                        
                        self.excursion_duration += min_distance / self.speed
                        self.package_count += 1
                        remaining_capacity -= 1
                        self.miles += min_distance
                        
                        self.update_package(package)
                        self.update_route(package, min_distance)
                        
                        unconstrained_packages.remove(package)
                        
                        break
        
        self.go_home(distance_table)
        
       

