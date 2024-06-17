# HashMap-Portfolio-Project

A portfolio project for my data structures course (CS261) implementing a hashmap from scratch using both chaining and open addressing to handle collisions. Data is stored and retrieved in O(1) time.

hashmap_oa.py utilizes quadratic probing (open addressing) to handle collisions. Load factor is calculated via a method and the table uses this to automatically resize if the load factor >= 0.5.

hashmap_sc.py utilizes chaining via linked lists to handle collisions. Load factor is calculated via a method and the table uses this to automatically resize if the load factor >= 1.

a6_include.py was provided as skeleton code and contains the classes for underlying data structures and iterators.

Methods implemented include:
put(key, value) = inserts a key-value pair into the hash table
get_index(key) = calculates the index for a key using the hash function
empty_buckets() = returns the number of empty buckets in the hash table
contains(key) = returns True if the key is found in the hash table, False if not
remove(key) = removes a key-value pair from the hash table
get_keys_and_values() = returns a dynamic array of key-value pairs as tuples
clear() = removes all values from the hash table, keeping capacity the same
table_load() = calculates and returns the table load for the hash table
find_mode() = only for the chaining implementation, returns the most frequently occuring value(s) and their frequency
HashMapIterator() = only for the open addressing implementation, an iterator for elmeents in the hash table
