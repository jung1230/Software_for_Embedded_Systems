class findPair:
    def find_pair(self, list, target):

        for i, num in enumerate(list):
            complement = target - num
            if complement in list:
                if list.index(complement) == i:
                    continue
                else:
                    return i, list.index(complement)
        return None

list = [10, 20, 10, 40, 50, 60, 70]

target = int(input("What is your target number? "))

# Create an instance of the findPair class
pair_finder = findPair()

# Call the find_pair method on the instance
index1, index2 = pair_finder.find_pair(list, target)

if index1 > index2:
    temp = index2
    index2 = index1
    index1 = temp

# Convert integers to strings before concatenating
print("index1=" + str(index1) + ", index2=" + str(index2))