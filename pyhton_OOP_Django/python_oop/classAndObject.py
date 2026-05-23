class Person:
    def __init__(self, name, age):
        self.name = name 
        self.age = age 
    
    def info(self):
        return f"My name is {self.name}. I am {self.age} years old!"


# obj1 = Person("Sijan", 24)
# obj2 = Person("Foysal", 17)

# print(obj1.info())
# print(obj2.info())
# obj2.name = 'Mahin'
# print(obj2.info())

'''
Output:
    My name is Sijan. I am 24 years old!
    My name is Foysal. I am 17 years old!
    My name is Mahin. I am 17 years old!
'''
