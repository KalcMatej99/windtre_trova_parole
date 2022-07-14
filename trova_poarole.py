import pandas as pd
import math

df = pd.read_csv("./paroleitaliane/parole_uniche.csv")


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

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]



word_length = input("Inserisci la lungezza della parola da indovinare:")

parole_provate = []
znane = "_" * word_length
mozne = []
ne_mozne = []
mozne_ampak_ne_na_mestu_x = [[], [], [], [], [], []]

for linea in range(6):
    print("Linea", linea)
    parola_provata = input("Inserisci la parola provata:")
    print("Risultato della parola provata è una sequenza di numeri. Il numero 0 indica la lettera non esiste (colore grigio). Il numero 1 indica la lettera esiste ma non nella coretta posizione (colore blu). Il numero 2 indica la lettera esiste nella coretta posizione (colore arancione). Esempio per 'reati' -> 00210.")
    risultato_parola_provata = input("Inserisci il risultato della parola provata:")

    parole_provate.append(parola_provata)

    indici_per_caratteri_coretti = find(risultato_parola_provata, "2")

    for indice_per_carattere_coretto in indici_per_caratteri_coretti:
        znane[indice_per_carattere_coretto] = parola_provata[indice_per_carattere_coretto]


    indici_per_caratteri_possibili = find(risultato_parola_provata, "1")
    for indice_per_carattere_possibile in indici_per_caratteri_possibili:
        mozne.append(parola_provata[indice_per_carattere_possibile])
        mozne_ampak_ne_na_mestu_x[indice_per_carattere_possibile].append(parola_provata[indice_per_carattere_possibile])

    
    indici_per_caratteri_non_possibili = find(risultato_parola_provata, "0")
    for indice_per_carattere_non_possibile in indici_per_caratteri_non_possibili:

        if parola_provata[indice_per_carattere_non_possibile] in znane:
            indici_per_carattere_risaputo = find(risultato_parola_provata, parola_provata[indice_per_carattere_non_possibile])
            for i in range(word_length):
                if i not in indici_per_carattere_risaputo: mozne_ampak_ne_na_mestu_x[i].append(parola_provata[indice_per_carattere_non_possibile])


        elif parola_provata[indice_per_carattere_non_possibile] in mozne:
            mozne_ampak_ne_na_mestu_x[indice_per_carattere_non_possibile].append(parola_provata[indice_per_carattere_non_possibile])
        else:
            ne_mozne.append(parola_provata[indice_per_carattere_non_possibile])

    word5 = [w[0].lower() for w in df.values if len(str(w[0])) == word_length and w[0].lower() not in parole_provate]

    poss = [w for w in word5 if all(znana == c for znana, c in zip(znane, w) if znana != "_") and not any(ne_mozna in w for ne_mozna in ne_mozne) and all(mozna in w for mozna in mozne) and not any(any(m == w[i] for m in position) for i, position in enumerate(mozne_ampak_ne_na_mestu_x) if i < word_length)]

    print(f"Ci sono {len(poss)} parole possibili")

    print(poss)

    print("Parole ottimali che coincidono con le attuali restrizioni.")
    print(make_guess(poss, poss))
    print("Parole ottimali che non coincidono con le attuali restrizioni.")
    print(make_guess(word5, poss))