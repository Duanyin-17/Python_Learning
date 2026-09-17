n,m = map(int,input().split())
v = []
w = []
for i in range(n):
    a,b = map(int,input().split())
    v.append(a)
    w.append(b)


dp = [0 for i in range(m+1)]

#print(dp)

for i in range(n):
    for j in reversed(range(m+1)):
        if not i == 0 :
            if j>=v[i]:
                dp[j] = max(dp[j],dp[j-v[i]]+w[i])
            else:
                dp[j] = dp[j]
        else:
            if j>=v[i]:
                dp[j] = w[i]


print(dp[-1])

'''
暴搜超时
import copy

n,m = map(int,input().split())
c = {}
for i in range(n):
    a,b = map(int,input().split())
    c[i] = [a,b]
d = [i for i in range(n)]
#暴力
sum = []
def dp(l,v,w):
    global c,m

    for i in l:
        down = copy.deepcopy(l)
        down.remove(i)
        if v+c[i][0]<=m and down :
            dp(down,v+c[i][0],w+c[i][1])
        else:
            global sum
            sum.append(w)

dp(d,0,0)
print(max(sum))
'''