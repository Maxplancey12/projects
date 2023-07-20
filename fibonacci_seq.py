def fibonacci_seq(n):
    fib_seq = [0, 1]
    for i in range(2, n):
        fib_seq.append(fib_seq[i-1] + fib_seq[i-2])
    return fib_seq[:n]

n = int(input("How many digits of the Fibonacci sequence would you like to output? "))
print(fibonacci_seq(n))
