# 綺麗なブロッコリー列を作るのに必要な作業回数を返すプログラム　O(n)

def gw_checker(text: str) -> bool:
    for w in text:
        if w not in ["G", "W"]:
            return False
    return True


def counting(text: str) -> int: # GGGG...WWWに直すための最小作業回数を数える
    str_list = list(text)
    num_g = str_list.count("G")
    min = num_g # 最小作業回数の初期化
    left = 0
    right = num_g
    for w in text:
        
        if w == "G":
            right -= 1
        else: # w == "W"
            left += 1
        
        if left + right < min:
            min = left + right

    return min


if __name__ == "__main__":
    print("Input GW:")
    input = input()
    if gw_checker(input):
        print(f"作業回数は {counting(input)}")
    else:
        raise ValueError("only use \"G\" or \"W\"")