# 宿題1
# 入力：文字列　出力：words.txtの中から見つかったアナグラム全部
import re

with open("test_new.txt", "r", encoding= "utf-8") as file:
    word_dic = file.read().splitlines()
    new_dictionary = []
    new_dictionary_orig = []
    for s in word_dic:
        match = re.search(r"{'([^']*)'\s*:\s*'([^']*)'}", s)
        if match:
            new_dictionary.append(match.group(1))
            new_dictionary_orig.append(match.group(2))

    len_dict = len(new_dictionary)

print(new_dictionary)
print(new_dictionary_orig)


# print(word_sort("daceb"))
# print(dictionary)
#print(make_sorted_dict(dictionary))

#main
print("Input word:")
input = input()
len_input = len(input)
if len_input == 0:
    print("Input word:")
list_input = list(input)
list_input.sort()
sorted_input = "".join(list_input)


# 二分探索で探す
find = False # 完全一致するものを見つける
start = 0
end = len_dict -1
print("start search")
target_i = int((start + end) / 2)

while(not find):
    target = new_dictionary[target_i]
    print(f"target = {target}")

    for i in range(min(len(target), len_input)): # 先頭から、各文字ごとに見る
        if target[i] < sorted_input[i]:
            start = target_i + 1
            target_i = int((start + end) / 2)
            print(f"start = {start}, end = {end}, tar = {target}")
            break # forから出る

        elif target[i] > sorted_input[i]:
            end = target_i - 1
            target_i = int((start + end) / 2)
            print(2)
            break
        elif i == min(len(target), len_input) - 1:
            if len(target) == len_input:
                print(3)
                answer = new_dictionary_orig[target_i]
                find = True
            elif len(target) < len_input: # inputはtargetより後ろ   
                start = target_i + 1
                target_i = int((start + end) / 2)
                print(4)
                break
            else:
                end = target_i - 1
                target_i = int((start + end) / 2)

                print(5)
                break
    


print(answer)
                

    