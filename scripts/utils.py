"""
Nathan Roos


"""

import numpy as np


def get_size_poisson_distrib_vector(mu: float, c: float) -> int:
    """
    Find the smallest integer k such that the representation of the Poisson distribution
    as a vector of size k will have a non represented tail less than c.

    Args:
        mu (float) : mean of the Poisson distribution.
        c (float) : maximum allowed tail non-represented tail probability (default is 1e-4).
    Returns:
        k (int) : size of the vector representing the Poisson distribution.
    """
    assert mu > 0, "Mean of the Poisson distribution must be positive."
    assert c > 0 and c < 1, "Tail probability must be in the range (0, 1)."
    k = -1
    tail_prob = 1.0
    while tail_prob > c:
        k += 1
        tail_prob -= np.exp(-mu) * (mu**k) / np.math.factorial(k)
    return k


def get_outer_bound_of_Zk(k: int, K: float, C: float, W: float, gamma: float) -> float:
    """
    Get the radius of the outer bound of Z_k for a given k.
    Z_k is the part of the circle where the users need k subcarriers to be served.

    See the README for more details about the model.

    Args:
        k (int): The index of zk.
        K (float) : constant of the model (see README)
        C (float) : data rate in bits/second
        W (float) : bandwidth in Hz
        gamma (float) : path loss exponent (gamma >= 2)
    Returns:
        float: The radius of the outer bound of Z_k.
    """
    assert K > 0 and C > 0 and W > 0 and gamma >= 2
    assert k >= 0, "k must be at least 0"
    if k == 0:
        return 0
    return (K / (2 ** (C / (W * k)) - 1)) ** (1 / gamma)

def get_Ak_poisson_parameter(
    k: int, p_active: float, lambda_: float, K: float, C: float, W: float, gamma: float
) -> float:
    """
    Get the parameter for the poisson distribution of A_k the number of users requiring k subcarriers.
    See the README for more details about the model.

    Args:
        k (int): The index of A_k.
        p_active (float): Probability that a user is active.
        lambda_ (float): Average number of users per square meter.
        K (float): Constant of the model (see README).
        C (float): Data rate in bits/second.
        W (float): Bandwidth in Hz.
        gamma (float): Path loss exponent (gamma >= 2).
    Returns:
        float: The parameter for the poisson distribution of A_k.
    """
    assert k >= 1, "k must be at least 1"
    upper_bound = get_outer_bound_of_Zk(k, K, C, W, gamma)
    lower_bound = get_outer_bound_of_Zk(k - 1, K, C, W, gamma)
    return p_active * lambda_ * np.pi * (upper_bound**2 - lower_bound**2)

def get_distribution_of_subcarriers_number(
    R: float, p_active: float, lambda_: float, K: float, C: float, W: float, gamma: float, snr_min:float
):
    """ 
    Return a vector representing the distribution of the number of subcarriers required by users.

    Args:
    """
    #we compute the maximum number of subcarriers required 
    max_subcarrier = np.ceil(C/(W* np.log2(1 + max(K/(R**gamma), snr_min))))

    
    