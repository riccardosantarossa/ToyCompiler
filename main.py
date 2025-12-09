#piccolo interprete del linguaggio basato su stack "Forth"
#implementazione iniziale che comprende soltanto funzioni matematiche di 
#base come le quattro operazioni e la stampa/visualizzazione
#del contenuto dello stack ad un dato momento dell'esecuzione mediante
#comandi dati al terminale

#----------------------IMPORTS------------------------------------#
import os
from objects import Context, Instruction      
from mathFunctions import executeBasicMathFunction, executeN_AryMathFunction
from stringFunctions import executeStringFunction, extractIndexes
      
#----------------------EXECUTION FUNCTIONS------------------------#       
     
#esegue una singola istruzione prelevando dallo 
#stack gli operandi e salvando in memoria i risultati
#@param ctx -> contesto di esecuzione dell'istruzione
#@return aggiornato con i risultati
def executeInstruction(ctx):
    
    #seleziono l'istruzione
    ins = ctx.selectInstruction()
    
    #inserisco gli operandi nello stack nell'ordine corretto
    for op in ins.instructionArguments:
        ctx.currentStack.append(op)
    
    #estraggo la funzione da eseguire
    func = ins.instructionFunctions.pop()
    
    #matching del tipo di funzione da eseguire
    if func in ctx.glossary.basicMathF:
        executeBasicMathFunction(ctx, func)
    elif func in ctx.glossary.nAryMathF:
        executeN_AryMathFunction(ctx, func)
    elif func in ctx.glossary.stringsF:
        #parsing delle funzioni del tipo 
        #s1 s2 ... sN startIndex endIndex (s1..sN stringhe da modificare)
        functionParams = extractIndexes(ctx)
        ctx.currentStack = ctx.currentStack[0:functionParams[2]]
        executeStringFunction(ctx, func, functionParams[0], functionParams[1])
        
    return ctx

#---------------------DISPLAY FUNCTIONS---------------------------#

def printChars(char, n):
    for i in range(1,n):
        print(char, end='')

def displayMenu():
    
    #mostra un riquadro
    printChars('#', 60)
    print('')
    print('#' + "              LITTLE PYTHON FORTH COMPILER               " + '#')
    print('#' + "[1] Modalità di esecuzione interattiva                   " + '#')    
    print('#' + "[2] Carica le istruzioni da un file testuale             " + '#')
    print('#' + "[3] Mostra il contenuto della memoria del compilatore    " + '#')    
    print('#' + "[4] Esci                                                 " + '#')    
    printChars('#', 60)
    print('')
    print('')


#----------------------MAIN---------------------------------------#

choice = 0
context = Context()

while choice != 4:
    
    displayMenu()
    choice = int(input('Scegli una tra le opzioni:  '))
    if choice == 1:
    
        inputString = input("Attendo l'istruzione \n")

        ins = Instruction()
        ins.parseInstruction(inputString)

        context.queueInstruction(ins)
        executeInstruction(context)
        context.printStackContent()
        
        os.system('clear')
        
    elif choice == 2:
        print("FILE EXECUTION --> TODO")
        os.system('clear')
    
    elif choice == 3:
        context.printStackContent()
        print('')
        print('')
        next = input()
        if next == "":
            os.system('clear')
            pass
        
    else: 
        pass