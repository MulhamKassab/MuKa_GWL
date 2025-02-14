# Task 11 - making a grade system
point = input("Give me a point:\n")
if int(point) >= 90:
    print("You got an A")
elif int(point) >= 75:
    print("You got an B")
elif int(point) >= 60:
    print("You got an C")
elif int(point) >= 45:
    print("You got an D")
else:
    print("You got an E")

print("")
