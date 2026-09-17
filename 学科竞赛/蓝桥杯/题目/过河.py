import numpy as np

n = int(input())
c = np.array([[1,0],[0,1],[1,1],[2,0],[0,2]])
s = []
for i in range(0,n+1):
    for j in range(0,n+1):
        s.append([i,j])
un = []
for i in s:
    if 0 < i[0] < i[1] or 0<n-i[0]<n-i[1]:
        un.append((i[0],i[1]))
un = set(un)
ans = []
path = []
def dfs(l,o,u):
    global path,c,n,un
    if u==len(path):
        path.append(l.tolist()+[o])
    else:
        path[u] =(l.tolist()+[o])
    if l[0]==l[1]==0:
        global ans
        ans.append(path)
        for j in path:
            print('→', '(', j[0], j[1], ')', end='')
        print()
        return
    for k in c[-o+1:]:
        match o:
            case 1:
                if not np.all((n-l)>=k):
                    continue
            case -1:
                if not np.all(l>=k) :
                    continue
        p = l+o*k
        if np.all(0<=p) and np.all(p<=n) and not tuple(p) in un :
            if not p.tolist()+[-o] in path[:u+1]:
                dfs(p, (-1) * o, u + 1)

dfs(np.array([n,n]),-1,0)
print(f"共{len(ans)}种方法")
print('(商人 仆从),路径显示剩余的人数')































