% coloring(M, G) :- complete(M,G), consistent(M, G)

% define colors
color(red).
color(blue).
color(yellow).
color(green).

% define different predicate for colors
different(X, Y) :- color(X), color(Y), X \= Y.

% ensure that every color has an assignment
complete([], [[],[]]).
complete([paint(X, _) | T], [[X | T1], [_ | T2]]) :- complete(T, [T1 , T2]).