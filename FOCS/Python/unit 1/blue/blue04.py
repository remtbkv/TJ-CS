'''
def avg_3(x, y, z):
    d=(x+y+z)/3
    print(d)

def string_is_blah():
    if input()=="blah":
        print("True")
    else:
        return print("False")
'''
def guess(lower_bound, upper_bound):
    avg = (lower_bound + upper_bound)//2
    print("I think this is your number:", avg)
    choice = input("correct / low / high ", )
    if choice == "correct":
        print("I guessed your number!")
    elif choice == "low":
        guess((avg + 1), upper_bound)
    elif choice == "high":
        guess(lower_bound, (avg- 1))

def guess2(lower_bound, upper_bound, guess_count=0):
    avg = (lower_bound + upper_bound)//2
    print("I think this is your number:", avg)
    choice = input("correct / low / high ", )
    if choice == "correct":
        print("I guessed your number! It took this many guesses", guess_count+1)
    elif choice == "low":
        guess2((avg + 1), upper_bound, guess_count+1)
    elif choice == "high":
        guess2(lower_bound, (avg- 1), guess_count+1)
guess2(0, 100)