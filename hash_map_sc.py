# Name: Anthony Stark
# OSU Email: starkan@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - Hashmap
# Due Date: 6/6/2024
# Description: Implements a hashmap, handling collisions by chaining via linked lists. Load factor is calculated via a
#              method and the table uses this to automatically resize if the load factor >= 1.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        if self.table_load() >= 1.0:
            self.resize_table(2 * self._capacity)

        # Finds the bucket that matches the key
        index = self.get_index(key)
        bucket = self._buckets[index]

        # Check if the key already exists in the bucket
        node = bucket.contains(key)
        if node is not None:
            # If key exists, update the value
            node.value = value
        else:
            # If key does not exist, insert new key-value pair and increment size
            bucket.insert(key, value)
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Increases the capacity of the array.
        """
        # checks that new_capacity is valid
        if new_capacity < 1:
            return
        # updates new_capacity to next prime number if it is not already prime
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # creates an array of empty buckets of size new_capacity
        old_buckets = self._buckets
        self._buckets = DynamicArray()
        for _ in range(new_capacity):
            self._buckets.append(LinkedList())
        self._capacity = new_capacity
        self._size = 0

        # copies key-value pairs from old_buckets to new array
        for i in range(old_buckets.length()):
            current_bucket = old_buckets[i]
            for element in current_bucket:
                self.put(element.key, element.value)

    def table_load(self) -> float:
        """
        Calculates and returns the load factor.
        """
        load_factor = self._size / self._capacity
        return load_factor

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the array.
        """
        empties = 0
        for i in range(self._capacity):
            if self._buckets[i].length() == 0:
                empties += 1
        return empties

    def get(self, key: str):
        """
        Returns the value of the key in the hashmap. If the key is not in the hashmap, returns None.
        """
        if self.contains_key(key) is False:
            return None
        index = self.get_index(key)
        bucket = self._buckets[index]
        for element in bucket:
            if element.key == key:
                return element.value
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the key is in the hash map. Returns False if it is not.
        """
        index = self.get_index(key)
        for i in range(self._capacity):
            if self._buckets[i] == self._buckets[index] and self._buckets[i].contains(key):
                return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes a key-value pair from the hashmap if the key matches the parameter.
        """
        if self.contains_key(key) is False:
            return
        index = self.get_index(key)
        bucket = self._buckets[index]
        bucket.remove(key)
        self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array of tuples containing the key and value for each element stored in the hashmap
        """
        new_array = DynamicArray()
        for i in range(self._capacity):
            current_bucket = self._buckets[i]
            for element in current_bucket:
                new_array.append((element.key, element.value))
        return new_array

    def clear(self) -> None:
        """
        Clears the hashmap, keeping the capacity the same.
        """
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())
        self._size = 0

    def get_index(self, key: str) -> int:
        """
        Returns the integer index of a given key.
        """
        index = self._hash_function(key) % self._capacity
        return index
def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Takes an unsorted dynamic array as a parameter and returns a tuple of the most frequently occuring values,
    along with their frequency in the array.
    """
    map = HashMap()

    max_frequency = 0
    mode_array = DynamicArray()

    # iterates through da and checks if the value has been added to map
    for i in range(da.length()):
        value = da[i]
        frequency = map.get(value)
        # if the value is not in map, it adds it with a frequency of 1
        if frequency is None:
            map.put(value, 1)
            frequency = 1
        # if it's already in map, it increments the frequency
        else:
            map.put(value, frequency + 1)
            frequency += 1

        # Resets mode_array if a new mode is found and adds the value, updates max_frequency for new mode
        if frequency > max_frequency:
            max_frequency = frequency
            mode_array = DynamicArray()
            mode_array.append(value)
        # adds another value if there is more than one mode
        elif frequency == max_frequency:
            mode_array.append(value)

    return mode_array, max_frequency


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
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
