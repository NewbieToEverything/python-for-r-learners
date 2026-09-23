print("----ex1----")
s1 = "mit u rock"
s2 = "i rule mit"
if len(s1) == len(s2):
    for char1 in s1:
        for char2 in s2:
            if char1 == char2:
                print("common letter")
            break

print("----ex2----")

cube = 8
for guess in range(cube + 1):
    if guess**3 == cube:
        print("Cube root of", cube, "is", guess)

print("----ex3----")

cube = 8
for guess in range(abs(cube)+1):
    if guess**3 >= abs(cube):
        break
    if guess**3 != abs(cube):
        print(cube, 'is not a perfect cube')
    else:
        if cube < 0:
            guess = -guess
            print('Cube root of '+str(cube)+' is '+str(guess))

print("----ex4----")

cube = 27
epsilon = 0.01
guess = 0.0
increment = 0.0001
num_guesses = 0
while abs(guess**3 - cube) >= epsilon and guess <= cube :
    guess += increment
    num_guesses += 1
    print('num_guesses =', num_guesses)
    if abs(guess**3 - cube) >= epsilon:
        print('Failed on cube root of', cube)
    else:
        print(guess, 'is close to the cube root of', cube)