#################################################################################################
#                                                                                               #
#                               Projet INF402                                                   #
#                           Université Grenoble Alpes                                           #
#                                                                                               #
#                 AlSABR Ibrahim  -  MAFADI Ziad  -  VITTET Brice                               #
#                                                                                               #
#                                                                                               #
#################################################################################################


from colorama import Fore
import string

#Le fichier qui contient le SAT solveur
from solveur import SAT_Solveur

#Le fichier qui génère les tableaux
from tableau import Tableau

class Squaro:

    def __init__(self, dimension, output, tableau=None):

        #Initialiser le Solveur SAT
        self.solver = SAT_Solveur()
        self.solutions = []
        self.var = [[]]

        #Initialiser le générateur de tableau
        self.generateur = Tableau(dimension, tableau)
        self.tableau = self.generateur.make_tableau()
      
        self.dimension = self.generateur.dimension

        #Le fichier sortie du programme
        self.output = output

        #Le premier ligne d'affichage de chaque tableau (A B ...)
        self.top_line = self.generer_top_line()
        
        #Pour stocker les choix faits par le joueur
        self.choix = []

        #Pour stocker les cases erreures du tableau (si une case de valeur 1, contient 2 coins choisis)
        self.erreure = []

        #Le fichier où on doit ecrire le format DIMACS 
        self.fichier_dimacs = self.output + ".dimacs"

        #Pour ecrire le format DIMACS du probleme dans un fichier
        self.ecrire_DIMACS()

        #Pour afficher le tableau au debut du jeu
        self.afficher_tableau(self.dimension)

        #Pour verifier si le tableau est résoluble. Sinon, on sort du programme
        self.check_tableau_res()

    def ecrire_DIMACS(self):
        '''
        Une fonction qui permette à ecrire le DIMACS du probleme dans un fichier
        '''
        self.solver.ecrire_DIMACS(self.dimension, self.tableau, self.fichier_dimacs)
        print(f"\n*** Le format DIMACS du probleme est ecrite dans le fichier {self.fichier_dimacs} ***\n\n")


    def check_tableau_res(self):
        '''
        Une fonction qui permette de vérifier si le tableau du jeu est résoluble ou pas
        '''        
        #Passer le fichier DIMACS généré au SAT Solveur
        res = self.solver.solve_SAT(self.fichier_dimacs)
        if not res:
            print("\n\nLe tableau donné n'est pas résoluble\n")
            exit(1)

    def generer_top_line(self):
        '''
        Une fonction qui permette à générer les 'n' premiers lettres d'Alphabet, utilisées pour faciliter le choix des cases au joueur
        '''                
        top_line = list(string.ascii_uppercase[:self.dimension+1])
        
        return top_line


    def afficher_tableau(self, n):
        '''
        Une fonction qui permette d'afficher le tableau
        '''      
        k = iter(range(1, n+2))
        
        print("    " + "   ".join(self.top_line))

        for i in range(n):
            
            print('{:2d}'.format(next(k)), end="  ")

            for j in range(n):
                #Si une case ne verifie pas les conditions du jeu, ses coins seront affichés en Rouge
                if [i, j] in self.erreure:
                    print(f"{Fore.RED}●{Fore.RESET}---", end="")
                #Si un coin d'case est choisie par le joueur, et n'est pas une case erreure, sera affiché en Vert
                elif [i, j] in self.choix:
                    print(f"{Fore.GREEN}●{Fore.RESET}---", end="")
                #Les coins normaux
                else:
                    print("O---", end="")
            
            if [i, n] in self.erreure:
                print(f"{Fore.RED}●{Fore.RESET} ")
            elif [i, n] in self.choix:
                print(f"{Fore.GREEN}●{Fore.RESET} ")
            else:
                print("O ")

            print("    ", end="")
            for j in range(n):
                print(f"| {self.tableau[i][j]} ", end="")

            print("| ")
        
        print('{:2d}'.format(next(k)), end="  ")
        for j in range(n):
            if [n, j] in self.erreure:
                print(f"{Fore.RED}●{Fore.RESET}---", end="")
            elif [n, j] in self.choix:
                print(f"{Fore.GREEN}●{Fore.RESET}---", end="")
            else:
                print("O---", end="")
        if [n, n] in self.erreure:
            print(f"{Fore.RED}●{Fore.RESET} ")
        elif [n, n] in self.choix:
            print(f"{Fore.GREEN}●{Fore.RESET} ")
        else:
            print("O ")

    def verifier_case(self, i, j):

        '''
        Une fonction qui verifie que le nbr de Coins choisis ne depasse pas la valeur de la case correspondante

        :param i: indice ligne
        :param j: indice colonne

        :return bool: True si le cases est fini (Nbr coins cochés égale à la valeur du la case)
        :return bool: False si le case n'est pas encore fini
        '''

        nbr_coins = 0

        #Variable bool utilisé pour détecter si le jeu est fini 
        fin = True

        #On doit verifier les 4 coins de chaque case
        cases_a_verifier = [[i, j], [i, j+1], [i+1, j], [i+1, j+1]]
        
        #Pour stocker les cases choisis parmi les cases à vérifier
        cases_existante = []
        for case in cases_a_verifier:
            if case in self.choix:
                cases_existante.append(case)
                nbr_coins += 1
        
        #Si le nbr_coins choisis plus grand que la valeur de la case, alors c'est une cse erreure
        if nbr_coins > int(self.tableau[i][j]):
            self.erreure.extend(cases_existante)

        #quand le nbr_coins == valeur de la case, alors ce case est fini. Et la fonction verifier_tableau, verifie si chaque case est finie alors le jeu est fini 
        if nbr_coins < int(self.tableau[i][j]):
            fin = False

        return fin
    
    def verifier_tableau(self):
        '''
        Une fonction qui verifie que le tableau ne contient pas une case interdite. Elle utilise la fonction verifier_case
        '''
        self.erreure = []
        
        #Une liste qui contienne un "bool" qui dit si chaque case est finie ou non. Si tous les cases sont finies alors le jeu est fini
        fin = []

        for i in range(self.dimension):

            for j in range(self.dimension):
                #On ajoute le "bool" renvoyé dans la liste fin
                fin.append(self.verifier_case(i, j))

        #Si tous les cases sont True (case finie), all(fin) renvoie True
        return all(fin)

    def restart(self):
        '''
        Si le joueur a choisi de jouer de nouveau, Une fonction qui redamarre le jeu
        '''
        #Pour re-initialiser tous les listes et les variables
        self.choix = []
        self.erreure = []

        #Pour que le generateur génère un tableau aléatoirement 
        self.generateur.fichier = None

        #Pour entrer la nouvelle dimension
        dim = input('\nEntrez la dimension voulue: ')

        while (not dim.isdigit() or int(dim) > 15):
            dim = input('\nEntrez la dimension voulue:(max 15) ')

        self.dimension = int(dim)
        self.generateur.dimension = int(dim)

        self.tableau = self.generateur.make_tableau()
        
        self.afficher_tableau(self.dimension)
        self.play()

    def valider_choix(self, choice):
        '''
        Une fonction qui est utilisée en mode 'play' et qui permette à valider le choix de l'utilisteur
        
        :param choice: Le choix de l'utilisateur
        
        :return bool: True si le choix est validé
        '''

        if len(choice) == 0:
            return False

        for elem in choice:

            if elem == "QUIT" or elem == "Q":
                return True

            if len(elem) < 2:
                return False

            if elem == "AUTO":
                return True

            #Le premier element de notre choix DOIT être un alphabet utilisé par le tableau
            if elem[0] not in self.top_line:
                return False

            #Le deuxieme element doit être un entier, et qui appartient à l'intervalle utilisé par le tableau
            if not elem[1].isdigit() or int(elem[1]) not in range(1, self.dimension+2): 
                return False

        return True

    def play(self):
        '''
        La fonction qui demarre le jeu en mode 'play' 
        '''      
        game = True
      
        print("\nParamètres d'entrée: ")
        print("----------------------")
        print("- Pour choisir une case, vous entrez un alphabet puis un numero (eg. A1)")
        print("- Pour retirer une case, vous re-entrez le même choix du case")
        print("- Vous pouvez entrer encore plusieus choix séparés par des espaces (eg. A1 B2 C3)")
        print("- Vous pouvez toujours entrez 'AUTO' pour afficher la solution finale du tableau (autosolve)")
        print("- 'quit' ou 'q' pour sortir du jeu\n\n")
        
        autosolve = False
        while (game):

            choice = input("\nEntrez votre choix: ").upper()
            choice = choice.split()

            while not self.valider_choix(choice):

                print("\nChoix Invalide")

                choice = input("(e.g A5) ou (eg. A1 B2 C3) ou AUTO: ").upper()
                choice = choice.split()
            

            if choice[0].rstrip() == "QUIT" or choice[0].rstrip() == "Q":
                
                print("\n\nAu revoir ...\n\n")
                exit(0)

            if choice[0].rstrip() == "AUTO":

                autosolve = True
                fin = True
                self.afficher_solution()

            else:
                for elem in choice:

                    #recuper les indices de tableau correspondants à notre choix
                    liste = [int(elem[1]) - 1, self.top_line.index(elem[0])]

                    #On ajoute notre choix à la liste des choix s'il etait pas choisi avant
                    if liste not in self.choix:
                        self.choix.append(liste)
                    #Si notre choix était choisi avant on l'enlève de nos choix,
                    else:
                        self.choix.remove(liste)

                #apres chaque choix, on doit recuperer les cases erreures de notre tableau
                fin = self.verifier_tableau()

                #Pour afficher le tableau
                self.afficher_tableau(self.dimension)

            if fin and len(self.erreure) == 0:
                
                if not autosolve:
                    print("\t\t\t\n****************************\n*    VOUS AVEZ GAGNÉ !!    *\n****************************\n")
                
                    fichier = self.output + "1.sat"
                    self.solver.ecrire_fichier_SAT(self.dimension, self.choix, fichier)
                    print(f"\nLa solution SAT est ecrite dans le fichier: {fichier}\n")

                g = input("Devez vous rejouer avec un nouveau tableau généré? [y/n]: ").lower()

                #si l'entrée n'est pas validée
                while g != 'y' and g != 'n':
                    g = input("Devez vous rejouer? [y/n]: ").lower()

                if g == 'y':
                    #re-initialiser les listes et re-affichez un nouveau tableau
                    self.restart()
                else:
                    #Le joueur ne veut pas jouer une autre fois
                    print("\n\nAu revoir ...\n")
                    exit(2)

    def recuperer_cases_dimacs(self, dimacs_tableau, entier):
        '''
        Avoir la case qui correspond au coin coché du solution du tableau DIMACS

        :param dimacs_tableau: La grille avec les cases au format DIMACS
        :param entier: entier qui corresponde au nom du coin dans le tableau DIMACS
        
        :return liste: les indices du l'entier specifié
        '''    

        liste = ["{},{}".format(index1,index2) for index1,value1 in enumerate(dimacs_tableau) for index2,value2 in enumerate(value1) if value2==entier]
        
        liste = [int(liste[0].split(',')[0]), int(liste[0].split(',')[1])]

        return liste


    def afficher_solution(self):

        '''
        La fonction qui affiche la solution du jeu     
        '''

        self.solver.solve_SAT(self.fichier_dimacs)
        self.solutions = self.solver.solutions
        
        #On recupère le tableau de dimacs deja généré pour qu'on puisse associer la solution au grille principal
        dimacs_tableau = self.solver.dimacs_tableau

        self.choix = []
        self.erreure = []

        count = 1
        
        #Pour chaque solution donnée par le SAT solveur
        for solution in self.solutions:      
            
            print(f"\n\nSolution {count}: \n\n")
        
            #on re-initialise la liste des choix pour chaque tableau
            self.choix = []
            

            for elem in solution:
        
                liste = self.recuperer_cases_dimacs(dimacs_tableau, int(str(elem)[2:]))
                self.choix.append(liste)

            #Affichier le tableau avec solution
            self.afficher_tableau(self.dimension)

            #Changer l'extension du fichier au format sat
            fichier = self.output + str(count) + ".sat"

            #Ecrire la solution SAT dans le fichier
            self.solver.ecrire_fichier_SAT(self.dimension, self.choix, fichier)
            print(f"\n*** La solution SAT est ecrite dans le fichier: {fichier} ***\n")


            count += 1

