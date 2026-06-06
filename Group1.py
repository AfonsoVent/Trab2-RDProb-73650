from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Glucose42

# Support Enconding
def TillingProblemSupport(n, maxW, maxH):
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

    # Support Clauses (From Lab 1)
    for p1 in range(n): # pieces
        id1 = p1 + 1
        for p2 in range(p1 + 1, n): # pieces
            id2 = p2 + 1

            for x1 in range(maxW - id1 + 1): # width
                for y1 in range(maxH - id1 + 1): # heigth
                    clause = [-x[id1, x1, y1]] # (¬x[piece1, (Pos1)] ∨ (...)) 

                    for x2 in range(maxW - id2 + 1): # width
                        for y2 in range(maxH - id2 + 1): # heigth
                            # If not overlaping then can be support var
                            if not overlap(id1, x1, y1, id2, x2, y2):
                                clause.append(x[id2, x2, y2]) # ((...) ∨ x[piece2, (Pos2)] ∨ x[piece2, (Pos3)]  ∨ (...))
                        clauses.append(clause) # (¬x[piece1, (Pos1)] ∨ x[piece2, (Pos2)] ∨ (...)) ∧ (...) ∧ (¬x[piece2, (Pos1)] ∨ x[piece3, (Pos2)]
    
    # Try solve and if SAT print
    solverPrinter(clauses, x, maxW, maxH)

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
            for x1 in range(maxW - id1 + 1):
                for y1 in range(maxH - id1 + 1):
                    for x2 in range(maxW - id2 + 1):
                        for y2 in range(maxH - id2 + 1):
                            # ... check if collide
                            if overlap(id1, x1, y1, id2, x2, y2):
                                # Then express Conflict Clauses → [Pairwise Enconding Logic]
                                clauses.append([-x[id1, x1, y1], -x[id2, x2, y2]])
    
    # Try solve and if SAT print
    solverPrinter(clauses, x, maxW, maxH)

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

# check if collide
def overlap(size1, x1, y1, size2, x2, y2):
    goodOnX = (x1 + size1 <= x2) or (x2 + size2 <= x1)
    goodOnY = (y1 + size1 <= y2) or (y2 + size2 <= y1)
    return not (goodOnX or goodOnY)

print("Tiling Problem(5, 9, 7):")

print("Direct:")
TillingProblemDirect(5, 9, 7)

print("Support:")
TillingProblemSupport(5, 9, 7)


# print("Para problema n = 200")
# Pigeonhole(200)