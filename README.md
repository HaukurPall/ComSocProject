# ComSocProject
## Authors 
Silvan Hungerbühler, Max Rapp, Grzegorz Lioswski, Haukur Páll Jónsson

## The Python model
Code is in code/model.py and is run using the command line

    python3 model.py --cost 0 --rule 0 --budget 100 test_preferences.txt

For help see

    python3 model.py -h

### Input
To run the program against some ballots just add the filename where the ballot is stored as a command line argument.

The format of the file is like in the preflib.org

    M=Candidate count
    Candidate_1=1,candidate_name_1
    ...
    Candidate_M=M,candidate_name_M
    N,B,U=Voters,Ballots,Unique ballots
    Ballot_1=1,2,...,M
    ...
    Ballot_B=1,2,...,M