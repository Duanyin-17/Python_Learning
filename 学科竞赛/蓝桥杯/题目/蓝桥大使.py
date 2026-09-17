
n = int(input())
a = n//2
b = n-a
l = []

for _ in range(n):
    sa,sb = map(int,input().split())
    l.append((sa,sb,sa-sb))

l.sort(key = lambda x:x[2] ,reverse = True )

ans = 0
for i,j,_ in l:
    if a > 0:
        ans+=i
        a-=1
    else:
        ans+=j
        b-=1
print(ans)
#贪心算法  差值
# https://www.lanqiao.cn/problems/20271/learning/?contest_id=250



