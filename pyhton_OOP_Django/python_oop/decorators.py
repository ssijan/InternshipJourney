def money_converter(func):
    def wrapper(amount, type):
        if type == 'BDT':
            amount = amount * 0.0081
        elif type =='EUR':
            amount = amount * 1.16
        res = func(amount)
        
        return round(res, 2)
    return wrapper

@money_converter
def tax(value):
    return value + value * 0.2

total = tax(1000, 'BDT')
print(total)

'''
output:
    9.72
'''