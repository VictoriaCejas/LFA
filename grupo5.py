def clasificar_gramatica(cadena):
    definicion = cadena.splitlines()
    #Definicion es una lista con cada una de las definiciones separadas
    verificarQueEs = 3
    cadenaError=''
    for x in definicion:
        #aca hay que tomar la primera defincion de la lista asi por cada continue que haga
        if verificarQueEs== 3:
            verificar=verificar_G3(x)
            if verificar:
                continue
            else:
                cadenaError= x
                verificar=verificar_G2(x)
                if verificar:
                    verificarQueEs=2
                    continue
                else:
                    verificar=verificar_G1(x,True,cadena)
                    if verificar[0]:
                        verificarQueEs=1
                        continue
                    else:
                        verificarQueEs=0
                        if  verificar[1]:
                            cadenaError=verificar[1]
                        #PONER CADENA ERROR
                        break
                #Si no es g3, ver que la cadena sea g2 si no es g2 g1 si no es g1 es g0 cortar la iteracion.
        if verificarQueEs== 2:
            verificar=verificar_G2(x)
            if verificar:
                continue
            else:
                cadenaError=x
                verificar=verificar_G1(x,True,cadena)
                if verificar[0]:
                    verificarQueEs=1
                    continue
                else:
                    verificarQueEs=0
                    cadenaError=verificar[1]
                    break
        if verificarQueEs==1:
            verificar= verificar_G1(x,False,"")
            if verificar:
                continue
            else:
                cadenaError=x
                verificarQueEs=0
        if verificarQueEs==0:
            break
    if cadenaError is not '':
        noEs=verificarQueEs+1
        diccionarioFinal[noEs] = '(' + cadenaError + ')' + ' , ' + diccionarioErrores[noEs]
    for key in diccionarioFinal:
        print (key,":",diccionarioFinal[key])
        diccionarioFinal[key]=""
        #Borra porque si se ejecutan varias pruebas el diccionarioFinal no vuelve a vacio.
    #print(diccionarioFinal)

    #Aca en no hay que retornar la lista, tengo que retornar el diccionario.
    #DICCIONARIOOOOOOOOOOOOOOOO


diccionarioFinal={
    3:[],
    2:[],
    1:[],
    0:[]}


diccionarioErrores={
    3:"No pertenece a G3, no corresponde a ninguna de las formas: NT → Nt, Nt→t, Nt→ Nt t, Nt→ t Nt, NT→ lambda",
    2:"No pertenece a G2, en la parte izquierda solo debe existir un no terminal",
    1:"No pertenece a G1, la parte izquierda es mas larga que la derecha\n o lambda esta definido por el distuinguido y el distinguido es recursivo\n o existe lambda y no esta definido por el distinguido",
    0:"",
    }

'''si da que es G2 o G1 bucar la cadena que hace que no sea G3 o G2
    osea que si me da algun false guardo esa cadena para mostrar como error.
'''

def separarTerminales(cadena):
    list=[]
    fin = len(cadena)
    noTerminales = ''
    terminales = ''
    indice = cadena.find(':')
    i = 0
    while i < indice:
        noTerminales = noTerminales + cadena[i]
        i=i+1
    list.append(noTerminales)
    i = indice+1
    while i < fin:
        terminales = terminales + cadena[i]
        i=i+1
    list.append(terminales)
    return list
    #Retorna lista el primer elemento son los no terminales, el segundo los terminales.

def verificar_G3(cadena):
    #devolver true o false dependiendo de lo que da y ademas si da error porque Asique devolver lista.
    lista=separarTerminales(cadena)
    noTerminales=lista[0].split()
    #longitudnoTerminales = len(noTerminales)
    if len(noTerminales) > 1 :
        return False
    if  noTerminales[0].isupper(): #ver que el unico no terminal comience en mayuscula
        terminales= lista[1].split()
        longitudTerminales= len(terminales)
        if longitudTerminales <= 2:
            if longitudTerminales== 2:
                if (terminales[0])[0].isupper() and (terminales[1])[0].isupper():
                    return False
                if (terminales[0])[0].islower() and (terminales[1])[0].islower():
                    return False
                return True
            return True
        else:
            return False
    else:
        return False
def verificar_G2(cadena):
    lista = separarTerminales(cadena)
    noTerminales = lista[0].split()
    #longitudnoTerminales = len(noTerminales)
    if len(noTerminales) > 1:
        return False
    if (noTerminales[0])[0].isupper():
        return  True
    else:
        return False

def verificar_G1 (cadena,bool,cadenaInicial):
    if bool:
        verificar=verificarLambdaEnDistinguido(cadenaInicial)
        if verificar[0] is False:
            return [False,verificar[1]]
    lista= separarTerminales(cadena)
    noTerminales= lista[0].split()
    terminales= lista[1].split()
    #if len(terminales)== 1:
     #   if terminales[0]=="lambda":
      #      return False
    if len(noTerminales) > len(terminales):
        return [False,""]
    else:
        return [True]

def verificarLambdaEnDistinguido(cadenaDefinicion):
    #Primero verifico que haya lambda
    if 'lambda' in cadenaDefinicion:
        definicion=cadenaDefinicion.splitlines()
        distinguido=definicion[0][0]
        #Calculé distinguido
        cadenaDefinicionLambda=distinguido+':lambda'
        if cadenaDefinicionLambda in cadenaDefinicion:
            for x in definicion:
                lista= separarTerminales(x)
                noTerminales=lista[0]
                terminales=lista[1]
                if distinguido in terminales:
                    return [False,cadenaDefinicionLambda]
                # Ver si distinguido es recursivo
                else:
                    continue
            return [True]
        else:
            indice=cadenaDefinicion.find('lambda')
            cadenaError=cadenaDefinicion[(indice-2):(indice+6)]
            return [False,cadenaError]
        #ver si el distinguido define 'lambda' y que no sea recursivo
    else:
        return [True]
        #Ver si distinguido es recursivo
        #ver si distinguido define lambda ej: S → lambda

#cadena="A:b A\nA:a\nA:A B c\nA:lambda\nB:b"
#prueba= verificarLambdaEnDistinguido(cadena)
#a=prueba
#pruebaG3= clasificar_gramatica("A:B a\nA:a\nA:A c\nA:lambda\nB:b") #G3
#pruebaG2= clasificar_gramatica("A:b A\nA:a\nA:A B c\nA:lambda\nB:b") #G2
#pruebaG1= clasificar_gramatica("A n:b A\nA a:a B\nA:A B c\nB:b") #G1
#pruebaG0= clasificar_gramatica("A n:b A\nA:a\nA:A B c\nB:b\nA:lambda") #G0 porque tiene lambda y A es recursiva
#prueba= clasificar_gramatica("A n:b a\nA:a\nA:B c\nB:b\nA:lambda") #G1 porque tiene lambda y A no es recursiva
#prueba= clasificar_gramatica("A n c:b A\nA:a\nA n B c:A B c\nB:b") #G0 hay mas cosas del lado izquiero
#prueba= clasificar_gramatica("S:AB palabra\nAB palabra:A palabra \nBC:a B\nC:D")
#prueba=clasificar_gramatica("S:C b a\nS:C\nS:lambda\nC:B c\nB:C b\nA:B a\nA:A a") #G2
#prueba=clasificar_gramatica("S:A B C\nA:A\nA:a B\nG:lambda\nC:a b C\nA b:c d") #G0 xq tiene lambda y no lo define distinguido
#prueba=clasificar_gramatica("S:a B\nS:c\nC:c A\nB:b C\nB:b\nA:a A\nA:a") #G3


a= clasificar_gramatica("A:B a\nA:a\nA:A c\nA:lambda\nB:b") #G3
b= clasificar_gramatica("A:b A\nA:a\nA:A B c\nA:lambda\nB:b") #G2
c= clasificar_gramatica("A n:b A\nA a:a B\nA:A B c\nB:b") #G1
d= clasificar_gramatica("A n v:b A\nA:a\nA:A B c\nB:b\nA:lambda") #G0 porque tiene lambda y A es recursiva
e= clasificar_gramatica("A n c:b A\nA:a\nA n B c:A B c\nB:b") #G0 hay mas cosas del lado izquiero

#EN G0 va a mostrar el error de lambda primero, si no hay error con lambda muesta la cadena que da error.
#Consultar.

'''
REGULARES (G3)
S ➜a
S ➜Aa (izquierda)
S ➜Aa (derecha)
S ➜λ
Son regulares aquellas que tengan estas formas.
Formas:
No terminal
No terminal, terminal
Terminal, no terminal 
λ
S ➜bc no cumple las formas

INDEPENDIENTE CONTEXTO (G2)
A la izquierda solo No terminales, de la derecha cualquier combinación de terminales y no terminales
S ➜ a
S ➜Aa
S ➜Aa
S ➜λ
S ➜abB

SENSIBLES AL CONTEXTO (G1)
Del lado izquierdo puedo tener mas cosas que solo un anterior, del lado derecho terminales y no terminales en cualquier combinación, 
la cantidad del lado izquierdo no puede ser mayor a lo que tengo del lado derecho ( aSB ➜ C)
puede tener lambda pero solo como no terminal del axioma y el axioma no tiene que ser recursivo

NO REINSTRINGIDAS (G0)
Permite todo. 
'''


