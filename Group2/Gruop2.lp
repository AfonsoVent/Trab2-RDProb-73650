#program base.

% Define (n) pieces
piece(1..n).

% Define board
#external boardSize(W, H).

% Auxiliar predicaded
position(X, Y) :- boardSize(W, H), 
                  X > 0, X < W, 
                  Y > 0, Y < H.

% AM1: Each piece needs to be somewhere
% (Each Piece has) {1} (position)
1 { place(P, X, Y) : position(X, Y) } 1 :- piece(P).

% The pieces *can't be* outside of the board - Write in negation
:- place(P, X, _Y), boardSize(W, _H), W < P + X
:- place(P, _X, Y), boardSize(_W, H), H < P + Y

% Conflict Clauses: 
% 2 pieces *can't be* overleaping - Write in negation
:- place(P1, X1, Y1), place(P2, X2, Y2), 
    X1 < X2 + P2, X2 < X1 + P1,
    Y1 < Y2 + P2, Y2 < Y1 + P1.

% Output
#show place/3.