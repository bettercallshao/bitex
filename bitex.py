import math

UNITLEN = 8

def make_header(n):
    return '<th>b%02d</th>' % n

def make_indicator(b):
    return '<td><span class="%s"></span></td>' % ('green' if b else 'grey')

def make_row(l):
    return '<tr>' + ''.join(l) + '</tr>'

def make_table(l):
    return '<table>' + ''.join(l) + '</table>'

def get_digits(n):
    return int(math.ceil(math.log(n, 2) / UNITLEN) * UNITLEN)

def truth_digit(n, d):
    return (n >> d) & 1 > 0

def count_backward(n):
    return reversed(range(n))

def segment_list(l):
    return [l[i:i+UNITLEN] for i in range(0, len(l), UNITLEN)]

def get_table(n):
    l = get_digits(n)
    header_lists = segment_list([make_header(b) for b in count_backward(l)])
    indica_lists = segment_list([make_indicator(truth_digit(n, b)) for b in count_backward(l)])
    return  make_table([make_row(header_lists[i]) + make_row(indica_lists[i]) for i in range(len(header_lists))])

def get_short(n):
    return '<h1>0x%x is %d</h1>' % (n, n)

def get_html(short, table):
    template = """
<!DOCTYPE html>
<html>
<head>
<style>
body {
    font-family: "Liberation Mono";
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
    height: 25px;
    width: 25px;
    background-color: #5c5;
    border-radius: 50%;
    display: inline-block;
}
.grey {
    background-color: #999;
}
</style>
</head>
<body>
<div class="adjuster">
<div>
<form method="POST" action="/timlyrics/bitex/">
<p> Hex (prefix with 0x) or decimal </p>
<input type="text" name="num"/>
<input type="submit" value="BitEx!"/>
</form>
{{short}}
{{table}}
</div>
</div>
<footer>
<a href="https://github.com/timlyrics/bitex">github:timlyrics/bitex</a>
</footer>
</body>
</html>
"""
    return template.replace('{{short}}', short).replace('{{table}}', table)

if 'num' in Hook['params']:
  try:
    num = abs(int(Hook['params']['num'], 0))
  except:
    num = 0xdeadbeef
else:
  num = 0xdeadbeef

print(get_html(get_short(num), get_table(num)))
