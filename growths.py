"""
1. Write a function that increases a number quadratically for N steps.
"""

def quadratic_increase(n):
    result = []
    for i in range(n):
        result.append(i**2)
    return result

# quadratic_increase(10)

"""
2. Write a function that increases a number linearly for N steps.
"""

def linear_increase(n):
    result = []
    for i in range(n):
        result.append(i)
    return result

# linear_increase(10)

"""
3. Write a function that increases a number exponentially for N steps.
"""

def exponential_increase(n):
    result = []
    for i in range(n):
        result.append(2**i)
    return result

# exponential_increase(10)

"""
4. Write a function that increases a number in logarithmic time for N steps.
"""

def logarithmic_increase(n):
    result = []
    for i in range(n):
        result.append(n**i)
    return result

# logarithmic_increase(10)

"""
5. Write a function that increases a number in constant time for N steps.
"""

def constant_increase(n):
    result = []
    for i in range(n):
        result.append(1)
    return result

# constant_increase(10)