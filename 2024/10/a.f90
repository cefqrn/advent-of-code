! https://fortran-lang.org/learn/
! https://userpages.cs.umbc.edu/squire/fortranclass/summary.shtml
! https://en.wikibooks.org/wiki/Fortran/io
! https://masuday.github.io/fortran_tutorial/files.html
!
! run with
!   gfortran a.f90 -o a && ./a <input

subroutine get_input(input, w, h)
  implicit none
  integer, intent(out) :: input(64,64)
  integer, intent(out) :: w, h

  integer :: io, info
  character(len=64) :: data(64)
  integer :: i, j

  open(newunit=io, file="input", status="old", action="read", iostat=info)
  if (info /= 0) stop "could not read input"

  h = 0
  do while (info == 0)
    h = h + 1
    data(h) = ""
    read(io,*,iostat=info) data(h)
  end do
  h = h - 1

  close(io)

  if (h < 1) stop "no input"
  w = len_trim(data(1))

  do i = 1, h
    do j = 1, w
      input(i,j) = ichar(data(i)(j:j)) - ichar("0")
    end do
  end do
end subroutine get_input

subroutine simulate(cheese, input, w, h)
  implicit none
  integer, intent(out) :: cheese(64, 64, 10)
  integer, intent(in) :: input(64, 64)
  integer, intent(in) :: w, h

  integer :: x, y, z, dx, dy

  do z = 0, 9
    do y = 1, h
      do x = 1, w
        cheese(x,y,z+1) = 0
      end do
    end do
  end do

  do y = 1, h
    do x = 1, w
      if (input(x,y) == 0) cheese(x,y,0+1) = cheese(x,y,0+1) + 1
    end do
  end do

  do z = 0, 8
    do y = 1, h
      do x = 1, w
        if (input(x,y) /= z) cycle

        if (x > 1) cheese(x-1,y,z+2) = cheese(x-1,y,z+2) + cheese(x,y,z+1)
        if (y > 1) cheese(x,y-1,z+2) = cheese(x,y-1,z+2) + cheese(x,y,z+1)
        if (x < w) cheese(x+1,y,z+2) = cheese(x+1,y,z+2) + cheese(x,y,z+1)
        if (y < h) cheese(x,y+1,z+2) = cheese(x,y+1,z+2) + cheese(x,y,z+1)
      end do
    end do
  end do
end subroutine simulate

program a
  implicit none
  integer :: cheese(64, 64, 10)
  integer :: input(64, 64)
  integer :: w, h
  integer :: x, y, x2, y2
  integer :: p1, p2

  call get_input(input, w, h)

  ! p2
  call simulate(cheese, input, w, h)
  p2 = 0
  do y = 1, h
    do x = 1, w
      if (input(x,y) == 9) p2 = p2 + cheese(x,y,9+1)
    end do
  end do

  ! p1
  do y = 1, h
    do x = 1, w
      if (input(x,y) == 0) input(x,y) = 999
    end do
  end do

  p1 = 0
  do y = 1, h
    do x = 1, w
      if (input(x,y) /= 999) cycle

      ! lmao
      input(x, y) = 0
      call simulate(cheese, input, w, h)
      do y2 = 1, h
        do x2 = 1, w
          if (input(x2,y2) == 9 .and. cheese(x2,y2,9+1) > 0) p1 = p1 + 1
        end do
      end do
      input(x, y) = 999
    end do
  end do

  print *, p1
  print *, p2
end program a
