coloring(M, G) :- complete(M, G), consistent(M, G).

% define colors
color(red).
color(blue).
color(yellow).
color(green).

% define different predicate for colors
different(X, Y) :- color(X), color(Y), X \= Y.

% define the complete predicate
complete([], [[],[]]).
complete([paint(X, _) | T], [[X | T1], [_ | T2]]) :- complete(T, [T1 , T2]).

% define the consistent predicate
consistent(_, [[],[]]).
consistent(M, [[X | T1], [[Y | T2] | T]]) :- assignment(M, X, Xc), assignment(M, Y, Yc), different(Xc, Yc), consistent(M, [[X | T1], [T2 | T]]).
consistent(M, [[_ | T], [[] | R]]) :- consistent(M, [T, R]).


% define assignment predicate
assignment([paint(X, Xc) | _], X, Xc).
assignment([_ | R], X, Xc) :- assignment(R, X, Xc).
