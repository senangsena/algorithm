import random, sys, time

###########################################################################
#                                                                         #
# Implement a hash table from scratch!  (STEP w2 hw1)                                  #
#                                                                         #
# Please do not use Python's dictionary or Python's collections library.  #
# The goal is to implement the data structure yourself.   
# ｂucket.sizeを37にすると97の時の2倍遅くなった。
# bucket.sizeを197にすると97の時の2倍速くなった.
# 97の時、i = 23, 30, 33において900秒を超える実行時間になった（なぜ？） 
# O(n / 6)くらい。再ハッシュは未実装               #
#                                                                         #
###########################################################################

# Hash function.
#
# 'key': string
# Return value: a hash value
def calculate_hash(key):
    assert type(key) == str # 引数は絶対str型
    # Note: This is not a good hash function. Make it better!
    hash = 0
    for i, char in enumerate(key): 
        hash += ord(char)  # iをunicodeに変換
        # "alice"と"elica"のように順番変わっているものを区別するため、
        # 何番目の文字かによってハッシュ値を変える
        if i % 3 == 0:
            hash += i * (ord(char) - 90) 
        elif i % 3 == 1:
            hash += 5 * i * (ord(char) - 90) + i
        else:
            hash -= 3 * i * (ord(char) - 90) + i
        
    
    return hash


# An item object that represents one key - value pair in the hash table.
class Item:
    # 'key': The key of the item. The key must be a string.
    # 'value': The value of the item.
    # 'next': The next item in the linked list. If this is the last item in the
    #         linked list, 'next' is None.
    def __init__(self, key, value, next):
        assert type(key) == str
        self.key = key
        self.value = value
        self.next = next


# The main data structure of the hash table that stores key - value pairs.
# The key must be a string. The value can be any type.
#
# 'self.bucket_size': The bucket size.
# 'self.buckets': An array of the buckets. self.buckets[hash % self.bucket_size]
#                 stores a linked list of items whose hash value is 'hash'.
# 'self.item_count': The total number of items in the hash table.
class HashTable:

    # Initialize the hash table.
    def __init__(self):
        # Set the initial bucket size to 97. A prime number is chosen to reduce
        # hash conflicts.
        self.bucket_size = 197
        self.buckets = [None] * self.bucket_size
        self.item_count = 0 

    # Put an item to the hash table. If the key already exists, the
    # corresponding value is updated to a new value.
    #
    # 'key': The key of the item.
    # 'value': The value of the item.
    # Return value: True if a new item is added. False if the key already exists
    #               and the value is updated.
    def put(self, key, value):
        assert type(key) == str
        #------------------------#
        # Write your code here!  #
        hash_value = calculate_hash(key) # 入れたいkeyのハッシュ値の計算
        hash_per_size = hash_value % self.bucket_size

        if self.buckets[hash_per_size] == None: # 入れたい枠が空の時はそのまま入れる
            self.buckets[hash_per_size] = Item(key, value, None)
            
        else: # もうすでに何かしらのデータ入っている時
            cur_item = self.buckets[hash_per_size] # 今見てるItem
            find = False
            while(not find):
                if cur_item.key == key: # キーがすでに存在する時、バリューを更新しFalseを返す
                    cur_item.value = value
                    return False
                
                if cur_item.next == None: # 結合リストの最後が見つかる
                    find = True
                else:
                    cur_item = cur_item.next

            cur_item.next = Item(key, value, None)

        self.item_count += 1
        #------------------------#
        return True


    # Get an item from the hash table.
    #
    # 'key': The key.
    # Return value: If the item is found, return (the value of the item, True).
    #               Otherwise, return (None, False).
    def get(self, key):
        assert type(key) == str
        #------------------------#
        # Write your code here!  #
        hash_value = calculate_hash(key) # ハッシュ値を計算
        hash_per_size = hash_value % self.bucket_size ##このselfは、hash_tableのこと？HashTableのインスタンスが一つだけだからselfで書けるという認識で合っているか
        
        cur_item = self.buckets[hash_per_size]

        if(cur_item): # cur_itemがNoneなら飛ばされる
            while(cur_item.next != None): # 結合リストの最後まで探す
                if cur_item.key == key:
                    return (cur_item.value, True)
                else:
                    cur_item = cur_item.next    

            if cur_item.next == None:
                if cur_item.key == key:
                    return (cur_item.value, True)
        #------------------------#
        return (None, False)

    # Delete an item from the hash table.
    #
    # 'key': The key.
    # Return value: True if the item is found and deleted successfully. False
    #               otherwise.
    def delete(self, key):
        assert type(key) == str
        #------------------------#
        # Write your code here! 
        if self.get(key) == (None, False): # keyが存在しない時、False
            return False
        
        hash_value = calculate_hash(key) # ハッシュ値を計算
        hash_per_size = hash_value % self.bucket_size 

        cur_item = self.buckets[hash_per_size] #今見てるItem
        
        # self.get(key)で、keyがあること確認してるのでif(cur_item)は要らない

        if cur_item.next == None: # 枠内にItem一つのみの時
            if cur_item.key == key:
                self.buckets[hash_per_size] = None
            else:
                return False  
        else:
            # 削除する際は、cur_itemの一個前のItem情報も必要。

            if cur_item.key == key: # リストの先頭が削除の対象の時
                self.buckets[hash_per_size] = cur_item.next
                
            else:
                while(cur_item.next.next != None): # 結合リストの最後まで探す
                    if cur_item.next.key == key: # cur_itemの次のItemを常に調べる
                        cur_item.next = cur_item.next.next # 削除したいものを飛ばす形で結合をし直す
                    else:
                        cur_item = cur_item.next

                if cur_item.next.next == None:
                    if cur_item.next.key == key: #結合リスト末尾のキーを削除するとき、その前のItemのnextをNoneにする。
                        cur_item.next = None    

        self.item_count -= 1
        return True
        #------------------------#
        pass ##この意味

    # Return the total number of items in the hash table.
    def size(self):
        return self.item_count


# Check that the hash table has a "reasonable" bucket size.
# The bucket size is judged "reasonable" if it is smaller than 100 or
# the buckets are 30% or more used.
#
# Note: Don't change this function.
def check_size(item_count, bucket_size):
    assert (bucket_size < 100 or item_count >= bucket_size * 0.3)


# Test the functional behavior of the hash table.
def functional_test():
    hash_table = HashTable()

    assert hash_table.put("aaa", 1) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.size() == 1

    assert hash_table.put("bbb", 2) == True
    assert hash_table.put("ccc", 3) == True
    assert hash_table.put("ddd", 4) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.get("bbb") == (2, True)
    assert hash_table.get("ccc") == (3, True)
    assert hash_table.get("ddd") == (4, True)
    assert hash_table.get("a") == (None, False)
    assert hash_table.get("aa") == (None, False)
    assert hash_table.get("aaaa") == (None, False)
    assert hash_table.size() == 4

    assert hash_table.put("aaa", 11) == False
    assert hash_table.get("aaa") == (11, True)
    assert hash_table.size() == 4

    assert hash_table.delete("aaa") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.size() == 3

    assert hash_table.delete("a") == False
    assert hash_table.delete("aa") == False
    assert hash_table.delete("aaa") == False
    assert hash_table.delete("aaaa") == False

    assert hash_table.delete("ddd") == True
    assert hash_table.delete("ccc") == True
    assert hash_table.delete("bbb") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.get("bbb") == (None, False)
    assert hash_table.get("ccc") == (None, False)
    assert hash_table.get("ddd") == (None, False)
    assert hash_table.size() == 0

    assert hash_table.put("abc", 1) == True
    assert hash_table.put("acb", 2) == True
    assert hash_table.put("bac", 3) == True
    assert hash_table.put("bca", 4) == True
    assert hash_table.put("cab", 5) == True
    assert hash_table.put("cba", 6) == True

    assert hash_table.get("abc") == (1, True)
    assert hash_table.get("acb") == (2, True)
    assert hash_table.get("bac") == (3, True)
    assert hash_table.get("bca") == (4, True)
    assert hash_table.get("cab") == (5, True)
    assert hash_table.get("cba") == (6, True)

    assert hash_table.size() == 6

    assert hash_table.delete("abc") == True
    assert hash_table.delete("cba") == True
    assert hash_table.delete("bac") == True
    assert hash_table.delete("bca") == True
    assert hash_table.delete("acb") == True
    assert hash_table.delete("cab") == True
    assert hash_table.size() == 0

    # Test the rehashing.
    for i in range(100):
        hash_table.put(str(i), str(i))
    for i in range(100):
        assert hash_table.get(str(i)) == (str(i), True)
    for i in range(100):
        assert hash_table.delete(str(i)) == True
    hash_table.put("abc", 1)
    hash_table.put("acb", 2)
    assert hash_table.get("abc") == (1, True)
    assert hash_table.get("acb") == (2, True)
    print("Functional tests passed!")


# Test the performance of the hash table.
#
# Your goal is to make the hash table work with mostly O(1).
# If the hash table works with mostly O(1), the execution time of each iteration
# should not depend on the number of items in the hash table. To achieve the
# goal, you will need to 1) implement rehashing (Hint: expand / shrink the hash
# table when the number of items in the hash table hits some threshold) and
# 2) tweak the hash function (Hint: think about ways to reduce hash conflicts).
def performance_test():
    hash_table = HashTable()

    for iteration in range(100):
        begin = time.time()
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.put(str(rand), str(rand))
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.get(str(rand))
        end = time.time()
        print("%d %.6f" % (iteration, end - begin))

    for iteration in range(100):
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.delete(str(rand))

    assert hash_table.size() == 0
    print("Performance tests passed!")


if __name__ == "__main__":
    functional_test()
    performance_test()