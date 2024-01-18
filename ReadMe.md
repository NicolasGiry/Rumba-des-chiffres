GIRY Nicolas - 9/12/2023

****************************
Pour le bon fonctionnement de l'affichage, veuillez installer la bibliothèque 'colored' :
pip install colored 
****************************


Le fichier Rumba.py contient un programme permettant la résolution d'un jeu de rumba des chiffres.
Son utilisation est guidée.
Vous pouvez modifier le fichier rumba.txt pour tester vos propres combinaisons : la première ligne correspond à l'état but, la deuxième à l'état initial et la dernière permet de définir la hauteur de la tige.
Les fichiers rumba_X_Y.txt sont des fichiers de tests. En utilisant la fonctionnalité "all" l'algorithme les résoudra tous.

![Screenshot 2024-01-18 112303](https://github.com/NicolasGiry/Rumba-des-chiffres/assets/114723956/bacf9ad8-6a10-4eee-b19e-30c48fd98e17)

Le programme utilise un algorithme IDA*, deux heuristiques sont proposées. 
La première est une heuristique minorante qui compte simplement le nombre d'éléments mal placés par rapport au but.
La deuxième heuristique n'est pas minorante mais essaye de mieux approximer le coût des mouvements. Un bloc placé sous plusieurs blocs coûtera plus cher à déplacer qu'un bloc placé en haut d'une tige.

![Screenshot 2024-01-18 112207](https://github.com/NicolasGiry/Rumba-des-chiffres/assets/114723956/95a66e11-9982-46d5-a1bb-3c11eab040bd)

Tous les résultats sont inscrits dans le fichier solution.txt à la fin de l'exécution du programme.
(plan solution, profondeur du noeud, le nombre de noeuds créés par itération, le nombre de noeuds développés par itération, le nombre d'itérations de l'algo IDA* et le temps d'exécution) 

![Screenshot 2024-01-18 112944](https://github.com/NicolasGiry/Rumba-des-chiffres/assets/114723956/5b773dc8-15e2-4ffd-ad41-15b5734333ac)

le plan solution propose un ensemble de tuples de la forme (A,B). 
Ils se lisent de cette manière: "je déplace le cube du sommet de la tige A vers le sommet de la tige B"
En suivant le plan solution, vous résoudrez le problème demandé.
Seule l'heuristique 1 (nombres mal mis) donne toujours un plan solution optimal.
