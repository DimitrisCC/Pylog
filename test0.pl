likes(john, mary).
likes(george, mary).
isBoy(kostas, aged, isMale(K)).
isBored(X) :- isSleeping(X), isBoy(X).
isGirl(xrusa).
isSleeping(leuterhs).
isBoy(leuterhs).
isAwesome(leuterhs).
jealous(X,Y):- loves(X,Z),loves(Y,Z).
loves(vincent,mia).
loves(lam0,mia0).
loves(X,Y):-likes(X,Y),likes(Y,X).
likes(lam,mia).
likes(mia,lam).
