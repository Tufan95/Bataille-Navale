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

        # Indicateurs des navires coulés
        self.label_navires_joueur = tk.Label(self.panneau_controle, text="Navires coulés (Joueur) : Aucun")
        self.label_navires_joueur.pack()

        self.label_navires_ordinateur = tk.Label(self.panneau_controle, text="Navires coulés (Ordinateur) : Aucun")
        self.label_navires_ordinateur.pack()

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

    def mettre_a_jour_indicateur_navires(self):
        navires_joueur_coules = [navire.nom for navire in self.joueur.navires if navire.est_coule()]
        navires_ordinateur_coules = [navire.nom for navire in self.ordinateur.navires if navire.est_coule()]

        self.label_navires_joueur.config(text=f"Navires coulés (Joueur) : {', '.join(navires_joueur_coules) if navires_joueur_coules else 'Aucun'}")
        self.label_navires_ordinateur.config(text=f"Navires coulés (Ordinateur) : {', '.join(navires_ordinateur_coules) if navires_ordinateur_coules else 'Aucun'}")

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

        # Réinitialisation des indicateurs
        self.mettre_a_jour_indicateur_navires()

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
                if joueur.plateau.peut_placer_navire(taille, x, y, orientation):
                    positions = [(x + i, y) if orientation == "vertical" else (x, y + i) for i in range(taille)]
                    navire = Navire(nom, taille)
                    joueur.plateau.placer_navire(navire, positions)
                    joueur.ajouter_navire(navire)
                    place = True

    def placer_navire(self, x, y):
        if self.partie_terminee:
            return

        if len(self.joueur.navires) >= 6:
            self.label_tour.config(text="Vous avez placé tous vos navires.")
            return

        if self.navire_a_placer:
            taille = self.navire_a_placer.taille
            if self.joueur.plateau.peut_placer_navire(taille, x, y, self.orientation):
                positions = [(x + i, y) if self.orientation == "vertical" else (x, y + i) for i in range(taille)]
                self.joueur.plateau.placer_navire(self.navire_a_placer, positions)
                for pos_x, pos_y in positions:
                    self.boutons_joueur[pos_x][pos_y].config(bg="gray")
                self.joueur.ajouter_navire(self.navire_a_placer)
                self.selectionner_prochain_navire()

    def tirer(self, x, y):
        if self.partie_terminee:
            return

        if self.tour_joueur and self.boutons_ordinateur[x][y]["state"] == "normal":
            touche, navire = self.ordinateur.plateau.tirer(x, y)
            bouton = self.boutons_ordinateur[x][y]
            bouton.config(bg="red" if touche else "blue", state="disabled")
            if touche and navire.est_coule():
                self.label_tour.config(text=f"Vous avez coulé le {navire.nom}!")
                for pos_x, pos_y in navire.positions:
                    self.boutons_ordinateur[pos_x][pos_y].config(bg="purple")
                self.mettre_a_jour_indicateur_navires()

            if self.ordinateur.tous_les_navires_coules():
                self.label_tour.config(text="Vous avez gagné!")
                self.partie_terminee = True
                return

            self.tour_joueur = False
            self.label_tour.config(text="Tour : Ordinateur")
            self.root.after(1000, self.tour_ordinateur)

    def selectionner_prochain_navire(self):
        if self.navires_a_placer:
            nom, taille = self.navires_a_placer.pop(0)
            self.navire_a_placer = Navire(nom, taille)
            self.label_tour.config(text=f"Placez votre {nom} ({taille} cases)")
        else:
            self.label_tour.config(text="Tour : Joueur")
            for x in range(10):
                for y in range(10):
                    self.boutons_ordinateur[x][y].config(state="normal")

    def tour_ordinateur(self):
        while True:
            x, y = random.randint(0, 9), random.randint(0, 9)
            if self.boutons_joueur[x][y]["state"] == "normal":
                break
        touche, navire = self.joueur.plateau.tirer(x, y)
        bouton = self.boutons_joueur[x][y]
        bouton.config(bg="red" if touche else "blue", state="disabled")
        if touche and navire.est_coule():
            self.label_tour.config(text=f"L'ordinateur a coulé votre {navire.nom}!")
            for pos_x, pos_y in navire.positions:
                self.boutons_joueur[pos_x][pos_y].config(bg="purple")
            self.mettre_a_jour_indicateur_navires()

        if self.joueur.tous_les_navires_coules():
            self.label_tour.config(text="L'ordinateur a gagné!")
            self.partie_terminee = True
            return

        self.tour_joueur = True
        self.label_tour.config(text="Tour : Joueur")

if __name__ == "__main__":
    root = tk.Tk()
    app = BatailleNavaleApp(root)
    root.mainloop()
