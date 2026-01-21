import math
import itertools
from typing import Optional
import matplotlib.pyplot as plt

EPS = 1e-9


class point:
    x: float
    y: float

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class FctObj:
    a: float
    b: float
    isMax: bool

    def __init__(self, a=0, b=0, isMax=False):
        self.a = a
        self.b = b
        self.isMax = isMax

    def lire(self):
        m = "Max" if self.isMax else "Min"
        return f"{m} {self.a if self.a != 1 else ''}X {"+" if self.b >= 0 else "-"} {abs(self.b) if abs(self.b) != 1 else ''}Y"

    def saisir(self):
        print("Structure: min/max aX + bY")
        a = float(input("Entrez a: ").replace(",", "."))
        b = float(input("Entrez b: ").replace(",", "."))
        c = (input("Entrez min ou max: ")).strip().lower()

        if c != "min" and c != "max":
            print("Mauvaise entree, saisie annulee!")
            return None

        self.a = a
        self.b = b
        self.isMax = c == "max"
        return self

    def calculer(self, point: point):
        return self.a * point.x + self.b * point.y


class Contrainte:
    a: float
    b: float
    c: float
    type: str

    def lire(self):
        if self.a == 0:
            return f"{self.b if self.b != 1 else ''}Y {self.type} {self.c}"
        if self.b == 0:
            return f"{self.a if self.a != 1 else ''}X {self.type} {self.c}"
        return f"{self.a if self.a != 1 else ''}X {"+" if self.b >= 0 else "-"} {abs(self.b) if abs(self.b) != 1 else ''}Y {self.type} {self.c}"

    def saisir(self):
        print("Structure: aX + bY <=/>=/= c")
        a = float(input("Entrez a: ").replace(",", "."))
        b = float(input("Entrez b: ").replace(",", "."))
        o = input("Entrez <= ou >= ou =: ").strip()
        c = float(input("Entrez c: ").replace(",", "."))

        if o not in ("=", "<=", ">="):
            print("Mauvaise entree, saisie annulee!")
            return None

        if abs(a) < 1e-15 and abs(b) < 1e-15:
            print("Mauvaise entree: a=b=0 (contrainte vide).")
            return None

        self.a = a
        self.b = b
        self.c = c
        self.type = o
        return self

    def __init__(self, a=1, b=1, c=0, type=">="):
        self.a = a
        self.b = b
        self.c = c
        self.type = type


class Plotteur:

    def plotIntersection(self, Inter: point):
        # On trace un point rouge pour l'intersection
        plt.plot(Inter.x, Inter.y, "ro", markersize=8, zorder=5)

    def tracerContrainte(self, contrainte: Contrainte):
        x_coords, y_coords = self.contrainteToPoints(contrainte)

        if x_coords is None:
            print("Contrainte invalide (a=0 et b=0).")
            return

        # On trace la ligne sans appeler plt.show() ici
        label = contrainte.lire()
        plt.plot(x_coords, y_coords, marker="", linestyle="-", label=label)

    def tracerContraintes(self, contraintes: list[Contrainte]):

        for c in contraintes:
            self.tracerContrainte(c)

    def tracerPolygoneFaisable(self, faisables: list[point]):
        if len(faisables) < 3:
            return  # Pas assez de points pour former un polygone

        x_coords, y_coords = pointsToXY(faisables)
        # Fermer le polygone en ajoutant le premier point à la fin
        x_coords.append(faisables[0].x)
        y_coords.append(faisables[0].y)

        plt.fill(
            x_coords, y_coords, color="lightblue", alpha=0.5, label="Région Faisable"
        )

    def showPlot(self):
        plt.grid(True)
        plt.legend()
        plt.show()

    def contrainteToPoints(self, contrainte: Contrainte):

        MIN_VAL = -1000
        MAX_VAL = 1000

        # Cas 1: Ligne Verticale (b = 0)
        if abs(contrainte.b) < EPS:
            if abs(contrainte.a) < EPS:
                return None, None

            x_val = contrainte.c / contrainte.a
            # X est constant et Y varie de MIN à MAX
            return [x_val, x_val], [MIN_VAL, MAX_VAL]

        # Cas 2: Ligne Horizontale (a = 0) ou ligne oblique
        y1 = (contrainte.c - contrainte.a * MIN_VAL) / contrainte.b
        y2 = (contrainte.c - contrainte.a * MAX_VAL) / contrainte.b

        return [MIN_VAL, MAX_VAL], [y1, y2]

    def drawSolution(self, sol: point):
        if sol:
            plt.plot(
                sol.x,
                sol.y,
                "r*",
                markersize=15,
                label=f"Optimum ({sol.x:.2f}, {sol.y:.2f})",
                zorder=10,
            )
            plt.text(
                sol.x,
                sol.y,
                f"  ({sol.x:.1f}, {sol.y:.1f})",
                color="red",
                fontweight="bold",
                zorder=10,
            )

    def plotProbleme(
        self,
        contraintes: list[Contrainte],
        faisables: list[point],
        objectif: FctObj,
        sol: point,
    ):
        plt.figure(figsize=(8, 8))
        plt.xlabel("Axe X")
        plt.ylabel("Axe Y")
        plt.xlim(-0.25, 20)
        plt.ylim(-0.25, 20)
        self.tracerContraintes(contraintes)
        self.tracerPolygoneFaisable(faisables)
        self.drawSolution(sol)
        plt.title("Représentation Graphique du Problème: " + objectif.lire())
        self.showPlot()


class Resolveur:
    intersections: list[point]
    solution: point
    pfaisables: list[point]

    def __init__(self):
        self.intersections = []
        self.solution = None
        self.pfaisables = []

    def testPointContrainte(self, p: point, c: Contrainte):
        d = c.a * p.x + c.b * p.y

        if c.type == "<=":
            return d <= c.c + EPS
        elif c.type == ">=":
            return d >= c.c - EPS
        elif c.type == "=":
            return abs(d - c.c) <= 1e-7
        else:
            print("type non supporté:", c.type)
            return False

    def testPointToutesContraintes(self, p: point, contraintes: list[Contrainte]):
        for c in contraintes:
            if not self.testPointContrainte(p, c):
                return False
        return True

    def intersectionDeuxContraintes(self, c1: Contrainte, c2: Contrainte):
        a1, b1, d1 = c1.a, c1.b, c1.c
        a2, b2, d2 = c2.a, c2.b, c2.c
        det = (a1 * b2) - (a2 * b1)
        if abs(det) < 1e-12:
            return None
        x = (d1 * b2 - d2 * b1) / det
        y = (a1 * d2 - a2 * d1) / det
        if not (math.isfinite(x) and math.isfinite(y)):
            return None
        if abs(x) < 1e-10:
            x = 0.0
        if abs(y) < 1e-10:
            y = 0.0
        return point(x, y)

    def calculerIntersections(self, contraintes: list[Contrainte]) -> list[point]:
        pts: list[point] = []
        for c1, c2 in itertools.combinations(contraintes, 2):
            p = self.intersectionDeuxContraintes(c1, c2)
            if p is not None:
                pts.append(p)
        uniques: list[point] = []
        for p in pts:
            deja = False
            for q in uniques:
                if abs(p.x - q.x) < 1e-8 and abs(p.y - q.y) < 1e-8:
                    deja = True
                    break
            if not deja:
                uniques.append(p)
        return uniques

    def trouver_faisables(
        self, points: list[point], contraintes: list[Contrainte]
    ) -> list[point]:
        faisables: list[point] = []
        for p in points:
            if self.testPointToutesContraintes(p, contraintes):
                faisables.append(p)
        return self.trierPoints(faisables)

    def choisirOptimum(self, obj: FctObj, faisables: list[point]):
        best_p = faisables[0]
        best_Z = obj.calculer(best_p)
        for p in faisables[1:]:
            Z = obj.calculer(p)

            if obj.isMax:
                if Z > best_Z:
                    best_Z = Z
                    best_p = p
            else:
                if Z < best_Z:
                    best_Z = Z
                    best_p = p

        return best_p, best_Z

    def resoudre(self, obj: FctObj, contraintes: list[Contrainte]):
        inters = self.calculerIntersections(contraintes)
        faisables = self.trouver_faisables(inters, contraintes)
        if len(faisables) == 0:
            return None, None, inters, faisables
        sol, Z = self.choisirOptimum(obj, faisables)
        return sol, Z, inters, faisables

    # tri des points en ordre circulaire ( utile pour le plotteur )
    def trierPoints(self, points: list[point]) -> list[point]:
        if len(points) < 3:
            return points
        cx = sum(p.x for p in points) / len(points)
        cy = sum(p.y for p in points) / len(points)
        return sorted(
            points, key=lambda p: math.atan2(p.y - cy, p.x - cx)
        )  # tri par angle par rapport au centre du poligone


# in progress
class Probleme:
    obj: FctObj
    contraintes: list[Contrainte]
    intersections: list[point]
    faisables: list[point]
    solution: Optional[point]
    z_opt: Optional[float]
    plot: Plotteur
    res: Resolveur
    resolu: bool

    def __init__(self):
        self.reinitialiser()

    def reinitialiser(self):
        # Contraintes par défaut : x >= 0 et y >= 0
        self.contraintes = [
            Contrainte(1, 0, 0, ">="),  # x >= 0
            Contrainte(0, 1, 0, ">="),  # y >= 0
            Contrainte(1, 0, 1000, "<="),  # x <= 100
            Contrainte(0, 1, 1000, "<="),  # y <= 100
        ]
        self.obj = FctObj()
        self.intersections = []
        self.faisables = []
        self.solution = None
        self.z_opt = None
        self.plot = Plotteur()
        self.res = Resolveur()
        self.resolu = False

    def menu(self):
        print("Menu:")
        a = 0
        print("")
        while a != 7:
            a = menuPrint()
            match a:
                case 1:
                    self.saisirObj()
                case 2:
                    self.saisirContrainte()
                case 3:
                    self.afficherProbleme()
                case 4:
                    self.reinitialiser()
                case 5:
                    self.tracerprobleme()
                case 6:
                    self.resoudreProbleme()
                case 7:
                    print("Bye!")
                case _:
                    print("Mauvaise entree reessayez!")
            print()
            print()

    def saisirObj(self):
        self.resolu = False
        tmp = self.obj.saisir()
        if tmp is None:
            print("Fonction objectif non modifiée (saisie annulée).")
        else:
            print("Fonction objectif enregistrée.")

    def tracerprobleme(self):
        if not self.resolu:
            print("Le problème n'a pas encore été résolu. Résolution en cours...")
            self.resoudreProbleme()
        self.plot.plotProbleme(
            self.contraintes, self.faisables, self.obj, self.solution
        )

    def saisirContrainte(self):
        c = Contrainte().saisir()
        if c is not None:
            self.resolu = False
            self.contraintes.append(c)
            print("Contrainte ajoutée.")
        else:
            print("Contrainte non ajoutée.")

    def afficherProbleme(self):
        print("__________________________________")
        print(self.obj.lire())
        print("S.C:")
        for c in reversed(self.contraintes):
            print(c.lire())
        print("___________________________________")

    def resoudreProbleme(self):

        sol, z, inters, faisables = self.res.resoudre(self.obj, self.contraintes)

        self.intersections = inters
        self.faisables = faisables
        self.solution = sol
        self.z_opt = z
        self.resolu = True
        if sol is None:
            print("Aucune solution faisable (infeasible).")
            return

        print("Résolution terminée")
        print(f"Nombre d'intersections calculées : {len(inters)}")
        print(f"Nombre de points faisables : {len(faisables)}")
        print(f"Solution optimale : x*={sol.x}, y*={sol.y}")
        print(f"Z* = {z}")


# helper functions
def menuPrint():
    print("1.Saisir la fonction objectif")
    print("2.Ajouter contrainte")
    print("3.Afficher probleme")
    print("4.Reinitialiser probleme")
    print("5.Tracer probleme")
    print("6.Resoudre le probleme")
    print("7.Quitter")

    try:
        return int(input("Entrez l'option choisie: "))
    except:
        return -1


def pointsToXY(p: list[point]):
    x = []
    y = []
    for pt in p:
        x.append(pt.x)
        y.append(pt.y)
    return x, y


if __name__ == "__main__":
    p = Probleme()
    p.menu()
