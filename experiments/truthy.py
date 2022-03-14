import random
for _ in range(20):
     x = random.randint(0, 1)
     print(x)
     if x == True:
         print(f"{x} is True")
     elif x == False:
         print(f"{x} is False")
   