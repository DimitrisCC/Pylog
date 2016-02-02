append([], Y, Y).
append([A|X], Y, [A|Z]):- append(X, Y, Z).
kati([]).
kati([a,b|[]]) :- kati([]).
