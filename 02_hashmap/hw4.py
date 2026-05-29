import random, sys
import hash_table # Use the hash table you implemented in Homework #2

###########################################################################
#                                                                         #
# Implement a cache that stores the most recently accessed items from     #
# scratch!     
# 一旦、ハッシュテーブル使わずにO(n)で実装してみる.                                                        #
#                                                                         #
# Please do not use Python's dictionary or Python's collections library.  #
# The goal is to implement the data structure yourself.                   #
#                                                                         #
###########################################################################

class Page:
    def __init__(self, url, contents):
        # URL
        self.url = url
        # The contents of the URL
        self.contents = contents
        # Previous page
        self.prev = None
        # Next page
        self.next = None

        
class Cache:
    # Initialize the cache.
    # 'limit': The size limit of the cache.
    def __init__(self, limit):
        assert(limit >= 1)
        self.limit = limit
        self.hit_count = 0 # Increment on a cache hit
        self.miss_count = 0 # Increment on a cache miss
        #------------------------#
        # Write your code here!  #
        self.first_page = None # もっとも最近アクセスされたページ
        self.page_num = 0 # 今入っているページの数
        #------------------------#
        pass

    # Access a page and update the cache so that it stores the most recently
    # accessed pages up to the 'limit'. This needs to be done with mostly O(1).
    # 'url': The accessed URL
    # 'contents': The contents of the URL
    def access_page(self, url, contents):
        #------------------------#
        # Write your code here!  #

        # まずはすでにキャッシュの中に入っているかを調べる。
        cur_page = self.first_page
        find = False
        while(cur_page):
            if cur_page.url == url: # url見つかったら、それを先頭に持ってくる
                # もうすでに先頭にある時、何もしない
                if cur_page == self.first_page:
                    find = True
                    break
                else: #そうでない時、page.prevがNoneでない時、そのpageを先頭に持ってくる。
                    # print(f"first page = {self.first_page.url}, pages = {self.get_pages()}")
                    # print(f"cur_page.prev = {cur_page.prev.url}, cur = {cur_page.url}")

                    prev_page = cur_page.prev 
                    next_page = cur_page.next
                    first_page = self.first_page 
                    prev_page.next = next_page # 途切れた部分を繋ぎ直す
                    if(next_page):
                        next_page.prev = prev_page # これがなかったのが途中うまくいかなかった原因
                    cur_page.prev = None
                    cur_page.next = first_page # 元々のfirst_pageは、２番目になる
                    first_page.prev = cur_page
                    self.first_page = cur_page
                    # print(f"[after]first page = {self.first_page.url}, pages = {self.get_pages()}")

    
                    self.hit_count += 1
                    find = True
                    break
            cur_page = cur_page.next
        
        if not find: #キャッシュの中になかったとき、先頭に付け加える
            new_page = Page(url, contents) # 新しくPageインスタンスを作成
            
            if self.first_page == None: #空の時
                self.first_page = new_page
                self.page_num += 1
            else:

                old_new = self.first_page
                new_page.next = old_new #new -- oldnewを繋ぐ
                old_new.prev = new_page
                self.first_page = new_page # 先頭を書き換え


                if self.page_num == self.limit: #キャッシュに限界まで入っている時、末端を消す。
                    last_page = self.first_page    

                    while(last_page.next != None): ## pageを末端まで進めて削除. Pageそのものを削除する方法がわからず、Noneにすることで削除を表している
                        last_page = last_page.next
                        

                    
                    prev = last_page.prev
                   
                    prev.next = None
                    last_page = None

                    


                else: # そうでない時、Page数を更新するだけ
                    self.page_num += 1

            self.miss_count += 1

        #------------------------#
        pass

    # Return the URLs stored in the cache. The URLs are ordered in the order
    # in which the URLs are mostly recently accessed.
    def get_pages(self):
        #------------------------#
        # Write your code here!  #

        urls = []
        cur_page = self.first_page
        while(cur_page != None): #削除したものがNoneになって出力されるのでそれは含めない（例：['e.com', 'a.com', 'c.com', 'd.com', None]）
            urls.append(cur_page.url)
            cur_page = cur_page.next
        
        return urls
        #------------------------#
        pass


    # Return the cache hit rate.
    def get_hitrate(self):
        total = self.hit_count + self.miss_count
        return self.hit_count / total if total > 0 else 0

    
def cache_test():
    # Set the size of the cache to 4.
    cache = Cache(4)

    # Initially, no page is cached.
    assert cache.get_pages() == []

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # "a.com" is cached.
    assert cache.get_pages() == ["a.com"]

    # Access "b.com".
    cache.access_page("b.com", "BBB")
    # The cache is updated to:
    #   (new)<-- "b.com", "a.com" -->(old)
    assert cache.get_pages() == ["b.com", "a.com"]

    # Access "c.com".
    cache.access_page("c.com", "CCC")
    # The cache is updated to:
    #   (new)<-- "c.com", "b.com", "a.com" -->(old)
    assert cache.get_pages() == ["c.com", "b.com", "a.com"]

    # Access "d.com".
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (new)<-- "d.com", "c.com", "b.com", "a.com" -->(old)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "d.com" again.
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (new)<-- "d.com", "c.com", "b.com", "a.com" -->(old)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "a.com" again.
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (new)<-- "a.com", "d.com", "c.com", "b.com" -->(old)
    assert cache.get_pages() == ["a.com", "d.com", "c.com", "b.com"]

    cache.access_page("c.com", "CCC")
    assert cache.get_pages() == ["c.com", "a.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is full, so we remove the least recently accessed page "b.com".
    # The cache is updated to:
    #   (new)<-- "e.com", "a.com", "c.com", "d.com" -->(old)
    assert cache.get_pages() == ["e.com", "a.com", "c.com", "d.com"]

    # Access "f.com".
    cache.access_page("f.com", "FFF")
    # The cache is full, so we remove the least recently accessed page "c.com".
    # The cache is updated to:
    #   (new)<-- "f.com", "e.com", "a.com", "c.com" -->(old)
    assert cache.get_pages() == ["f.com", "e.com", "a.com", "c.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is updated to:
    #   (new)<-- "e.com", "f.com", "a.com", "c.com" -->(old)
    assert cache.get_pages() == ["e.com", "f.com", "a.com", "c.com"]

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (new)<-- "a.com", "e.com", "f.com", "c.com" -->(old)
    assert cache.get_pages() == ["a.com", "e.com", "f.com", "c.com"]

    print("Tests passed!")


def performance_test():
    # Set the size of the cache to 100.
    cache = Cache(150)

    # Generate queries based on the Zipf law.
    ALPHA = 1.5
    NUM_QUERIES = 1000000
    NUM_PAGES = 1000
    ranks = range(1, NUM_PAGES + 1)
    weights = [1.0 / (r ** ALPHA) for r in ranks]
    random.seed(1)
    queries = random.choices(ranks, weights=weights, k=NUM_QUERIES)    
    for query in queries:
        cache.access_page(str(query), "")

    # If your cache implementation is correct, the hit rate will be 91%.
    print("Cache hit rate = %d %%" % (cache.get_hitrate() * 100))
    print("Performance tests passed!")


if __name__ == "__main__":
    cache_test()
    performance_test()