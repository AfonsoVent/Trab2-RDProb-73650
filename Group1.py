from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Glucose42

def TillingProblem(n, maxW, maxH):
    clauses = []

    if n > maxW or n > maxH:
        print("UNSAT")
        return [] # Return list empty (Project 1 requirement)
    
    # Instantiate vars
    pool = IDPool()
    x = {}
    for p in range(n): # pieces
        pieceId = p + 1
        for w in range(maxW - pieceId + 1): # Already removing some impossible tiling pieces
            for h in range(maxH - pieceId + 1): # Already removing some impossible tiling pieces
                x[pieceId, w, h] = pool.id(f"piece {pieceId} has origin at (x:{w}, y:{h})")
    
    # At Least 1: Each piece needs to be somewhere
    for p in range(n): # pieces
        pieceId = p + 1
        clause = []
        for w in range(maxW - pieceId + 1): # width
            for h in range(maxH - pieceId + 1): # heigth
                clause.append(x[pieceId, w, h]) # (x[PieceX, 0, 0] ∨ ... ∨ x[PieceX, (maxW - pieceId + 1), (maxH - pieceId + 1)])
        clauses.append(clause) # (x[1, _, _] ∧ ... ∧ x[p, _, _])

    # At Most 1: One piece can't be place on 2 places
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
    
    with Glucose42() as solver:
        # Add each clause on solver
        for c in clauses: solver.add_clause(c)
        
        # call Sat
        sat = solver.solve()
        
        # Check if exists solution
        print("SAT" if sat else "UNSAT")
        
        # TODO: make a better printer
        # Print Solution
        if sat:
            print(solver.get_model())

# check if collide
def overlap(size1, x1, y1, size2, x2, y2):
    goodOnX = (x1 + size1 <= x2) or (x2 + size2 <= x1)
    goodOnY = (y1 + size1 <= y2) or (y2 + size2 <= y1)
    return not (goodOnX or goodOnY)


TillingProblem(5, 9, 7)

# print("Para problema n = 200")
# Pigeonhole(200)