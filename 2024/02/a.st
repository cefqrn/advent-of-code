| isSafe isSafeDampened zip split p1 p2 ios x |

zip := [:a1 :a2 |
	| a |

	a := OrderedCollection new.
	1 to: (a1 size min: a2 size) do: [:i |
		a add: (Array with: (a1 at: i) with: (a2 at: i))].

	a
].

isSafe := [:report |
	| window diffs isMonotone isGraduallyChanging |

	window := zip value: report value: (report copyFrom: 2 to: report size).
	diffs := window collect: [:a | (a at: 2) - (a at: 1)].

	isMonotone := (diffs allSatisfy: [:a | a >= 0]) | (diffs allSatisfy: [:a | a <= 0]).
	isGraduallyChanging := diffs allSatisfy: [:a | (1 <= a abs) & (a abs <= 3)].

	isMonotone & isGraduallyChanging
].

isSafeDampened := [:report |
	(((1 to: report size)
		collect: [:i |
			((1 to: report size)
				reject: [:a | a == i])
				collect: [:a | report at: a]])
		select: isSafe)
		isEmpty not
].

split := [:s |
	| words curr left |

	words := OrderedCollection new.

	left := s.
	curr := left indexOf: $  ifAbsent: [-1].
	[curr > 0] whileTrue: [
		words add: (left copyFrom: 1 to: curr-1).

		left := left copyFrom: curr+1 to: left size.
		curr := left indexOf: $  ifAbsent: [-1].
	].
	words add: left.

	words
].


Transcript clear.

p1 := p2 := 0.

ios := FileStream oldFileNamed: 'input'.
[(x := ios nextLine) notNil]
	whileTrue: [
		| record |

		record := ((split value: x) collect: [:a | a asInteger]).

		(isSafe value: record) ifTrue: [ p1 := p1 + 1 ].
		(isSafeDampened value: record) ifTrue: [ p2 := p2 + 1 ].
	].
ios close.

Transcript show: p1; cr.
Transcript show: p2; cr.
