'''
    Python file to implement the class CrewMate
'''
import heap
import treasure

class CrewMate:
    '''
    Class to implement a crewmate
    '''
    
    def __init__(self):
        '''
        Arguments:
            None
        Returns:
            None
        Description:
            Initializes the crewmate
        '''
        # Write your code here
        self.load=0
        self.treasure_heap=heap.Heap(self.treasure_comparator,[])
        self.last_time_updated=0
        self.treasure_array=[]
        self.alloted=False
        self.last_updated_for_completion=0

    def reset_heap(self):
        self.treasure_heap=heap.Heap(self.treasure_comparator,[])
        

    def treasure_comparator(self, treasure1, treasure2, time):
        #priority is (t-arrival_time_of_treasure_instance)-remaining_size_of_treasure_instance
        #treasure1 is baccha
        #treasure2 is bada

        #Changes maade
        if((time-treasure1.arrival_time)-treasure1.remaining_size == (time-treasure2.arrival_time)-treasure2.remaining_size):
            if(treasure1.id<treasure2.id):
                return True
            else:
                return False
        elif (time-treasure1.arrival_time)-treasure1.remaining_size < (time-treasure2.arrival_time)-treasure2.remaining_size:
            return False 
        else:
            return True

    # Add more methods if required