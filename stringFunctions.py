#----------------------STRING FUNCTIONS---------------------------#

#funzione padre che contiene i callback a funzioni base 
#come capitalize, slice...
#@param ctx -> contesto di esecuzione
#@param func -> funzione da applicare alla stringa 
#@param start -> indice di partenza 
#@param end -> indice di fine
#return contesto aggiornato 
def executeStringFunction(ctx, func, start = 0, end = 1):
    
    match func:
        #funzione capitalize (anche generalizzata)
        case 'capitalize':
                capitalizeStrings(ctx, start, end)
        #slicing applicando il substring 
        case 'slice':
                sliceStrings(ctx, start, end)
        case 'reverse':
                reverseString(ctx)            
        

#funzione che rende maiuscole le lettere delle stringhe nello stack
#in un determinato intervallo numerico
#@param ctx -> contesto di esecuzione
#@param start -> indice di partenza 
#@param end -> indice di fine
#return contesto aggiornato
def capitalizeStrings(ctx, start, end):
    
    #applico il capitalize a tutte le stringhe
    #presenti nello stack in quel momento
    while ctx.currentStack:
        str = ctx.currentStack.pop()
        splittedStr = list(str)
        for i in range(0, len(splittedStr)):
            if i in range(start, end):
                splittedStr[i] = splittedStr[i].upper()
        
        #salvo in memoria il risultato
        splittedStr.append(' ')
        str = ''.join(splittedStr)
        ctx.memory.append(str)
    
    return ctx


#funzione che estrae la sottostringa di lunghezza (end - start)
#a partire dall'indice start a tutte le strnghe presenti nello stack
#@param ctx -> contesto di applicazione della funzione
#param start -> indice di partenza del substring
#param end -> indice di fine del substring
#@return contesto aggiornato
def sliceStrings(ctx, start = 0, end = 1):
    while ctx.currentStack:
      str = ctx.currentStack.pop()
      slicedString = [str[i] for i in range(start,end + 1)]
      str = ''.join(slicedString)
      ctx.memory.append(str)
      
    return ctx


#funzione che applica il reverse alle stringhe presenti nello stack
#@param ctx -> contesto di applicazione della funzione
#@return contesto aggiornato 
def reverseString(ctx):
    while ctx.currentStack:
        str = ctx.currentStack.pop()
        reversedString = [str[i] for i in range(len(str) - 1, -1, -1)]    
        reversedString.append(' ')
        str = ''.join(reversedString)
        ctx.memory.append(str)
        
    return ctx


#funzione ausiliaria per estrarre gli indici di partenza e arrivo
#per l'utilizzo di procedure su stringhe e/o liste
#@param ctx -> contesto di utilizzo della funzione
#@return lista contenente i due indici da passare alle procedure successive
#        e il numero di stringhe su cui applicare le procedure successive
def extractIndexes(ctx):
    start, end , wordNumber= 0, 1, 0
    for i in range(0, len(ctx.currentStack)):
        try:
            idx = int(ctx.currentStack[i])
            if isinstance(ctx.currentStack[i-1], str):
                start = idx
            else:
                end = idx
        except ValueError:
            wordNumber += 1
            pass
        
    return [start, end, wordNumber]
