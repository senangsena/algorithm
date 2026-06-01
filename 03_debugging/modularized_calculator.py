# モジュール化された演算プログラム。宿題1〜4すべて実装済み
# 入力：str型の計算式　出力：計算結果
# ✅宿題1...掛け算、割り算の実装
# ✅宿題2...テストケースを加える
# ✅宿題3...かっこに対応させる。
# ✅宿題4...abs(), int(), round()にも対応させる


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

# "*"を読む関数
def read_mul(line, index):
    token = {'type': 'MUL'}
    return token, index + 1

# "/"を読む関数
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

###ここからは関数を読む関数
def read_abs(line, index):
    token = {'type': 'FUNCTION', 'function_type': 'ABS'}
    return token, index + 3
 
def read_int(line, index):
    token = {'type': 'FUNCTION', 'function_type': 'INT'}
    return token, index + 3

def read_round(line, index):
    token = {'type': 'FUNCTION', 'function_type': 'ROUND'}
    return token, index + 5

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

        # "abs"
        elif line[index] == 'a' and line[index + 1] == 'b' and line[index + 2] == 's':
            (token, index) = read_abs(line, index)

        # "int"   
        elif line[index] == 'i' and line[index + 1] == 'n' and line[index + 2] == 't':
            (token, index) = read_int(line, index)
        
        # "round"
        elif line[index] == 'r' and line[index + 1] == 'o' and line[index + 2] == 'u' and line[index + 3] == 'n' and line[index + 4] == 'd':
            (token, index) = read_round(line, index)

        # その他
        else:
            print('Invalid character found: ' + line[index])
            exit(1)

        tokens.append(token)

    return tokens

# 括弧の中に入っているトークン列のみを新しいトークン列として返す関数
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
    tokens[index]['number'] = evaluate(brackets_tokens)
    tokens[index]['type'] = 'NUMBER'

    # brackets_tokensと閉じ括弧を取り除く
    for i in range(brackets_len + 1): 
        tokens.pop(index + 1)

    # indexの返り値は計算結果を指す
    return tokens, index

# ある一つの関数のみ計算する関数
def calculate_one_function(tokens, index):
    assert tokens[index]['type'] == 'FUNCTION'
    assert tokens[index + 1]['type'] == 'BRACKETS_START'
    function_type = tokens[index]['function_type']

    # 関数の引数の中身を計算
    index += 1
    tokens, index = calculate_one_brackets(tokens, index)
    assert tokens[index]['type'] == 'NUMBER' # indexの返り値は、計算結果を指す

    if function_type == 'ABS':
        tokens[index]['number'] = abs(tokens[index]['number'])
    elif function_type == 'INT':
        tokens[index]['number'] = int(tokens[index]['number'])
    elif function_type == 'ROUND':
        tokens[index]['number'] = round(tokens[index]['number'])
    else:
        print("Unknown function type")
        exit(1)

    # 関数を示すトークンを削除
    tokens.pop(index - 1)
    
    # indexの返り値は計算結果を指す
    return tokens, index

# トークン列の中の一つの掛け算もしくは割り算を行う
def calculate_one_mul_div(tokens, index):
    assert tokens[index - 1]['type'] == 'NUMBER'
    assert tokens[index]['type'] in ['MUL', 'DIV']
    assert tokens[index + 1]['type'] == 'NUMBER'

    # token[index + 1]に結果を入れ、token[index - 1], token[index]を削除する
    # 削除するとindexが一つズレることに注意
    if tokens[index]['type'] == 'MUL':
        tokens[index + 1]['number'] = tokens[index - 1]['number'] * tokens[index + 1]['number']
    elif tokens[index]['type'] == 'DIV':
        tokens[index + 1]['number'] = tokens[index - 1]['number'] / tokens[index + 1]['number']
      
    tokens.pop(index - 1)
    tokens.pop(index - 1) # さっきまでのtokens[index]はtokens[index - 1]に
    index -= 1

    # indexの返り値は計算結果を指す
    return tokens, index
            
#　トークン列の演算を行う関数     
def evaluate(tokens):

    # 関数を計算する
    def evaluate_functions(tokens):

        index = 0

        while index < len(tokens):
            if tokens[index]['type'] == 'FUNCTION':

                # 見つかった関数を計算
                tokens, index = calculate_one_function(tokens, index)
            
            index += 1
        
    
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
            if tokens[index]['type'] in ['MUL', 'DIV']:

                # 見つかった掛け算・割り算を計算
                tokens, index = calculate_one_mul_div(tokens, index)

          
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
    # 関数の計算　→ 括弧の中身　→ 掛け算割り算　→　足し算引き算　の順に計算する
    def evaluate_main(tokens):

        evaluate_functions(tokens)
        evaluate_brackets(tokens)
        evaluate_mul_div(tokens)
        answer = evaluate_plus_minus(tokens)

        return answer
    
    return evaluate_main(tokens)



def test(line):
    line = line.replace(" ", "")
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
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
        print("==== plus_minus_test started! ====")

        test("1+2")
        test("5-1")
        test("1555+904") # 複数桁の数も読めるか
        test("1.0+2.1-3") # 小数も読めるか
        test("3947-8.249")

        # 空白あり
        test("1 + 2")
        test("1.0 + 2.154 - 3")

        print("==== plus_minus_test finished! ====")
        print()
        

    def mul_div_test():
        print("==== mul_div_test started! ====")

        
        # 掛け算割り算のみ
        test("1 * 2")
        test("5 / 9")
        test("5 * 83.0 / 4.5")
        test("1.0 / 3 * 9.153")

        # 四則演算（掛け算割り算を優先させられているか）
        test("1 + 9 * 4 - 8 / 3")
        test("3 / 2 + 8 * 10 - 1")
        test("4397 + 809 / 3.0 * 0.1 - 32.214")

        print("==== mul_div_test finished! ====")
        print()


    def brackets_test():
        
        print("==== brackets_test started! ====")
        
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

        print("==== brackets_test finished! ====")
        print()


    def abs_test():

        print("==== abs()_test started! ====")

        test("abs(1)")
        test("abs(-1)")
        test("abs(1.5)")
        test("abs(-32.489)")
        test("abs(4.9) + 4")

        test("abs(1 - 32 + 5)")
        test("abs(3 + (3 + 3))")
        test("abs(54 * (6 / 2.0) + 21 + (5 - 1.2))")
        
        test("5 + abs(-4.0)")
        test("5 + 9 * abs(4.2)")
        test("5 + (4 * abs(3 * (4.24 - 4) / abs(3 - 10.2)) - abs(7))")

        print("==== abs()_test finished! ====")
        print()


    def int_test():

        print("==== int()_test started! ====")


        test("int(2.0)")
        test("int(0.431)")
        test("int(2 - 4.1)")
        test("int(3 * 2.5)")

        test("int(3 * (4 + 2.5432))")
        test("int(3 / (2 + 13.32) * (324 - 32.13))")

        test("4 + int(4.2)")
        test("4 + 42 * int(0.24)")
        test("42 + (34 * int(3.9) - int(123.43 / 4))")

        test("int(abs(43 - 89.24))")
        test("abs(int(53.2 - 689) * 4 / 9)")
        test("abs(int(abs(3 - 9.6)))")

        print("==== int()_test finished! ====")
        print()


    def round_test():

        print("==== round()_test started! ====")

        test("round(2.4)")
        test("round(5.9)")
        test("round(2 - 5.3)")

        test("round(3 * (4 + 2.5432))")
        test("round(3 / (2 + 13.32) * (324 - 32.13))")

        test("4 + round(4.2)")
        test("4 + 42 * round(0.24)")
        test("42 + (34 * round(3.9) - round(123.43 / 4))")

        test("int(round(43 - 89.24))")
        test("abs(round(53.2 - 689) * 4 / 9)")

        test("abs(round(int(3 - 9.6)))")
        test("round(int(abs(int(round(3.532-6.342)))))")

        print("==== round()_test finished! ====")
        print()



    # テスト開始
    print("==== Test started! ====")
    print()
    
    plus_minus_test()
    mul_div_test()
    brackets_test()
    abs_test()
    int_test()
    round_test()

    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input().replace(" ", "") # 空白を除去
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
