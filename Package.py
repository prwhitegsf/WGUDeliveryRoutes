import datetime
import sys

class Package:

    def __init__(self, row):

        self.id = int(row[0])
        self.delivery_address = row[1].strip()
        self.delivery_city = row[2].strip()
        self.delivery_state = row[3].strip()
        self.delivery_zip = row[4].strip()
        
        self.delivery_deadline = row[5].strip()
        self.package_weight = row[6].strip()
        
        self.special_notes = row[7].strip()
        self.delivery_status = "at hub"
        
        self.load_to_truck_time = datetime.timedelta(hours=0, minutes=0)
        # defaults to end of day, updated on truck load
        self.delivery_time = datetime.timedelta(hours=17, minutes=0)
        
        self.delivery_priority = sys.maxsize
        self.truck_id = 0

    # add method to determine package status based on the time
    def __str__(self):
        return ("id : " + str(self.id) + "\n" + "status: " + self.delivery_status + 
                ", expected delivery: "+ str(self.delivery_time) + "\n" +
                "address: " + self.delivery_address + ", " + self.delivery_city + ", " + 
                self.delivery_state + " " + self.delivery_zip + "\n" + 
                "delivery deadline: " + self.delivery_deadline + "\n"
                +"package weight: " + self.package_weight +"\n")
        
    




    

