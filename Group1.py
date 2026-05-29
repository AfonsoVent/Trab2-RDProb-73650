from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Glucose42

def TillingProblem(n, maxW, maxH):
    # Create pieces
    pieces = ConstructPieces(n)
    
    # Instantiate vars
    pool = IDPool()
    varsIds = []
    for p in range(n):
        pieceId = p + 1
        for w in range(maxW):
            for h in range(maxH):
                varsIds.append([pool.id(f"piece {pieceId} has origin at (x:{w}, y:{h})"), (f"piece {pieceId} has origin at (x:{w}, y:{h})")])

    print(varsIds)
    # Check 

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

print("Para problema n = 3")
TillingProblem(2, 2, 2)

# print("Para problema n = 200")
# Pigeonhole(200)