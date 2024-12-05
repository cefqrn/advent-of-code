\ parse a 2 digit number
: parse-int  ( a -- u )
   dup c@ 48 - 10 * swap char+ c@ 48 - + ;


\ open the file
variable fid
s" input" r/o open-file drop fid !

create line
256 constant line-size
line-size chars allot

\ reads the next line of the file into the buffer, returns length read
: readline  ( -- u )
   line line-size fid @ read-line 2drop ;

create rules
4096 chars allot
variable rule-count 0 rule-count !

: read-rules  ( -- )
   begin
      readline
      0<>
   while
      line           parse-int rules rule-count @ 2*    chars + !
      line 3 chars + parse-int rules rule-count @ 2* 1+ chars + !
      1 rule-count +!
   repeat
;

\ returns true if u1 < u2
: cmp  ( u1 u2 -- ? )
   rule-count @ 0 ?do
      over
      rules i 2* chars + c@
      =
      if
         dup
         rules i 2* 1+ chars + c@
         =
         if
            2drop
            true
            unloop exit
         then
      then
   loop
   2drop
   false
;

\ like selection sort but worse
: sort  ( a u -- )
   swap
   over 0 ?do
      over i 1+ ?do
         dup i chars + c@
         over j chars + c@
         cmp
         0<> if
            dup j chars +  \ i
            over i chars + \ i j
            over c@        \ i j *i
            over c@        \ i j *i *j
            swap           \ i j *j *i
            rot            \ i *j *i j
            c!             \ i *j       (*i stored in j)
            swap           \ *j i
            c!             \            (prev *j stored in i)
         then
      loop
   loop
   2drop
;

\ returns whether the update is sorted
: is-sorted  ( a u -- u )
   swap
   over 0 ?do
      over i 1+ ?do
         dup i chars + c@
         over j chars + c@
         cmp
         if
            2drop
            false
            unloop unloop exit
         then
      loop
   loop
   2drop
   true
;

variable p1 0 p1 !
variable p2 0 p2 !
: read-updates  ( -- )
   begin
      readline
      dup
      0<>
   while
      1+ 3 /
      dup 0 ?do
         line i 3 * chars + parse-int line i chars + c!
      loop

      line over is-sorted
      if
         2/ chars line + c@ p1 +!
      else
         line over sort
         2/ chars line + c@ p2 +!
      then
   repeat
   drop
;

cr

read-rules
read-updates

p1 ? cr
p2 ? cr
