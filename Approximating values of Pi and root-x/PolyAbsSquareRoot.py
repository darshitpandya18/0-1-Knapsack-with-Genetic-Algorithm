# -*- coding: utf-8 -*-
"""
@author: Pandya, Darshit
@title: Polynomial abstraction for Square root using the power series (Taylor series)
"""
import math

#-----------------------------------------------------------------------------------
def SquareRootPolyAbs(number):
    '''
    In the polynomial approximation of the sqrt, we will use taylor series 
    to compute the sqrt in minimum possible iteration
    
    sqrt(x) = 1 + x/2 - x^2/8 + x^3/16 - ....
    '''
    ##Calculate the square root using library first
    lib_sqrt = math.sqrt(number)
    temp_1 = number
    ##Step 1: Divide/multiply the values by 4 till the value is not between 0.4 and 1.6
    total_div = 1
    if number > 0.4:
        while number > 1.6:
                number = number / 4
                total_div *= 2
    else:
        while number < 0.4:
                number = number * 4
                total_div /=2
    
    ##Step 2: as sqrt of x is not possible, we always compute square root of 1 + x
    number = (number - 1)
    
    ##Step 3: the degree of threshold is 1.0E-8 means till the difference between
    ##the previous one and the current one is <=1.0E-8, we continue to compute
    square_root = 1
    prev  = 0
    i = 1
    square_root_comps = 1
    while (square_root>prev and (square_root - prev) > 0.00000001) \
            or (prev>square_root and (prev - square_root)>0.000000001):
        
        prev_comps = square_root_comps
        prev = square_root
        square_root_comps = (prev_comps) * ((3 - (2*i)) /(2*i)) * (number)
        square_root =square_root + square_root_comps
        i = i + 1
    print("x = {0}, n = {1}".format(number + 1, i))
    print("PolyAbsSquareRoot.py({0}) = {1}, Lib. sqrt({0}) = {2}".format(temp_1, square_root*total_div\
         , lib_sqrt))    
#-----------------------------------------------------------------------------------        
def collectInput():
    number = float(input("Enter the number (0 to exit): "))
    if not number == 0: 
        SquareRootPolyAbs(number)
        collectInput()
    else:
        print("Exited")
#-----------------------------------------------------------------------------------   
if __name__ == '__main__':
        collectInput()


