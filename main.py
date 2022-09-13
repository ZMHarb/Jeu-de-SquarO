#!/usr/bin/env python3
#################################################################################################
#                                                                                               #
#                               Projet INF402                                                   #
#                           Université Grenoble Alpes                                           #
#                                                                                               #
#                 AlSABR Ibrahim  -  MAFADI Ziad  -  VITTET Brice                               #
#                                                                                               #
#                                                                                               #
#################################################################################################
'''
usage: 

main.py -t [FILE TABLEAU] -m [play/autosolve] -o [NOM_FICHIER]
main.py -d [DIMENSION] -m [play/autosolve] -o [NOM_FICHIER]
main.py -m [play/autosolve] -d [DIMENSION] -o [NOM_FICHIER]

'''

import os
from argparse import SUPPRESS, ArgumentParser, RawTextHelpFormatter

#Le fichier qui contient le jeu
from squaro import Squaro

#Cette commande essentielle pour afficher les couleurs si le code est executé depuis le CMD
os.system('')


parser = ArgumentParser(epilog= __doc__, formatter_class= RawTextHelpFormatter, usage= SUPPRESS)

parser.add_argument("-t", "--tableau", dest="tableau", help="\nUn fichier qui contient un tableau.\nIl faut ecrire sur la premiere ligne la dimesnion 'n' [entier] du tableau\nPuis sur n lignes les valeurs du case du tableau\nSi un fichier n'etait pas spécifié, le tableau sera généré aléatoirement\n")
parser.add_argument("-d", "--dimension", dest="dimension", type=int ,help="\nSpecifier la dimension du tableau (Max = 15).\nUtilisé si y a pas un fichier de tableau donné\n")
parser.add_argument("-m", "--mode", choices=["play", "autosolve"], dest="mode", help="\nMode du jeu souhaité:\nplay:\t\t pour jouer le jeu avec mode actif.\nautosolve:\t Pour trouver la solution du tableau automatiquement\n")
parser.add_argument("-o", "--output", dest="output", default="resultat", help="\nLe fichier sortie pour ecrire DIMACS et La solution SAT\nC'est conseillé de donner un nom du fichier sans extension\nDefault: resultat")

args = parser.parse_args()

if not args.tableau and not args.dimension and not args.mode:
  parser.print_help()
  exit(1)

if not args.tableau and not args.dimension:
  parser.error("Specifez la dimension souhaité du tableau. Utilisez --help pour plus d'informations")

if not args.mode:
  parser.error("Specifer le mode souhaité ['play' ou 'autosolve']. Utilisez --help pour plus d'informations")

if args.dimension and int(args.dimension) > 25:
  parser.error("La dimension maximale du tableau est 25. Utilisez --help pour plus d'informations")


game = Squaro(args.dimension, args.output, args.tableau)
if args.mode == 'play':
  game.play()
else:
  game.afficher_solution()

