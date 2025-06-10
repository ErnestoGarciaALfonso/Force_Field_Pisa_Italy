program histogram 

  implicit none

!--------------------------------------------
!           VARIABLES
!--------------------------------------------
  type input
       real*8   :: p1, p2 !proj1, proj2, MD sim
  end type input

  type histo
       real*8   :: h1, h2, h3 !proj_x, proj_y, energy histo
  end type histo

  type(input),allocatable  :: values(:)
  type(histo)              :: his(10000)
  real*8,allocatable       :: prob(:,:), energy(:,:)
  real*8                   :: axis1, axis2, step1, step2, min_x,&
                              &min_y, max_x, max_y, temp, delta,KT
  integer                  :: i, j, k, tmp, dime, bin_x, bin_y, time, dime_his
  real*8, parameter        :: R=8.314
!--------------------------------------------

  dime = 0
  open(unit = 2, file = 'header-isto', status = 'old')
      read(2,*) dime, temp, bin_x, bin_y, delta
  close(2)
  allocate(values(dime), prob(bin_x,bin_y), energy(bin_x, bin_y))

  KT=temp*R  !!! Temperature in KJ/mol, modified by  EGA, see Marta's thesis page 68/239

  do i = 1, dime
     read(*,*) values(i)%p1, values(i)%p2
  enddo
  do i = 1, bin_x
     do j = 1, bin_y
        prob(i,j) = 0.d0
     enddo
  enddo

  min_x = minval(values%p1)
  min_y = minval(values%p2)
  max_x = maxval(values%p1)
  max_y = maxval(values%p2)
  call step_calc(max_x, min_x, bin_x, step1)
  call step_calc(max_y, min_y, bin_y, step2)

  do i = 1, bin_x - 1
     do j = 1, bin_y - 1
        do k = 1, dime
           if(values(k)%p1.lt.min_x+step1*(i+1).and.&
             &values(k)%p1.ge.min_x+step1*i.and.&
             &values(k)%p2.lt.min_y+step2*(j+1).and.&
             &values(k)%p2.ge.min_y+step2*j) then
                prob(i,j) = prob(i,j) + 1.d0
           endif
        enddo
      enddo
  enddo
!-----------------------------------------------------------
!                OUTPUT FILES - HISTOGRAM & TIMES
!-----------------------------------------------------------
  axis1 = min_x - step1
  tmp = 0
  do i = 1, bin_x
     axis1 = axis1 + step1
     axis2 = min_y - step2
     do j = 1, bin_y
        axis2 = axis2 + step2
        if(prob(i,j).ne.0.d0) then
          energy(i,j) = -R*temp*log(prob(i,j)/maxval(prob))
          write(*,10) axis1+step1/2.d0, axis2+step2/2.d0, energy(i,j)
          if(energy(i,j).le.KT) then
            tmp = tmp + 1
            his(tmp)%h1 = axis1 + step1/2.d0
            his(tmp)%h2 = axis2 + step2/2.d0
            his(tmp)%h3 = energy(i,j)
          endif
        endif
     enddo
  enddo
write(*,*) "************"    !!!! Lines of the basin of minimum energy, it is useful to get the time and the structure (EGA)
  dime_his = tmp
  do i = 1, dime_his
     do j = 1, dime
        if(abs(his(i)%h1-values(j)%p1).le.delta.and.&
          &abs(his(i)%h2-values(j)%p2).le.delta) then
           time = 2*j - 2
           write(*,11) time, values(j)%p1, values(j)%p2, his(i)%h3
           exit
        endif
     enddo
  enddo  


! Frecuency of printing out coordinates = nstxout*nsteps (input MD file.....EGA)
! Time is computed as Nlines=(whole_time)/(nstxout*nsteps), so if you have line 1200 then -> 1200*nstxout*nsteps is the simulation  time you look for 

10 FORMAT(F12.5,1X,F12.5,1X,F12.5)
11 FORMAT(I10,1X,F12.5,1X,F12.5,1X,F12.5)

  deallocate(values, prob, energy)
  stop
end program histogram

subroutine step_calc(a,b,c,step)

  implicit none
  
  real*8,intent(in)    :: a,b
  integer,intent(in)   :: c
  real*8, intent(out)  :: step

  step = (a-b)/c

  return
end subroutine step_calc
