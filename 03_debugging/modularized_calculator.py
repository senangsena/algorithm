# モジュール化された演算プログラム。
# 入力：str型の計算式　出力：計算結果
# 宿題1...掛け算、割り算の実装
# 宿題2...テストケースを加える
# 宿題3...かっこに対応させる。
# 宿題4...abs(), int(), round()にも対応させる


# 関数(abs(), int(), round())を読む関数

# 数字を読む関数
def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index

### ここからは演算記号を読む関数 ###
# "+"を読む関数
def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1

# "-"を読む関数
def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_mul(line, index):
    token = {'type': 'MUL'}
    return token, index + 1

def read_div(line, index):
    token = {'type': 'DIV'}
    return token, index + 1


### ここからは括弧(brackets)を読む関数 ###
def read_brackets_start(line, index):
    token = {'type': 'BRACKETS_START'}
    return token, index + 1

def read_brackets_end(line, index):
    token = {'type': 'BRACKETS_END'}
    return token, index + 1

def read_abs(line, index):
    token = {'type': 'FUNCTION'}
 


# 計算式をトークンのリスト化する関数
def tokenize(line):
    tokens = []
    index = 0

    # 演算記号を読む関数によってindexを随時更新しながら、トークンを作成していく
    while index < len(line):

        # 数字
        if line[index].isdigit():
            (token, index) = read_number(line, index)

        # "+"
        elif line[index] == '+':
            (token, index) = read_plus(line, index)

        # "-"
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        
        # "*"
        elif line[index] == '*':
            (token, index) = read_mul(line, index)

        # "/"
        elif line[index] == '/':
            (token, index) = read_div(line, index)

        # "("
        elif line[index] == '(':
            (token, index) = read_brackets_start(line, index)

        # ")"
        elif line[index] == ')':
            (token, index) = read_brackets_end(line, index)

        # 
        elif line[index] == 'a' and line[index + 1] == 'b' and line[index + 2] == 's':
            (token, index) = read_abs(line, index)
            pass 
        
        # その他
        else:
            print('Invalid character found: ' + line[index])
            exit(1)

        tokens.append(token)

    return tokens

# 括弧の中に入っているトークン列を返す関数
# トークン全体と、開き括弧のindexを受け取り、その開き括弧に対応する閉じ括弧を探す
def make_brackets_tokens(tokens, index):
    assert tokens[index]['type'] == 'BRACKETS_START'

    index += 1
    brackets_tokens = []
    brackets_count = 1

    # 見つけた開き括弧に対応する閉じ括弧を見つけ、それまでのトークン列をbrackets_tokensに保存
    # brackets_countは（見つけた開き括弧の数　ー　見つけた閉じ括弧の数）
    while brackets_count > 0:
        
        if tokens[index]['type'] == 'BRACKETS_START':
            brackets_count += 1
        elif tokens[index]['type'] == 'BRACKETS_END':
            brackets_count -= 1
            if brackets_count == 0:
                break

        brackets_tokens.append(tokens[index])
        index += 1
    
    return brackets_tokens

# ある一つの括弧の中身のみ計算する関数
def calculate_one_brackets(tokens, index):
    assert tokens[index]['type'] == 'BRACKETS_START'

    brackets_tokens = make_brackets_tokens(tokens, index)
    brackets_len = len(brackets_tokens)

    # 括弧の中身を計算し、1トークンにまとめる
    # 現在indexが指すのは開き括弧。それを計算結果の数字で上書きする
    tokens[index]['number'] = evaluate_main(brackets_tokens)
    tokens[index]['type'] = 'NUMBER'

    # indexが指す位置を開き括弧の次の位置に
    index += 1

    # brackets_tokensと閉じ括弧を取り除く
    for i in range(brackets_len + 1): 
        tokens.pop(index)

    
    return tokens, index
            
     

### ここからはトークン列の演算を行う関数
# 括弧の中身を計算する
def evaluate_brackets(tokens):

    index = 0

    while index < len(tokens):
        if tokens[index]['type'] == 'BRACKETS_START':
            
            # 見つかった括弧の中身を計算
            tokens, index = calculate_one_brackets(tokens, index)
            
        index += 1
    

# 掛け算と割り算を行う
def evaluate_mul_div(tokens):
    index = 0

    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'MUL':

                # token[index]に結果を入れ、token[index - 2], token[index - 1]を削除する
                # 削除するとindexが一つズレることに注意
                tokens[index]['number'] = tokens[index]['number'] * tokens[index - 2]['number']
                tokens.pop(index - 2)
                tokens.pop(index - 2) # さっきまでのtokens[index - 1]はtokens[index - 2]に
                index -= 2

            elif tokens[index - 1]['type'] == 'DIV':

                # token[index]に結果を入れ、token[index - 2], token[index - 1]を削除する
                # 削除するとindexが一つズレることに注意
                tokens[index]['number'] = tokens[index - 2]['number'] / tokens[index]['number']
                tokens.pop(index - 2)
                tokens.pop(index - 2) # さっきまでのtokens[index - 1]はtokens[index - 2]に
                index -= 2
        index += 1
    
    

# 足し算と引き算を行い演算結果をかえす
def evaluate_plus_minus(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1

    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer

# メインのevaluate関数
# 括弧の中身　→ 掛け算割り算　→　足し算引き算　の順に計算する
def evaluate_main(tokens):
    evaluate_brackets(tokens)
    evaluate_mul_div(tokens)
    answer = evaluate_plus_minus(tokens)

    return answer


def test(line):
    line = line.replace(" ", "")
    tokens = tokenize(line)
    actual_answer = evaluate_main(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
# 機能ごとにテストできるように、モジュール化した
def run_test():

    # 足し算引き算
    def plus_minus_test():
        test("1+2")
        test("5-1")
        test("1555+904") # 複数桁の数も読めるか
        test("1.0+2.1-3") # 小数も読めるか
        test("3947-8.249")

    # 空白あり
    def mul_div_test():
        test("1 + 2")
        test("1.0 + 2.154 - 3")

        # 掛け算割り算のみ
        test("1 * 2")
        test("5 / 9")
        test("5 * 83.0 / 4.5")
        test("1.0 / 3 * 9.153")

        # 四則演算（掛け算割り算を優先させられているか）
        test("1 + 9 * 4 - 8 / 3")
        test("3 / 2 + 8 * 10 - 1")
        test("4397 + 809 / 3.0 * 0.1 - 32.214")

    def brackets_test():
        
        
        test("(1 + 2)")
        test("2 * (3 + 5)")
        test("5 + (6.0 + 1.54) / 3")
        test("(6.4 + 2) * (5.0 - 2)")
        test("5 * (135.42 + 542) + 8.0")

        # 括弧の中に括弧
        test("(3 + (3 + 2))")
        test("(3 + (4.0 - 4.3234) * (3 / (2 - 6.5)))")
        test("4.0 + ((((3.0 + 1) - 6.95) * 321) / 4)")
        test("(354 + (32 * (5.0) - 43 - (1.0)))")

        # エッジケース 
        test("(2)")
        test("(4)/(5)")

    


    # テスト開始
    print("==== Test started! ====")
    
    # plus_minus_test()
    # mul_div_test()
    brackets_test()

    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input().replace(" ", "") # 空白を除去
    tokens = tokenize(line)
    answer = evaluate_main(tokens)
    print("answer = %f\n" % answer)
