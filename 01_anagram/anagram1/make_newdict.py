# まずwords.txt（もとの辞書）の各単語の文字をソートして、並べ直す
# 関数書く順番

with open("words.txt", "r", encoding= "utf-8") as file:
    dictionary = file.read().splitlines()

# 単語を文字単位でソートする関数。（練習用、実際には.sortを使用）
def word_sort(word):
    word_list = list(word)
    sort = False
    
    while(not sort):
        tmp_sort = True # 先頭から最後まで一度もひっくり返さなければTrue
        for i in range(len(word) - 1):
            if word_list[i] > word_list[i + 1]:
                tmp = word_list[i]
                word_list[i] = word_list[i + 1]
                word_list[i + 1] = tmp
                tmp_sort = False
        
        if(tmp_sort): #一度もひっくり返さず最後まで終われば、完了。sort, tmp_sort２個じゃなくて一つの変数のみで書けない？
            sort = True
            
            
    return "".join(word_list)


def make_sorted_dict(orig_dictionary):
    new_dictionary = []
    for word in orig_dictionary:
        list_word = list(word)
        list_word.sort()
        w = "".join(list_word)
        new_dictionary.append({w : word}) #元の単語を忘れないように
        new_dictionary.sort(key=lambda d: list(d.keys())[0])

    return new_dictionary


new_dictionary = make_sorted_dict(dictionary)


with open("new_dictionary.txt", "w", encoding="utf-8") as file:
    for word in new_dictionary:
        file.write(f"{word}\n")

# print(word_sort("daceb"))
# print(dictionary)
#print(make_sorted_dict(dictionary))
