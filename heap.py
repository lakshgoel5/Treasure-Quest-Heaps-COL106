'''
Python Code to implement a heap with general comparison function
'''

class Heap:
    '''
    Class to implement a heap with general comparison function
    '''
    
    def __init__(self, comparison_function, init_array):
        '''
        Arguments:
            comparison_function : function : A function that takes in two arguments and returns a boolean value
            init_array : List[Any] : The initial array to be inserted into the heap
        Returns:
            None
        Description:
            Initializes a heap with a comparison function
            Details of Comparison Function:
                The comparison function should take in two arguments and return a boolean value
                If the comparison function returns True, it means that the first argument is to be considered smaller than the second argument
                If the comparison function returns False, it means that the first argument is to be considered greater than or equal to the second argument
        Time Complexity:
            O(n) where n is the number of elements in init_array
        '''
        
        # Write your code here
        self.comparison_function = comparison_function  # Store the comparison function
        self.heap = init_array[:]  # Create a copy of the initial array

        # Build the heap using a bottom-up approach
        n = len(self.heap)
        for i in reversed(range(n // 2)):
            self._heapify_down(i)
        
    def insert(self, value):
        '''
        Arguments:
            value : Any : The value to be inserted into the heap
        Returns:
            None
        Description:
            Inserts a value into the heap
        Time Complexity:
            O(log(n)) where n is the number of elements currently in the heap
        '''
        
        # Write your code here
        self.heap.append(value)  # Add value to the end
        self._heapify_up(len(self.heap) - 1)  # Restore heap property by bubbling up

    def insert_new(self, value,time):
        '''
        Arguments:
            value : Any : The value to be inserted into the heap
        Returns:
            None
        Description:
            Inserts a value into the heap
        Time Complexity:
            O(log(n)) where n is the number of elements currently in the heap
        '''
        
        # Write your code here
        self.heap.append(value)  # Add value to the end
        self._heapify_up_new(len(self.heap) - 1,time)  # Restore heap property by bubbling up

    def _heapify_up_new(self, index,time):
        '''Maintains the heap property by shifting up an element'''
        parent = self._parent(index)
        
        if parent is not None and self.comparison_function(self.heap[index], self.heap[parent],time):
            # Swap with parent if current element is smaller
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self._heapify_up_new(parent, time)
    
    def extract(self):
        '''
        Arguments:
            None
        Returns:
            Any : The value extracted from the top of heap
        Description:
            Extracts the value from the top of heap, i.e. removes it from heap
        Time Complexity:
            O(log(n)) where n is the number of elements currently in the heap
        '''
        
        # Write your code here
        if not self.heap:
            raise IndexError("Extract from an empty heap")
        
        top_value = self.heap[0]  # Get the top value (root)
        last_value = self.heap.pop()  # Remove the last element
        
        if self.heap:
            self.heap[0] = last_value  # Move the last element to the root
            self._heapify_down(0)  # Restore heap property by bubbling down
        
        return top_value
    
    def extract_new(self,time):
        '''
        Arguments:
            None
        Returns:
            Any : The value extracted from the top of heap
        Description:
            Extracts the value from the top of heap, i.e. removes it from heap
        Time Complexity:
            O(log(n)) where n is the number of elements currently in the heap
        '''
        
        # Write your code here
        if not self.heap:
            raise IndexError("Extract from an empty heap")
        
        top_value = self.heap[0]  # Get the top value (root)
        last_value = self.heap.pop()  # Remove the last element
        
        if self.heap:
            self.heap[0] = last_value  # Move the last element to the root
            self._heapify_down_new(0,time)  # Restore heap property by bubbling down
        
        return top_value
    
    def _heapify_down_new(self, index,time):
        '''Maintains the heap property by shifting down an element'''
        left = 2 * index + 1
        right = 2 * index + 2
        smallest = index
        
        # Compare left child
        if left < len(self.heap) and self.comparison_function(self.heap[left], self.heap[smallest],time):
            smallest = left
        
        # Compare right child
        if right < len(self.heap) and self.comparison_function(self.heap[right], self.heap[smallest],time):
            smallest = right
        
        # Swap and continue heapifying down if necessary
        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down_new(smallest,time)
    
    def top(self):
        '''
        Arguments:
            None
        Returns:
            Any : The value at the top of heap
        Description:
            Returns the value at the top of heap
        Time Complexity:
            O(1)
        '''
        
        # Write your code here
        if not self.heap:
            raise IndexError("Top from an empty heap")
        return self.heap[0]
    
    # You can add more functions if you want to

    def _parent(self, index):
        '''Returns the parent index of a given index'''
        return (index - 1) // 2 if index > 0 else None


    def _heapify_down(self, index):
        '''Maintains the heap property by shifting down an element'''
        left = 2 * index + 1
        right = 2 * index + 2
        smallest = index
        
        # Compare left child
        if left < len(self.heap) and self.comparison_function(self.heap[left], self.heap[smallest]):
            smallest = left
        
        # Compare right child
        if right < len(self.heap) and self.comparison_function(self.heap[right], self.heap[smallest]):
            smallest = right
        
        # Swap and continue heapifying down if necessary
        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)

    def _heapify_up(self, index):
        '''Maintains the heap property by shifting up an element'''
        
        parent = self._parent(index)
        
        if parent is not None and self.comparison_function(self.heap[index], self.heap[parent]):
            # Swap with parent if current element is smaller
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self._heapify_up(parent)
