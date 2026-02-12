
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np



def calculate_gram_mat(x, sigma):
    """calculate gram matrix for variables x
        Args:
        x: random variable with two dimensional (N,d).
        sigma: kernel size of x (Gaussain kernel)
    Returns:
        Gram matrix (N,N)
    """
    x = x.view(x.shape[0],-1)
    instances_norm = torch.sum(x**2,-1).reshape((-1,1))
    dist= -2*torch.mm(x,x.t()) + instances_norm + instances_norm.t()
    return torch.exp(-dist /sigma)

def renyi_entropy(x,sigma,alpha):
    
    """calculate entropy for single variables x (Eq.(9) in paper)
        Args:
        x: random variable with two dimensional (N,d).
        sigma: kernel size of x (Gaussain kernel)
        alpha:  alpha value of renyi entropy
    Returns:
        renyi alpha entropy of x. 
    """
    
    k = calculate_gram_mat(x,sigma)
    k = k/torch.trace(k) 
    eigv, _ = torch.linalg.eigh(k, UPLO='U')  # or 'L' if you want the lower part
    eigv = torch.abs(eigv)  
    eig_pow = eigv**alpha
    entropy = (1/(1-alpha))*torch.log2(torch.sum(eig_pow))
    return entropy


def joint_entropy(x,y,s_x,s_y,alpha):
    
    """calculate joint entropy for random variable x and y (Eq.(10) in paper)
        Args:
        x: random variable with two dimensional (N,d).
        y: random variable with two dimensional (N,d).
        s_x: kernel size of x
        s_y: kernel size of y
        alpha:  alpha value of renyi entropy
    Returns:
        joint entropy of x and y. 
    """
    
    x = calculate_gram_mat(x,s_x)
    y = calculate_gram_mat(y,s_y)
    k = torch.mul(x,y)
    k = k/torch.trace(k)
    eigv, _ = torch.linalg.eigh(k, UPLO='U')  # or 'L' if you want the lower part
    eigv = torch.abs(eigv)
    eig_pow =  eigv**alpha
    entropy = (1/(1-alpha))*torch.log2(torch.sum(eig_pow))
    return entropy

def calculate_MI(x,y,alpha,s_x,s_y,normalize):
    
    """calculate Mutual information between random variables x and y

    Args:
        x: random variable with two dimensional (N,d).
        y: random variable with two dimensional (N,d).
        s_x: kernel size of x
        s_y: kernel size of y
        normalize: bool True or False, noramlize value between (0,1)
    Returns:
        Mutual information between x and y (scale)

    """
    Hx = renyi_entropy(x,sigma=s_x , alpha=alpha)
    Hy = renyi_entropy(y,sigma=s_y , alpha=alpha)
    Hxy = joint_entropy(x,y,s_x,s_y , alpha=alpha)
    if normalize:
        Ixy = Hx+Hy-Hxy
        Ixy = Ixy/(torch.max(Hx,Hy))
    else:
        Ixy = Hx+Hy-Hxy
    return Ixy


def get_sigma(dim, n, std):
    h = (0.9*std)/(n**1.5)
    return h*n**(-1/(4+dim))


def mbre(observations_at_time):
    o = np.array(observations_at_time)
    x = torch.tensor(o, dtype=torch.float32)
    sigma_x = get_sigma(1,256,torch.std(x) )
    return renyi_entropy(x,sigma_x,1.01)