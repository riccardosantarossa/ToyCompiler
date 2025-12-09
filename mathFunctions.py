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
    
    #implementazione di funzioni con case match
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


