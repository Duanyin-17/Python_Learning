import pandas as pd
import numpy as np

df = pd.read_excel('C:\\Users\\27047\\Desktop\\数模培训\\test.xlsx',header=None)
a = df.to_numpy()
print('原题:\n',a)

def thr(c):
    pass
    if c < 3:
        return 0
    elif c < 6:
        return 3
    else:
        return 6

def fun(ad,y,x):
    return np.setdiff1d(np.arange(10),np.unique(np.concatenate((np.unique(ad[y, :]),
                                                                np.unique(ad[:, x]),
                                                                np.unique(ad[thr(y):thr(y)+3,thr(x):thr(x)+3])))))
def coor(u):
    y = (u-1) // 9
    x = u - y*9 - 1
    return y,x

ans = 0
t = 0
def d(ad,u):
    y,x = (coor(u))
    if u == 82:
        global ans,t
        ans = ad.copy()
        t = 1
        return
    if ad[y,x] != 0:
        d(ad,u+1)
    else:
        s = fun(ad, y, x)
        if s.size != 0:
            for i in s:
                ads = ad.copy()
                ads[y,x] = i
                d(ads,u+1)


d(a,1)
if t:
    print("答案:\n",ans)
    df_ans = pd.DataFrame(ans)
    df_ans.to_excel('C:\\Users\\27047\\Desktop\\ans.xlsx',index = False,header = False)
    print("答案已保存")
else:
    print("无解")