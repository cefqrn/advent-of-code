#!/bin/bash

# npos_valid pos dpos
npos_valid() {
  npos=$(($1 + $2))

  ny=$((npos / w))
  nx=$((npos - w * ny))
  y=$(($1 / w))
  x=$(($1 - w * y))

  # || and && have the same precedence
  [ $nx -eq $x ] || [ $ny -eq $y ] \
    && [ 0 -le $npos ] && [ $ny -lt $h ]
}

# npos_clear grid pos dpos
npos_clear() {
  npos_valid "$pos" "$dpos" && [ "${1:$(($2 + $3)):1}" != "#" ]
}

# has_loop
has_loop() {
  dposi=0

  pos=$ipos
  dpos=${dposa[dposi]}

  states_seen=()
  while
    while
      seeni=$((pos + n*dposi))
      if [ -n "${states_seen[seeni]}" ]; then
        return 0
      else
        states_seen[seeni]=1
      fi

      npos_clear "$grid" "$pos" "$dpos"
    do
      pos=$((pos + dpos))
    done

    npos_valid "$pos" "$dpos"
  do
    dposi=$(((dposi + 1) % 4))
    dpos=${dposa[dposi]}
  done

  return 1
}

read -r grid
w=${#grid}
while
  read -r row
  x=$?
  grid="$grid$row"
  test $x -eq 0
do :; done

h=$((${#grid} / w))

t=${grid%%^*}
ipos=${#t}
pos=$ipos

dposa=(-"$w" 1 "$w" -1)

dposi=0
dpos=${dposa[dposi]}

while
  while
    seen[pos]=1
    npos_clear "$grid" "$pos" "$dpos"
  do
    pos=$((pos + dpos))
  done

  npos_valid "$pos" "$dpos"
do
  dposi=$(((dposi + 1) % 4))
  dpos=${dposa[dposi]}
done
echo ${#seen[*]}

n=$((w * h))
p2=0
for ((i=0; i < n; ++i)); do
  if [ -z "${seen[i]}" ] || [ $i -eq "$ipos" ]; then
    continue
  fi

  grid="${grid::i}#${grid:i+1}"
  if has_loop "$grid"; then
    : $((p2++))
  fi
  grid="${grid::i}.${grid:i+1}"
done

echo $p2
