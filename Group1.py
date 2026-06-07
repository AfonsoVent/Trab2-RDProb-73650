from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Glucose42

import math
import sys

# (Project 1)
def min_pack(n):
    # (Theorical) Min area: [Ei²] - sum(1^2 + (...) + n^2)
    min_area = sum(i**2 for i in range(1, n + 1))

    # Slowly incresing the area to pack()
    for area in range(min_area, min_area * 2):
        candidates = []
        
        # (Theorical) Creating candidates
        for h in range(n, int(math.sqrt(area)) + 1):
            # The value must be entire number
            if area % h == 0:
                w = area // h

                # (Theorical) (Width >= Height) and (Width >= n) and (Height >= n):
                if w >= h and h >= n:
                    # (Theorical) k = [(H + 1) / 2].floor()
                    k = math.floor((h + 1) / 2)

                    # Creating the Theorical Value: (Ej)
                    sum_j = sum(j for j in range(k, n + 1))

                    # (Theorical) Width >= (Ej)
                    if w >= sum_j: candidates.append((w, h))

        # Sort candidates[Weigth, Heigth]
        candidates.sort(key=lambda x: x[1])

        # Test candidates
        for w_cand, h_cand in candidates:
            # Debug
            print("Valid candidate found.") 
            print(f"Testing with area: {area} | Dimensions: {w_cand} x {h_cand}")
            if TillingProblemDirect(n, w_cand, h_cand):
                # if - True; optimal solution found
                print(f"Minimum area: {area}")
                print(f"Dimensions: {w_cand} x {h_cand}")
                sys.exit(0)
            else:
                # Debug
                print(f"Failed with Dimensions: {w_cand} x {h_cand}")
        # Debug
        print(f"With area: {area} none combination didn't worked")

# Direct Enconding
def TillingProblemDirect(n, maxW, maxH):
    clauses = []

    if n > maxW or n > maxH:
        print("UNSAT")
        return [] # Return list empty (Project 1 requirement)
    
    # Instantiate vars
    x = Instantiater(n, maxW, maxH)
    
    # At Least 1: Each piece needs to be somewhere
    AL1(clauses, x, n, maxW, maxH)

    # At Most 1: One piece can't be place on 2 places
    AM1(clauses, x, n, maxW, maxH)

    # Conflict Clauses: One piece must not overlap another
    for p1 in range(n):
        id1 = p1 + 1
        for p2 in range(p1 + 1, n):
            id2 = p2 + 1
            
            # On each position...
            for w1 in range(maxW - id1 + 1):
                for h1 in range(maxH - id1 + 1):
                    for w2 in range(maxW - id2 + 1):
                        for h2 in range(maxH - id2 + 1):
                            # ... check if collide
                            if overlap(id1, w1, h1, id2, w2, h2):
                                # Then express Conflict Clauses → [Pairwise Enconding Logic]
                                clauses.append([-x[id1, w1, h1], -x[id2, w2, h2]])
    
    # Try solve and if SAT print
    return solverPrinter(clauses, x, maxW, maxH)

def AL1(clauses, x, n, maxW, maxH):
    for p in range(n): # pieces
        pieceId = p + 1
        clause = []
        for w in range(maxW - pieceId + 1): # width
            for h in range(maxH - pieceId + 1): # heigth
                clause.append(x[pieceId, w, h]) # (x[PieceX, 0, 0] ∨ ... ∨ x[PieceX, (maxW - pieceId + 1), (maxH - pieceId + 1)])
        clauses.append(clause) # (x[1, _, _] ∧ ... ∧ x[p, _, _])

def AM1(clauses, x, n, maxW, maxH):
    for p in range(n): # pieces
        pieceId = p + 1

        # Creating every piece with position
        pieceVars = []
        for w in range(maxW - pieceId + 1): # width
            for h in range(maxH - pieceId + 1): # heigth
                pieceVars.append(x[pieceId, w, h])

        # Then we apply per pairs
        numVars = len(pieceVars)
        for i in range(numVars): # PieceX on Pos1
            for j in range(i + 1, numVars): # PieceX on Pos2
                clauses.append([-pieceVars[i], -pieceVars[j]]) # (~x[PieceX, (Pos1)] ∨ ~x[PieceX, (Pos2)]) ∧ (~x[PieceX, (Pos2)] ∨ ~x[PieceX, (Pos3)]) ∧ ...
 
def Instantiater(n, maxW, maxH):
    pool = IDPool()
    x = {}

    for p in range(n): # pieces
        pieceId = p + 1
        for w in range(maxW - pieceId + 1): # Already removing some impossible tiling pieces
            for h in range(maxH - pieceId + 1): # Already removing some impossible tiling pieces
                x[pieceId, w, h] = pool.id(f"piece {pieceId} has origin at (x:{w}, y:{h})")
    
    return x

def solverPrinter(clauses, x, maxW, maxH):
    with Glucose42() as solver:
        # Add each clause on solver
        for c in clauses: solver.add_clause(c)
        
        # call Sat
        sat = solver.solve()
        
        # Check if exists solution
        print("SAT:" if sat else "UNSAT")
        
        # Print Solution (Adaptation of Project 1)
        if sat:
            # Get model
            modelSet = set(solver.get_model())

            # Colums
            colums = "    "
            for i in range(maxW):
                colums += f"{i + 1} "
            print(colums)

            # The second line
            print("  /" + "--" * maxW)

            # Empty grid
            grid = [["." for _ in range(maxW)] for _ in range(maxH)]

            # Insert values
            for ((pieceId, w, h), varId) in x.items():
                if varId in modelSet:
                    dPiece = pieceId
                    
                    for dy in range(dPiece):
                        for dx in range(dPiece):
                            grid[h + dy][w + dx] = str(pieceId)
            
            # Print grid
            for hIdx in range(maxH):
                rowStr = f"{hIdx} | "
                for wIdx in range(maxW):
                    rowStr += f"{grid[hIdx][wIdx]} "
                print(rowStr)
            
            return True
        return False

# check if collide
def overlap(size1, w1, h1, size2, w2, h2):
    goodOnX = (w1 + size1 <= w2) or (w2 + size2 <= w1)
    goodOnY = (h1 + size1 <= h2) or (h2 + size2 <= h1)
    return not (goodOnX or goodOnY)

print("Tiling Problem(5, 9, 7):")

print("Direct:")
TillingProblemDirect(5, 9, 7)

print("Optimal Tiling Problem(5, 9, 7):")

print("Direct:")
min_pack(5)