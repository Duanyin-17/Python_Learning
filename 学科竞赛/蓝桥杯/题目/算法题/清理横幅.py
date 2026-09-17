import os
import sys

# 请在此输入您的代码


x = list(input())


cnt = x.count('L') + x.count('Q') + x.count('B')

ans = 0

while 1:
    if cnt >0:
        n = x[cnt-1]
        del x[cnt - 1]
        if n == 'L' or n == 'Q' or n == 'B':
            cnt -= 1

        ans += 1
    else:
        break


print(ans)











