'''
    This file contains the class definition for the StrawHat class.
'''

import crewmate
import heap
import treasure


class StrawHatTreasury:
    '''
    Class to implement the StrawHat Crew Treasury
    '''

    def __init__(self, m):
        '''
        Arguments:
            m : int : Number of Crew Mates (positive integer)
        Returns:
            None
        Description:
            Initializes the StrawHat
        Time Complexity:
            O(m)
        '''
        # Write your code here
        self.alloted_crewmates=[]
        self.initial_array=[]
        self.time=0
        for i in range(m):
            c=crewmate.CrewMate()
            # c.id=i
            self.initial_array.append(c)
        self.crew_heap=heap.Heap(self.crew_comparator,self.initial_array)
        

        return
    
    def add_treasure(self, treasure_instance):
        '''
        Arguments:
            treasure : Treasure : The treasure to be added to the treasury
        Returns:
            None
        Description:
            Adds the treasure to the treasury
        Time Complexity:
            O(log(m) + log(n)) where
                m : Number of Crew Mates
                n : Number of Treasures
        '''
        self.time=treasure_instance.arrival_time
        treasure_instance.set_remaining_size()
        # print()
        # for i in range(len(self.crew_heap.heap)):
        #     print(self.crew_heap.heap[i].load,'a')
        #Extract crew
        #allot treasure(don;t insert)
        #Update load of that crew person
        #update last time updated (done inside function)
        #down_heapify crew
        #O(log(m)+log(n))
        crew=self.crew_heap.extract()

        # treasure_instance.crewmate_alloted=crew.id
        crew.treasure_array.append(treasure_instance)

        if(crew.alloted==False):
            crew.alloted=True
            self.alloted_crewmates.append(crew)

        self.update_old_crew_load(crew)
        crew.load+=treasure_instance.size

        self.crew_heap.insert(crew)

        
    
    def get_completion_time(self):
        '''
        Arguments:
            None
        Returns:
            List[Treasure] : List of treasures in the order of their completion after updating Treasure.completion_time
        Description:
            Returns all the treasure after processing them
        Time Complexity:
            O(n(log(m) + log(n))) where
                m : Number of Crew Mates
                n : Number of Treasures
        '''
        
        # Write your code here
        #O(n(log(m)+log(n)))
        


        ans=[]
        for crew in self.alloted_crewmates:
            old_time=0
            crew.reset_heap()
            #If array is empty, it will not go inside for loop
            #i is a treasure to be inserted
            global_time=0
            #Make a copy of trasure_array
            for i in crew.treasure_array:
                time_present=i.arrival_time
                global_time=time_present
                #if treasure heap not empty, extract top treasure
                #else insert back both extracted treasure and i
                #insert should have an appropriate treasure comparator
                if(len(crew.treasure_heap.heap)==0):
                    crew.treasure_heap.insert_new(i,time_present)
                else:
                    extracted_treasure=self.pick_high_priority_treasure(crew,crew.treasure_heap,old_time,time_present,ans)
                    if(extracted_treasure!=None):
                        crew.treasure_heap.insert_new(extracted_treasure,time_present)
                    crew.treasure_heap.insert_new(i,time_present)
                    

                crew.last_updated_for_completion=time_present
                old_time=time_present


            #If the treasure heap is not empty, extract top treasure considering time_present very large
        # In get_completion_time
        for crew in self.alloted_crewmates:
            while len(crew.treasure_heap.heap) > 0:
                high_treasure = crew.treasure_heap.extract_new(global_time)
                high_treasure.completion_time = crew.last_updated_for_completion + high_treasure.remaining_size
                high_treasure.remaining_size = 0
                ans.append(high_treasure)
                crew.last_updated_for_completion = high_treasure.completion_time
        
        #sort by first element of tuple
        sorted_ans=sorted(ans,key=lambda x: x.id)

        #update cre.last_updated_for_completition to 0
        for i in self.alloted_crewmates:
            i.last_updated_for_completion=0
            # i.treasure_heap.heap=[]

        #Change remaining_size to original values
        for i in sorted_ans:
            i.remaining_size=i.size

        return sorted_ans
    

    # You can add more methods if required
    def update_old_crew_load(self, crew_instance):
        #Requires time, so defines inside the class
        '''
        Arguments:
            None
        Returns:
            None
        Description:
            Updates the load of the crewmate who has not been alloted any treasure for a long time
        Time Complexity:
            O(log(m))
        '''
        # Write your code here
        crew_instance.load=crew_instance.load-(self.time-crew_instance.last_time_updated)
        crew_instance.last_time_updated=self.time
        if(crew_instance.load<0):
            crew_instance.load=0
        return
    
    def crew_comparator(self,crewmate1, crewmate2):
        #requires update_old_crew_load, so defines inside the class
        '''
        Arguments:
            crewmate1 : CrewMate : First crew mate to compare
            crewmate2 : CrewMate : Second crew mate to compare
        Returns:
            int : -1 if crewmate1 should be higher in the heap (i.e., has lower load),
                1 if crewmate2 should be higher (i.e., has lower load),
                0 if both are considered equal.
        Description:
            Comparator function that compares two crew mates based on their load.
        Time Complexity:
            O(1)
        '''
        
        #First update the load of both crewmates
        #Then compare

        #crewmate1 is bacha
        #crewmate2 is baap

        self.update_old_crew_load(crewmate1)
        self.update_old_crew_load(crewmate2)

        if(crewmate1.load<crewmate2.load):
            return True
        elif(crewmate1.load>=crewmate2.load):
            return False
        
    def pick_high_priority_treasure(self,crew_instance,heap_instance_of_treasures,old_time,time_present,ans):
        if(len(heap_instance_of_treasures.heap)==0):
            return None
        
        high_treasure=heap_instance_of_treasures.extract_new(time_present)
        #then update remaining sizes of both extracted treasure and i
        #if remaining size of extracted treasure <=0, update completion time
        #and make a loop
        old_remaining_size=high_treasure.remaining_size
        high_treasure.remaining_size=high_treasure.remaining_size-(time_present-crew_instance.last_updated_for_completion)
        if(high_treasure.remaining_size<0):
            high_treasure.remaining_size=0
            high_treasure.completion_time=crew_instance.last_updated_for_completion+old_remaining_size
            ans.append(high_treasure)
            crew_instance.last_updated_for_completion=high_treasure.completion_time
            return self.pick_high_priority_treasure(crew_instance,heap_instance_of_treasures,old_time,time_present,ans)
        else:
            return high_treasure
        
        

# strawhat=StrawHatTreasury(3)
# t1=treasure.Treasure(1,8,1)
# t2=treasure.Treasure(2,7,2)
# t3=treasure.Treasure(3,4,4)
# t4=treasure.Treasure(4,1,5)
# strawhat.add_treasure(t1)
# strawhat.add_treasure(t2)
# strawhat.add_treasure(t3)
# strawhat.add_treasure(t4)
# print(strawhat.crew_heap.heap[0].treasure_array[0].id)
# print(strawhat.crew_heap.heap[1].treasure_array[0].id)
# print(strawhat.crew_heap.heap[2].treasure_array[0].id,strawhat.crew_heap.heap[2].treasure_array[1].id)
# #ans (2)(1)(3 4)
# processed=strawhat.get_completion_time()
# print('Completion Time:', [(treasure_obj.id, treasure_obj.completion_time) for treasure_obj in processed])

# strawhat=StrawHatTreasury(3)
# t1=treasure.Treasure(1,8,1)
# t2=treasure.Treasure(2,4,2)
# t3=treasure.Treasure(3,4,4)
# t4=treasure.Treasure(4,1,5)
# strawhat.add_treasure(t1)
# strawhat.add_treasure(t2)
# strawhat.add_treasure(t3)
# strawhat.add_treasure(t4)
# print(strawhat.crew_heap.heap[0].treasure_array[0].id,strawhat.crew_heap.heap[0].treasure_array[1].id)
# print(strawhat.crew_heap.heap[1].treasure_array[0].id)
# print(strawhat.crew_heap.heap[2].treasure_array[0].id)
#ans (2 4),(1),(3)

# strawhat=StrawHatTreasury(2)
# t1=treasure.Treasure(1,8,1)
# t2=treasure.Treasure(2,7,2)
# t3=treasure.Treasure(3,4,4)
# t4=treasure.Treasure(4,1,5)
# strawhat.add_treasure(t1)
# strawhat.add_treasure(t2)
# strawhat.add_treasure(t3)
# strawhat.add_treasure(t4)
# print(strawhat.crew_heap.heap[0].treasure_array[0].id,strawhat.crew_heap.heap[0].treasure_array[1].id)
# print(strawhat.crew_heap.heap[1].treasure_array[0].id,strawhat.crew_heap.heap[1].treasure_array[1].id)
# #ans (2 4),(1 3)

# strawhat=StrawHatTreasury(2)
# t1=treasure.Treasure(1,8,1)
# t2=treasure.Treasure(2,7,2)
# t3=treasure.Treasure(3,4,4)
# t4=treasure.Treasure(4,1,5)
# t5=treasure.Treasure(5,7,6)
# t6=treasure.Treasure(6,12,7)
# t7=treasure.Treasure(7,4,8)
# t8=treasure.Treasure(8,6,9)
# t9=treasure.Treasure(9,3,10)
# strawhat.add_treasure(t1)
# strawhat.add_treasure(t2)
# strawhat.add_treasure(t3)
# strawhat.add_treasure(t4)
# strawhat.add_treasure(t5)
# strawhat.add_treasure(t6)
# strawhat.add_treasure(t7)
# strawhat.add_treasure(t8)
# strawhat.add_treasure(t9)
# print(strawhat.crew_heap.heap[0].treasure_array[0].id,strawhat.crew_heap.heap[0].treasure_array[1].id,strawhat.crew_heap.heap[0].treasure_array[2].id,strawhat.crew_heap.heap[0].treasure_array[3].id,strawhat.crew_heap.heap[0].treasure_array[4].id)
# print(strawhat.crew_heap.heap[1].treasure_array[0].id,strawhat.crew_heap.heap[1].treasure_array[1].id,strawhat.crew_heap.heap[1].treasure_array[2].id,strawhat.crew_heap.heap[1].treasure_array[3].id)
# #ans (2 4 5 7 8),(1 3 6 9)


# strawhat=StrawHatTreasury(5)
# t1=treasure.Treasure(1,8,1)
# t2=treasure.Treasure(2,7,2)
# t3=treasure.Treasure(3,4,4)
# t4=treasure.Treasure(4,1,5)
# t5=treasure.Treasure(5,7,6)
# t6=treasure.Treasure(6,12,7)
# t7=treasure.Treasure(7,4,8)
# t8=treasure.Treasure(8,6,9)
# t9=treasure.Treasure(9,3,10)
# t10=treasure.Treasure(10,8,11)
# t11=treasure.Treasure(11,7,12)
# strawhat.add_treasure(t1)
# strawhat.add_treasure(t2)
# strawhat.add_treasure(t3)
# strawhat.add_treasure(t4)
# strawhat.add_treasure(t5)
# strawhat.add_treasure(t6)
# strawhat.add_treasure(t7)
# strawhat.add_treasure(t8)
# strawhat.add_treasure(t9)
# strawhat.add_treasure(t10)
# strawhat.add_treasure(t11)
# # print(strawhat.crew_heap.heap[0].treasure_array[0].id,strawhat.crew_heap.heap[0].treasure_array[1].id,strawhat.crew_heap.heap[0].treasure_array[2].id,strawhat.crew_heap.heap[0].treasure_array[3].id,strawhat.crew_heap.heap[0].treasure_array[4].id)
# # print(strawhat.crew_heap.heap[1].treasure_array[0].id,strawhat.crew_heap.heap[1].treasure_array[1].id,strawhat.crew_heap.heap[1].treasure_array[2].id,strawhat.crew_heap.heap[1].treasure_array[3].id)
# for i in range(5):
#     #print ids
#     print(strawhat.crew_heap.heap[i].treasure_array)

# print(strawhat.crew_heap.heap[0].treasure_array[0].id)
# print(strawhat.crew_heap.heap[1].treasure_array[0].id,strawhat.crew_heap.heap[1].treasure_array[1].id)
# print(strawhat.crew_heap.heap[2].treasure_array[0].id,strawhat.crew_heap.heap[2].treasure_array[1].id,strawhat.crew_heap.heap[2].treasure_array[2].id)
# print(strawhat.crew_heap.heap[3].treasure_array[0].id,strawhat.crew_heap.heap[3].treasure_array[1].id)
# print(strawhat.crew_heap.heap[4].treasure_array[0].id,strawhat.crew_heap.heap[4].treasure_array[1].id,strawhat.crew_heap.heap[4].treasure_array[2].id)
# #ans (3 7 10),(4 6),(2 9 11),(1 8),(5)


# strawhat=StrawHatTreasury(5)
# t1=treasure.Treasure(1,8,1)
# t2=treasure.Treasure(2,7,2)
# t3=treasure.Treasure(3,4,4)
# t4=treasure.Treasure(4,1,5)
# t5=treasure.Treasure(5,7,6)
# t6=treasure.Treasure(6,12,7)
# t7=treasure.Treasure(7,4,8)
# t8=treasure.Treasure(8,6,9)
# t9=treasure.Treasure(9,3,10)
# t10=treasure.Treasure(10,8,11)
# t11=treasure.Treasure(11,7,12)
# t12=treasure.Treasure(12,4,13)
# strawhat.add_treasure(t1)
# strawhat.add_treasure(t2)
# strawhat.add_treasure(t3)
# strawhat.add_treasure(t4)
# strawhat.add_treasure(t5)
# strawhat.add_treasure(t6)
# strawhat.add_treasure(t7)
# strawhat.add_treasure(t8)
# strawhat.add_treasure(t9)
# strawhat.add_treasure(t10)
# strawhat.add_treasure(t11)
# strawhat.add_treasure(t12)
# processed=strawhat.get_completion_time()
# print('Completion Time:', [(treasure_obj.id, treasure_obj.completion_time) for treasure_obj in processed])

# # ans (3 7 10),(4 6),(2 9 11),(1 8),(5 12)
# print(strawhat.crew_heap.heap[0].treasure_array[0].id,strawhat.crew_heap.heap[0].treasure_array[1].id,strawhat.crew_heap.heap[0].treasure_array[2].id,strawhat.crew_heap.heap[0].treasure_array[3].id,strawhat.crew_heap.heap[0].treasure_array[4].id)
# print(strawhat.crew_heap.heap[1].treasure_array[0].id,strawhat.crew_heap.heap[1].treasure_array[1].id,strawhat.crew_heap.heap[1].treasure_array[2].id,strawhat.crew_heap.heap[1].treasure_array[3].id)
# for i in range(5):
#     #print ids
#     print(strawhat.crew_heap.heap[i].treasure_array)

# print(strawhat.crew_heap.heap[0].treasure_array[0].id,strawhat.crew_heap.heap[0].treasure_array[1].id)
# print(strawhat.crew_heap.heap[1].treasure_array[0].id,strawhat.crew_heap.heap[1].treasure_array[1].id)
# print(strawhat.crew_heap.heap[2].treasure_array[0].id,strawhat.crew_heap.heap[2].treasure_array[1].id,strawhat.crew_heap.heap[2].treasure_array[2].id)
# print(strawhat.crew_heap.heap[3].treasure_array[0].id,strawhat.crew_heap.heap[3].treasure_array[1].id,strawhat.crew_heap.heap[3].treasure_array[2].id)
# print(strawhat.crew_heap.heap[4].treasure_array[0].id,strawhat.crew_heap.heap[4].treasure_array[1].id)


# strawhat=StrawHatTreasury(2)
# # Add 1000 1000000000 1
# # Get
# # Add 1001 2000000000 300000000
# # Get
# # Add 1002 100000000 400000000
# # Get
# # Add 1003 5000000000 600000000
# # Get
# # Add 1004 1200000000 700000000
# # Get
# t1=treasure.Treasure(1000,1000000000,1)
# t2=treasure.Treasure(1001,2000000000,300000000)
# t3=treasure.Treasure(1002,100000000,400000000)
# t4=treasure.Treasure(1003,5000000000,600000000)
# t5=treasure.Treasure(1004,1200000000,700000000)
# strawhat.add_treasure(t1)
# strawhat.add_treasure(t2)
# strawhat.add_treasure(t3)
# strawhat.add_treasure(t4)
# processed=strawhat.get_completion_time()
# print('Completion Time:', [(treasure_obj.id, treasure_obj.completion_time) for treasure_obj in processed])
# strawhat.add_treasure(t5)

# # for i in range(2):
# #     #print ids
# #     print(strawhat.crew_heap.heap[i].treasure_array)

# # print(strawhat.crew_heap.heap[0].treasure_array[0].id,strawhat.crew_heap.heap[0].treasure_array[1].id)
# # print(strawhat.crew_heap.heap[1].treasure_array[0].id,strawhat.crew_heap.heap[1].treasure_array[1].id,strawhat.crew_heap.heap[1].treasure_array[2].id)

# processed=strawhat.get_completion_time()

# # print(strawhat.crew_heap.heap[0].treasure_array[0].id,strawhat.crew_heap.heap[0].treasure_array[1].id)
# # print(strawhat.crew_heap.heap[1].treasure_array[0].id,strawhat.crew_heap.heap[1].treasure_array[1].id,strawhat.crew_heap.heap[1].treasure_array[2].id)
# #Print crew_heap
# # print(strawhat.crew_heap.heap[0].treasure_heap.heap[0].id)
# # print(strawhat.crew_heap.heap[1].treasure_heap.heap[0].id,strawhat.crew_heap.heap[1].treasure_heap.heap[1].id)

# # for i in range(2):
# #     #print ids
# #     print(strawhat.crew_heap.heap[i].treasure_array)

# print('Completion Time:', [(treasure_obj.id, treasure_obj.completion_time) for treasure_obj in processed])

# strawHatTreasury=StrawHatTreasury(3)
# t1=treasure.Treasure(1,8,1)
# t2=treasure.Treasure(2,7,2)
# t3=treasure.Treasure(3,4,4)
# t4=treasure.Treasure(4,1,5)
# t5=treasure.Treasure(5,4,6)
# t6=treasure.Treasure(6,4,7)
# t7=treasure.Treasure(7,5,30)
# t8=treasure.Treasure(8,4,31)
# t9=treasure.Treasure(9,6,32)
# strawHatTreasury.add_treasure(t1)
# strawHatTreasury.add_treasure(t2)
# strawHatTreasury.add_treasure(t3)
# strawHatTreasury.add_treasure(t4)
# strawHatTreasury.add_treasure(t5)
# strawHatTreasury.add_treasure(t6)
# strawHatTreasury.add_treasure(t7)
# strawHatTreasury.add_treasure(t8)
# strawHatTreasury.add_treasure(t9)

# for i in strawHatTreasury.alloted_crewmates:
#     #print ids
#     for j in i.treasure_array:
#         print(j.id)
#     print()
# # # print(strawhat.crew_heap.heap[0].treasure_array[0].id,strawhat.crew_heap.heap[0].treasure_array[1].id)
# # # print(strawhat.crew_heap.heap[1].treasure_array[0].id,strawhat.crew_heap.heap[1].treasure_array[1].id,strawhat.crew_heap.heap[1].treasure_array[2].id)
# processed=strawHatTreasury.get_completion_time()
# print('Completion Time:', [(treasure_obj.id, treasure_obj.completion_time) for treasure_obj in processed])


# strawHatTreasury=StrawHatTreasury(2)

# t1=treasure.Treasure(1,10,1)
# t2=treasure.Treasure(2,5,3)
# t3=treasure.Treasure(3,8,5)
# t4=treasure.Treasure(4,3,7)
# t5=treasure.Treasure(5,6,9)

# strawHatTreasury.add_treasure(t1)
# strawHatTreasury.add_treasure(t2)
# strawHatTreasury.add_treasure(t3)

# processed=strawHatTreasury.get_completion_time()
# print('Completion Time:', [(treasure_obj.id, treasure_obj.completion_time) for treasure_obj in processed])

# strawHatTreasury.add_treasure(t4)
# processed=strawHatTreasury.get_completion_time()
# print('Completion Time:', [(treasure_obj.id, treasure_obj.completion_time) for treasure_obj in processed])

# for i in strawHatTreasury.alloted_crewmates:
#     for j in i.treasure_array:
#         print(j.id)
#     print()

# strawHatTreasury.add_treasure(t5)
# processed=strawHatTreasury.get_completion_time()
# print('Completion Time:', [(treasure_obj.id, treasure_obj.completion_time) for treasure_obj in processed])

# for i in strawHatTreasury.alloted_crewmates:
#     for j in i.treasure_array:
#         print(j.id)
#     print()





# strawHatTreasury=StrawHatTreasury(3)

# t1=treasure.Treasure(10,15,1)
# t2=treasure.Treasure(20,10,2)
# t3=treasure.Treasure(30,5,3)
# t4=treasure.Treasure(40,8,4)
# t5=treasure.Treasure(50,12,5)
# t6=treasure.Treasure(60,6,6)
# t7=treasure.Treasure(70,3,7)

# strawHatTreasury.add_treasure(t1)
# strawHatTreasury.add_treasure(t2)
# strawHatTreasury.add_treasure(t3)

# processed=strawHatTreasury.get_completion_time()
# print('Completion Time:', [(treasure_obj.id, treasure_obj.completion_time) for treasure_obj in processed])

# strawHatTreasury.add_treasure(t4)
# strawHatTreasury.add_treasure(t5)

# processed=strawHatTreasury.get_completion_time()
# print('Completion Time:', [(treasure_obj.id, treasure_obj.completion_time) for treasure_obj in processed])

# strawHatTreasury.add_treasure(t6)

# processed=strawHatTreasury.get_completion_time()
# print('Completion Time:', [(treasure_obj.id, treasure_obj.completion_time) for treasure_obj in processed])

# strawHatTreasury.add_treasure(t7)

# processed=strawHatTreasury.get_completion_time()
# print('Completion Time:', [(treasure_obj.id, treasure_obj.completion_time) for treasure_obj in processed])

# for i in strawHatTreasury.alloted_crewmates:
#     for j in i.treasure_array:
#         print(j.id)
#     print()

