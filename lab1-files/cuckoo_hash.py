# explanations for member functions are provided in requirements.py
# each file that uses a cuckoo hash should import it from this file.
import random as rand
from typing import List

class CuckooHash:
    def __init__(self, init_size: int):
        self.__num_rehashes = 0
        self.CYCLE_THRESHOLD = 10

        self.table_size = init_size
        self.tables = [[None]*init_size for _ in range(2)]
        
        self.current_table = 0
        self.current_evictions = 0



    def hash_func(self, key: int, table_id: int) -> int:
        key = int(str(key) + str(self.__num_rehashes) + str(table_id))
        rand.seed(key)
        return  rand.randint(0, self.table_size-1)

    def get_table_contents(self) -> List[List[int]]:
        return self.tables

    # you should *NOT* change any of the existing code above this line
    # you may however define additional instance variables inside the __init__ method.

    def insert(self, key: int) -> bool:
        # TODO
        """
        use hash function to find key of table 1
        if that slot is filled, then do for table 2 
        this will be in some sort of loop
        at every clash, update the count of evictions needed
        """
        self.current_table = 0 # don't keep previous insertion's leftover current_table
        self.current_evictions = 0 # don't keep previous insertion's leftover eviction count
        while self.current_evictions <= self.CYCLE_THRESHOLD:
            index = self.hash_func(key, self.current_table)
            
            if self.tables[self.current_table][index] is None:
                self.tables[self.current_table][index] = key
                break
            else:
                # there is an eviction required
                # print("Eviction required")
                # exchange the current key with what is being evicted 
                # i.e. place current key in table and extract the stored key and treat it as key to store next
                key, self.tables[self.current_table][index] = self.tables[self.current_table][index], key
                self.current_table = 1 - self.current_table
                self.current_evictions += 1
        
        if self.current_evictions > self.CYCLE_THRESHOLD:
            
            print(f'Cycle detected! {self.current_evictions = }')
            return False
        
        return True
        
        

    def lookup(self, key: int) -> bool:
        # TODO
        if self.tables[0][self.hash_func(key, 0)] == key or self.tables[1][self.hash_func(key, 1)] == key:
            return True
        return False
        

    def delete(self, key: int) -> None:
        # TODO
        # set the key to None
        if self.tables[0][self.hash_func(key, 0)] == key:
            self.tables[0][self.hash_func(key, 0)] = None
        elif self.tables[1][self.hash_func(key, 1)] == key:
            self.tables[1][self.hash_func(key, 1)] = None
        else:
            return False
        return True
        

    def rehash(self, new_table_size: int) -> None:
        self.__num_rehashes += 1; self.table_size = new_table_size # do not modify this line
        # TODO
        old_tables = self.tables.copy()
        self.tables = [[None]*self.table_size for _ in range(2)]
        for table in old_tables:
            for element in table:
                if element is not None:
                    self.insert(element)

    # feel free to define new methods in addition to the above
    # fill in the definitions of each required member function (above),
    # and for any additional member functions you define

