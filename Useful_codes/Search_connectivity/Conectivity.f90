program search_neighbour
  implicit none
  integer :: i, j,k,m,k2,m2,k3,m3,lm,lm3,ngold,ngold_ligand, nlines,unit_read=18
  integer :: nneighb
  double precision :: cova_bond(6),distance
  double precision,allocatable :: pos(:,:)
  character(len=100) :: line
  character(len=3),allocatable :: element(:)
  character(len=6) :: name
  CHARACTER(LEN=10) :: temp
  logical:: switch

! Covalent radii of Au,S,O,H,C and N given in \AA
! see Kittel p[age 91/700 and  DOI: 10.1039/b801115j (covalent radii revisited)
cova_bond=0d0

cova_bond(1)=1.36d0  ! Au
cova_bond(2)=1.05d0  ! S
cova_bond(3)=0.66d0  ! O
cova_bond(4)=0.31d0  ! H
cova_bond(5)=0.77d0  ! C
cova_bond(6)=0.71d0  ! N

!*********************************Reading and allocation section
Open(unit=unit_read,File="file.in",status="old")

    nlines = 0
    ! Count the number of rows in the file
    do
       read(unit_read, '(A)', iostat=i) line
       if (i /= 0) exit
       nlines = nlines + 1
    end do
    
    Write(6,*)"Number of lines read=",nlines
    rewind(unit_read)

    allocate(pos(nlines,3))
    allocate(element(nlines))


    do i = 1, nlines
       read(unit_read,*) element(i),pos(i,1),pos(i,2),pos(i,3)
       !write(6,*)data (i,:) 
    end do
    
    close(unit_read)
!**********************************************

 Open(unit=unit_read+1,File="connection_map.out")
 Open(unit=unit_read+2,File="Neighbours_map.out")

 Write(unit_read+2,*)"Atoms   Neighbours"
 Write(unit_read+1,*)"Atoms   Atom-Neighbour   Distance"
  do i=1,nlines
     nneighb=0

    do j=1,nlines
       distance=dsqrt((pos(i,1)-pos(j,1))**2 + (pos(i,2)-pos(j,2))**2 + (pos(i,3)-pos(j,3))**2)
        
         call  selection(k,m,element(i),element(j))

        if (distance .le. (cova_bond(k)+cova_bond(m))*1.15d0 .and. i .ne. j) then
           nneighb=nneighb+1 
         Write(unit_read+1,1994)i, j,distance
        endif
        
     
    enddo


    Write(unit_read+2,1995)i,nneighb
    Write(unit_read+1,*) " "
  enddo





!************************************************************************
1994   Format(I3,1X,I3,2X,F12.5,2X)
1995   Format(I3,1X,I3,2X)
1996   Format(I3,1X,I3,2X,A3,2X,A3)
1997   Format(I3,1X,I3,1X,I3,2X,A3,2X,A3,2X,A3)
1998   Format(I3,1X,I3,1X,I3,1X,I3,2X,A3,2X,A3,2X,A3,2X,A3)
end program search_neighbour



subroutine selection(k,m,element1,element2)

Integer, intent(out) :: k,m
character(len=3), intent(in)::element1,element2

 select case (element1)
      case ("Au")
         k=1
      case ("S")
         k=2
      case ("O")
         k=3
      case ("H")
         k=4
      case ("C")
         k=5
      case ("N")
         k=6
      end select

      select case (element2)
      case ("Au")
         m=1
      case ("S")
         m=2
      case ("O")
         m=3
      case ("H")
         m=4
      case ("C")
         m=5
      case ("N")
         m=6
      end select


end subroutine selection
