#################################################################################################
#                                                                                               #
#                               Projet INF402                                                   #
#                           Université Grenoble Alpes                                           #
#                                                                                               #
#                 AlSABR Ibrahim  -  MAFADI Ziad  -  VITTET Brice                               #
#                                                                                               #
#                                                                                               #
#################################################################################################

from z3 import *


class SAT_Solveur:
    
    '''
    Une fonction qui permette de bloquer un model de SAT solveur, pour looper sur tous les models possibles
    '''
    def block_model(self, model):
        m = model
        self.s.add(Or([ f() != m[f] for f in m.decls() if f.arity() == 0])) 

    #   return: 1 -> le tableau est résoluble (sat problem)
    #   return: 0 -> le tableau n'est pas résoluble (unsat problem)
    def solve_SAT(self, fichier):

        #On initialise le solveur
        self.s = Solver()

        #On donne le fichier Dimacs au solveur
        self.s.from_file(fichier)
       
        # si s.check() == -1 alors le tableau n'est pas resoluble
        if self.s.check().r == -1:
            
            return 0
    
        else:
            
            #Une liste pour ajouter tous les solutions possibles
            self.solutions = []


            while self.s.check() == sat:
                
                #Extraire un model du solveur
                solution = self.s.model()

                r = []
                for x in solution:
                    #Ajouter les coins True, cad les coins qui doivent être cochés
                    if is_true(solution[x]):

                        r.append(x())

                #On ajoute la solution au liste de tous les solutions
                self.solutions.append(r)

                #On bloque le model courant pour pouvoir essayer d'extraire un model different
                self.block_model(solution)

            return 1
    
    
    '''
    Fonction utilisée pour ecrire les solutions dans un fichier au format SAT
    coin coché      -> 1 
    coin non coché  -> 0 
    '''
    def ecrire_fichier_SAT(self, dimension, cases, fichier):

        n = dimension + 1
        with open(fichier, "w") as f:
            for i in range(n):
                for j in range(n):
                    if [i, j] in cases:
                        f.write('1')
                    else:
                        f.write('0')
                f.write('\n')


    '''
    Une fonction qui donne les coins du grille avec differents nomenclatures selon la dimension, 
    utile pour générer fichier dimacs.
    '''
    def cases_dimacs_vide(self, dimension):
            
        cases = [[1, 2], [2, 5]]
        max = 5
        for _ in range(2, dimension):

            nbr = cases[len(cases)-1][1]
            liste = [nbr, nbr + 2]
            cases.append(liste)
    

        cases.append([3, 4])
        cases.append([4, 6])
        for _ in range(2, dimension):

            nbr = cases[-1][1]
    
            liste = [nbr, nbr + 2]
            cases.append(liste)                
            max = nbr + 2

        for _ in range(dimension - 1):

            liste = [max + 1, max + 2]
            cases.append(liste)
            max += 1
            for _ in range(dimension-1):

                liste = [max + 1, max + 2]
                cases.append(liste)
                max += 1
            max+=1
            
        return cases
    

    '''
    Une fonction qui fait echanger les variables d'une clause avec ce qui correspond dans le grille
    old_string      -> la clause avec (1, 2, 3, 4) comme variables
    variables_case  -> les variables qui doivent remplacer (1, 2, 3, 4) dans la clause de Dimacs
    '''
    def replace_variables(self, old_string, variables_case):

        s = old_string.split()
        new_string = ""

        for part in s:

            if part == "4" or part == "-4":
                new_part = part.replace("4", str(variables_case[3]))
            elif part == "3" or part == "-3":
                new_part = part.replace("3", str(variables_case[2]))
            elif part == "2" or part == "-2":
                new_part = part.replace("2", str(variables_case[1]))
            elif part == "1" or part == "-1":
                new_part = part.replace("1", str(variables_case[0]))
            else:
                new_part = part

            new_string += new_part
            new_string += " "

        new_string += "\n"

        return new_string

    '''
    Une fonction qui donne le grille correspondant au DIMACS
    cad differents nomenclature pour chaque coin du case
    '''
    def recup_tableau_dimacs(self, cases_dimacs_vide, dimension):
        
        tableau = []
        n = dimension        
        i = 0
        iter = 0
        while i < ( n * (n+1)):
            
            liste = []
            nbr = n + iter*n
            
            for l in cases_dimacs_vide[i:nbr]:
                liste.extend(l)
            
            for num in liste:
                if liste.count(num) > 1 : 
                    liste.remove(num)
            
            tableau.append(liste)
            i += n
            iter += 1

        return tableau

    '''
    Fonction utilisée pour ecrire DIMACS d'un probleme dans un fichier
    '''    
    def ecrire_DIMACS(self, dimension, tableau, fichier):

        n = dimension
        dicto = {
            '0':{'nbr_clauses': 4, 'nbr_variables': 4},
            '1':{'nbr_clauses': 7, 'nbr_variables': 4},
            '2':{'nbr_clauses': 8, 'nbr_variables': 4},
            '3':{'nbr_clauses': 7, 'nbr_variables': 4},
            '4':{'nbr_clauses': 4, 'nbr_variables': 4},
        }

        clauses = []
        nbr_clauses_total = 0

        if dimension > 1:
            cases_tab_vide = self.cases_dimacs_vide(dimension)

        #utilisé lors de l'affichage du solution dans le fichier squaro.py
        self.dimacs_tableau = self.recup_tableau_dimacs(cases_tab_vide, dimension)

        for i in range(n):
            
            for j in range(n):

                file = "DIMACS/case" + str(tableau[i][j]) + ".dimacs"

                with open(file, 'r') as f:
                
                    liste = f.readlines()

                #on determine les variables correspondantes au ce case
                lig_haut = cases_tab_vide[i*n + j]
                lig_bas  = cases_tab_vide[i*n + j+n]

                variables_case = []
                #on ajoute les variables deteminés au liste de variable
                variables_case.extend(lig_haut)
                variables_case.extend(lig_bas)
                
                for elem in liste[1:]:
                    
                    #on rend la clause au format convenable pour le dimacs (echange de variables)
                    new_elem = self.replace_variables(elem, variables_case)

                    clauses.append(new_elem)
                
                #chaque valeur de case a un nombre specifique de clauses
                nbr_clauses_total += dicto[str(tableau[i][j])]['nbr_clauses']



        nbr_variables_total = (n+1) * (n+1)

        f = open(fichier, "w")

        f.write("p cnf {} {}\n".format(nbr_variables_total, nbr_clauses_total))

        for i in range(len(clauses)):
        
            #on ecrit les clauses dans le fichier
            f.write(clauses[i])
            
        f.close()

    