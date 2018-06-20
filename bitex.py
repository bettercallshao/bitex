import math

UNITLEN = 8

def make_header(n):
    return '<th>b%02d</th>' % n

def make_indicator(d, b):
    return '<td><button type="submit" name="bit" value="%d" class="%s"></span></td>' % (d, ('green' if b else 'grey'))

def make_row(l):
    return '<tr>' + ''.join(l) + '</tr>'

def make_table(l):
    return '<table>' + ''.join(l) + '</table>'

def get_digits(n):
    n = max(n, 2)
    return int(math.ceil(math.log(0.1 + n, 2) / UNITLEN) * UNITLEN)

def truth_digit(n, d):
    return (n >> d) & 1 > 0

def count_backward(n):
    return reversed(range(n))

def segment_list(l):
    return [l[i:i+UNITLEN] for i in range(0, len(l), UNITLEN)]

def get_table(n):
    l = get_digits(n)
    header_lists = segment_list([make_header(b) for b in count_backward(l)])
    indica_lists = segment_list([make_indicator(b, truth_digit(n, b)) for b in count_backward(l)])
    return  make_table([make_row(header_lists[i]) + make_row(indica_lists[i]) for i in range(len(header_lists))])

def get_short(n):
    return '<h1>0x%x is %d</h1>' % (n, n)

def get_html(input_, short, table):
    template = """
<!DOCTYPE html>
<html>
<head>
<style>
body,
button {
    font-family: "Liberation Mono";
}
button {
    font-size: 12pt;
}
table {
    border-spacing: 10px;
}
tr {
    text-align: center;
}
footer {
    position: fixed;
    bottom: 10px;
    right: 30px;
}
.adjuster {
  display: flex;
  justify-content: center;
}
.green,
.grey {
    height: 23px;
    width: 23px;
    border-radius: 50%;
    border-style: solid;
    border-width: 2px;
    border-color: #5c5;
    background-color: #5c5;
    display: inline-block;
}
.grey {
    border-color: #999;
    background-color: #fff;
}
</style>
</head>
<body>
<div class="adjuster">
<div>
<form method="POST" action="/timlyrics/bitex/">
<p> Hex (prefix with 0x) or decimal </p>
<input type="text" name="num" value="{{input}}"/>
<button type="submit">BitEx!</button>
{{short}}
<p> Click on indicators to toggle </p>
{{table}}
</form>
</div>
</div>
<footer>
<a href="https://github.com/timlyrics/bitex">github:timlyrics/bitex</a>
</footer>
</body>
</html>
"""
    return (template.replace('{{input}}', input_)
                    .replace('{{short}}', short)
                    .replace('{{table}}', table))

def get_proper_input(num_str, bit_str):
    convert = lambda x: abs(int(x, 0))
    try:
        num = convert(num_str)
    except:
        num = 0xdeadbeef
    try:
        bit = convert(bit_str)
        mask = 1 << bit
    except:
        mask = 0
    return num ^ mask

def run(num_str, bit_str):
    num = get_proper_input(num_str, bit_str)
    print(get_html(hex(num), get_short(num), get_table(num)))

if __name__ == '__main__':
    num_str = ''
    bit_str = ''
    if 'num' in Hook['params']:
        num_str = Hook['params']['num']
    if 'bit' in Hook['params']:
        bit_str = Hook['params']['bit']

    run(num_str, bit_str)
