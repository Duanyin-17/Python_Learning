
n = 3000000
o = 0
down = [0 for _ in range(30 * 13)]
# add = 0
for i in range(30 * 13):
    o -= down[i]

    if i < 30 * 12 and n >= 300000:
        a = n // 300000
        o += a
        down[i + 30] += a
        n -= 300000 * a
    if i <= 30 * 12:
        n += 11000 * o
    else:
        n += 10000 * o

    print(f'第{i + 1}天：', f'资金：{n}', f'贷款人数：{o}')
# print(n)
print(f"共赚{n-3000000}元")







'''ans = []
for m in range(0,31):

    ans.append(n)

print(max(ans))

'''










