# Función que obtiene la precedencia de un operador
def getPrecedence(c):
    precedences = {
        '(': 1,
        '|': 2,
        '.': 3,
        '?': 4,
        '*': 4,
        '+': 4,
        '^': 5
    }
    return precedences.get(c, 0)


# Función que formatea la expresión regular para agregar concatenación explícita donde sea necesario
def formatRegEx(regex):
    allOperators = ['|', '?', '+', '*', '^']
    binaryOperators = ['^', '|']

    res = ''
    for i in range(len(regex)):
        c1 = regex[i]

        # Verifica si hay otro carácter después de c1
        if i + 1 < len(regex):
            c2 = regex[i + 1]

            # Concatena c1 con el resultado
            res += c1

            # Agrega '.' a res si c1 no es '(', c2 no es ')' y ambos no son operadores válidos
            if c1 != '(' and c2 != ')' and c2 not in allOperators and c1 not in binaryOperators:
                res += '.'

    # Concatena el último carácter de regex a res
    res += regex[-1]

    return res


# Función que convierte una expresión regular de notación infix a notación postfix
def infixToPostfix(regex):
    postfix = ''  # Inicializa la notación postfix
    stack = []    # Inicializa la pila para los operadores
    formattedRegEx = formatRegEx(regex)  # Formatea la expresión regular

    # Recorre cada carácter en la expresión formateada
    for c in formattedRegEx:
        if c == '(':  # Si es paréntesis de apertura, lo agrega a la pila
            stack.append(c)
        elif c == ')':  # Si es paréntesis de cierre, saca operadores de la pila hasta encontrar el paréntesis de apertura correspondiente
            while stack and stack[-1] != '(':
                postfix += stack.pop()

            # Elimina el paréntesis de apertura de la pila
            if stack and stack[-1] == '(':
                stack.pop()
        else:  # Si es operador
            # Saca operadores de la pila y los agrega a postfix mientras la pila no esté vacía y el operador en la cima tenga mayor o igual precedencia
            while stack and getPrecedence(stack[-1]) >= getPrecedence(c):
                postfix += stack.pop()

            # Agrega el operador actual a la pila
            stack.append(c)

    # Saca los operadores restantes de la pila y los agrega a postfix
    while stack:
        postfix += stack.pop()

    return postfix


# Función principal que procesa las expresiones regulares
def main():
    expressions = [
        r'(a|t)c',
        r'(a|b)*',
        r'(a*|b*)*',
        r'((ε|a)|b*)*',
        r'(a|b)*abb(a|b)*',
        r'0?(1?)?0*',
        r'if\([ae]+\){[ei]+}(\n(else{[jl]+}))?',
        r'[ae03]+@[ae03]+.(com|net|org)(.(gt|cr|co))?',
    ]

    # Procesa cada expresión regular en la lista expressions
    for i, expression in enumerate(expressions, start=1):
        postfix_expr = infixToPostfix(expression)  # Convierte la expresión a notación postfix
        print(f"Expresión {i}:")
        print("Infix:", expression)
        print("Postfix:", postfix_expr)
        print("--------------------")


if __name__ == "__main__":
    main()
