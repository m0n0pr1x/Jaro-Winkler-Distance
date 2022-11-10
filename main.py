import math
import string

def load_lexicon(path: str = "lexicon.txt", mode: str = "r") -> list:
    """
    Charge le fichier fourni dans path, qui par défaut prend la valeur
    lexicon.txt
    Et renvoi une liste contenant tous les mots du lexique
    """
    with open(path, mode) as f:
        content_list = f.read().splitlines()
    return content_list


def check_word(lexique: str, mot: str) -> bool:
    """
    Regarde si le paramètre mot est dans le lexique fourni aussi en paramètre
    """
    mot = mot.lower()
    return mot in lexique


def len_prefixe(mot1: str, mot2: str) -> int:
    """
    Calcule la longueur du prefix du mot le plus petit dans le mot le plus grand
    Avec la longueur inférieur ou égale à 4, d'après wikipédia
    """
    total = 0
    for i in range(min(len(mot1), len(mot2))):
        if mot1[i] != mot2[i]:
            return total
        total += 1

    # Condition pour respecter la condition de la longueur inférieur à 4
    if total > 4:
        total = 4
    return total


def jaro(mot1, mot2):
    # Determination de m
    liste_mot = []
    formule = math.floor(max(len(mot1), len(mot2)) / 2) - 1

    check_mot1 = [False] * len(mot1)# On veut éviter de compter 2 fois les mêmes élements
    for i in range(len(mot1)):
        for j in range(len(mot2)):
            #print(mot1[i],mot2[j],check_mot1)
            if mot1[i] == mot2[j] and abs(i - j) <= formule and check_mot1[i] == False:
                liste_mot.append(mot1[i])
                check_mot1[i] = True
            

    # Transpositions
    liste_mot_mot1 = []
    liste_mot_mot2 = []
    for i in mot1:
        if i in liste_mot:# and not(i in liste_mot_mot1):
            liste_mot_mot1.append(i)

    for i in mot2:
        if i in liste_mot:#: and not(i in liste_mot_mot2):
            liste_mot_mot2.append(i)
            

            
    m=min(len(liste_mot_mot1),len(liste_mot_mot2))# On prend le minimum pour éviter les erreurs d'indices
    t = 0
    for i in range(m):
        if (
            liste_mot_mot1[i] != liste_mot_mot2[i]
        ): 
            t += 1


    #return liste_mot_mot1,liste_mot_mot2,liste_mot,m,t//2
    if m == 0:
        return 0
    #print(f"1 / 3 * ({m} / {len(mot1)} + {m} / {len(mot2)} + ({m} - {t//2}) / {m})")
    return 1 / 3 * (m / len(mot1) + m / len(mot2) + (m - t // 2) / m)


#assert jaro("bien", "bienvenu")[1] == 0
#assert jaro("bien", "bienvenue")[1] == 0
#assert jaro("cant", "chaton")[1] == 0
#assert jaro("duane", "dwayne")[1] == 0
#assert jaro("dixon", "dicksonx")[1] == 0
#assert jaro("xabcdxxxxxx", "yaybycydyyyyyy")[1] == 0

# def generateur_test():
#     alphabet = string.ascii_lowercase
#     for _ in range(100):
#         len_random1 = random.randint(4, 15)
#         len_random2 = random.randint(4, 15)
#         mot1 = "".join([random.choice(alphabet) for i in range(len_random1)])
#         mot2 = "".join([random.choice(alphabet) for i in range(len_random2)])
#         


def jaro2(mot1: str, mot2: str, p=0.1) -> float:
    """
    Calcul la distance de jaro entre 2 mots
    Version améliorée d'après wikipédia
    """
    mot1 = mot1.lower()
    mot2 = mot2.lower()
    l = len_prefixe(mot1, mot2)
    #print(
      #  f"{jaro(mot1, mot2)} + ({ l } * { p }* {(1 -jaro(mot1,mot2))})"
    #)

    return jaro(mot1, mot2) + (l * p * (1 - jaro(mot1, mot2)))


def closest_word(mot1: str, lexique: list) -> list:
    """
    Renvoi 5 mots du lexique dont la distance de jaro est la plus
    élevé avec le mot fourni en paramètre
    """
    mot1 = mot1.lower()
    liste = []
    # On créé une liste avec pour chaque mot du lexique, un tuple
    # contenant l'indice du mot et sa distance avec le mot fourni
    # en paramètre.
    for i in range(len(lexique)):
        try:
            liste.append((i, jaro(mot1, lexique[i])))
            #print(f"{mot1} et {lexique[i]}")
        except:
         #   print(f"erreur entre {mot1} et {lexique[i]}")
            continue
    # On trie la liste précédemnt créee mais en triant sur les distances
    # Donc le 2eme element de chaque tuple de la liste.
    # Puis on inverse le tri, pour avoir un ordre décroissant
    # Et on récupérere les 5 premiers tuple.
    liste = sorted(liste, key=lambda x: x[1], reverse=True)[:5]
    # Sur nos 5 tuples que l'ont a récupéré, on accède aux indices
    # et on renvoi les mots du lexique correspondant


    return [lexique[i[0]]  for i in liste]


def correcteur(phrase, lexique: list, auto: bool = False) -> str:
    phrase = phrase.split()
    if auto is True:
        for i in range(len(phrase)):
            choix = closest_word(phrase[i], lexique)
            phrase[i] = choix[0]
        return " ".join(phrase)
    else:
        for i in range(len(phrase)):
            # Si le mot n'est pas dans le lexique
            if check_word(lexique, phrase[i]) is False:
                choix = closest_word(phrase[i], lexique)+[phrase[i]]
                print("choisir le mot grâce à son indice")
                while True:  # tant que le input n'est pas bon
                    try:
                        print(f"{phrase[i]}->{choix}")
                        indice = int(input("indice: "))
                        phrase[i] = choix[indice]
                    except IndexError:
                        print("L'indice doit être compris entre 0 et 5")
                        continue
                    except ValueError:
                        print("L'indice doit être un int ")
                        continue
                    except KeyboardInterrupt:
                        return " ".join(phrase)

                    break

        return " ".join(phrase)


def gestion_lexique(lexique: list, path: str = "lexicon.txt"):
    print('Vous pouvez soit supprimer soit ajouter un mot')
    print('Pour supprimez tapez  0')
    print('Pour ajoutez tapez 1')
    while 42:
        try:
            check = int(input("action: "))
        except ValueError:
            print("Un indice, soit 0 pour supprimer soit 1 pour ajouter")
            continue
        if check < 0 or check > 1:
            print("Un indice, soit 0 pour supprimer soit 1 pour ajouter")
            continue
        if check == 0:
            try:
                lexique.remove(input("mot: ").lower())
            except ValueError:
                print("le mot n'est pas dans la liste\n")
                continue
        if check == 1:
            mot = input("mot: ").lower()
            if not(mot in lexique):
                lexique.append(mot)
            else:
                print("mot déja présent dans le lexique")
                continue
        print("Voulez vous ajouter ou supprimer un autre mot [oui|non]")
        ouinon = input("")
        if ouinon in ["Oui", "oui", "y", "Y", "o", "O"]:
            continue
        else:
            break
    lexique=sorted(lexique)
    with open(path, "w") as f:
        for mot in lexique:
            f.write(mot + "\n")


def main():
    lexique = load_lexicon()
    if input("Modifier le lexique ?[Oui|Non]\n") in ["Oui", "oui", "y", "Y", "o", "O"]:
        gestion_lexique(lexique)
    phrase = input("Phrase à corriger:\n")
    print(correcteur(phrase, lexique))
    
# `bonjeur` -> `bonheur`, `bonjour`, `boxeur`
#bonheur: m=6 t=0
#bonjour: m=6 t=0
#bonjeur: m=5 t=0
# `tabble` -> `table`, `tables`, `tableau`
#table:  m=5 t=0
#tables: m=5 t=0
#taleau: m=5 t=0
# `plenchet` -> `penche`, `planche`, `plancher`
#penche: m=6 t=0
#planche: m=7 t=0
#plancher: m=6 t=0

#assert closest_word("plenchet",load_lexicon("lexicon.txt"))[:3]==['penche', 'planche', 'plancher']
#assert closest_word("tabble",load_lexicon("lexicon.txt"))[:3]==['table', 'tables', 'tableau']
#assert closest_word("bonjeur",load_lexicon("lexicon.txt"))[:3]==['bonheur', 'bonjour', 'boxeur']




