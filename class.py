'''class person():
    def __init__(self,name,age):
        self.name = name
        self.age = age

p1 = person("Ram",36)
print(p1.name , p1.age)

class Cars:
    def __init__(self,brand,model):
        self.brand = brand
        self.model = model
    def show_details(self):
         print(f"brand: {self.brand}")
         print(f"model: {self.model}")
p1 = Cars("lamborgini","Gt4-958948")
p1.show_details()

class Area:
    def __init__(self,length,width):
        self.length= length
        self.width = width
    def area1(self):
        area = self.length * self.width
        print("The area of rectangle:", area)

p1 = Area(100,20)
p1.area1()

class Employee:
    def __init__(self,Name,age,salary):
        self.name = Name
        self.age = age
        self.salary = salary
    def unincremented_salary(self):
        print("Name:",self.name)
        print("age:",self.age)
        print("salary",self.salary)
    def incremented_salary(self):
        increment = self.salary + 1000
        print("Imcremented salary:",increment)
p1 = Employee("Ram",45,1000000)
p1.unincremented_salary()
p1.incremented_salary()
    
class BankAccount:
    def __init__(self, account_number, balance):
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"Amount Deposited: {amount}")
        print(f"Updated Balance: {self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient balance!")
        else:
            self.balance -= amount
            print(f"Amount Withdrawn: {amount}")
            print(f"Remaining Balance: {self.balance}")


# Creating object
p1 = BankAccount(2495089801948, 100000)

p1.deposit(19000)
p1.withdraw(50000)


class Book:
    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price

    def discount(self, percent):
        discount_amount = (percent / 100) * self.price
        final_price = self.price - discount_amount
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"Original Price: {self.price}")
        print(f"Discount: {percent}%")
        print(f"Price After Discount: {final_price}")


p1 = Book("William Shakespeare", "Daffodils", 8900)
p1.discount(10)   # 10% discount

class Calulator:
    def __init__(self,A,B):
        self.A = A
        self.B = B
    def add(self):
        Add = self.A + self.B
        print(f"the sum of two numbers: {Add}")

    def sub(Self):
        Sub = Self.A - Self.B
        print(f"the substraction of two numbers: {Sub}")

    def div(Self):
        try:
            div = Self.A / Self.B
        except ZeroDivisionError as e:
            print("can't divide by zero")
        else:
            print(f"the division of two numbers: {div}")



p1  = Calulator(10,0)
p1.add()
p1.sub()
p1.div()
'''