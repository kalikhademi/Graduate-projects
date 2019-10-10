# -*- coding: utf-8 -*-
""" CIS6930PML -- Homework 1 -- hw1.py

# This file is the main homework file
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import os
import math 
## os / paths
def ensure_exists(dir_fp):
    if not os.path.exists(dir_fp):
        os.makedirs(dir_fp)

## parsing / string conversion to int / float
def is_int(s):
    try:
        z = int(s)
        return z
    except ValueError:
        return None


def is_number(s):
    try:
        z = int(s)
        return z
    except ValueError:
        try:
            z = float(s)
            return z
        except ValueError:
            return None

## noise distributions
"""
## returns sample from the Laplace distribution with mean 0 and shape b > 0
"""
def laplace_noise(b, sz=1):
    return stats.laplace.rvs(loc=0, scale=b)


"""
## returns sample from the Gaussian distribution with mean 0 and std sigma > 0
"""
def gaussian_noise(sigma):
    return stats.norm.rvs(loc=0, scale=sigma)

"""
## Load the dataset
"""
def load_data(fp = './data/ds.csv'):
    ds = np.loadtxt(fp, delimiter=',', skiprows=1)
    assert ds is not None, 'Could not load dataset {}!'.format(fp)
    return ds

"""
## queries; note that the queries also return their (global) sensitivity
#the queries mentioned here are counting queries so the global senitivity is 1 at maximum. global sensitivity is between 0 and 1. 
"""
# assume that the age range for any individual is [16, 100] and the yearly income range is [0, 1000000]
def mean_age_query(ds):
    assert ds is not None
    ## Insert your code here to set the global sensitivity
    sensitivity = 2
    # raise NotImplementedError()

    return np.mean(ds[:,0]), sensitivity
def mean_income_query(ds):
    sensitivity = 1000000/42
    # raise NotImplementedError()

    return np.mean(ds[:,1]), sensitivity

def income_per_age_query(ds):
    assert ds is not None
   
    sensitivity = (1000000/16)/42
    
    return np.mean(ds[:,1] / ds[:,0]), sensitivity


"""
## dp mechanisms
"""
def laplace_mech(ds, query_fn,  epsilon):
    assert epsilon > 0, 'Invalid parameters.'

    answer, sensitivity = query_fn(ds)
    assert sensitivity > 0

    b = sensitivity/epsilon
    noisy_answer = answer + laplace_noise(b)

    return noisy_answer


def gaussian_mech(ds, query_fn, epsilon, delta):
    assert epsilon > 0 and 0 < delta < 1.0, 'Invalid parameters.'

    answer, sensitivity = query_fn(ds)
    assert sensitivity > 0
    sigma = (sensitivity/epsilon )* math.sqrt(2*math.log2(5/(4*delta)))
    noisy_answer = answer + gaussian_noise(sigma)
    return noisy_answer


"""
## plots
"""
def dp_accuracy_plot(ds, query_fn, epsilon, delta, num_sim=10000, xlim=[25.0, 50.0], fname='fig.png'):

    true_answer, _ = query_fn(ds)

    noisy_answers_laplace = np.zeros((num_sim,))    # will be an array of num_sim simulations of the laplace mechanism
    noisy_answers_gaussian = np.zeros((num_sim,))   # will be an array of num_sim simulations of the gaussian mechanism

    ## TODO ##
    ## Insert your code here to populate the noisy_answers arrays
    for i in range(num_sim):
        noisy_answers_laplace[i] =laplace_mech(ds,query_fn,epsilon)
        noisy_answers_gaussian[i]= gaussian_mech(ds,query_fn,epsilon,delta)
    # raise NotImplementedError()

    # create histograms out of the simulations array
    lc, bin_edges = np.histogram(noisy_answers_laplace, bins=50, range=xlim, density=True)
    gc, _ = np.histogram(noisy_answers_gaussian, bins=50, range=xlim, density=True)
    assert lc.shape == gc.shape

    # figure out bin centers
    bin_width = (bin_edges[1] - bin_edges[0]) / 2.0
    bin_centers = bin_edges[0:len(bin_edges)-1] + bin_width
    ylim = [0.0, np.maximum(0.2, np.minimum(1.0, 1.1*np.amax([gc, lc])))]

    # plot the stuff
    fig = plt.figure()
    plt.plot([true_answer, true_answer], [0.0, 1.0], color='r', label='True')
    plt.bar(bin_centers, lc, color='b', alpha=0.6, label='Laplace', width=0.5)
    plt.bar(bin_centers, gc, color='g', alpha=0.6, label='Gaussian', width=0.5)

    plt.grid(axis='y', alpha=0.7)
    plt.xlabel('Answer')
    plt.ylabel('Probability')
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.legend()

    # save the plot
    ensure_exists('./plots')
    out_fp = './plots/{}'.format(fname)
    plt.savefig(out_fp)

    plt.show()      # comment out if the code is invoked in non-interactive contexts


def budget_plot(ds, query_fn, max_comp, base_epsilon, base_delta, max_delta, fname='fig.png'):
    m_values = np.arange(1,101)
    naive_comp, advanced_comp = [], []

    for item in m_values:
        #m.epsilon and m.delta
        advanced_delta = item*base_delta
        naive_comp.append(item*base_epsilon)
        advanced_comp.append(base_epsilon * (math.sqrt(2*item*math.log(1/advanced_delta))) + base_epsilon * item *(math.exp(base_epsilon)-1))
    
    fig = plt.figure()
    plt.plot(m_values, naive_comp,c='r', label='Naive')
    plt.plot(m_values, advanced_comp,c='b', label='Advanced')
    plt.legend()
    ensure_exists('./plots')
    out_fp = './plots/{}'.format(fname)
    plt.savefig(out_fp)
    plt.show()


def income_per_age_comp(ds, epsilon, delta):
    ## TODO ##
    ## Insert your code here
    n = np.arange(1,101)
    prop, noisy_answer_1= [],[]
    for i in n:
        answer, sensitivity = income_per_age_query(ds)
        query_fn = income_per_age_query
        noisy_answer_1.append(laplace_mech(ds, query_fn, epsilon))

        query_fn = mean_income_query
        answer_b, sensitivity_b = mean_income_query(ds)
        noisy_answer_2 = laplace_mech(ds, query_fn, epsilon)
        query_fn = mean_age_query
        answer_b_age, sensitivity_b_age = mean_age_query(ds)
        noisy_answer_3 = laplace_mech(ds, query_fn, epsilon)

        prop.append(noisy_answer_2/noisy_answer_3)
    

    fig = plt.figure()
    plt.plot(n,noisy_answer_1,'o', c='r', label='Income per age')
    plt.plot(n,prop,'o', c='b',  label='Proposition')
    plt.legend()
    plt.show()


    



def main():

    # figure out the problem number and subproblem number
    assert len(sys.argv) >= 2, 'Incorrect number of arguments!'
    p_split = sys.argv[1].split('problem')
    assert len(p_split) == 2 and p_split[0] == '', 'Invalid argument {}.'.format(sys.argv[1])
    problem_str = p_split[1]

    assert is_number(problem_str) is not None, 'Invalid argument {}.'.format(sys.argv[1])
    problem = float(problem_str)
    probno = int(problem)

    if probno != 4:
        assert False, 'Problem {} is not a valid problem # for this assignment/homework!'.format(problem)

    sp = problem_str.split('.')
    assert len(sp) == 2 and sp[1] != '', 'Invalid problem numbering.'
    subprob = int(sp[1])
    if subprob <= 0 or subprob > 4:
        assert False, 'Problem {} is not a valid problem # for this assignment/homework!'.format(problem)

    data_fp = os.path.join(os.getcwd(), 'data')
    assert os.path.exists(data_fp), 'Can''t find data!'

    # load the dataset
    ds = load_data()

    # parameter for all subproblems except 3
    delta = np.power(2.0, -20.0)

    if subprob == 1: ## problem 4.1
        assert len(sys.argv) == 2, 'Invalid extra argument'

        query_fn = mean_age_query
        epsilon = 1.0

        true_mean_age, sensitivity = query_fn(ds)
        laplace_answer = laplace_mech(ds, query_fn, epsilon)
        gaussian_answer = gaussian_mech(ds, query_fn, epsilon, delta)

        print('Problem 4.1: true mean age {:.2f}, laplace noisy answer: {:.2f}, gaussian noisy answer: {:.2f} [epsilon = {:.3f}, log2 delta = {}, sensitivity = {:.3f}]'.
                    format(true_mean_age, laplace_answer, gaussian_answer, epsilon, np.log2(delta), sensitivity))

    elif subprob == 2: ## problem 4.2
        assert len(sys.argv) > 2, 'Epsilon value not specified!'
        epsilon = is_number(sys.argv[2])
        assert epsilon is not None and epsilon > 0, 'Invalid epsilon.'

        query_fn = mean_age_query
        dp_accuracy_plot(ds, query_fn, epsilon, delta, fname='mean_age_accuracy_eps{}.png'.format(epsilon))

    elif subprob == 3: ## problem 4.3
        assert len(sys.argv) == 2, 'Invalid extra argument'

        base_epsilon = 0.1
        base_delta = delta
        max_delta = np.power(2.0, -30.0)

        query_fn = mean_age_query
        max_comp = 100

        budget_plot(ds, query_fn, max_comp, base_epsilon, base_delta, max_delta, fname='budget_plot.png')

    elif subprob == 4: ## problem 4.4
        assert len(sys.argv) == 2, 'Invalid extra argument'

        epsilon = 1.0
        income_per_age_comp(ds, epsilon, delta)
        
        


if __name__ == '__main__':
    main()
