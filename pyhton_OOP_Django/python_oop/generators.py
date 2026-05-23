def cal(n):
    if not n:
        yield 0
        return
    
    yield from cal(n-1)
    yield n

print(list(cal(10)))
print("Sum of 0 to 10:",sum(cal(10)))

'''
output:
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    Sum of 0 to 10: 55
'''