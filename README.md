# Jeu-de-SquarO

Projet INF402

Année 2021 - 2022 : Université Grenoble Alpes

Ce projet permet de générer et résoudre des plateaux du jeu Squaro en utilisant le SAT Solveur Z3

## Authors

- [MAFADI Ziad](https://github.com/ZiadMafadi)
- [ALSABR Ibrahim](https://github.com/IbrahimAlsabr)
- VITTET Brice



## Installation


```bash
  git clone https://github.com/ZiadMafadi/Jeu-de-SquarO.git
  cd Jeu-de-SquarO
```

    
## Configuration


```bash
  pip install -r requirements.txt
```

```bash
  chmod u+x main.py
```
Pour lancer le programme, exécutez le script (./main.py) avec les options choisies. Ces options sont décrites dans le paragraphe suivant.

## Utilisation

Pour avoir les instructions d'excution du programme:
```bash
  ./main.py --help
```

Options:
```
  -h, --help            show this help message and exit
  -t TABLEAU, --tableau TABLEAU

                        Un fichier qui contient un tableau.
                        Il faut ecrire sur la premiere ligne la dimesnion 'n' [entier] du tableau
                        Puis sur n lignes les valeurs du case du tableau
                        Si un fichier n'etait pas spécifié, le tableau sera généré aléatoirement
  -d DIMENSION, --dimension DIMENSION

                        Specifier la dimension du tableau (Max = 15).
                        Utilisé si y a pas un fichier de tableau donné
  -m {play,autosolve}, --mode {play,autosolve}

                        Mode du jeu souhaité:
                        play:            pour jouer le jeu avec mode actif.
                        autosolve:       Pour trouver la solution du tableau automatiquement
  -o OUTPUT, --output OUTPUT

                        Le fichier sortie pour ecrire DIMACS et La solution SAT
                        C'est conseillé de donner un nom du fichier sans extension
                        Default: resultat
```

## Usage
```bash
./main.py -t [FILE TABLEAU] -m [play/autosolve] -o [NOM_FICHIER]
./main.py -d [DIMENSION] -m [play/autosolve] -o [NOM_FICHIER]
./main.py -m [play/autosolve] -d [DIMENSION] -o [NOM_FICHIER]
```

## Examples

```bash
  ./main.py -d 5 -m autosolve
```
![image](https://user-images.githubusercontent.com/105078630/168067362-3416d701-3f77-48b8-8300-63bfe4ecea01.png)



```bash
  ./main.py -d 2 -m play
```
![image](https://user-images.githubusercontent.com/105078630/168068997-e906b631-80c0-4aee-9355-b34745802276.png)
