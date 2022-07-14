import pandas as pd
import math

word_length = 6

df = pd.read_csv("./paroleitaliane/parole_uniche.csv")

znane = "______"
mozne = ""
ne_mozne = ""
mozne_ampak_ne_na_mestu_x = ["", "", "", "", "", ""]
guessed_words = [""]

word5 = [w[0].lower() for w in df.values if len(str(w[0])) == word_length and w[0].lower() not in guessed_words]

poss = [w for w in word5 if all(znana == c for znana, c in zip(znane, w) if znana != "_") and not any(ne_mozna in w for ne_mozna in ne_mozne) and all(mozna in w for mozna in mozne) and not any(any(m == w[i] for m in position) for i, position in enumerate(mozne_ampak_ne_na_mestu_x) if i < word_length)]



print(f"Ci sono {len(poss)} parole possibili")
print(poss)

def get_mask(guess, answer):
    # Mask defaults to all wrong and convert strings to lists
    guess = list(guess)
    answer = list(answer)
    mask = [0] * word_length

    # If exact match
    for i in range(word_length):
        if guess[i] == answer[i]:
            mask[i] = 2
            guess[i] = 'X'     # Make sure it doesn't get double counted
            answer[i] = 'Y'

    # Find anything in wrong spot
    for i,l in enumerate(guess):
        try:
            j = answer.index(l)
            mask[i] = 1
            answer[j] = 'Y'
        except ValueError as err:
            pass
    
    # Convert to number (little-endian, so it reads the same way it was typed in)
    mask.reverse()
    return sum([(10**i)*v for i,v in enumerate(mask)])

def make_guess(guessing_list, answer_list):

    if len(answer_list) <= 2:
        return answer_list[0]

    results = []
    max_entropy = -1
    best_guess = "idk"

    for guess_index, guess in enumerate(guessing_list):
        #print(best_guess)
        bins = {}
        for a in answer_list:
            mask = get_mask(guess, a)
            if not mask in bins.keys():
                bins[mask] = 1
            else:
                bins[mask] += 1

        # Replace best guess if there's a word with better entropy
        new_entropy = compute_entropy(bins.values())
        results.append([guess, new_entropy])
        if new_entropy > max_entropy:
            max_entropy = new_entropy
            best_guess = guess

    df_rez = pd.DataFrame(results, columns=["guess", "entropy"])
    df_rez = df_rez.sort_values(by='entropy', ascending = False)
    print(df_rez.head(50))

    return best_guess

def compute_entropy(int_list):
    total = sum(int_list)
    entropy = 0.0

    for i in int_list:
        p = i / total
        entropy -= math.log(p) * p

    return entropy

print("Parole ottimali che coincidono con le attuali restrizioni.")
print(make_guess(poss, poss))
print("Parole ottimali che non coincidono con le attuali restrizioni.")
print(make_guess(word5, poss))