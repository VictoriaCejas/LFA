def clasificar_gramatica(cadena):

    definicion = cadena.splitlines()
    verificarQueEs = 3
    cadenaError=''
    indiceError=''

    for x in definicion:

        if verificarQueEs== 3:
            verificar=verificar_G3(x)

            if verificar:
                continue
            else:
                cadenaError= x
                verificar=verificar_G2(x)

                if verificar:
                    verificarQueEs=2
                    indiceError=definicion.index(x)
                    continue
                else:
                    verificar=verificar_G1(x,True,cadena)

                    if verificar[0]:
                        verificarQueEs=1
                        indiceError = definicion.index(x)
                        continue
                    else:
                        verificarQueEs=0

                        if  verificar[1]:
                            cadenaError=verificar[1]
                            indiceError = definicion.index(x)
                            break

        if verificarQueEs== 2:
            verificar=verificar_G2(x)

            if verificar:
                continue
            else:
                cadenaError=x
                verificar=verificar_G1(x,True,cadena)

                if verificar[0]:
                    verificarQueEs=1
                    indiceError=definicion.index(x)
                    continue
                else:
                    verificarQueEs=0
                    cadenaError=verificar[1]
                    indiceError=definicion.index(x)
                    break

        if verificarQueEs==1:
            verificar= verificar_G1(x,False,"")

            if verificar:
                continue
            else:
                cadenaError=x
                verificarQueEs=0

        if verificarQueEs==0:
            indiceError = definicion.index(x)
            break

    if cadenaError is not '':
        noEs=verificarQueEs+1
        listaErrores=guardarErrores(cadena,noEs,indiceError)

        for x in listaErrores:
            errorAAgregar= (x[0], diccionarioErrores[x[1]])
            diccionarioFinal[noEs].append(errorAAgregar)

    for key in diccionarioFinal:
        print (key,":",diccionarioFinal[key])
        diccionarioFinal[key]=[]

diccionarioFinal = {
    3: [],
    2: [],
    1: [],
    0: []}

diccionarioErrores={
    4:"No pertenece a G3, no corresponde a ninguna de las formas: NT → Nt, Nt→t, Nt→ Nt t, Nt→ t Nt, NT→ lambda",
    3:"No pertenece a G2, en la parte izquierda solo debe existir un no terminal",
    2:"No pertenece a G1, la parte izquierda es mas larga que la derecha",
    1:"No pertenece a G1, existe lambda y no esta definido por el distinguido",
    0:"No pertenece a G1, lambda esta definido por el distuinguido y el distinguido es recursivo",
    }

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

def verificar_G3(cadena):

    lista=separarTerminales(cadena)
    noTerminales=lista[0].split()

    if len(noTerminales) > 1 :
        return False

    if  noTerminales[0].isupper():
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

    if len(noTerminales) > 1:
        return False

    if (noTerminales[0])[0].isupper():
        return True
    else:
        return False

def verificar_G1 (cadena,bool,cadenaInicial):

    if bool:
        verificar=verificarLambdaEnDistinguido(cadenaInicial)

        if verificar[0] is False:
            return [False,verificar[1],verificar[2]]

    lista= separarTerminales(cadena)
    noTerminales= lista[0].split()
    terminales= lista[1].split()

    if len(noTerminales) > len(terminales):
        error=2
        return [False,cadena,error]
    else:
        return [True]

def verificarLambdaEnDistinguido(cadenaDefinicion):

    if 'lambda' in cadenaDefinicion:
        definicion=cadenaDefinicion.splitlines()
        distinguido=definicion[0][0]

        cadenaDefinicionLambda=distinguido+':lambda'

        if cadenaDefinicionLambda in cadenaDefinicion:

            for x in definicion:

                lista= separarTerminales(x)
                terminales=lista[1]

                if distinguido in terminales:
                    error=0
                    return [False,cadenaDefinicionLambda,error]
                else:
                    continue
            return [True]
        else:
            indice=cadenaDefinicion.find('lambda')
            cadenaError=cadenaDefinicion[(indice-2):(indice+6)]
            error=1
            return [False,cadenaError,error]
    else:
        return [True]

def guardarErrores(cadena,error,indiceError):

    definicion = cadena.splitlines()
    verificarQueEs = error
    errores = []
    flag=1
    tamañoCadena= len(definicion)-1
    i=indiceError

    while i <= tamañoCadena:

        x=definicion[i]

        if verificarQueEs== 3:
            verificar = verificar_G3(x)
            codigo=4

        if verificarQueEs==2:
            verificar= verificar_G2(x)
            codigo=3

        if verificarQueEs==1:

            if flag==1:
                verificar= verificar_G1(x,True,cadena)
                codigo= verificar[2]
                flag=0

                if 'lambda' in cadena:
                    i=i-1
            else:
                verificar= verificar_G1(x,False,cadena)
                codigo=2

            if verificar[0] is False:
                x=verificar[1]
                verificar = False

        if verificar is False:
            listar=(x,codigo)
            errores.append(listar)
        i=i+1
    return errores

#pruebaG3= clasificar_gramatica("A:B a\nA:a\nA:A c\nA:lambda\nB:b") #G3
#pruebaG2= clasificar_gramatica("A:b A\nA:a B a\nA:A B c\nA:lambda\nB:b") #G2
#pruebaG1= clasificar_gramatica("A n:b A\nA a:a B\nA:A B c\nB:b") #G1
#pruebaG0= clasificar_gramatica("A n:b A\nA:a\nA a B:A B c\nB:b\nA:lambda") #G0 porque tiene lambda y A es recursiva
#prueba= clasificar_gramatica("S:AB palabra\nAB:A palabra \nBC:a B\nC:D") #G3
#prueba= clasificar_gramatica("S:AB palabra\nAB:A palabra \nBC:a B\nC:D") #G3
#prueba= clasificar_gramatica("S:AB palabra\nAB palabra:A palabra \nBC:a B\nC:D") #G2
#prueba=clasificar_gramatica("S:C b a\nS:C\nS:lambda\nC:B c\nB:C b\nA:B a\nA:A a") #G2
#prueba= clasificar_gramatica("A n:b a\nA:a\nA:B c\nB:b\nA:lambda") #G1 porque tiene lambda y A no es recursiva
#prueba= clasificar_gramatica("A n c:b A\nA:a\nA n B c:A B c\nB:b") #G0 hay mas cosas del lado izquiero
#prueba=clasificar_gramatica("S:A B C\nA:A\nA:a B\nG:lambda\nC:a b C\nA b:c d") #G0 xq tiene lambda y no lo define distinguido
#prueba=clasificar_gramatica("S:A B C\nA:A\nA:a B\nG:lambda\nC:a b C\nA b c:c d") #G0 Tiene lamba no lo define el distinguindo, hay mas cosas a izq que derecha


#a= clasificar_gramatica("A:B a\nA:a\nA:A c\nA:lambda\nB:b") #G3
#b= clasificar_gramatica("A:b A\nA:a\nA:A B c\nA:lambda\nB:b") #G2
#c= clasificar_gramatica("A n:b A\nA a:a B\nA:A B c\nB:b") #G1
#d= clasificar_gramatica("A n v:b A\nA:a\nA:A B c\nB:b\nA:lambda") #G0 porque tiene lambda y A es recursiva
#e= clasificar_gramatica("A n c:b A\nA:a\nA n B c:A B c\nB:b") #G0 hay mas cosas del lado izquiero


class AutomataPila:

    def __init__(self, estados, estados_aceptacion):

        self.estados= estados
        self.estado_actual = None
        self.cadena_restante = ''
        self.lkAHYTope = []
        self.TransicionesEstadoActual = []
        self.pila=[]
        self.estadosAceptacion=estados_aceptacion

    def validar_cadena(self, cadena):

        self.cadena_restante=list(cadena)
        key= list(self.estados.keys())

        while len(self.cadena_restante) >0 :
            lookAHead=self.cadena_restante[0]

            if self.estado_actual is None:
                self.pila.append("Z0")
                self.estado_actual=key[0]

            lookAHeadYTope=[]
            s=lookAHead
            p=self.pila.pop()
            lookAHeadYTope.append(s)
            lookAHeadYTope.append(p)
            self.lkAHYTope=lookAHeadYTope
            self.TransicionesEstadoActual= self.estados.get(self.estado_actual)
            aceptado= AutomataPila.validar_Caracter(self)

            if aceptado is True:
                self.cadena_restante.pop(0)
            else:
                return False

        if len(self.cadena_restante) == 0 and self.estado_actual in self.estadosAceptacion:
            return True
        else:
            return False

    def validar_Caracter(self):

        for i in self.TransicionesEstadoActual:

            if self.lkAHYTope[0] in i[0]:

                if self.lkAHYTope[1] in i[1]:
                    elementosAApilar = i[2]

                    if elementosAApilar[0] != '':
                        listaReverse=[]
                        listaReverse=elementosAApilar[:]
                        listaReverse.reverse()

                        for x in listaReverse:

                          self.pila.append(x)

                    self.estado_actual = i[3]
                    return True
        return False



'''estadosPrueba= {'a': [('(', 'Z0', ['(','Z0'], 'a'),
                ('(', '(', ['(', '('], 'a'),
                (')', '(', [''], 'b')],
                'b': [(')', '(', [''], 'b'),
                ('$', 'Z0', ['Z0'], 'b')]}

estadosAceptacion=['b']
prueba=AutomataPila(estadosPrueba,estadosAceptacion).validar_cadena('((()))$')
print(prueba)'''

'''estadosPrueba= {
    1: [('(', 'Z0',['(','Z0'], 1),
        ('(', '(', ['(', '('], 1),
        (')', '(', [''], 2)],
    2: [(')', '(', [''], 2),
        ('(','Z0',['(','Z0'],2),
        ('(','(',['(','('],2),
        ('$', 'Z0', ['Z0'], 2)
       ]
}
estadosAceptacion=[2]
prueba=AutomataPila(estadosPrueba,estadosAceptacion).validar_cadena('((())()())$')
print(prueba)'''


'''estadosPrueba= {
    1: [('a', 'Z0', ['a','a','a','Z0'], 1),
        ('a', 'a', ['a', 'a','a'], 1),
        ('b', 'a', ['a'], 2),
        ('b','Z0',['a','Z0'],2)],
    2: [('c', 'a', [''], 2),
        ('$', 'Z0', ['Z0'], 2)
       ]
}
estadosAceptacion=[2]

prueba= AutomataPila(estadosPrueba,estadosAceptacion).validar_cadena('aabccccc$')
print(prueba)'''
