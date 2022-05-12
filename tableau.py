#################################################################################################
#                                                                                               #
#                                Projet INF402                                                  #
#                            Université Grenoble Alpes                                          #
#                                                                                               #
#                 AlSABR Ibrahim  -  MAFADI Ziad  -  VITTET Brice                               #
#                                                                                               #
#                                                                                               #
#################################################################################################


import random

from solveur import SAT_Solveur 

class Tableau:

  def __init__(self, dimension, tableau=None):

    self.fichier = tableau
    self.dimension = dimension
    
    #Initialiser le Solveur SAT
    self.solver = SAT_Solveur()
      
  def verifier_tableau(self, tableau):

    '''
    Une fonction qui verifie si le fichier contenant le tableau, donné par argument, satisfait les conditions d'un tableau de Squaro

    :param tableau: Une double Liste qui contient les lignes du tableau. Chaque ligne est une liste

    :return None
    ''' 

    
    #Le nbr listes dans le tableau(nbr_de_ligne) doit être égale à la dimension specifiée 
    if len(tableau) != self.dimension:
      print("\nLe format du fichier donné n'est pas convenable.\nLe nbr de lignes contenants les cases du tableau ne correspond pas à la dimension donnée.\nUtilisez --help pour plus d'informations")
      exit(1)

    for liste in tableau:
      #Les lignes doivent contenir seulement des entiers
      if any(map(lambda x: not x.isdigit(), liste)):
        print("\nLe format du fichier donné n'est pas convenable.\nLes valeurs donnés doivent être des entiers\n")
        exit(1)
      
      #La valeure maximale d'une case de tableau est 4
      if any(map(lambda x: int(x) > 4, liste)):
        print("\nLe format du fichier donné n'est pas convenable.\nLa valeur maximale d'une case est 4")
        exit(1)
      
      #Le nbr de colonne du tableau doit être égale à la dimension spécifiée
      if len(liste) != self.dimension:
        print("\nLe format du fichier donné n'est pas convenable.\nLe nbr de colonnes contenants les cases du tableau ne correspond pas à la dimension donnée.\nUtilisez --help pour plus d'informations")
        exit(1)
    
  def lire_fichier(self, fichier):
    '''
    Une fonction qui lit le tableau du fichier

    :param fichier: Le fichier du grille donné par argument
    
    :return tab: Une double Liste qui correspond  aux lignes de la grille du jeu
    '''     
    plateau = []
    
    try:
      with open(fichier, "r") as f:
        liste = f.readlines()

      liste = list(map(lambda x: x.strip(), liste))
      if len(liste[-1]) == 0:
        liste.pop()

      #Si la dimension donnée n'est pas un chiffre
      if liste[0].isdigit():
        self.dimension = int(liste[0])
      else:
        print("Le format du fichier donné n'est pas convenable.\nLa dimension doit être un entier <= 40.\nUtilisez --help pour plus d'informations")
        exit(1)

      plateau.extend(liste[1:])

      #Transformer le tableau en liste double
      plateau = list(map(list, plateau))

      #Pour vérifier le format du tableau donné
      self.verifier_tableau(plateau)

      #Durant la lecture du fichier, les entiers sont lus comme des chaines de caracteres. Ici on les transrome en entier
      tab = [[int(x) for x in elem] for elem in plateau]

      return tab

    #Si le fihcier donné n'existe pas dans le repartoire
    except FileNotFoundError:
      print(f"Erreure d'Ouverture du fichier {fichier}")
      exit(1)


  def generate_SAT(self):
    
    '''
    Pour créer un tableau aléatoriement, on pars de l'inverse.
    On génère aléatoirement une solution SAT. Et on ecrit le tableau qui la convient
    
    :param None

    :return sat: Une solution SAT
    '''
    sat = [[random.randint(0, 1) for _ in range(self.dimension+1)] for _ in range(self.dimension+1)]

    return sat

  def recuperer_cases(self, sat):
    
    '''
    Pour recupérer les cases cochés (qui ont valeur 1 dans la solution SAT)

    :param sat: Une double Liste qui contient une solution SAT
    
    :return cases: les Cases du tableau généré aléatoirement 
    '''

    cases = []
    for i in range(len(sat)):
        for j in range(len(sat)):
            if sat[i][j] == 1:
                cases.append([i, j])
    return cases 


  def remplir_case(self, tableau, i, j, cases):

    '''
    Pour mettre dans chaque case, la valeur de ces coins cochés

    :param i: indice ligne
    :param j: indice colonne
    :param cases: les cases du tableau

    :return tableau: La grille avec la valeur de chaque case
    '''      
    cases_a_verifier = [[i, j], [i, j+1], [i+1, j], [i+1, j+1]] 
    count = 0
    for case in cases_a_verifier:
        if case in cases:
            count += 1

    tableau[i][j] = count

    return tableau


  def generer_tableau(self) :

    ''''
    Pour générer un tableau aléatoirement

    :param None

    :return tableau: le tableau généré aléatoirement
    '''

    #generer la solution SAT
    sat = self.generate_SAT()

    #recuperer les cases cochés
    cases = self.recuperer_cases(sat)

    #initialiser un tableau avec des valeurs 0
    tableau = [[0 for _ in range(self.dimension)] for _ in range(self.dimension)]

    #remplir les cases de tableau avec ce qui correspond aux coins cochés
    for i in range(self.dimension):
        for j in range(self.dimension):
            tableau = self.remplir_case(tableau, i, j, cases) 
      

    return tableau       


  def make_tableau(self):

    '''
    La fonction initiale du fichier, qui doit generer la grille de jeu selon les arguments passés au programme

    :param None

    :return tableau: La grille du jeu
    '''

    if not self.fichier:
      #Si le tableau n'est pas donné dans un fichier, on doit le générer aléatoirement
      tableau = self.generer_tableau()
    else:
      #Lire le tableau de fichier donné par argument
      tableau = self.lire_fichier(self.fichier)

    return tableau

