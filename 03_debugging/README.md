# モジュール化された演算プログラム　modularized_calculator.py

### プログラムの概要
str型の計算式を入力として受け取り、　その計算結果を表示するプログラム  
対応している演算は、四則演算、（）のついた計算、abs()、int()、round()  
プログラムはモジュール化されていて、機能を追加するのが簡単

### 大まかな流れ
入力された文字列を、tokenize()関数でトークン化し、evaluate()関数で計算する
```python 
    line = str型の計算式   # "3 + 2"
    line = input().replace(" ", "") # 3+2
    tokens = tokenize(line) # [3, add, 2]
    answer = evaluate(tokens) # 5
    print("answer = %f\n" % answer) 
```

### tokenize()
式をトークンのリストに変換する  
入力された文字列を先頭から一文字ずつ読み、有効な文字の時その文字を読むための関数 `read_XXX()`を呼ぶ  
読める文字は、[0~9, +, -, *, /, (, ), abs, int, round]
```python
def tokenize(line):
    tokens = []
    index = 0

    # 演算記号を読む関数によってindexを随時更新しながら、トークンを作成していく
    while index < len(line):

        # 数字
        if line[index].isdigit():
            (token, index) = read_number(line, index)

        ...省略
        
        # "round"
        elif line[index] == 'r' and line[index + 1] == 'o' and line[index + 2] == 'u' and line[index + 3] == 'n' and line[index + 4] == 'd':
            (token, index) = read_round(line, index)

        # その他
        else:
            print('Invalid character found: ' + line[index])
            exit(1)

        tokens.append(token)

    return tokens
```
文字からトークンへの変換例
```
"443"   ->  {'type': 'NUMBER', 'number' = '443'}
"+"     ->  {'type': 'PLUS'} 
"("     ->  {'type': 'BRACKETS_START'}
"abs"   ->  {'type': 'FUNCTION', 'function_type': 'ABS'}

```
### evaluate(tokens)
トークン列を計算しその結果を返す。  
計算の流れは、①関数をすべて計算　→ ②掛け算割り算を計算　→ ③足し算割り算を計算  
この中では`evaluate_main(tokens)`が動いている
```python
def evaluate_main(tokens):

    evaluate_functions(tokens)
    evaluate_brackets(tokens)
    evaluate_mul_div(tokens)
    answer = evaluate_plus_minus(tokens)
    return answer
```
### モジュール化されている関数
* make_brackets_tokens(tokens, index)  
    トークン列の中の、indexの指す開きカッコから始まる特定の括弧の中身を取り出したトークン列を返す  
    `1 + ( 2 + 3 ) -> 2 + 3`

* calculate_one_brackets(tokens, index)  
    トークン列の中の、indexの指す開きカッコから始まる特定の括弧の中身を計算して、計算後のトークン列と計算結果を指すindexを返す  
    途中で`evaluate(make_brackets_tokens(tokens, index))`を呼ぶ  
    `1 + ( 2 + 3 ) -> 1 + 5`

* calculate_one_function(tokens, index)
    トークン列の中の、indexが指している一つの関数を計算して、計算後のトークン列と計算結果を指すindexを返す  
    関数は引数が括弧で囲われているので、途中で`calculate_one_brackets(tokens, index)`を呼ぶ

これらの関数を使うことで、関数をすべて計算する`evaluate_functions(tokens)`ではトークンの先頭から関数を見つけるたびに`calculate_one_function(tokens, index)`を実行する、括弧の中身をすべて計算する`evaluate_brackets(tokens)`では開き括弧が見つかるたびに`calculate_one_brackets(tokens, index)`を実行する、といったように簡単に考えることができる。

### テスト
* test("計算式")  
実装が正しくできているかを確かめる関数。  
プログラムによって導かれた結果と、pythonの機能eval()を用いて計算した正しい値を比較し、差が1e-8以下の時にPASS!、そうでない時にFAIL!と表示する

* run_test()  
テストを実行する。テストしたい機能によって、以下の６つの関数に分かれている。適宜コメントアウトすることでテストしたい機能に絞ってテストを実行できる
```python
    plus_minus_test()
    mul_div_test()
    brackets_test()
    abs_test()
    int_test()
    round_test()
```
### テストケース
まずはその機能が動くべき最小のテストケースを作る。その後より複雑な入力に変えていく。また、機能を追加した際は、それまでに作った機能も含めたテストケースを作成する。例えば関数を付け加えた際は、関数単体のみのテストケースだけでなく、それまでに実装した括弧も含めたテストケースも作る。
