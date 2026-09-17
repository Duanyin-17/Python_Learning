def count_subsequence(s):
    n = len(s)
    dp = [[0] * 4 for _ in range(n + 1)]
    dp[0][0] = 1

    for i in range(n):
        for j in range(4):
            dp[i + 1][j] = dp[i][j]
        if s[i] == 'l':
            dp[i + 1][1] = dp[i][0] + dp[i][1]
        elif s[i] == 'a':
            dp[i + 1][2] = dp[i][1] + dp[i][2]
        elif s[i] == 'n':
            dp[i + 1][3] = dp[i][2] + dp[i][3]

    return dp[n][3]

# 读取输入
s = input()
# 计算并输出结果
print(count_subsequence(s))