# Importation des bibliothèques nécessaires
import tkinter as tk  # Bibliothèque pour créer une interface graphique
import random  # Bibliothèque pour générer des placements aléatoires

# Classe représentant un navire
class Navire:
    def __init__(self, nom, taille):
        # Initialise le nom du navire
        self.nom = nom  # Nom du navire (ex: Porte-avions, Croiseur)
        # Initialise la taille du navire (en nombre de cases)
        self.taille = taille
        # Initialise les positions occupées par le navire (vide au départ)
        self.positions = []
        # Initialise le compteur de touches (0 au départ)
        self.touche = 0

    def est_coule(self):
        # Vérifie si le nombre de touches est supérieur ou égal à la taille du navire
        return self.touche >= self.taille

# Classe représentant le plateau de jeu
class Plateau:
    def __init__(self):
        # Initialise une grille 10x10 remplie de None (vide)
        self.grille = [[None for _ in range(10)] for _ in range(10)]

    def placer_navire(self, navire, positions):
        # Pour chaque position dans la liste de positions
        for x, y in positions:
            # Associe le navire à la case correspondante dans la grille
            self.grille[x][y] = navire
        # Stocke les positions dans l'objet navire
        navire.positions = positions

    def peut_placer_navire(self, taille, x, y, orientation):
        # Vérifie si le navire peut être placé horizontalement
        if orientation == "horizontal":
            # Vérifie si le navire dépasse les limites horizontales
            if y + taille > 10:
                return False
            # Vérifie que toutes les cases nécessaires sont libres
            for i in range(taille):
                if self.grille[x][y + i] is not None:
                    return False
        else:  # Cas d'orientation verticale
            # Vérifie si le navire dépasse les limites verticales
            if x + taille > 10:
                return False
            # Vérifie que toutes les cases nécessaires sont libres
            for i in range(taille):
                if self.grille[x + i][y] is not None:
                    return False
        # Si toutes les vérifications passent, le placement est possible
        return True

    def tirer(self, x, y):
        # Vérifie si une cible est présente à la position donnée
        if self.grille[x][y] is not None:
            # Récupère le navire présent sur la case
            navire = self.grille[x][y]
            # Incrémente le compteur de touches du navire
            navire.touche += 1
            # Marque la case comme touchée
            self.grille[x][y] = "X"
            # Retourne True (touché) et le navire affecté
            return True, navire
        else:
            # Marque la case comme manquée
            self.grille[x][y] = "O"
            # Retourne False (manqué) et aucune référence de navire
            return False, None

# Classe représentant un joueur
class Joueur:
    def __init__(self, nom):
        # Initialise le nom du joueur
        self.nom = nom
        # Initialise un plateau vide pour le joueur
        self.plateau = Plateau()
        # Initialise une liste vide pour stocker les navires du joueur
        self.navires = []

    def ajouter_navire(self, navire):
        # Vérifie que le nombre de navires ne dépasse pas 6
        if len(self.navires) < 6:
            # Ajoute le navire à la liste
            self.navires.append(navire)
        else:
            # Lève une exception si le maximum est atteint
            raise ValueError("Le nombre maximum de navires a déjà été atteint.")

    def tous_les_navires_coules(self):
        # Vérifie si tous les navires du joueur sont coulés
        return all(navire.est_coule() for navire in self.navires)

# Interface graphique principale
class BatailleNavaleApp:
    def __init__(self, root):
        # Référence à la fenêtre racine
        self.root = root
        # Définit le titre de la fenêtre
        self.root.title("Bataille Navale")

        # Initialise le joueur humain
        self.joueur = Joueur("Joueur")
        # Initialise le joueur ordinateur
        self.ordinateur = Joueur("Ordinateur")

        # Indique si c'est au tour du joueur (True par défaut)
        self.tour_joueur = True
        # Indique si la partie est terminée (False par défaut)
        self.partie_terminee = False

        # Référence au navire en cours de placement (None au départ)
        self.navire_a_placer = None
        # Orientation par défaut pour le placement des navires
        self.orientation = "horizontal"

        # Crée l'interface graphique
        self.creer_interface()
        # Initialise une nouvelle partie
        self.nouvelle_partie()

    def creer_interface(self):
        # Création de la grille pour le joueur
        self.grille_joueur = tk.Frame(self.root)
        # Place la grille dans la fenêtre
        self.grille_joueur.grid(row=0, column=0, padx=10, pady=10)
        # Génère les boutons associés à la grille du joueur
        self.boutons_joueur = self.creer_grille(self.grille_joueur, self.joueur.plateau, False)

        # Création de la grille pour l'ordinateur
        self.grille_ordinateur = tk.Frame(self.root)
        # Place la grille dans la fenêtre
        self.grille_ordinateur.grid(row=0, column=1, padx=10, pady=10)
        # Génère les boutons associés à la grille de l'ordinateur
        self.boutons_ordinateur = self.creer_grille(self.grille_ordinateur, self.ordinateur.plateau, True)

        # Création du panneau de contrôle pour les interactions
        self.panneau_controle = tk.Frame(self.root)
        # Place le panneau sous les grilles
        self.panneau_controle.grid(row=1, column=0, columnspan=2, pady=10)

        # Label pour afficher les informations de tour
        self.label_tour = tk.Label(self.panneau_controle, text="Placez vos navires")
        self.label_tour.pack()

        # Label pour indiquer les navires coulés du joueur
        self.label_navires_joueur = tk.Label(self.panneau_controle, text="Navires coulés (Joueur) : Aucun")
        self.label_navires_joueur.pack()

        # Label pour indiquer les navires coulés de l'ordinateur
        self.label_navires_ordinateur = tk.Label(self.panneau_controle, text="Navires coulés (Ordinateur) : Aucun")
        self.label_navires_ordinateur.pack()

        # Bouton pour changer l'orientation en horizontal
        self.bouton_horizontal = tk.Button(self.panneau_controle, text="Horizontal", command=lambda: self.set_orientation("horizontal"))
        self.bouton_horizontal.pack(side=tk.LEFT, padx=5)

        # Bouton pour changer l'orientation en vertical
        self.bouton_vertical = tk.Button(self.panneau_controle, text="Vertical", command=lambda: self.set_orientation("vertical"))
        self.bouton_vertical.pack(side=tk.LEFT, padx=5)

        # Bouton pour démarrer une nouvelle partie
        self.bouton_nouvelle_partie = tk.Button(self.panneau_controle, text="Nouvelle Partie", command=self.nouvelle_partie)
        self.bouton_nouvelle_partie.pack(side=tk.RIGHT, padx=5)

    def creer_grille(self, frame, plateau, est_ordinateur):
        # Initialise une liste pour contenir les boutons de la grille
        boutons = []
        # Parcourt les lignes de la grille
        for x in range(10):
            # Initialise une liste pour la ligne courante
            ligne = []
            # Parcourt les colonnes de la grille
            for y in range(10):
                # Crée un bouton avec une commande spécifique selon le type de grille
                bouton = tk.Button(frame, width=2, height=1, bg="light blue", command=lambda x=x, y=y: self.placer_navire(x, y) if not est_ordinateur else self.tirer(x, y))
                # Place le bouton dans la grille Tkinter
                bouton.grid(row=x, column=y)
                # Ajoute le bouton à la ligne courante
                ligne.append(bouton)
            # Ajoute la ligne complète à la liste des boutons
            boutons.append(ligne)
        # Retourne la grille complète de boutons
        return boutons

    def set_orientation(self, orientation):
        # Met à jour l'orientation actuelle des navires
        self.orientation = orientation

    def mettre_a_jour_indicateur_navires(self):
        # Liste des noms des navires coulés pour le joueur
        navires_joueur_coules = [navire.nom for navire in self.joueur.navires if navire.est_coule()]
        # Liste des noms des navires coulés pour l'ordinateur
        navires_ordinateur_coules = [navire.nom for navire in self.ordinateur.navires if navire.est_coule()]

        # Met à jour le texte du label des navires coulés du joueur
        self.label_navires_joueur.config(text=f"Navires coulés (Joueur) : {', '.join(navires_joueur_coules) if navires_joueur_coules else 'Aucun'}")
        # Met à jour le texte du label des navires coulés de l'ordinateur
        self.label_navires_ordinateur.config(text=f"Navires coulés (Ordinateur) : {', '.join(navires_ordinateur_coules) if navires_ordinateur_coules else 'Aucun'}")

    def nouvelle_partie(self):
        # Réinitialise les plateaux des deux joueurs
        self.joueur.plateau = Plateau()
        self.ordinateur.plateau = Plateau()
        # Réinitialise les listes de navires des deux joueurs
        self.joueur.navires = []
        self.ordinateur.navires = []
        # Réinitialise le tour du joueur
        self.tour_joueur = True
        # Réinitialise l'état de la partie (non terminée)
        self.partie_terminee = False
        # Met à jour le texte du label pour indiquer le placement des navires
        self.label_tour.config(text="Placez vos navires")

        # Réinitialise les boutons des grilles
        for x in range(10):
            for y in range(10):
                self.boutons_joueur[x][y].config(text="", bg="light blue", state="normal")
                self.boutons_ordinateur[x][y].config(text="", bg="light blue", state="disabled")

        # Met à jour les indicateurs de navires coulés
        self.mettre_a_jour_indicateur_navires()
        # Définit les navires à placer pour le joueur
        self.navires_a_placer = [
            ("Porte-avions", 5),
            ("Croiseur", 4),
            ("Destroyer 1", 3),
            ("Destroyer 2", 3),
            ("Sous-marin 1", 2),
            ("Sous-marin 2", 2)
        ]
        # Place les navires de l'ordinateur aléatoirement
        self.placement_navires_aleatoire(self.ordinateur)
        # Prépare le placement du premier navire du joueur
        self.selectionner_prochain_navire()

    def placement_navires_aleatoire(self, joueur):
        # Parcourt la liste des navires à placer
        for nom, taille in [
            ("Porte-avions", 5),
            ("Croiseur", 4),
            ("Destroyer 1", 3),
            ("Destroyer 2", 3),
            ("Sous-marin 1", 2),
            ("Sous-marin 2", 2)
        ]:
            place = False
            # Essaye de placer le navire jusqu'à trouver une position valide
            while not place:
                x = random.randint(0, 9)
                y = random.randint(0, 9)
                orientation = random.choice(["horizontal", "vertical"])
                if joueur.plateau.peut_placer_navire(taille, x, y, orientation):
                    positions = [(x + i, y) if orientation == "vertical" else (x, y + i) for i in range(taille)]
                    navire = Navire(nom, taille)
                    joueur.plateau.placer_navire(navire, positions)
                    joueur.ajouter_navire(navire)
                    place = True

    def placer_navire(self, x, y):
        # Gère le placement manuel d'un navire par le joueur
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
        # Gère le tir sur la grille de l'ordinateur
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
        # Prépare le placement du prochain navire pour le joueur
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
        # Simule le tour de l'ordinateur avec un tir aléatoire
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
    # Crée la fenêtre principale Tkinter
    root = tk.Tk()
    # Initialise l'application Bataille Navale
    app = BatailleNavaleApp(root)
    # Lance la boucle principale de Tkinter
    root.mainloop()
