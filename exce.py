try:
     num1 = int(input("enter your number "))
     num2 = int(input("Please enter the second number"))
     result = num1/num2
except ValueError:
    print("invalid number")
except ZeroDivisionError:
    print("cannot divide with 0")
else:
    print("result",result)

finally:
    print("whole code executed")