#program base.

% Define (n) pieces
piece(1..n).

% Define limits - Script already decremented
#program dim(w, h).
limW(0..w).
limH(0..h).

% Will change - external
#external boardSize(w, h).

% Auxiliar predicaded - safe: has on body positive pred(X)
position(X, Y) :- limW(X), limH(Y).

% AL1: Each piece needs to be somewhere -> min: 1
% AM1: Each piece can't be in two places -> max: 1
% (Each Piece has) {1} (position)
1 { place(P, X, Y) : position(X, Y) } 1 :- piece(P).

% The pieces *can't be* outside of the board - Write in negation
:- place(P, X, _Y), w < P + X.
:- place(P, _X, Y), h < P + Y.

% Conflict Clauses: 
% 2 pieces *can't be* overleaping - Write in negation
:- place(P1, X1, Y1), place(P2, X2, Y2), P1 < P2,
    X1 < X2 + P2, X2 < X1 + P1,
    Y1 < Y2 + P2, Y2 < Y1 + P1.

% Output
#show place/3.