# Devika Prasanth
# 010101895

# Hash Map
# Code derived from (Tepe, Lets Get Hashing, 2020 WGU) educational material
# HashTable class using chaining.
class ChainingHashTable:
    # Constructor with optional initial capacity parameter.
    # Assigns all buckets with an empty list for chaining
    def __init__(self, initial_capacity=40):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Computes the bucket index for given key with hash function
    def _get_bucket(self, key):
        return hash(key) % len(self.table)

    # Add a new key-value pair into has table/updates value if key already exists
    def insert(self, key, item):  # does both insert and update
        # get the bucket list where this item will go.
        bucket = self._get_bucket(key)
        bucket_list = self.table[bucket]
        # Check if key exists. Update key if it is already in the bucket
        for kv in bucket_list:
            # print (key_value)
            if kv[0] == key:
                kv[1] = item
                return True
        # Key does not already exist. Append new key-value pair
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Searches for an item with matching key in the hash table.
    # Returns the item if found, or None if not found.
    def search(self, key):
        # get the bucket list where this key would be.
        bucket = self._get_bucket(key)
        bucket_list = self.table[bucket]
        # search for the key in the bucket list
        for kv in bucket_list:
            # print (key_value)
            if kv[0] == key:
                return kv[1]  # Return the value
        return None

    # Removes a key-value pair from the hash table.
    # Return True if successfully removed, or False if key not found.
    def remove(self, key):
        # get the bucket list where this item will be removed from.
        bucket = self._get_bucket(key)
        bucket_list = self.table[bucket]
        # remove the item from the bucket list if it is present.
        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove([kv[0], kv[1]])
                return True
        return False


