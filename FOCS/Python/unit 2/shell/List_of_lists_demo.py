example = [["A", "B", "C", "D"],
           ["E", "F", "G", "H"],
           ["I", "J", "K", "L"]]


#Printing a list of lists
print("This is what it looks like in the console when you print a list of lists directly:")
print(example)
print()

print("A somewhat nicer way to print:")
for row in example:
    print(row)
print()

print("Even better:")
for row in example:
    print(" ".join(row))
print()


#Modifying a list of lists
example[0][2] = "X"
#Row first then column!  Notice which value changes:
print("[0][2] has been changed to X:")
for row in example:
    print(" ".join(row))
print()


#Adding another list onto a list of lists
new_list = ["M", "N", "O", "P"]
example.append(new_list)
print("Another list appended:")
for row in example:
    print(" ".join(row))
print()


#Adding another letter onto each interior list:
letters_to_add = ["W", "X", "Y", "Z"]
for index, letter in enumerate(letters_to_add):
    example[index].append(letter)
print("Modified interior lists:")
for row in example:
    print(" ".join(row))
print()


#Try some more stuff; see if it behaves the way you expect!