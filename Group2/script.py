import clingo
import math
import sys
#TODO: Se a dim for 1..12 => tem 13 para colocar aidna
def pack(ctl, w, h):
    # Define dimensions of board
    ctl.ground([("dim", [
                clingo.Number(w), 
                clingo.Number(h)])
    ])

    # Call
    ctl.assign_external(
        clingo.Function("boardSize", [
                clingo.Number(w), 
                clingo.Number(h)]), 
        True)
    
    placements = []
    sat = False

    # Try solve
    with ctl.solve(yield_=True) as handle:
        for model in handle:
            sat = True
            
            for symbol in model.symbols(shown=True):
                if symbol.name == "place": # place(P, X, Y)
                    # Extract ints
                    p, x, y = [arg.number for arg in symbol.arguments]
                    placements.append((p, x, y))
        
        # Save result
        result = handle.get()

    # If sat then print result
    if result.satisfiable:
        print("SAT:")
        solverPrinter(placements, w, h)
    
    # Clean call
    ctl.release_external(
        clingo.Function("boardSize", [
                clingo.Number(w), 
                clingo.Number(h)])
    )

    return sat

def solverPrinter(placements, maxW, maxH):
    # Print Solution (Adaptation of Project 1)
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
    for (pieceId, w, h) in placements:            
        for dy in range(pieceId):
            for dx in range(pieceId):
                if h + dy < maxH and w + dx < maxW:
                    grid[h + dy][w + dx] = str(pieceId)
    
    # Print grid
    for hIdx in range(maxH):
        rowStr = f"{hIdx + 1} | "
        for wIdx in range(maxW):
            rowStr += f"{grid[hIdx][wIdx]} "
        print(rowStr)

def minPack(n):
    ctl = clingo.Control()
    ctl.load("Group2.lp")
    
    # Base - n never changes, we only need 1 time
    ctl.add("base", [], f"#const n={n}.")
    ctl.ground([("base", [])])

    # (Project 1)
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
            if pack(ctl, w_cand, h_cand):
                # if - True; optimal solution found
                print(f"Minimum area: {area}")
                print(f"Dimensions: {w_cand} x {h_cand}")
                sys.exit(0)
            else:
                # Debug
                print(f"Failed with Dimensions: {w_cand} x {h_cand}")
        # Debug
        print(f"With area: {area} none combination didn't worked")

if __name__ == "__main__":
    minPack(5)