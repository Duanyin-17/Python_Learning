import numpy as np
import sympy as sp

a = np.array([[0.2,0.6,0.2],
              [0.3,0,0.7],
              [0.5,0,0.5]])

A = np.vstack([a.T - np.eye(3), np.ones((1,3))])
b =np.array([0,0,0,1])


# #最小二乘法
# x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
#
# print("平稳分布（最小二乘解）:\n",x)
#
# #Numpy直接计算(同上)
# x_num = np.linalg.lstsq(A, b, rcond=None)[0]
# print("数值解:\n", x_num)


# #符号计算
#
# π1, π2, π3 = sp.symbols('π1 π2 π3')
# π = sp.Matrix([π1, π2, π3])
# A_sym = a.T - sp.eye(3)
# equations = [eq for eq in A_sym @ π] + [π1 + π2 + π3 - 1]
# solution = sp.solve(equations, (π1, π2, π3))
#
# print("\nSymbolic solution:")
# print(solution)
