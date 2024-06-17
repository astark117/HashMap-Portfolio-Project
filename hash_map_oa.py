# Name: Anthony Stark
# OSU Email: starkan@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - Hashmap
# Due Date: 6/6/2024
# Description: Implements a hashmap, handling collisions using quadratic open addressing. Load factor is calculated via
#              a method and the table uses this to automatically resize if the load factor >= 0.5.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Adds a key-value pair to the hash map. If the key already exists, it replaces the value.
        """
        # Check the load factor and resize if necessary
        if self.table_load() >= 0.5:
            self.resize_table(2 * self._capacity)

        # calculates quadratic index and probes for element
        index_initial = self.get_index(key)
        for j in range(self._capacity):
            index = (index_initial + j ** 2) % self._capacity
            current_bucket = self._buckets[index]
            # if key is not found in the hashmap
            if current_bucket is None or current_bucket.is_tombstone:
                self._buckets[index] = HashEntry(key, value)
                self._size += 1
                return
            # updates value if key is found
            elif current_bucket.key == key:
                self._buckets[index].value = value
                return

    def get_index(self, key: str) -> int:
        """
        Takes a key as a parameter and returns the corresponding index.
        """
        index = self._hash_function(key) % self._capacity
        return index

    def resize_table(self, new_capacity: int) -> None:
        """
        Increases the capacity of the array.
        """
        # checks if new capacity is valid
        if new_capacity < self._size:
            return
        # updates new_capacity to next prime number if it is not already prime
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # initializes an empty array of size new_capacity
        old_buckets = self._buckets
        self._buckets = DynamicArray()
        for _ in range(new_capacity):
            self._buckets.append(None)
        self._capacity = new_capacity
        self._size = 0

        # copies over non-tombstone values to new table
        for i in range(old_buckets.length()):
            current_entry = old_buckets[i]
            if current_entry is not None and current_entry.is_tombstone is False:
                self.put(current_entry.key, current_entry.value)

    def table_load(self) -> float:
        """
        Calculates and returns the load factor of the hashmap.
        """
        load_factor = self._size / self._capacity
        return load_factor

    def empty_buckets(self) -> int:
        """
        Returns number of empty buckets in the hash table.
        """
        empties = self._capacity - self._size
        return empties

    def get(self, key: str) -> object:
        """
        Returns value of key-value pair to the corresponding key parameter, if key is not found returns None.
        """
        index_initial = self.get_index(key)
        # quadratic probing for key
        for j in range(self._capacity):
            index = (index_initial + j ** 2) % self._capacity
            current_bucket = self._buckets[index]
            # if key is not found
            if current_bucket is None:
                return None
            # if key is found but has been removed
            elif current_bucket.key == key and current_bucket.is_tombstone is True:
                return None
            # if key is found
            elif current_bucket.key == key and current_bucket.is_tombstone is False:
                return current_bucket.value

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the key is found in the hashmap. Returns False if not.
        """
        index_initial = self.get_index(key)
        # quadratic probing for the key
        for j in range(self._capacity):
            index = (index_initial + j ** 2) % self._capacity
            current_bucket = self._buckets[index]
            # if key is not found
            if current_bucket is None:
                return False
            # if key is found but has been removed
            elif current_bucket.key == key and current_bucket.is_tombstone is True:
                return False
            # if key is found
            elif current_bucket.key == key and current_bucket.is_tombstone is False:
                return True

    def remove(self, key: str) -> None:
        """
        Removes the key and its value from the hashmap.
        """
        index_initial = self.get_index(key)
        # quadratic probing for the key
        for j in range(self._capacity):
            index = (index_initial + j ** 2) % self._capacity
            current_bucket = self._buckets[index]
            # if key is not found
            if current_bucket is None:
                return
            # if key is found and tombstone is False
            elif current_bucket.key == key and current_bucket.is_tombstone is False:
                current_bucket.is_tombstone = True
                self._size -= 1
                return

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns an array of key-value pair tuples for each element in hashmap.
        """
        new_array = DynamicArray()
        for i in range(self._capacity):
            current = self._buckets[i]
            if current is not None and current.is_tombstone is False:
                new_array.append((current.key, current.value))
        return new_array

    def clear(self) -> None:
        """
        Clears the hashmap, keeping the capacity the same.
        """
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

    def get_bucket(self, index) -> object:
        """
        Returns a bucket from the hashmap based on its index in the dynamic array
        """
        if 0 <= index < self._capacity:
            return self._buckets[index]

    def __iter__(self):
        return HashMapIterator(self)


class HashMapIterator:
    def __init__(self, hashmap):
        """
        Initializes a hashmap iterator class
        """
        self._current_index = 0
        self._hashmap = hashmap

    def __iter__(self):
        """
        Creates an iterator for loop
        """
        return self

    def __next__(self):
        """
        Advances iterator and obtains next value
        """
        if self._current_index >= self._hashmap.get_capacity():
            raise StopIteration
        current_bucket = self._hashmap.get_bucket(self._current_index)
        self._current_index += 1
        if current_bucket is not None and current_bucket.is_tombstone is False:
            return current_bucket
        else:
            raise StopIteration





# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
