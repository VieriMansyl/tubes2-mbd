### Serial Optimistic Concurency Control

## Phase OCC :
- Read Phase
- Validation Phase
- Write Phase

## Validation
    
    If for all Ti with TS (Ti) < TS (Tj) either one of the following condition holds:
        • finishTS(Ti) < startTS(Tj)
        • startTS(Tj) < finishTS(Ti) < validationTS(Tj) and the set of data items written by Ti
        does not intersect with the set of data items read by Tj
    
## Run Program
- Clone source code
- Run file OCC.py

