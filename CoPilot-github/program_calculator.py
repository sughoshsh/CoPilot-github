def calcutor():
    print("Welcome to the calculator")
    print("Please enter the first number")
    num1 = int(input())
    print("Please enter the second number")
    num2 = int(input())
    print("Please enter the operation you would like to perform")
    operation = input()
    if operation == "+":
        print(num1 + num2)
    elif operation == "-":
        print(num1 - num2)
    elif operation == "*":
        print(num1 * num2)
    elif operation == "/":
        print(num1 / num2)
    else:
        print("Invalid operation")

calcutor() 