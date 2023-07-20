numOfNumbers = int(input("How many numbers would you like sorted?"))
numbers = []
for p in range (numOfNumbers):
    numbers.append(int(input("Please enter your numbers")))
import os
os.system('cls')
import time
bubble = True
start_time = time.time()
while bubble == True:
    for x in range(len(numbers) - 1):
        if numbers[x] < numbers[x + 1]:
            numbers[x + 1], numbers[x] = numbers[x], numbers[x + 1]
            print(numbers, 'Sorting...', time.time() - start_time)
            time.sleep(0.1)
