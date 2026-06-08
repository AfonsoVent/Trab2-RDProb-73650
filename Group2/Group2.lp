#program base.

% Define place(Piece, PosX, PosY)
#defined place/3.

% Define (n) pieces
piece(1..n).

% Define limits
#program dim(w, h).

% Will change - switches / external
#external boardSize(w, h).

% Auxiliar predicaded
position(w, h, X, Y) :- boardSize(w, h), 
                        X = 0..(w - 1), 
                        Y = 0..(h - 1).

% AL1: Each piece needs to be somewhere -> min: 1
% AM1: Each piece can't be in two places -> max: 1
% (Each Piece has) {1} (position)
1 { place(P, X, Y) : position(w, h, X, Y) } 1 :- piece(P), boardSize(w, h).

% The pieces *can't be* outside of the board - Write in negation
:- place(P, X, _Y), boardSize(w, h), w < P + X.
:- place(P, _X, Y), boardSize(w, h), h < P + Y.

% Conflict Clauses: 
% 2 pieces *can't be* overleaping - Write in negation
:- place(P1, X1, Y1), place(P2, X2, Y2), P1 < P2,
    X1 < X2 + P2, X2 < X1 + P1,
    Y1 < Y2 + P2, Y2 < Y1 + P1.

% Output
#show place/3.