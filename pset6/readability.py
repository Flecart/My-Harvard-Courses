from cs50 import *

text = get_string("Text: ")

array_words = text.split(" ")

words = len(array_words)

sentences = 0
letters = 0
for word in array_words:

    # check if at the end of the word there is a end of sentence
    if word[-1] == "!" or word[-1] == "?" or word[-1] == ".":
        sentences += 1
        word = word[:-1]

    # after i removed that, i check for word len
    for char in word:
        if char.isalpha():
            letters += 1


# average of letters per 100 words in the text
L = letters / words * 100

# the average number of sentences per 100 words in the text
S = sentences / words * 100

grade = int(round(0.0588 * L - 0.296 * S - 15.8))

# printing out the grades as i should do
if grade < 1:
    print('Before Grade 1')
elif grade > 16:
    print("Grade 16+")
else:
    print(f"Grade {grade}")