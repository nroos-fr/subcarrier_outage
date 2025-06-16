# Estimating the probability of outage based on the number of subcarriers required at the same time

**Context:** In OFDMA (Orthogonal Frequency Division Multiple Access) systems, the emitter is given several subcarriers for a few time
slots. The number of subcarriers required depends on the distance of the emitter to the reciever. 

We want to be able to compute two values:

1. The probability of outage based on the number of subcarriers required at the same time and the number of subcarriers available.
2. The number of subcarriers required to achieve a certain probability of outage.

This code provides two scripts to compute these two elemnts and a notebook to play with the parameters.

## Usage

### Requirements

### Scripts

## Modeling

### Law of the number of required subcarriers

We consider the receiving antenna to be located at the origin of $\mathbb{R}^2$ the 2D plane. The cell is a circle of radius $R$ centered at the origin.
A user located at a point $x$ in the cell will require a number of subcarriers $N_s(x)$:

$$
N_s(x) = \left\lceil \frac{C}{W\log_2\left(1+\frac{K}{||x||^\gamma}\right)} \right\rceil \text{ if $\frac{K}{||x||^\gamma} > \text{SNR}_\text{min}$, else the communication is not possible.}
$$

where:

* $C>0$ is the data rate (in bits/s),
* $W>0$ is the bandwidth of a subcarrier (in Hz),
* $K>0$ is a constant (no unit) which takes into account emitting power, fading and shadowing,
* $\gamma\geq 2$ is a constant (no unit) that models the path loss,
* $\text{SNR}_\text{min}$ is the minimum required signal-to-noise ratio for the communication to happen (no unit).

The maximum number of subcarriers required in the cell is given by:

$$
N_{s,\text{max}} = \left\lceil \frac{C}{W\log_2(1+\max\left(\text{SNR}_\text{min}, \frac{K}{R^\gamma}\right))} \right\rceil
$$

We represent the users by a Poisson point process noted $N_u$ with intensity measure $\lambda dx$ (where $\lambda$ is the average number of users per $\text{m}^2$). A proportion $p_\text{active}$ of the users are active at the same time. Therefore the number of active users $N_a$ is a Poisson process with intensity measure $p_\text{active}\lambda dx$.

We need to compute the law of the number of required subcarriers $R_s$ at the same time. The number of required subcarriers is given by:

$$
R_s = \sum_{x \in N_a} N_s(x).
$$

Let $A_k$ be the number of active users requiring $k$ subcarriers at the same time. The number of required subcarriers is then given by:

$$
R_s = \sum_{k=1}^{N_{s,\text{max}}} k A_k.
$$

We need to compute the law of the random variables (r.v.) ${(A_k)}_k$. For all $k\in[|1;N_{s,\text{max}}|]$, let $Z_k$ be the part of the cell where the users require $k$ subcarriers. Then by definition $A_k = N_a(Z_k)$. We characterize $Z_k$ :

$$
\begin{aligned}
x \in Z_k &\iff N(x) = \left\lceil \frac{C}{W\log_2(1+\frac{K}{||x||^\gamma})} \right\rceil = k \\
&\iff 
\begin{cases}
    \left(\frac{K}{2^{\frac{C}{W(k-1)}} - 1}\right)^\frac{1}{\gamma} < ||x|| \leq \left(\frac{K}{2^{\frac{C}{Wk}} - 1}\right)^\frac{1}{\gamma}, \text{ if $k>1$} \\
    ||x|| \leq \left(\frac{K}{2^{\frac{C}{W}} - 1}\right)^\frac{1}{\gamma} , \text{ if $k=1$}\\
\end{cases}
\end{aligned}
$$

Since $N_a$ is a Poisson process with intensity measure $p_\text{active}\lambda dx$ the r.v. ${(A_k)}_k$ are independent Poisson r.v. with parameters:

$$
A_k \sim \mathcal{P}(p\lambda \cdot \text{Area}(Z_k)).
$$

Then the law of $R_s$ is easily computed by convolving the law of the r.v $(kA_k)_{k \in [|1;N_{s,\text{max}}|]}$.

### Example values of the parameters

|                |  $C$   | $W$   | $K$    | $\gamma$ | $R$  | $\lambda$ | $\text{SNR}_\text{min}$ | $p$   |
|:--------------:|:---:     |:-----:|:------:|:--------:|:----:|:---------:|:-----------------------:|:-----:|
| **Value**     | 200    | 250   | $10^6$ | 2.8      | 300  | 0.01      | 0.1                     | 0.01  |
| **Unit**      | kb/s    | kHz   | -      | -        | m    | $\text{m}^{-2}$  | -                       |
