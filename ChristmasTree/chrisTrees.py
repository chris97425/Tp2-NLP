#Version python 3.5.0

def chrisTrees(hauteur):
    '''
Hauteur:  pour la hauteur de l'arbre
bool: si true permet d'écrire l'arbre dans un fichier texte sinon un print de chrisTrees(10,false) affiche l'arbre en console
addSpace: permet à chaque étape de la boucle "for" d'enlever un espace
christmasTree: résultat final

Démarche: À chaque itération j'enlève un espace et j'ajoute 2 étoiles à l'arbre,
           pour le tronc je précise qu'à chaque fois que je tombe sur un modulo 10 valant
            0 j'incrémente le tronc de 2 et aussi j'augmente ma variable decalForEnd qui me
            permet de savoir combien d'espace j'ai à enlevé.

            '''
    addSpace = hauteur
    baseTree = 1
    decalForEnd = 0
    christmasTree=""

    for i in range(0,hauteur):

        christmasTree += hilite(addSpace*" "+i*"*"+"*"+i*"*"+"\n",2)
        addSpace-=1
        if(i!=0 and i%10==0):

            baseTree+=2
            decalForEnd+=1

    christmasTree+=hilite((hauteur-decalForEnd)*" "+baseTree*"*",1)

    return christmasTree

def hilite(string, status):
    attr = []
    if (status==1):
        # green
        attr.append('33')
    else:
        # red
        attr.append('32')


    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)

print(chrisTrees(12))
# help(chrisTrees)
