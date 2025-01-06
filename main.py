# Importation des bibliothèques nécessaires
import tkinter as tk
import random

# Classe représentant un navire
class Navire:
    def __init__(self, nom, taille):
        self.nom = nom
        self.taille = taille
        self.positions = []
        self.touche = 0

    def est_coule(self):
        return self.touche >= self.taille

# Classe représentant le plateau de jeu
class Plateau:
    def __init__(self):
        self.grille = [[None for _ in range(10)] for _ in range(10)]

    def placer_navire(self, navire, positions):
        for x, y in positions:
            self.grille[x][y] = navire
        navire.positions = positions

    def peut_placer_navire(self, taille, x, y, orientation):
        if orientation == "horizontal":
            if y + taille > 10:
                return False
            for i in range(taille):
                if self.grille[x][y + i] is not None:
                    return False
        else:  # orientation == "vertical"
            if x + taille > 10:
                return False
            for i in range(taille):
                if self.grille[x + i][y] is not None:
                    return False
        return True

    def tirer(self, x, y):
        if self.grille[x][y] is not None:
            navire = self.grille[x][y]
            navire.touche += 1
            self.grille[x][y] = "X"
            return True, navire
        else:
            self.grille[x][y] = "O"
            return False, None

# Classe représentant un joueur
class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.plateau = Plateau()
        self.navires = []

    def ajouter_navire(self, navire):
        self.navires.append(navire)

    def tous_les_navires_coules(self):
        return all(navire.est_coule() for navire in self.navires)

# Interface graphique principale
class BatailleNavaleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bataille Navale")

        self.joueur = Joueur("Joueur")
        self.ordinateur = Joueur("Ordinateur")

        self.tour_joueur = True

        self.navire_a_placer = None
        self.positions_temp = []

        self.creer_interface()
        self.nouvelle_partie()

    def creer_interface(self):
        # Création des grilles pour le joueur et l'ordinateur
        self.grille_joueur = tk.Frame(self.root)
        self.grille_joueur.grid(row=0, column=0, padx=10, pady=10)
        self.boutons_joueur = self.creer_grille(self.grille_joueur, self.joueur.plateau, False)

        self.grille_ordinateur = tk.Frame(self.root)
        self.grille_ordinateur.grid(row=0, column=1, padx=10, pady=10)
        self.boutons_ordinateur = self.creer_grille(self.grille_ordinateur, self.ordinateur.plateau, True)

        # Panneau de contrôle
        self.panneau_controle = tk.Frame(self.root)
        self.panneau_controle.grid(row=1, column=0, columnspan=2, pady=10)

        self.label_tour = tk.Label(self.panneau_controle, text="Placez vos navires")
        self.label_tour.pack()

        self.bouton_nouvelle_partie = tk.Button(self.panneau_controle, text="Nouvelle Partie", command=self.nouvelle_partie)
        self.bouton_nouvelle_partie.pack()

    def creer_grille(self, frame, plateau, est_ordinateur):
        boutons = []
        for x in range(10):
            ligne = []
            for y in range(10):
                bouton = tk.Button(frame, width=2, height=1, command=lambda x=x, y=y: self.placer_navire(x, y) if not est_ordinateur else self.tirer(x, y))
                bouton.grid(row=x, column=y)
                ligne.append(bouton)
            boutons.append(ligne)
        return boutons

    def nouvelle_partie(self):
        # Réinitialisation des plateaux
        self.joueur.plateau = Plateau()
        self.ordinateur.plateau = Plateau()
        self.tour_joueur = True
        self.label_tour.config(text="Placez vos navires")

        # Réinitialisation des boutons
        for x in range(10):
            for y in range(10):
                self.boutons_joueur[x][y].config(text="", bg="SystemButtonFace", state="normal")
                self.boutons_ordinateur[x][y].config(text="", bg="SystemButtonFace", state="disabled")

        # Préparation pour le placement manuel des navires
        self.navires_a_placer = [
            ("Porte-avions", 5),
            ("Croiseur", 4),
            ("Destroyer 1", 3),
            ("Destroyer 2", 3),
            ("Sous-marin 1", 2),
            ("Sous-marin 2", 2)
        ]
        self.placer_navires_aleatoires(self.ordinateur)
        self.selectionner_prochain_navire()

    def placer_navires_aleatoires(self, joueur):
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
                x = random.randint(0, 9)
                y = random.randint(0, 9)
                orientation = random.choice(["horizontal", "vertical"])
                if joueur.plateau.peut_placer_navire(taille, x, y, orientation):
                    positions = [(x + i, y) if orientation == "vertical" else (x, y + i) for i in range(taille)]
                    navire = Navire(nom, taille)
                    joueur.plateau.placer_navire(navire, positions)
                    joueur.ajouter_navire(navire)
                    place = True

    def selectionner_prochain_navire(self):
        if self.navires_a_placer:
            nom, taille = self.navires_a_placer.pop(0)
            self.navire_a_placer = Navire(nom, taille)
            self.positions_temp = []
            self.label_tour.config(text=f"Placez votre {nom} ({taille} cases)")
        else:
            self.label_tour.config(text="Tour : Joueur")
            for x in range(10):
                for y in range(10):
                    self.boutons_ordinateur[x][y].config(state="normal")

    def placer_navire(self, x, y):
        if self.navire_a_placer:
            taille = self.navire_a_placer.taille
            if len(self.positions_temp) == 0:
                self.positions_temp.append((x, y))
                self.boutons_joueur[x][y].config(bg="yellow")
            elif len(self.positions_temp) < taille:
                dernier_x, dernier_y = self.positions_temp[-1]
                if (x == dernier_x and abs(y - dernier_y) == 1) or (y == dernier_y and abs(x - dernier_x) == 1):
                    self.positions_temp.append((x, y))
                    self.boutons_joueur[x][y].config(bg="yellow")
                    if len(self.positions_temp) == taille:
                        self.joueur.plateau.placer_navire(self.navire_a_placer, self.positions_temp)
                        self.joueur.ajouter_navire(self.navire_a_placer)
                        self.selectionner_prochain_navire()

    def tirer(self, x, y):
        if self.tour_joueur and self.boutons_ordinateur[x][y]["state"] == "normal":
            touche, navire = self.ordinateur.plateau.tirer(x, y)
            bouton = self.boutons_ordinateur[x][y]
            bouton.config(bg="red" if touche else "blue", state="disabled")
            if touche and navire.est_coule():
                self.label_tour.config(text=f"Vous avez coulé le {navire.nom}!")
            if self.ordinateur.tous_les_navires_coules():
                self.label_tour.config(text="Vous avez gagné!")
                return
            self.tour_joueur = False
            self.label_tour.config(text="Tour : Ordinateur")
            self.root.after(1000, self.tour_ordinateur)

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
        if self.joueur.tous_les_navires_coules():
            self.label_tour.config(text="L'ordinateur a gagné!")
            return
        self.tour_joueur = True
        self.label_tour.config(text="Tour : Joueur")

# Lancement de l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = BatailleNavaleApp(root)
    root.mainloop()
