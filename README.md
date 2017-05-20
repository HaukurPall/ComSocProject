# ComSocProject
## Authors 
Silvan Hungerbühler, Max Rapp, Grzegorz Lioswski, Haukur Páll Jónsson

## The Python model
Code is in code/model.py and is run using the command line

    python3 model.py --cost 0 --rule 0 --budget 100 test_preferences.txt

### Input
The input of the program is given with the command line and should be formatted like so:

    "Preference_identifier" (one word)
    Some description of the preference
    number of voters (one integer=N)
    number of preferences (one integer=M)
    0 1 10 3 4 7 2 9 8 ... (a preference order with M integers)
    ...
    N lines of preference orders