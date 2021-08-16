from sys import argv, exit
import csv


def main():

    # checking if arguments are right
    check_argv()

    # creating dict of people with their sequences
    people, sequences = load_people()

    # dict of counted sequences
    count = count_STR(sequences)

    # checking if there are any matches
    check_matches(people, count)


# checking maches


def check_matches(people, count):

    for person in people:
        # variable to see if there is a match
        # if later counts will be different, this will be set to false
        match = True
        for sequence in count:

            # exit from cicle and go to next if its different?
            if person[sequence] != count[sequence]:
                match = False
                break

        if match:
            print(person['name'])
            return

    # if there were no matches i exit with negative output
    print("No match")
    return


# checking if arguments are right


def check_argv():
    if len(argv) != 3:
        print("USAGE: python dna.py ./csvfile ./dnasequence")
        exit()

    return


# returning array of people with their dna


def load_people():
    people = []
    possible_sequences = set()
    with open(argv[1], "r") as file:
        reader = csv.DictReader(file)
        for line in reader:

            # transform in number
            for key in line:
                if key != 'name':
                    possible_sequences.add(key)
                    line[key] = int(line[key])

            people.append(line)

    return people, possible_sequences


# returning number of sequences found
# INPUT  the sequences to look for


def count_STR(sequences):

    # initialize the values
    count = {}
    for seq in sequences:
        count[seq] = 0

    # loading the sequence
    with open(argv[2], "r") as file:
        seqstring = file.read()

    # counting for each sequence
    for key in count:
        count[key] = count_consecutive_sequence(key, seqstring)

    return count

# helper function for count_STR


def count_consecutive_sequence(key, sequence):

    # coutner conto attuale e longest sequence quella dopo
    longest_sequence = 0
    counter = 0

    # preferisco while perché controllo meglio index con cui si sposta
    i = 0
    keyLen = len(key)
    seqLen = len(sequence)

    # i < seqLen - keyLen perché tanto dopo nonce spazio per altre occorrenze
    while i < seqLen - keyLen:
        if (sequence[i:i + keyLen] == key):
            counter += 1
            i += keyLen
        else:
            # non è più consecutiva e quindi resetto i valori
            longest_sequence = max(longest_sequence, counter)
            counter = 0
            i += 1

    return longest_sequence


main()