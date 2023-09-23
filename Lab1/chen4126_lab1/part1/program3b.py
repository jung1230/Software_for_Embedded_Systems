import random

rand = random.randint(0, 10)
# print(rand)
temp = 0
for i in range (3):
    num = int(input("Enter your guess: "))
    if(num == rand):
        temp = 1
        break

if(temp == 1):     
    print("You win!")
else:     
    print("You lose!")

