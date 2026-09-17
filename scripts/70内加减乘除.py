import random,time,os

random.seed(int.from_bytes(os.urandom(4), 'big') ^ int(time.time_ns()))

d = {0:"+",1:"-",2:"x",3:"÷"}

i=10

def cof(a,b,f):
    c = 0
    match f:
        case 0:c = a + b
        case 1:c = a - b
        case 2:c = a * b
        case 3:c = a / b
    return c

for i in range(10):
    f = random.randint(1, 3)
    while 1:
        a = random.randint(2, 70)
        b = random.randint(2, 70)

        c = cof(a, b, f)
        if((f==2 and (a>9 or b>9))or(f==3 and (a<b or not a%b==0))or(c < 0 or c > 100 or a==b)):
            continue
        else:
            break

    print(f"{a} {d[f]} {b} = {int(c)}\n")

