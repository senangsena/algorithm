import random, sys, time

###########################################################################
#                                                                         #
# テスト用コード。メインのコードはhash_table.py
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
    len_key = len(key)
    for i, char in enumerate(key): 
        hash += ord(char)  # iをunicodeに変換
        # "alice"と"elica"のように順番変わっているものを区別するため、
        
        # 何番目の文字かによってハッシュ値を変える
        if i % 3 == 0:
            hash += 7 * i * (ord(char) - 90)
        elif i % 3 == 1:
            hash += 5 * i * (ord(char) - 90)
        else:
            hash -= 3 * i * (ord(char) - 90)
    
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
        self.bucket_size = 97
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

if __name__ == "__main__":
    print(calculate_hash("abc"))
    print(calculate_hash("acb"))
    print(calculate_hash("bac"))
    print(calculate_hash("bca"))
    print(calculate_hash("cab"))
    print(calculate_hash("cba"))

    hash_table = HashTable()


    print(hash_table.put("abc", 1)) #== True
    print(hash_table.put("acb", 2)) #== True
    print(hash_table.put("bac", 3)) #== True
    print(hash_table.put("bca", 4)) #== True
    print(hash_table.put("cab", 5)) #== True
    print(hash_table.put("cba", 6)) #== True
    
    print(hash_table.get("abc")) #== (1, True)
    print(hash_table.get("acb")) #== (2, True)
    print(hash_table.get("bac")) #== (3, True)
    print(hash_table.get("bca")) #== (4, True)
    print(hash_table.get("cab")) #== (5, True)
    print(hash_table.get("cba")) #== (6, True)

    print(hash_table.size()) #== 6

    print(hash_table.delete("abc")) #== True
    print(hash_table.delete("cba")) #== True

    print(hash_table.delete("bac")) #== True F
    print(hash_table.delete("bca")) #== True F
    print(hash_table.delete("acb")) #== True
    print(hash_table.delete("cab")) #== True F
    print(hash_table.size()) #== 0
