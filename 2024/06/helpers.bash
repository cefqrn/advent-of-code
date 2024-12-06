# print_grid grid width
print_grid() {
  grid=$1
  while [ -n "$grid" ]; do
    row=$(<<<$grid head -c $2)
    echo $row

    grid=$(<<<$grid tail -c +$(($2 + 1)))
  done
}

# pos_to_coord pos
pos_to_coord() {
  y=$(($1 / w))
  x=$(($1 - w * y))

  echo $x $y
}

read -r row
grid="$(cat <(echo -n $row) - | tr -d '\n')"
