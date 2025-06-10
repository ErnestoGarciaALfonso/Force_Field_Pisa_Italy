program read_pdb
    implicit none
    integer, parameter :: max_atoms = 5000  ! Adjust based on expected file size
    character(len=6) :: record_name
    integer :: atom_serial, res_seq, i
    character(len=4) :: atom_name
    character(len=5) :: res_name
    character(len=1) :: chain_id
    real :: x, y, z, occupancy, temp_factor
    character(len=2) :: element
    character(len=80) :: line
    integer :: num_atoms
    character(len=5) :: ligand_elements(max_atoms)
    integer :: num_ligands
    logical::replace
    replace=.true.

    open(unit=15, file='ligand.out', status='old', action='read')
    num_ligands = 0
    
    do i = 1, max_atoms
        read(15, *, end=200) atom_serial, ligand_elements(i)
        write(6, *) atom_serial, ligand_elements(i)
        num_ligands = num_ligands + 1
    end do
    
200 continue
    close(15)
    
    open(unit=10, file='automatic.pdb', status='old', action='read')
    open(unit=20, file='output.pdb', status='replace', action='write')
    num_atoms = 0
    
    do i = 1, max_atoms
        read(10, '(A)', end=100) line
        
        if (line(1:6) == 'ATOM  ' .or. line(1:6) == 'HETATM') then
            num_atoms = num_atoms + 1
            read(line, '(A6, I5,  A5,  A5, 1X, A1, I4, 4X, F8.3, F8.3, F8.3, F6.2, F6.2, 6X, A2)') &
                record_name, atom_serial, atom_name, res_name, chain_id, res_seq, x, y, z, occupancy, temp_factor, element
            
            if(replace)then
               if (atom_serial <= num_ligands) then
                   atom_name = ligand_elements(atom_serial)
               end if
            endif

            !print *, record_name, atom_serial, atom_name, res_name, chain_id, res_seq, x, y, z, occupancy, temp_factor, element
            write(20, '(A6,  I5, A5, A5, 1X, A1, I4, 1X, F8.3, 1X, F8.3, 1X, F8.3, 1X, F6.2, 1X, F6.2, 1X, A2)') &
                record_name, atom_serial, atom_name, res_name, chain_id, res_seq, x, y, z, occupancy, temp_factor, element
        end if
    end do
    
100 continue
    print *, 'Total atoms read: ', num_atoms
   ! write(20, '(A, I5)') 'Total atoms read: ', num_atoms
    close(10)
    close(20)
    
end program read_pdb