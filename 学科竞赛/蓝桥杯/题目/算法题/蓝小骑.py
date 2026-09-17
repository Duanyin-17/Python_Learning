import os
import sys

# 请在此输入您的代码


x1,x2,x3,x4 = map(int,input().split())
t2,t3,t4 = map(int,input().split())
q = int(input())

c0 = q*x1
s1 = max(0,q-t2)*x1+x2
s2=max(0,q-t3)*x1+x3
s3=max(0,q-t4)*x1+x4
s4=max(0,q-t2-t3)*x1+x2+x3
s5=max(0,q-t2-t4)*x1+x2+x4
s6=max(0,q-t3-t4)*x1+x3+x4
s7=max(0,q-t2-t3-t4)*x1+x2+x3+x4
minc=min(c0,s1,s2,s3,s4,s5,s6,s7)
print(minc)























