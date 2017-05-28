# ComSocProject
## Authors 
Silvan Hungerbühler, Max Rapp, Grzegorz Lioswski, Haukur Páll Jónsson

## The Python model
Code is in the python directory and can be run via the command line

    python3 CR.py --cost 0 --rule 0 --budget 100 test_preferences.txt

For help see

    python3 CR.py -h

### Prerequisites
Python3.5, Numpy

### Input
To run the program against some ballots just add the filename where the ballot is stored as a command line argument.

The format of the file is like in the preflib.org

    M=Candidate count
    Candidate_1=1,candidate_name_1
    ...
    Candidate_M=M,candidate_name_M
    N,B,U=Voters,Ballots,Unique ballots
    Ballot_1=C_1,1,2,...,M
    ...
    Ballot_B=C_B1,2,...,M
    
To generate ballots and save to file 'random_profile.txt'

    python3 CR.py random_profile.txt --write --voters 11 --candidates 10 --swaps 1 --noise 2 --base 3