from math import floor

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



def jaro_distance(mot1:str,mot2:str)->float:
    """
    Calcul la distance de jaro entre 2 mots
    """
    
    formule = floor(max(len(mot1), len(mot2)) / 2) - 1
    #Compteur de caractères correspondants
    m=0
    #Compteur de transpositions
    t=0

    #Cette liste qu'on va faire évoluer va nous permettre de compter le nombre de
    #transpositions par la suite
    check_mot1 = [0 for i in range(len(mot1))]
    index_mot1=0
    
    #Cette liste qu'on va faire évoluer va nous permettre de compter le nombre de
    #transpositions par la suite mais va aussi nous permettre de ne pas recompter les mêmes
    #lettres
    check_mot2 = [0 for i in range(len(mot2))]
    index_mot2=0
    
    while index_mot1 < len(mot1):
        #On commence par le premier mot
        index_mot2=0
        while index_mot2 < len(mot2):
            #Si les 2 mots sont égaux et qu'ils sont compris dans une fenetre d'indices
            #définie par formule et que la lettre n'a pas déja était compté dans le mot2 alors
            if mot1[index_mot1] == mot2[index_mot2] and abs(index_mot1 - index_mot2) <= formule and check_mot2[index_mot2] == 0:
                #On note l'emplacement dans le mot1
                check_mot1[index_mot1] =1
                #On note l'emplacement dans le mot2
                check_mot2[index_mot2] =1
                #On ajoute un caractère correspondant
                m+=1
                #On passe a la lettre suivante
                break
            
            #Sinon on continu à avancer dans le mot2  
            else:
                index_mot2+=1
        index_mot1+=1
        
    #---------------------------------------------------
    #On réinitialise nos index
    index_mot1=0
    index_mot2=0
    #On possède 2 listes, check_mot1 et check_mot2, qui nous indiquent quand un
    #caractère est présent avec un 1 et absent avec un 0
    while index_mot1 < len(mot1):
        
        #Si on ne trouve pas un caractere correspondant dans check_mot1
        #On passe au caractere suivant de mot1
        if check_mot1[index_mot1] == 0:
            index_mot1+=1
            continue # si on est pas au bon indice on recommence
        
        elif check_mot1[index_mot1]==1:
            #On a trouve un element dans mot1 qui est aussi dans mot2
            #Maintenant on cherche a savoir si ils sont dans le bon ordre
            
            #On parcours donc mot2 (la ou on s'est arreté)
            for j in range(index_mot2,len(mot2)):
                #Une fois qu'on trouve un nombre à 1 danc check_mot2 (qui nous indique donc
                #un caractere présent dans les 2 listes) on chercher a savoir si l'indice de
                #ce 1, donc lindice de la lettre correspondante dans mot2 est la meme que
                #la lettre presente dans mot1
                if check_mot2[index_mot2]==1 and mot1[index_mot1]!=mot2[index_mot2]:
                    #Si non il ya transposition
                    index_mot2+=1
                    t+=1
                    break
                elif check_mot2[index_mot2]==1 and mot1[index_mot1]==mot2[index_mot2]:
                    #Si oui il ny a pas de transposition tout est dans l'ordre
                    index_mot2+=1
                    break
                elif check_mot2[index_mot2]==0:
                    #On continue tant qu'on ne trouve pas un élément dans check_mot2
                    index_mot2+=1
                    continue
            index_mot1+=1
            
    if m==0:return 0 #pour eviter les divisions par 0
    if mot1==mot2:return 1 # les 2 mots sont identiques
    return 1 / 3 * (m / len(mot1) + m / len(mot2) + (m - t // 2) / m) 



def jaro_distance_V2(mot1: str, mot2: str, p=0.1) -> float:
    """
    Calcul la distance de jaro entre 2 mots
    Version améliorée d'après wikipédia
    """
    mot1 = mot1.lower()
    mot2 = mot2.lower()
    l = len_prefixe(mot1, mot2)
    #print(
      #  f"{jaro_distance(mot1, mot2)} + ({ l } * { p }* {(1 -jaro_distance(mot1,mot2))})"
    #)

    return jaro_distance(mot1, mot2) + (l * p * (1 - jaro_distance(mot1, mot2)))


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
            liste.append((i, jaro_distance(mot1, lexique[i])))
            #print(f"{mot1} et {lexique[i]}")
        except:
            print(f"erreur entre {mot1} et {lexique[i]}")
            continue
    # On trie la liste précédemnt créee mais en triant sur les distances
    # Donc le 2eme element de chaque tuple de la liste.
    # Puis on inverse le tri, pour avoir un ordre décroissant
    # Et on récupérere les 5 premiers tuple.
    liste = sorted(liste, key=lambda x: x[1], reverse=True)[:5]
    # Sur nos 5 tuples que l'ont a récupéré, on accède aux indices
    # et on renvoi les mots du lexique correspondant


    return [lexique[i[0]]  for i in liste]

def closest_word_oneliner(mot1,lexique):
    return list(map(lambda cpl:lexique[cpl[1]],sorted(list(map(lambda x:(jaro_distance(mot1,x[1]),x[0]),enumerate(lexique))),key=lambda x:x[0],reverse=True)))[:5]#waw


def correcteur(phrase:str, lexique: list, auto: bool = False) -> str:
    """
    Correcteur qui interagit directement avec l'utilisateur
    Idiot-proof
    """
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
    """
    Prend en charge l'ajout et la suppression de mots dans le lexique
    Interaction directe avec l'utilisateur
    idiot-proof
    """
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
    
    
if __name__=='__main__':
    main()
    
#----------------------------------------------------------------------------
#DEBUG

def _transposition(mot1,mot2):
    """
    Fonction _transposition debug
    """
    formule = floor(max(len(mot1), len(mot2)) / 2) - 1
    check_mot1 = [0 for i in range(len(mot1))]
    index_mot1=0
    index_mot2=0
    check_mot2 = [0 for i in range(len(mot2))]
    while index_mot1 < len(mot1):
        index_mot2=0
        while index_mot2 < len(mot2):
            if mot1[index_mot1] == mot2[index_mot2] and abs(index_mot1 - index_mot2) <= formule and check_mot2[index_mot2] == 0:
                check_mot1[index_mot1] =1
                check_mot2[index_mot2] =1
                break
            else:
                index_mot2+=1
        index_mot1+=1
        
    t=0
    index_mot1=0
    index_mot2=0
    while index_mot1 < len(mot1):
        if check_mot1[index_mot1] == 0:
            index_mot1+=1
            continue 
        elif check_mot1[index_mot1]==1:
            for j in range(index_mot2,len(mot2)):
                if check_mot2[index_mot2]==1 and mot1[index_mot1]!=mot2[index_mot2]:
                    index_mot2+=1
                    t+=1
                    break
                elif check_mot2[index_mot2]==1 and mot1[index_mot1]==mot2[index_mot2]:
                    index_mot2+=1
                    break
                elif check_mot2[index_mot2]==0:
                    index_mot2+=1
                    continue
            index_mot1+=1
            
    return t

def _caractere(mot1,mot2):
    """
    fonction caractere debug
    """
    formule = floor(max(len(mot1), len(mot2)) / 2) - 1
    index_mot1=0
    index_mot2=0
    m=0
    check_mot2 = [0 for i in range(len(mot2))]
    while index_mot1 < len(mot1):
        index_mot2=0
        while index_mot2 < len(mot2):
            if mot1[index_mot1] == mot2[index_mot2] and abs(index_mot1 - index_mot2) <= formule and check_mot2[index_mot2] == 0:
                m+=1
                check_mot2[index_mot2]=1
                break
            else:
                index_mot2+=1
        index_mot1+=1
    return m


def check():
    try:
        assert _caractere("plenchet","penche")==6
        assert _caractere("plenchet","planche")==6
        assert _caractere("plenchet","plancher")==6
        assert _caractere("penche","plenchet")==6
        assert _caractere("planche","plenchet")==6
        assert _caractere("plancher","plenchet")==6

        
        assert _caractere("bonjeur","bonheur")==6
        assert _caractere("bonjeur","bonjour")==6
        assert _caractere("bonjeur","boxeur")==5
        assert _caractere("bonheur","bonjeur")==6
        assert _caractere("bonjour","bonjeur")==6
        assert _caractere("boxeur","bonjeur")==5

        assert _caractere("tabble","table")==5
        assert _caractere("tabble","tables")==5
        assert _caractere("tabble","tableau")==5
        assert _caractere("table","tabble")==5
        assert _caractere("tables","tabble")==5
        assert _caractere("tableau","tabble")==5

        
        assert _transposition("plenchet","penche")==0
        assert _transposition("plenchet","planche")==0
        assert _transposition("plenchet","plancher")==0

        assert _transposition("bonjeur","bonheur")==0
        assert _transposition("bonjeur","bonjour")==0
        assert _transposition("bonjeur","boxeur")==0

        assert _transposition("tabble","table")==0
        assert _transposition("tabble","tables")==0
        assert _transposition("tabble","tableau")==0

        assert closest_word("plenchet",load_lexicon("lexicon.txt")) == ['penche', 'planche', 'plancher', 'pleine', 'blanche']
        assert closest_word("tabble",load_lexicon("lexicon.txt")) == ['table', 'tables', 'tableau', 'bible', 'sable']
        assert closest_word("bonjeur",load_lexicon("lexicon.txt")) == ['bonheur', 'bonjour', 'boxeur', 'bon', 'honneur']
        return "kek"
    except AssertionError:
        return "too bad"
