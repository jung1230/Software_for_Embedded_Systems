num = int(input("How many Fibonacci numbers would you like to generate? "))

fib = [1]
if num == 1:
    print(fib)
fib = [1,1]
if num == 2:
    print(fib)

i = 0
while(i < (num -2)):
    fib.append(fib[i + 1] + fib[i])
    i += 1

print("The Fibonacci Sequence is:",fib)
