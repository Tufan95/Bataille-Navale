# Importation des bibliothèques nécessaires
import tkinter as tk  # Bibliothèque pour créer une interface graphique
import random  # Bibliothèque pour générer des placements aléatoires

# Classe représentant un navire
class Navire:
    def __init__(self, nom, taille):
        self.nom = nom  # Nom du navire
        self.taille = taille  # Taille du navire en cases
        self.positions = []  # Liste des positions occupées par le navire
        self.touche = 0  # Nombre de fois où le navire a été touché

    def est_coule(self):
        return self.touche >= self.taille  # Retourne True si le navire est coulé

# Classe représentant le plateau de jeu
class Plateau:
    def __init__(self):
        self.grille = [[None for _ in range(10)] for _ in range(10)]  # Grille 10x10 vide

    def placer_navire(self, navire, positions):
        for x, y in positions:
            self.grille[x][y] = navire  # Place le navire sur les cases spécifiées
        navire.positions = positions  # Stocke les positions du navire

    def peut_placer_navire(self, taille, x, y, orientation):
        if orientation == "horizontal":
            if y + taille > 10:  # Vérifie si le navire dépasse à droite
                return False
            for i in range(taille):
                if self.grille[x][y + i] is not None:  # Vérifie si les cases sont libres
                    return False
        else:  # orientation == "vertical"
            if x + taille > 10:  # Vérifie si le navire dépasse en bas
                return False
            for i in range(taille):
                if self.grille[x + i][y] is not None:  # Vérifie si les cases sont libres
                    return False
        return True

    def tirer(self, x, y):
        if self.grille[x][y] is not None:  # Si un navire est présent sur la case
            navire = self.grille[x][y]
            navire.touche += 1  # Incrémente le nombre de touches sur le navire
            self.grille[x][y] = "X"  # Marque la case comme touchée
            return True, navire  # Retourne que la case a été touchée et le navire
        else:
            self.grille[x][y] = "O"  # Marque la case comme manquée
            return False, None

# Classe représentant un joueur
class Joueur:
    def __init__(self, nom):
        self.nom = nom  # Nom du joueur
        self.plateau = Plateau()  # Plateau du joueur
        self.navires = []  # Liste des navires du joueur

    def ajouter_navire(self, navire):
        if len(self.navires) < 6:  # Limite le nombre de navires à 6
            self.navires.append(navire)
        else:
            raise ValueError("Le nombre maximum de navires a déjà été atteint.")  # Ajoute un navire à la liste

    def tous_les_navires_coules(self):
        return all(navire.est_coule() for navire in self.navires)  # Vérifie si tous les navires sont coulés

# Interface graphique principale
class BatailleNavaleApp:
    def __init__(self, root):
        self.root = root  # Fenêtre principale
        self.root.title("Bataille Navale")  # Titre de la fenêtre

        self.joueur = Joueur("Joueur")  # Joueur humain
        self.ordinateur = Joueur("Ordinateur")  # Joueur ordinateur

        self.tour_joueur = True  # Indique si c'est le tour du joueur
        self.partie_terminee = False  # Indique si la partie est terminée

        self.navire_a_placer = None  # Navire en cours de placement
        self.orientation = "horizontal"  # Orientation par défaut

        self.creer_interface()  # Création de l'interface graphique
        self.nouvelle_partie()  # Initialisation d'une nouvelle partie

    def creer_interface(self):
        # Création des grilles pour le joueur et l'ordinateur
        self.grille_joueur = tk.Frame(self.root)  # Grille du joueur
        self.grille_joueur.grid(row=0, column=0, padx=10, pady=10)
        self.boutons_joueur = self.creer_grille(self.grille_joueur, self.joueur.plateau, False)

        self.grille_ordinateur = tk.Frame(self.root)  # Grille de l'ordinateur
        self.grille_ordinateur.grid(row=0, column=1, padx=10, pady=10)
        self.boutons_ordinateur = self.creer_grille(self.grille_ordinateur, self.ordinateur.plateau, True)

        # Panneau de contrôle
        self.panneau_controle = tk.Frame(self.root)  # Panneau pour les boutons et informations
        self.panneau_controle.grid(row=1, column=0, columnspan=2, pady=10)

        self.label_tour = tk.Label(self.panneau_controle, text="Placez vos navires")  # Indicateur de tour
        self.label_tour.pack()

        # Boutons pour changer l'orientation
        self.bouton_horizontal = tk.Button(self.panneau_controle, text="Horizontal", command=lambda: self.set_orientation("horizontal"))
        self.bouton_horizontal.pack(side=tk.LEFT, padx=5)

        self.bouton_vertical = tk.Button(self.panneau_controle, text="Vertical", command=lambda: self.set_orientation("vertical"))
        self.bouton_vertical.pack(side=tk.LEFT, padx=5)

        self.bouton_nouvelle_partie = tk.Button(self.panneau_controle, text="Nouvelle Partie", command=self.nouvelle_partie)  # Bouton pour réinitialiser
        self.bouton_nouvelle_partie.pack(side=tk.RIGHT, padx=5)

    def creer_grille(self, frame, plateau, est_ordinateur):
        boutons = []  # Liste des boutons de la grille
        for x in range(10):
            ligne = []
            for y in range(10):
                bouton = tk.Button(frame, width=2, height=1, bg="light blue", command=lambda x=x, y=y: self.placer_navire(x, y) if not est_ordinateur else self.tirer(x, y))  # Bouton avec action différente selon le type de grille
                bouton.grid(row=x, column=y)  # Placement du bouton dans la grille
                ligne.append(bouton)
            boutons.append(ligne)
        return boutons

    def set_orientation(self, orientation):
        self.orientation = orientation  # Change l'orientation des navires

    def nouvelle_partie(self):
        # Réinitialisation des plateaux
        self.joueur.plateau = Plateau()  # Nouveau plateau pour le joueur
        self.ordinateur.plateau = Plateau()  # Nouveau plateau pour l'ordinateur
        self.joueur.navires = []  # Réinitialise les navires du joueur
        self.ordinateur.navires = []  # Réinitialise les navires de l'ordinateur
        self.tour_joueur = True  # Le joueur commence
        self.partie_terminee = False  # Réinitialise l'état de la partie
        self.label_tour.config(text="Placez vos navires")

        # Réinitialisation des boutons
        for x in range(10):
            for y in range(10):
                self.boutons_joueur[x][y].config(text="", bg="light blue", state="normal")  # Réinitialisation des boutons du joueur
                self.boutons_ordinateur[x][y].config(text="", bg="light blue", state="disabled")  # Réinitialisation des boutons de l'ordinateur

        # Préparation pour le placement manuel des navires
        self.navires_a_placer = [
            ("Porte-avions", 5),
            ("Croiseur", 4),
            ("Destroyer 1", 3),
            ("Destroyer 2", 3),
            ("Sous-marin 1", 2),
            ("Sous-marin 2", 2)
        ]
        self.placement_navires_aleatoire(self.ordinateur)  # Placement aléatoire des navires de l'ordinateur
        self.selectionner_prochain_navire()  # Préparation pour le placement des navires du joueur

    def placement_navires_aleatoire(self, joueur):
        for nom, taille in [
            ("Porte-avions", 5),
            ("Croiseur", 4),
            ("Destroyer 1", 3),
            ("Destroyer 2", 3),
            ("Sous-marin 1", 2),
            ("Sous-marin 2", 2)
        ]:
            place = False
            while not place:
                x = random.randint(0, 9)  # Coordonnée aléatoire en x
                y = random.randint(0, 9)  # Coordonnée aléatoire en y
                orientation = random.choice(["horizontal", "vertical"])  # Orientation aléatoire
                if joueur.plateau.peut_placer_navire(taille, x, y, orientation):  # Vérifie si le navire peut être placé
                    positions = [(x + i, y) if orientation == "vertical" else (x, y + i) for i in range(taille)]  # Génère les positions du navire
                    navire = Navire(nom, taille)  # Crée le navire
                    joueur.plateau.placer_navire(navire, positions)  # Place le navire sur le plateau
                    joueur.ajouter_navire(navire)  # Ajoute le navire à la liste
                    place = True

    def placer_navire(self, x, y):
        if self.partie_terminee:  # Vérifie si la partie est terminée
            return

        if len(self.joueur.navires) >= 6:  # Vérifie si le joueur a déjà placé 6 navires
            self.label_tour.config(text="Vous avez placé tous vos navires.")
            return

        if self.navire_a_placer:  # Si un navire est en cours de placement
            taille = self.navire_a_placer.taille
            if self.joueur.plateau.peut_placer_navire(taille, x, y, self.orientation):  # Vérifie si le placement est valide
                positions = [(x + i, y) if self.orientation == "vertical" else (x, y + i) for i in range(taille)]
                self.joueur.plateau.placer_navire(self.navire_a_placer, positions)  # Place le navire sur le plateau
                for pos_x, pos_y in positions:
                    self.boutons_joueur[pos_x][pos_y].config(bg="gray")  # Change la couleur du navire en gris
                self.joueur.ajouter_navire(self.navire_a_placer)  # Ajoute le navire à la liste du joueur
                self.selectionner_prochain_navire()  # Passe au navire suivant

    def tirer(self, x, y):
        if self.partie_terminee:  # Vérifie si la partie est terminée
            return

        if self.tour_joueur and self.boutons_ordinateur[x][y]["state"] == "normal":  # Si c'est le tour du joueur et la case est valide
            touche, navire = self.ordinateur.plateau.tirer(x, y)  # Tente de toucher un navire
            bouton = self.boutons_ordinateur[x][y]
            bouton.config(bg="red" if touche else "blue", state="disabled")  # Change la couleur selon le résultat
            if touche and navire.est_coule():  # Si un navire est coulé
                self.label_tour.config(text=f"Vous avez coulé le {navire.nom}!")
                for pos_x, pos_y in navire.positions:
                    self.boutons_ordinateur[pos_x][pos_y].config(bg="purple")  # Change la couleur du navire coulé en violet
            if self.ordinateur.tous_les_navires_coules():  # Si tous les navires de l'ordinateur sont coulés
                self.label_tour.config(text="Vous avez gagné!")
                self.partie_terminee = True  # Marque la partie comme terminée
                return
            self.tour_joueur = False  # Passe au tour de l'ordinateur
            self.label_tour.config(text="Tour : Ordinateur")
            self.root.after(1000, self.tour_ordinateur)  # Lance le tour de l'ordinateur après 1 seconde

    def selectionner_prochain_navire(self):
        if self.navires_a_placer:  # S'il reste des navires à placer
            nom, taille = self.navires_a_placer.pop(0)  # Récupère le prochain navire
            self.navire_a_placer = Navire(nom, taille)  # Prépare le navire en cours de placement
            self.label_tour.config(text=f"Placez votre {nom} ({taille} cases)")  # Met à jour le texte
        else:  # Tous les navires sont placés
            self.label_tour.config(text="Tour : Joueur")  # Passe au tour du joueur
            for x in range(10):
                for y in range(10):
                    self.boutons_ordinateur[x][y].config(state="normal")  # Active les boutons de l'ordinateur

    def tour_ordinateur(self):
        while True:
            x, y = random.randint(0, 9), random.randint(0, 9)  # Coordonnées aléatoires
            if self.boutons_joueur[x][y]["state"] == "normal":  # Vérifie que la case est valide
                break
        touche, navire = self.joueur.plateau.tirer(x, y)  # Tente de toucher un navire du joueur
        bouton = self.boutons_joueur[x][y]
        bouton.config(bg="red" if touche else "blue", state="disabled")  # Change la couleur selon le résultat
        if touche and navire.est_coule():  # Si un navire est coulé
            self.label_tour.config(text=f"L'ordinateur a coulé votre {navire.nom}!")
            for pos_x, pos_y in navire.positions:
                self.boutons_joueur[pos_x][pos_y].config(bg="purple")  # Change la couleur du navire coulé en violet
        if self.joueur.tous_les_navires_coules():  # Si tous les navires du joueur sont coulés
            self.label_tour.config(text="L'ordinateur a gagné!")
            self.partie_terminee = True  # Marque la partie comme terminée
            return
        self.tour_joueur = True  # Passe au tour du joueur
        self.label_tour.config(text="Tour : Joueur")

# Lancement de l'application
if __name__ == "__main__":
    root = tk.Tk()  # Création de la fenêtre principale
    app = BatailleNavaleApp(root)  # Création de l'application
    root.mainloop()  # Lancement de la boucle principale
