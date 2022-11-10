import math
from main import load_lexicon

def caractere_debug(mot1,mot2):
    liste_mot = []
    formule = math.floor(max(len(mot1), len(mot2)) / 2) - 1
    print(formule)
    m=0
    check_mot1 = [0] * len(mot1)# On veut éviter de compter 2 fois les mêmes élements
    # par exemeple pour plenchet et penche
    # on ne veut pas un duplicata des 2 e à pEnche et plEnchet
    check_mot2 = [0] * len(mot2) # a enlever
    for i in range(len(mot1)):
        for j in range(len(mot2)):
            if mot1[i] == mot2[j] and abs(i - j) <= formule and check_mot2[j] == 0:
                liste_mot.append(mot1[i])
                check_mot1[i] =1
                check_mot2[j] =1 # a enlever
                m+=1
                print(mot1[i],mot2[j],check_mot1,"+1")
                break#si on a trouve le mot on sarrette
            elif abs(i - j) > formule:
                print(mot1[i],mot2[j],check_mot1,"STP")
            else:
                print(mot1[i],mot2[j],check_mot1)

        print("-"*50)
    print(liste_mot,check_mot1,check_mot2,sep='\n')
#     if len(check_mot1) < len(check_mot2):
#         m=check_mot1.count(1)
#     else:
#         m=check_mot2.count(1)
            
    return check_mot1,check_mot2,m

def caractere(mot1,mot2):
    formule = math.floor(max(len(mot1), len(mot2)) / 2) - 1
    m=0

    check_mot1 = [0] * len(mot1)#compteur de lettre par indice pr le mot1
    # On veut éviter de compter 2 fois les mêmes élements
    # Par exemple: on ne veut pas un duplicata des 2 e à pEnche et plEnchet
    check_mot2 = [0] * len(mot2)#compteur de lettre par indice pr le mot1
    for i in range(len(mot1)):
        #on commence par le premier mot
        for j in range(len(mot2)):
            if mot1[i] == mot2[j] and abs(i - j) <= formule and check_mot2[j] == 0:
                #si les 2 mots sont égaux et qu'ils sont compris dans une fenetre définie
                #par formule et que la lettre n'a pas déja était compté dans le mot2
                check_mot1[i] +=1
                check_mot2[j] +=1 
                m+=1
                break#on sarrete car on a trouvé nos 2 lettres correspondantes
                #on passe donc a la lettre suivante du mot1
    
 
    return check_mot1,check_mot2,m

def transposition_debug(mot1,mot2):
    check_mot1,check_mot2,m=caractere(mot1,mot2)
    t=0
    index_mot1=0
    index_mot2=0
    print(check_mot1,check_mot2,sep='\n')
    while index_mot1 < len(mot1):
        if check_mot1[index_mot1] == 0:
            index_mot1+=1
            continue # si on est pas au bon indice on recommence
        elif check_mot1[index_mot1]>=1:
            # on a trouve un element dans mot1 qui est aussi dans mot2
            #maintenant on parcours mot2
            # tant quon a pas trouve un element >=1 dans matricemot2 on parcours
            # si on trouve un nombre>=1 dans matricemot2 ça veux dire quon a trouve
            #un element dans mot2 qui est aussi dans mot1
            #on regarde si ces elements sont correspondants, si non il ya une transposition
            #si oui il nya pas de transposition
            for j in range(index_mot2,len(mot2)):
                if check_mot2[index_mot2]>=1 and mot1[index_mot1]!=mot2[index_mot2]:
                    index_mot2+=1
                    t+=1
                    #si on a:
                    #- trouve un element qui est present dans le meme ordre
                    #
                    #on a trouvé 2 caractères pas correspondants
                    #print(mot1[index_mot1],mot2[index_mot2])
                    #print(index_mot1,index_mot2)
                    #print('-'*10)
                    break
                elif check_mot2[index_mot2]>=1 and mot1[index_mot1]==mot2[index_mot2]:
                    index_mot2+=1
                    break
                elif check_mot2[index_mot2]==0:
                    #on continue tant quon trouve pas un élément dans check_mot2
                    index_mot2+=1
                    continue
            index_mot1+=1
    return t//2

def transposition(mot1,mot2):
    check_mot1,check_mot2,m=caractere(mot1,mot2)
    t=0
    index_mot1=0
    index_mot2=0
    while index_mot1 < len(mot1):
        if check_mot1[index_mot1] == 0:
            index_mot1+=1
            continue # si on est pas au bon indice on recommence
        elif check_mot1[index_mot1]>=1:
            # on a trouve un element dans mot1 qui est aussi dans mot2
            #maintenant on parcours mot2
            # tant quon a pas trouve un element >=1 dans matricemot2 on parcours
            # si on trouve un nombre>=1 dans matricemot2 ça veux dire quon a trouve
            #un element dans mot2 qui est aussi dans mot1
            #on regarde si ces elements sont correspondants, si non il ya une transposition
            #si oui il nya pas de transposition
            for j in range(index_mot2,len(mot2)):
                if check_mot2[index_mot2]==1 and mot1[index_mot1]!=mot2[index_mot2]:
                    index_mot2+=1
                    t+=1#on a trouvé 2 caractères pas correspondants
                    #print(mot1[index_mot1],mot2[index_mot2])
                    #print(index_mot1,index_mot2)
                    #print('-'*10)
                    break
                elif check_mot2[index_mot2]==1 and mot1[index_mot1]==mot2[index_mot2]:
                    #on a trouvé 2 caractères présents dans les 2 listes
                    #mais dans la mauvais ordre
                    index_mot2+=1
                    break
                elif check_mot2[index_mot2]==0:
                    #on continue tant quon trouvve pas un élément dans matricemot2
                    index_mot2+=1
                    continue
            index_mot1+=1
    return t//2
                    
        
def closest_word(mot1: str, lexique: list) -> list:
    mot1 = mot1.lower()
    liste = []
    for i in range(len(lexique)):
        liste.append((i, jaro(mot1, lexique[i])))

    liste = sorted(liste, key=lambda x: x[1], reverse=True)[:5]
    # Sur nos 5 tuples que l'ont a récupéré, on accède aux indices
    # et on renvoi les mots du lexique correspondant


    return [lexique[i[0]]  for i in liste]

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
#planche: m=6 t=0
#plancher: m=6 t=0

def check():
    try:
        assert caractere("plenchet","penche")[2]==6
        assert caractere("plenchet","planche")[2]==6
        assert caractere("plenchet","plancher")[2]==6
        
        assert caractere("bonjeur","bonheur")[2]==6
        assert caractere("bonjeur","bonjour")[2]==6
        assert caractere("bonjeur","boxeur")[2]==5

        assert caractere("tabble","table")[2]==5
        assert caractere("tabble","tables")[2]==5
        assert caractere("tabble","tableau")[2]==5
        
        assert transposition("plenchet","penche")==0
        assert transposition("plenchet","planche")==0
        assert transposition("plenchet","plancher")==0

        assert transposition("bonjeur","bonheur")==0
        assert transposition("bonjeur","bonjour")==0
        assert transposition("bonjeur","boxeur")==0

        assert transposition("tabble","table")==0
        assert transposition("tabble","tables")==0
        assert transposition("tabble","tableau")==0

        

        
        assert transposition("bien", "bienvenu")== 0
        assert transposition("bien", "bienvenue")== 0
        assert transposition("cant", "chaton") == 0
        assert transposition("duane", "dwayne") == 0
        assert transposition("dixon", "dicksonx") == 0
        assert transposition("xabcdxxxxxx", "yaybycydyyyyyy") == 0
        assert caractere("plenchet","place")[2]==4
        assert closest_word("plenchet",load_lexicon("lexicon.txt")) == ['penche', 'planche', 'plancher', 'pleine', 'blanche']
        assert closest_word("tabble",load_lexicon("lexicon.txt")) == ['table', 'tables', 'tableau', 'bible', 'sable']
        assert closest_word("bonjeur",load_lexicon("lexicon.txt")) == ['bonheur', 'bonjour', 'boxeur', 'bon', 'honneur']
        return "kek"
    except AssertionError:
        return "too bad"
    



def jaro(mot1, mot2):
    t=transposition(mot1,mot2)
    m=caractere(mot1,mot2)[2]
    if m == 0:
        return 0
    #print(f"1 / 3 * ({m} / {len(mot1)} + {m} / {len(mot2)} + ({m} - {t}) / {m})")
    #print(f"{m} et {t}")
    return 1 / 3 * (m / len(mot1) + m / len(mot2) + (m - t) / m)






