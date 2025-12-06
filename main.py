#piccolo interprete del linguaggio basato su stack "Forth"
#implementazione iniziale che comprende soltanto funzioni matematiche di 
#base come le quattro operazioni e la stampa/visualizzazione
#del contenuto dello stack ad un dato momento dell'esecuzione mediante
#comandi dati al terminale

#----------------------IMPORTS-----------------------------------------#

#----------------------BASE OBJECTS------------------------------------#

#glossario delle funzioni possibili
class FunctionsWiki():
    def __init__(self):
        self.basicMathF = ['+', '-', '*', '/', '^']
        self.nAryMathF = ['sum', 'dup', 'mul']
        self.stringsF = ['capitalize', 'slice', 'reverse']


#classe che rappresenta un'istruzione Forth
#l'istruzione è rappresentata come lista di argomenti
#seguita dalla lista di funzioni da applicare agli argomenti 
class Instruction():
    
    #le istruzioni di base sono formate da una serie di numeri
    #e da una o più funzioni matematiche alla fine, ad esempio 5 10 + 
    #le funzioni più complesse sono identificate dal loro nome
    
    instructionArguments = None
    instructionFunctions = None
    glossary = FunctionsWiki()
    
    def __init__(self, args = [], funcs = []):
      self.instructionArguments = args
      self.instructionFunctions = funcs
    
    #decodifica l'istruzione riempiendo i campi con gli elementi corrispondenti
    #@param instruction -> istruzione da decodificare 
    #@return un oggetto istruzione con i campi popolati
    def parseInstruction(self, instruction):
        
        parsedInstruction = Instruction()

        #splitto l'istruzione nei vari componenti
        splittedInstruction = instruction.split(' ')

        #popola i vari campi dell'oggetto controllando se sono
        #numeri interi, stringhe o nomi di funzioni
        for el in splittedInstruction:
            
            try:
                numArg = int(el)
                parsedInstruction.instructionArguments.append(numArg)
            except ValueError:
                if el in self.glossary.nAryMathF or el in self.glossary.stringsF or el in self.glossary.basicMathF:
                    parsedInstruction.instructionFunctions.append(el)
                else:
                    parsedInstruction.instructionArguments.append(el)
        
        return parsedInstruction       
            
    
    #stampa l'istruzione mostrando tutti i suoi campi
    #@param self -> l'istruzione stessa
    def toString(self):
        
        print("Argomenti numerici: ", end='')
        for arg in self.instructionArguments:
            print(f"{arg}  ", end='')
        
        print("")
        
        print("Funzioni matematiche: ", end='')
        for func in self.instructionFunctions:
            print(f"{func}  ")
        
#classe che rappresenta il contesto di esecuzione delle istruzioni
#simulando uno stack che contiente operandi numerici e istruzioni testuali 
class Context():     
    
    currentStack = None
    memory = None
    instructionsQueue = None
    glossary = FunctionsWiki()
    
    def __init__(self, stack = [], mem = [], queue = []):
        self.currentStack = stack
        self.memory = mem
        self.instructionsQueue = queue
        
    #ritorna l'istruzione da eseguire seguendo la 
    #politica LIFO di uno stack 
    def selectInstruction(self):
        return self.instructionsQueue.pop()
    
    #accoda un'istruzione da eseguire in seguito seguendo la 
    #politica LIFO di uno stack 
    def queueInstruction(self, instruction):
        self.instructionsQueue.append(instruction)     
        
    
    #mostra il contenuto delle componenti del contesto
    #per monitorare l'evoluzione dell'esecuzione
    def printStackContent(self):
        print("Memoria di lavoro: ", end='')
        for elem in self.currentStack:
            print(f"{elem} ", end='')
            
        print("")    
            
        print("Memoria di lungo termine: ", end='')
        for elem in self.memory:
            print(elem, end='')
       
        print("")    
            
        print("Coda delle istruzioni: ")
        for ins in self.instructionsQueue:
            print(ins, end='')
      
      
#----------------------EXECUTION FUNCTION-------------------------#       
     
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
        start, end , wordNumber= 0, 1, 0
        for i in range(0, len(ctx.currentStack)):
            try:
                idx = int(ctx.currentStack[i])
                if wordNumber == 0:
                    wordNumber = i 
                if isinstance(ctx.currentStack[i-1], str):
                    start = idx
                else:
                    end = idx
            except ValueError:
                pass
        ctx.currentStack = ctx.currentStack[0:wordNumber]
        executeStringFunction(ctx, func, start, end)
        
    return ctx

#----------------------MATH FUNCTIONS----------------------------#

#funzione che esegue una delle operazioni matematiche elementari
#@param ctx -> contesto di esecuzione
#@param func -> funzione matematica da eseguire
#@return contesto aggiornato
def executeBasicMathFunction(ctx, func):
    
    #isolo gli operandi
    op1, op2 = ctx.currentStack.pop(), ctx.currentStack.pop()
    
    #eseguo l'operazione
    match func:
        case '+':
            ctx.memory.append(op1 + op2)
        case '-':
            ctx.memory.append(op2 - op1)
        case '*':
            ctx.memory.append(op1 * op2)
        case '/':
            ctx.memory.append(op2 / op1)
        case '^':
            ctx.memory.append(op2 ^ op1)
        
    return ctx


#applica una funzione ad un numero di argomenti diverso da 2
#funzioni di esempio sono duplicazione, somma ad n argomenti, ecc..
#@param ctx -> contesto di esecuzione
#@param func -> funzione da applicare agli operandi
#return contesto aggiornato 
def executeN_AryMathFunction(ctx, func):
    
    #implementazione di alcune funzioni con case match
    match func:
        #funzione duplicazione
        case 'dup':
            op = ctx.currentStack.pop()
            ctx.memory.append(op)
            ctx.memory.append(op)
        #funzione somma n-aria
        case 'sum':
            sum = 0
            for i in range(0, len(ctx.currentStack)):
                sum += ctx.currentStack.pop()
            ctx.memory.append(sum)
        #funzione moltiplicazione n-aria
        case 'mul':
            mul = 1
            for i in range(0, len(ctx.currentStack)):
                mul *= ctx.currentStack.pop()
            ctx.memory.append(mul)
        
    return ctx


#----------------------STRING FUNCTIONS---------------------------#

#funzione padre che contiene i callback a funzioni base 
#come capitalize, slice...
#@param ctx -> contesto di esecuzione
#@param func -> funzione da applicare alla stringa 
#@param start -> indice di partenza 
#@param end -> indice di fine
#return contesto aggiornato 
def executeStringFunction(ctx, func, start = 0, end = 1):
    
    #funzione capitalize (standard e generalizzata)
    match func:
        case 'capitalize':
            for str in ctx.currentStack:
                capitalizeString(ctx, start, end)



#funzione che rende maiuscole le lettere di una stringa 
#in un determinato intervallo numerico
#@param ctx -> contesto di esecuzione
#@param start -> indice di partenza 
#@param end -> indice di fine
#return contesto aggiornato
def capitalizeString(ctx, start, end):
    
    #applico il capitalize a tutte le stringhe
    #presenti nello stack in quel momento
    while ctx.currentStack:
        str = ctx.currentStack.pop()
        splittedStr = list(str)
        for i in range(0, len(splittedStr)):
            if i in range(start, end + 1):
                splittedStr[i] = splittedStr[i].upper()
        
        #salvo in memoria il risultato
        splittedStr.append(' ')
        str = ''.join(splittedStr)
        ctx.memory.append(str)
    
    return ctx
        

#----------------------MAIN---------------------------------------#

context = Context()

inputString = input("Attendo l'istruzione \n")

ins = Instruction()
ins.parseInstruction(inputString)

context.queueInstruction(ins)
executeInstruction(context)
context.printStackContent()