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
