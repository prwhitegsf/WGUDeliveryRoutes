import csv

class Distance:

    def __init__(self, distances_filepath):

        self.distances_filepath = distances_filepath
        # holds the index for each address in the distance table
        self.address_table = []
        self.distance_table =[]
        # building distance table in constructor
        self.import_distances()


    def import_distances(self):
        
        with open(self.distances_filepath) as csv_input:
            # open the csv
            input_table = csv.reader(csv_input, delimiter=',')
            # initialize line index 
            line_idx = 0
            # read in rows line by line
            # skip first line, then add rest to out packages 
            for row in input_table:
                if line_idx != 0:
                    # write address lookup table
                    # we want our keys to start at 0
                    key = line_idx - 1
                    address_arr = row[0].split("\n")
                    self.address_table.append([address_arr[1].strip(), key])
                    
                    # write distance table
                    self.distance_table.append(row[2:])
                    
                    
                line_idx += 1     


    def get_key_from_address(self, address):

        for row in self.address_table:
            if address in row[0]:
                return int(row[1])
            
        return None


    def get_distance(self, address_1, address_2):
        
        address_1_key = self.get_key_from_address(address_1)
        address_2_key = self.get_key_from_address(address_2)
      
        if address_1_key != None and address_2_key != None:
            
            distance = self.distance_table[address_1_key][address_2_key]

            # check if our x/y are reversed and fix it
            if distance == "":
                distance = self.distance_table[address_2_key][address_1_key]
            
            return float(distance)
        
        return None