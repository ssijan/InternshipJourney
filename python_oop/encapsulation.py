class BankAccount:
    def __init__(self, name, balance = 0):
        self.name = name
        self.__balance = balance

    # using decorator property
    @property
    def deposit(self):
        return self.__balance
    
    @deposit.setter
    def deposit(self, balance):
        self.__balance += balance if balance > 0 else 0
    
    def get_balance(self):
        return f"Name: {self.name} \nBalance: {self.__balance}"
    

obj = BankAccount("Sijan", 500000)
print(obj.get_balance(), end='\n\n')

obj.deposit = 500
print(obj.get_balance())

'''
output:
    Name: Sijan 
    Balance: 500000

    Name: Sijan 
    Balance: 500500
'''
        