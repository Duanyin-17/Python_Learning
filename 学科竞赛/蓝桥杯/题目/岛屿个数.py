

"""
5 5
01111
11001
10101
10001
11111
"""
num = int(input())
ans = []
for qwe in range(num):
    m, n = map(int, input().split())
    m += 2
    n += 2
    c = []
    c.append([0 for _ in range(n)])
    for i in range(m - 2):
        a = input()
        ap = [int(j) for j in a]
        c.append([0] + ap + [0])
    c.append([0 for _ in range(n)])
    cp = [[0 for _ in range(n)] for _ in range(m)]

    yd = [0, 1, 0, -1]
    xd = [1, 0, -1, 0]

    yh = [0, 1, 0, -1, 1, 1, -1, -1]
    xh = [1, 0, -1, 0, 1, -1, 1, -1]


    def dfs_0(y, x):
        cp[y][x] = 1
        for i in range(8):
            # print(i,j)
            if y + yh[i] < 0 or y + yh[i] > m - 1 or x + xh[i] < 0 or x + xh[i] > n - 1:
                continue
            if c[y + yh[i]][x + xh[i]] == 0 and cp[y + yh[i]][x + xh[i]] == 0:
                dfs_0(y + yh[i], x + xh[i])


    def dfs(y, x):
        cp[y][x] = 1
        for i in range(4):
            if y + yd[i] < 0 or y + yd[i] > m - 1 or x + xd[i] < 0 or x + xd[i] > n - 1:
                continue
            if cp[y + yd[i]][x + xd[i]] == 0:
                dfs(y + yd[i], x + xd[i])


    dfs_0(0, 0)

    sum = 0

    for i in range(m):
        for j in range(n):
            if cp[i][j] == 0:
                sum += 1
                dfs(i, j)

    ans.append(sum)


for i in ans:
    print(i)








