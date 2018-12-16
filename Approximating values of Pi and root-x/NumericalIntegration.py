# -*- coding: utf-8 -*-
"""
@author: Pandya, Darshit
@title: Numerical Integration Using Monte Carlo, Simpson, Trapezoidal and Simpson Method
"""
import random
#-----------------------------------------------------------------------------------
calc_partial = lambda x: 1/(1 + x*x)
#-----------------------------------------------------------------------------------
def TrapezoidalNiPi(): 
    
    ''' 
    This method is used to approximate the value of pi summing
    up the area of the trapezoids. 1/1+x^2 integrated over [0,1]
    constitutes of 45 degree, and pi is 180 radian as pi * d = circumference
    Hence we multiply the integration by 4 to predict the value of pi
    '''
    intervals = 1
    upper_limit = 1.0
    lower_limit = 0.0
    
    ## As per the calculus theory, the upconcave curve is overestimated
    ## by the trapezoidal rule. So the below process follows
    ## Step1: Calculate height as (upperlimit - lowerlimit) / totaldivisions
    ## Step2: Iterate through all the trapezoids i.e. N
    ## Step3: Calculate the area by sum of trapezoids using the formula i.e (base1 + base2) * height /2
    ## Step4: Apply the check on the significant difference between the areas calculated
    
    done = False 
    approx_area_before = 0.0
    approx_area_after = 0.0
    
    while done == False:
        lower = 0.0
        approx_area_after = 0.0
        height = (upper_limit - lower_limit) / intervals ##<--1
        cal_lower = calc_partial(lower)
        for i in range(1, intervals+1):                  ##<--2
            upper = lower + height
            cal_upper = calc_partial(upper) ## <----------"ONLY ONE COMPUTATION => DECREASING COMPUTATIONS"
            if lower <= upper_limit - lower_limit:
                    approx_area_after +=  ((cal_lower + cal_upper)/2)  ##<--3
            lower = upper
            cal_lower = cal_upper
        approx_area_after = height * approx_area_after
        if approx_area_after > approx_area_before and approx_area_after - approx_area_before > 0.0000001: ##<--4
                approx_area_before = approx_area_after
                intervals += 1
        else:
                done = True
    
    
    print("The value of pi using the Trapezoidal Method: {0},".format(approx_area_after * 4))
    print("The number of intervals used is {0}.".format(intervals))
    return intervals
#-----------------------------------------------------------------------------------
def SimpsonNiPi(intervals):
    '''
    This method is used to approximate the value of pi
    using the sum of arcs. Here, the intervals calculated above
    will be used to approximate pi with this method
    '''
    
    ## Step1: Calculate height as (upperlimit - lowerlimit) / totaldivisions
    ## Step2: Iterate through all the intervals
    ## Step3: Calculate the area using the formula of simpson 1/3 rule
    ##       Sum over intervals [(current -prev)/6 * (f(prev) + 4*f(prev/2 + cur/2) + f(curr)]
    approx_area = 0.0
    upper_limit = 1.0
    lower_limit = 0.0
    lower = 0.0
    diff = (upper_limit -lower_limit) / intervals
    cal_lower = calc_partial(lower)##<--1
    for i in range(1, intervals + 1): ##<--2
        upper = lower + diff
        cal_upper = calc_partial(upper)## <----------"ONLY ONE COMPUTATION => DECREASING COMPUTATIONS"

        approx_area += (cal_lower + 4*(4/((1/cal_lower) + (1/cal_upper) + (2*lower*upper + 2))) + cal_upper)##<--3
        ## above statement is mathematically solved to reduce the number of computations
        lower = upper
        cal_lower = cal_upper
    print("The value of pi using the Simpson's Method: {0},".format((diff / 6)*approx_area * 4))    
#-----------------------------------------------------------------------------------       
def MidPointNiPi(intervals):
    '''
    This method is used to approximate the value of pi 
    using the midpoint of the interval points on the function 1/1+x^2.
    Total intervals calculated from the trapezoidal rule 
    will be used here
    '''        
    ## Step1: Calculate height as (upperlimit - lowerlimit) / totaldivisions
    ## Step2: Iterate through all intervals
    ## Step3: Calculate the area using the midpoint rule formula
    ##          Sum over intervals[(cur - prev) * f(cur/2 + prev/2)]
    approx_area = 0.0
    upper_limit = 1.0
    lower_limit = 0.0
    lower = 0.0
    diff = (upper_limit -lower_limit) / intervals##<--1
    for i in range(1, intervals + 1): ##<--2
        upper = lower + diff
        approx_area += (calc_partial((lower + upper )/2))                  ##<--3
        lower = upper
    print("The value of pi using the Midpoint rule Method: {0},".format(diff * approx_area * 4)) 
#-----------------------------------------------------------------------------------    
def MonteCarloNiPi():
    '''
    This method is used to approximate the value of pi 
    by inscribing a circle inside a square of radius (b-a)
    and taking out the ratio of the total points inside a circle to
    total random points and then multiplying by 4
    '''
    points_circle = 0
    total_points = 0
    
    ## As per the calculus theory, it takes 200000 iterations to approximate value of pi
    ## Step1: 20000 iterations for loop
    ## Step2: Generate a random (x,y) coordinate
    ## Step3: For the generated coordinate, check if its inside the circle
    ## Step4: If yes, increment points_circle else pass
    ## Step5: After all iterations complete, compute the value of pi
    for i in range(0, 200000): #<--1
            x_point = random.uniform(0, 1)  #<--2
            y_point = random.uniform(0, 1)  #<--2
            total_points += 1
            if x_point**2 + y_point**2 <= 1:  #<--3
                    points_circle += 1        #<--4
    
    approx_pi = 4 * (points_circle / total_points) #<--5
    print("The value of pi using Monte Carlo Method with 200000 iterations is: {0}".format(approx_pi))
#-----------------------------------------------------------------------------------    
if __name__ == '__main__':
    intervals = TrapezoidalNiPi()
    SimpsonNiPi(intervals)
    MidPointNiPi(intervals)
    MonteCarloNiPi()
    
