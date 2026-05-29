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
        clause = []
        for w in range(maxW - pieceId + 1):
            for h in range(maxH - pieceId + 1):
                clause.append(x[p, w, h]) # (x[PieceX, 0, 0] ∨ ... ∨ x[PieceX, (maxW - pieceId + 1), (maxH - pieceId + 1)])
        clauses.append(clause) # (x[1, _, _] ∧ ... ∧ x[p, _, _])

    # At Most 1: Two pieces can't be place on the same place


def ConstructPieces(nBlocks):
    pieces = []
    for i in range(nBlocks):
        pieces.append([i + 1, i + 1])

    return pieces




# Pingeon Lab: (Para referencia, q ja fiz algo moldavel)

def Pigeonhole(n):
    pool = IDPool()
    n_vars = n * (n + 1)
    clauses = []

    x = [pool.id(f'x{i}') for i in range(1, n_vars + 1)]

    # Notice: This is Support Enconding

    # Each var needs 1 value (a)
    for i in range(n + 1):
        clause = []
        for j in range(n):
            clause.append(x[i * n + j]) # (x[v, 0] ∨ (...) ∨ x[v, n])
        clauses.append(clause)
    
    # Each var only has one value (b)
    for i in range(n + 1): # vars
        for j in range(n): # holes
            for l in range(j + 1, n):
                clauses.append([-x[i * n + j], -x[i * n + l]]) # (~x[v, i] ∨ ~x[v, j])

    # Support clauses (c)
    for i in range(n + 1): # vars
        for j in range(i, n + 1): # vars
            if i == j: 
                continue
            for l in range(n): # values
                clause = [-x[j * n + l]]

                for k in range(l, n): # values
                    if k != l:
                        clause.append(x[i * n + k])
                clauses.append(clause)


    with Glucose42() as solver:
        # Add each clause on solver
        for c in clauses: solver.add_clause(c)
        
        # call Sat
        sat = solver.solve()
        
        # Check if exists solution
        print("SAT" if sat else "UNSAT")
        
        # Print Solution
        if sat:
            print(solver.get_model())


TillingProblem(3, 2, 2)

# print("Para problema n = 200")
# Pigeonhole(200)