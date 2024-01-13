def add_two_numbers(num1,num2,num3):
    """
    This function adds three numbers
    :param num1:
    :param num2:
    :param num3:
    :return:
    
    """
    return num1+num2+num3

def add_three_numbers(num1,num2,num3):
    return num1+num2+num3

def add_four_numbers(num1,num2,num3,num4):
    return num1+num2+num3+num4

#create a function for fibanochi series

def fib(n):
    if n==0:
        return 0
    elif n==1:
        return 1
    else:
        return fib(n-1)+fib(n-2)
    
#create a function for factorial

def fact(n):
    if n==0:
        return 1
    else:
        return n*fact(n-1)        

#create a function of login and signup with if and else condition

def login(username,password):
    if username=="admin" and password=="admin":
        print("login successful")
    else:
        print("login unsuccessful")     



