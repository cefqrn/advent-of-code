normal! gg}ge
let lines = getline(1, ".")

let a = []
let b = []
for l in lines
  let [x, y] = l->split()->map("str2nr(v:val)")

  call add(a, x)
  call add(b, y)
endfor

call sort(a)
call sort(b)

let p1 = 0
let p2 = 0

let i = 0
let l = len(lines)
while i < l
  let x = a[i]
  let y = b[i]

  let p1 += abs(x - y)
  let p2 += x * b->count(x)

  let i += 1
endwhile

echo p1
echo p2
