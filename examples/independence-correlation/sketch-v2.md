# 独立性与不相关

## 一、独立性与条件分布

考虑两个取有限多个实数值的随机变量 $X$ 和 $Y$. 如果对 $X$ 的每个取值 $x$ 和 $Y$ 的每个取值 $y$ 都有

$$
P(X=x,Y=y)=P(X=x)P(Y=y),
$$

就称 $X$ 与 $Y$ 相互独立. 这里左边是〔C01：X=x和Y=y同时发生的概率，名词短语〕，右边是两个事件各自概率的乘积；等式要对所有取值组合成立.

这一条件可以用条件概率来理解. 对任意满足 $P(X=x)>0$ 的 $x$，将独立条件除以 $P(X=x)$，便得到

$$
P(Y=y\mid X=x)
=\frac{P(X=x,Y=y)}{P(X=x)}
=P(Y=y).
$$

也就是说，得知 $X$ 的取值后，〔C02：Y各个取值的概率保持原样，谓语句〕，整个分布都保持不变.[独立定义与有限情形的推导](https://ocw.mit.edu/courses/2-854-introduction-to-manufacturing-systems-fall-2016/pages/lecture-notes/notes-on-covariance/)

## 二、协方差与不相关

独立性对每一对取值的概率都提出了要求，协方差则用一个平均数刻画两个变量的共同变化. 记 $\mu_X=\mathbb E[X]$、$\mu_Y=\mathbb E[Y]$，并定义它们的协方差为：

$$
\operatorname{Cov}(X,Y)
=\mathbb E[(X-\mu_X)(Y-\mu_Y)].
$$

当两个变量同时高于或同时低于各自均值时，〔C04：偏差同号使乘积为正，单一结果分句〕；当一个高于、另一个低于均值时，〔C05：偏差异号使乘积为负，与前项平行〕. 把这些乘积按各自发生的概率求平均，就得到协方差.

将乘积展开并取期望，便有

$$
\begin{aligned}
\operatorname{Cov}(X,Y)
&=\mathbb E[XY]-\mu_X\mathbb E[Y]-\mu_Y\mathbb E[X]+\mu_X\mu_Y\\
&=\mathbb E[XY]-\mathbb E[X]\mathbb E[Y].
\end{aligned}
$$

当协方差等于零时，我们称 $X$ 与 $Y$ **不相关**. 若两个变量的方差都大于零，记它们各自的标准差为 $\sigma_X$ 和 $\sigma_Y$，则Pearson相关系数为 $\rho=\operatorname{Cov}(X,Y)/(\sigma_X\sigma_Y)$，因而在这一条件下，〔C07：不相关与rho为零等价，完整结论分句〕.[协方差与相关系数的定义](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/mit18_05_s22_class07-prep-b.pdf)

现在，来比较独立性与不相关这两个条件. 若 $X$ 与 $Y$ 独立，就能把联合概率拆为各自概率的乘积，因此

$$
\begin{aligned}
\mathbb E[XY]
&=\sum_x\sum_y xy\,P(X=x,Y=y)\\
&=\sum_x\sum_y xy\,P(X=x)P(Y=y)\\
&=\left(\sum_x xP(X=x)\right)
  \left(\sum_y yP(Y=y)\right)\\
&=\mathbb E[X]\mathbb E[Y].
\end{aligned}
$$

代回协方差的计算式，便得到 $\operatorname{Cov}(X,Y)=0$，即 $X$ 与 $Y$ 不相关.

## 三、不相关而不独立

协方差为零时，两个变量仍然可以有确定的函数关系. 例如，令 $X$ 以相同概率取 $-1,0,1$，并设 $Y=X^2$，则所有可能的取值组合为：

| $X$ | $Y$ | 概率 |
|---:|---:|---:|
| $-1$ | $1$ | $1/3$ |
| $0$ | $0$ | $1/3$ |
| $1$ | $1$ | $1/3$ |

这是一组由[MIT讲义例2](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/mit18_05_s22_class07-prep-b.pdf)简化而来的三点分布. 从表中可以算出 $\mathbb E[X]=0$、$\mathbb E[Y]=2/3$，而 $\mathbb E[XY]=(-1+0+1)/3=0$，所以 $\operatorname{Cov}(X,Y)=0$. 然而，$Y=0$ 原来的概率为 $1/3$，而在已知 $X=0$ 的条件下，〔C09：Y=0的条件概率为1，与原概率比较〕；两者不同，因此〔C10：X与Y不独立，术语结论〕.

这里的零协方差来自正负贡献的抵消. 由于 $\mu_X=0$、$\mu_Y=2/3$，当 $X=-1$ 时，偏差乘积为 $-1/3$；当 $X=1$ 时，偏差乘积为 $1/3$；当 $X=0$ 时，乘积为 $0$. 对这三个值按相同概率求平均，〔C12A：非零两项相抵使平均为0，单一结果分句〕；但给定 $X$ 后，$Y$ 的分布就集中在 $X^2$ 这一个值上，〔C12B：与未知道X时的Y分布不同，承接当前例子〕.
