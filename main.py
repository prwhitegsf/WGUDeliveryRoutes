import datetime

from PackageTable import PackageTable
from Distance import Distance
from Truck import Truck

# User interface
print("WGU Package Router and Tracker")
print("-------------------------------------------\n")
print("Welcome to the WGU Package Tracker!\n")
print("At any time enter 'q' to quit application\n")

# packages
# PackageTable contructor calls method to import and parse package.csv
# Creates a package object for each row of csv
# Package constructor parses row and sets fields with initial values
packages = PackageTable('data/package.csv')

# distances
# Distance constructor calls method to import and parse distance.csv
# creates address table allowing us to get the distance table index from an address
# creates distance table with lookup by index
distance_table = Distance("data/distance.csv")

# Load Trucks: 
# Priority packages are packages that must be on a particular truck
# Priority packages are assigned a priority based on delivery deadline
# Then program creates a route based first on priority and second on nearest neighbor
# The remainder of the truck is filled based on nearest neighbor algo

priority_packages = [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40]
truck_1 = Truck("08:00", 1, packages.sort_packages_by_deadline(priority_packages))
truck_1.load_truck(packages.get_packages_without_constraints(), distance_table)

# lookup function - see package still at hub, expected delivery still at default (17:00)
packages.lookup_package(3)

# includes packages arriving late
priority_packages = [3, 6, 18, 25, 28, 32, 36, 38]
truck_2 = Truck("09:10", 2, packages.sort_packages_by_deadline(priority_packages))
truck_2.load_truck(packages.get_packages_without_constraints(), distance_table)

# lookup function - now it's en route and has the delivery time set
#packages.lookup_package(3)

# update delivery address before loading truck 3
packages.search(9).delivery_address = '410 S State St'
priority_packages = [9]
truck_3 = Truck("10:25", 3, packages.sort_packages_by_deadline(priority_packages))
truck_3.load_truck(packages.get_packages_without_constraints(), distance_table)




print("About today's route:")
print("Mileage: ")
print("Truck_1: ", truck_1.miles)
print("Truck_2: ", truck_2.miles)
print("Truck_3: ", truck_3.miles)
total_miles = truck_1.miles + truck_2.miles + truck_3.miles
print("Total Mileage: ", round(total_miles,2),"\n")



while True:
    status_time = input("Please enter the status time (HH:MM) you wish to view: ")
    hour = 0
    minute = 0
    if status_time == "q":
        break
    try:
        # check that format is ok
        time = status_time.split(':')
        hour = int(time[0])
        minute = int(time[1])
        
    except:
        print("input format error: please enter time as HH:MM")
        print("For example: 12:35 or 09:40")

    print("\nThank you. You can track a package by its ID or you can see the status of all packages by entering 'all'")
    package_id = input("Please enter the package id (1-40 or 'all') you wish to track: ")
    
    if package_id == "q":
        break
    elif package_id == "all":
        total_package_count = 40 # get this from package table
        print("\n")
        print('{0:3} {1:8} {2:10} {3:10} {4:9} {5:6} {6:7} {7:}'.format("ID", "Time", "Status","Scheduled", "Deadline", "Truck", "Weight", "Address"))
        for package in range(1, total_package_count + 1):
            packages.get_package_delivery_status(package, datetime.timedelta(hours=hour,minutes=minute))
        print("\n")
    else:
        try:
            id = int(package_id)
            packages.get_package_delivery_status(id, datetime.timedelta(hours=hour,minutes=minute))
            print("\n")
        except:
            print("input format error: please enter 'all' or a number between 1 and 40")


print("\n Application closing, thanks and see you soon!")


