# Graphical Method - Linear Programming Solver

A Python implementation of the graphical method for solving linear programming problems, developed as a course project for "Recherche Opérationnelle" (Operations Research).

## Overview

This project provides an interactive tool to solve 2D linear programming problems using the graphical method. It allows users to define an objective function and constraints, visualizes the feasible region, and finds the optimal solution by evaluating all corner points of the feasible polygon.

## Features

- **Interactive Menu**: User-friendly command-line interface to input problems
- **Constraint Management**: Support for linear constraints with `<=`, `>=`, and `=` operators
- **Objective Function**: Define minimization or maximization problems (aX + bY)
- **Intersection Calculation**: Automatically computes all intersection points of constraints
- **Feasibility Testing**: Identifies feasible points that satisfy all constraints
- **Optimization**: Finds the optimal solution by evaluating the objective function at all feasible vertices
- **Visualization**: Plots constraints, feasible region, and optimal solution using Matplotlib
- **Point Ordering**: Automatically orders vertices in circular order for correct polygon rendering

## Requirements

- Python 3.7+
- `matplotlib` - for visualization

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd <project-directory>
```

2. Install dependencies:

```bash
pip install matplotlib
```

## Usage

Run the program:

```bash
python methode_graphique_Projet_ro.py
```

### Interactive Menu

Once started, you'll see the following options:

```
1. Saisir la fonction objectif        (Enter objective function)
2. Ajouter contrainte                  (Add constraint)
3. Afficher probleme                   (Display problem)
4. Reinitialiser probleme              (Reset problem)
5. Tracer probleme                     (Plot problem)
6. Resoudre le probleme                (Solve problem)
7. Quitter                             (Quit)
```

### Example Workflow

1. **Define Objective Function**: Enter coefficients for a linear objective function
   - Structure: `min/max aX + bY`
   - Example: `a = 2`, `b = 3`, `max` → Maximize 2X + 3Y

2. **Add Constraints**: Input linear constraints
   - Structure: `aX + bY <= c` (or `>=` or `=`)
   - Example: `a = 1`, `b = 1`, `<=`, `c = 10` → X + Y ≤ 10

3. **Solve**: The solver will:
   - Calculate all intersection points
   - Identify feasible points
   - Find the optimal solution

4. **Visualize**: Display a graph showing:
   - Constraint lines
   - Feasible region (shaded in light blue)
   - Optimal solution (marked with a red star)

## Project Structure

### Core Classes

- **`point`**: Represents a 2D point (x, y)

- **`FctObj`**: Represents the objective function
  - Coefficients: `a`, `b`
  - Type: `isMax` (maximize or minimize)
  - Methods: `saisir()`, `lire()`, `calculer()`

- **`Contrainte`**: Represents a linear constraint
  - Coefficients: `a`, `b`, `c`
  - Type: `<=`, `>=`, `=`
  - Methods: `saisir()`, `lire()`

- **`Plotteur`**: Handles visualization
  - Plots constraint lines and feasible region
  - Marks intersection points and optimal solution
  - Methods: `plotProbleme()`, `tracerContraintes()`, `drawSolution()`

- **`Resolveur`**: Solves the linear programming problem
  - Calculates intersections between constraint pairs
  - Tests feasibility of points
  - Selects optimal solution
  - Methods: `resoudre()`, `trierPoints()`, `choisirOptimum()`

- **`Probleme`**: Main problem management class
  - Manages objective function, constraints, and solutions
  - Provides interactive menu interface
  - Methods: `menu()`, `saisirObj()`, `saisirContrainte()`, `resoudreProbleme()`

## How It Works

1. **Constraint Intersection**: Solves systems of linear equations to find all intersection points where constraints meet
2. **Feasibility Check**: Tests each intersection point against all constraints
3. **Optimization**: Evaluates the objective function at each feasible vertex
4. **Solution Selection**: Chooses the point with the best objective value (max or min)
5. **Visualization**: Renders the problem in a 2D plot showing the feasible region and optimal point

## Technical Notes

- Uses numerical precision handling (EPS = 1e-9) for floating-point comparisons
- Automatically removes duplicate intersection points within tolerance
- Sorts vertices in circular order to correctly draw the feasible polygon
- Handles edge cases: vertical lines, horizontal lines, degenerate constraints

## Limitations

- Solves only 2D linear programming problems (2 variables)
- Requires at least 3 vertices to form a feasible region
- Graphical method is impractical for large-scale problems (use simplex method instead)

## Example Problem

Maximize: Z = 2X + 3Y

Subject to:

- X + Y ≤ 10
- 2X + Y ≤ 15
- X ≥ 0
- Y ≥ 0

The solver will find the optimal solution at the vertex where Z is maximized.

## Contributors

This project was developed as a collaborative school project for the Recherche Opérationnelle course by:

# [Amine El-baydaouy](https://github.com/amineamine762)

# [Anouar Habib Allah](https://github.com/Otter-1)

## Notes

- All input accepts both `.` and `,` as decimal separators for convenience
- The program includes default non-negativity constraints (X ≥ 0, Y ≥ 0)
- Coefficients of 1 or -1 are displayed without showing the coefficient in equations

# RO_Graphic_Solver
