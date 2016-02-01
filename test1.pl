link(a, b).
link(b, c).
path(X, Z):- link(X, Z).
path(X, Z):- path(X, Y), link(Y, Z).
member(X, [X|Rest]).
member(X, [Head|Rest]):- member(X, Rest).