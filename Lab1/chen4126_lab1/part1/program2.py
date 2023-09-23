a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
num = int(input("Enter number: "))

# Use a while loop to iterate over the list
i = 0
while i < len(a):
    if a[i] >= num:
        a.remove(a[i])
    else:
        i += 1

print("The new list is", a)
