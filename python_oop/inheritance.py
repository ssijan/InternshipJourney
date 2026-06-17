from pyhton_OOP_Django.python_oop.classAndObject import Person

class Student(Person):
    def __init__(self, name, age, varsity):
        super().__init__(name, age)
        self.varsity = varsity

    def info(self):
        return f"My varsity name is {self.varsity}"
    
obj = Student("Sijan", 24, "DIU")

    
print(Person.info(obj))
print(obj.info())

'''
Output:
    My name is Sijan. I am 24 years old!
    My varsity name is DIU
'''