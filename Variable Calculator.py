class Node:
    def __init__(self, value):
        self.value = value
        self.next = None 
    
    def __str__(self):
        return "Node({})".format(self.value) 

    __repr__ = __str__
                          

#=============================================== Part I ==============================================

class Stack:
    '''
        >>> x=Stack()
        >>> x.pop()
        >>> x.push(2)
        >>> x.push(4)
        >>> x.push(6)
        >>> x
        Top:Node(6)
        Stack:
        6
        4
        2
        >>> x.pop()
        6
        >>> x
        Top:Node(4)
        Stack:
        4
        2
        >>> len(x)
        2
        >>> x.peek()
        4
    '''
    def __init__(self):
        self.top = None
    
    def __str__(self):
        temp=self.top
        out=[]
        while temp:
            out.append(str(temp.value))
            temp=temp.next
        out='\n'.join(out)
        return ('Top:{}\nStack:\n{}'.format(self.top,out))

    __repr__=__str__


    def isEmpty(self):
        
        # if self.top equals None, the stack must be empty, if it doesnt then there are nodes in the stack
        if self.top == None:
            return True
        else:
            return False

    def __len__(self): 
        current = self.top
        counter = 0
        while current != None:
            counter += 1
            current = current.next
        
        return counter


    def push(self,value):

        if self.isEmpty():
            # if the stack is empty, it sets self.top to a new node with the value passed in
            self.top = Node(value)
        else:
            # mades a new node, sets its next value to the current top, then updates self.top to equal the new node
            newNode = Node(value)
            newNode.next = self.top
            self.top = newNode

     
    def pop(self):
        # if the stack is empty, there is nothing to pop so it returns None
        if self.isEmpty():
            return None
        
        # if the stack isn't empty, it returns the top value and removes that node from the stack
        topVal = self.top.value
        self.top = self.top.next
        return topVal

    def peek(self):
        # if the stack is empty, it returns None. Otherwise, it returns the value of the top node without removing that node from the stack
        if self.isEmpty():
            return None
        
        return self.top.value


#=============================================== Part II ==============================================

class Calculator:
    def __init__(self):
        self.__expr = None


    @property
    def getExpr(self):
        return self.__expr

    def setExpr(self, new_expr):
        if isinstance(new_expr, str):
            self.__expr=new_expr
        else:
            return None

    def _isNumber(self, txt):
        '''
            >>> x=Calculator()
            >>> x._isNumber(' 2.560 ')
            True
            >>> x._isNumber('7 56')
            False
            >>> x._isNumber('2.56p')
            False
        '''
        # if txt can be converted to a float, it returns True. Otherwise it returns False.
        try:
            float(txt.strip())
            return True
        except:
            return False
        




    def _getPostfix(self, txt):
        '''
            Required: _getPostfix must create and use a Stack for expression processing
            >>> x=Calculator()
            >>> x._getPostfix('2 ^ 4')
            '2.0 4.0 ^'
            >>> x._getPostfix('2')
            '2.0'
            >>> x._getPostfix('2.1 * 5 + 3 ^ 2 + 1 + 4.45')
            '2.1 5.0 * 3.0 2.0 ^ + 1.0 + 4.45 +'
            >>> x._getPostfix('2 * 5.34 + 3 ^ 2 + 1 + 4')
            '2.0 5.34 * 3.0 2.0 ^ + 1.0 + 4.0 +'
            >>> x._getPostfix('2.1 * 5 + 3 ^ 2 + 1 + 4')
            '2.1 5.0 * 3.0 2.0 ^ + 1.0 + 4.0 +'
            >>> x._getPostfix('( 2.5 )')
            '2.5'
            >>> x._getPostfix ('( ( 2 ) )')
            '2.0'
            >>> x._getPostfix ('2 * ( ( 5 + -3 ) ^ 2 + ( 1 + 4 ) )')
            '2.0 5.0 -3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix ('( 2 * ( ( 5 + 3 ) ^ 2 + ( 1 + 4 ) ) )')
            '2.0 5.0 3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix ('( ( 2 * ( ( 5 + 3 ) ^ 2 + ( 1 + 4 ) ) ) )')
            '2.0 5.0 3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix('2 * ( -5 + 3 ) ^ 2 + ( 1 + 4 )')
            '2.0 -5.0 3.0 + 2.0 ^ * 1.0 4.0 + +'

            # In invalid expressions, you might print an error message, adjust doctest accordingly
            # If you are veryfing the expression in calculate before passing to postfix, this cases are not necessary

            >>> x._getPostfix('2 * 5 + 3 ^ + -2 + 1 + 4')
            >>> x._getPostfix('2 * 5 + 3 ^ - 2 + 1 + 4')
            >>> x._getPostfix('2    5')
            >>> x._getPostfix('25 +')
            >>> x._getPostfix(' 2 * ( 5 + 3 ) ^ 2 + ( 1 + 4 ')
            >>> x._getPostfix(' 2 * ( 5 + 3 ) ^ 2 + ) 1 + 4 (')
            >>> x._getPostfix('2 * 5% + 3 ^ + -2 + 1 + 4')
        '''

        postfixStack = Stack()  # method must use postfixStack to compute the postfix expression
        postFix = ''
        lastWasOperator = False # Is made False when a number is added and is made True when an opperator is added.
                                # If it is True while an operator is being added, then nothing is returned because there are two operators in a row

        precedence = {'(': 0, '-': 1, '+': 1, '/': 2, '*': 2, '^': 5, ')': 6} # used to check the precedence when adding operators


        # split on spaces to loop through each aspect of the expression
        txtLst = txt.split()

############################################### CHECKS IF EXPRESSION IS INVALID #########################################################

        noOperators = True # keeps track of whether there are operators or not
        for i in txt:
            if i == '+' or i == '-' or i == '*' or i == '/' or i == '^' or i == '(' or i == ')':
                noOperators = False

        # counts the amount of numbers and parenthesis and operators in txt
        numCount = 0 # amount of operands
        leftParenCount = 0
        rightParenCount = 0
        numOperators = 0
        for i in txtLst:
            if self._isNumber(i):
                numCount += 1
            elif i == '(':
                leftParenCount += 1
            elif i == ')':
                rightParenCount += 1
            elif i == '+' or i == '-' or i == '*' or i == '/' or i == '^':
                numOperators += 1


        # if there are no operators in the expression and more than one number, it is invalid
        if noOperators == True and numCount > 1:
            return None
        
        # if there are a different number of left and right parenthesis, the expression is invalid
        if leftParenCount != rightParenCount:
            return None

        # checks if there are not enough operadns in the expression
        if numOperators + 1 != numCount:
            return None

###################################################################################################################################

        for i in txtLst:
            if self._isNumber(i):
                postFix += str(float(i)) + ' '
                lastWasOperator = False
            else:
                # left parenthesis has lowest precedence, so it is automatically pushed
                iStr = i.strip()
                if iStr == '(':
                    postfixStack.push(i)
                
                # pop everything in the stack and add it onto postFix until you reach a left parenthesis
                elif iStr == ')':
                    leftFound = False
                    while leftFound == False:
                        if postfixStack.top == None:
                            # Error, not enough left parenthesis "("
                            leftFound = True
                            return
                        elif postfixStack.top.value == '(':
                            postfixStack.pop()
                            leftFound = True
                        else:
                            postFix += postfixStack.pop() + ' '


                # adds operators to their proper position in the stack based on precedence
                elif iStr == '+' or iStr == '-' or iStr == '*' or iStr == '/' or iStr == '^':

                    if lastWasOperator == True:
                        # invalid expression: two operators in a row
                        return None
                    
                    # if the stack is empty, the operator is automatically pushed in
                    if postfixStack.isEmpty():
                        postfixStack.push(iStr)
                    else:
                        # pops the top item and adds it to postFix until if finds an operator with lower precedence then pushes the current operator
                        pushed = False
                        while pushed == False:

                            # TODO: there is a chance that this if statement should only run on the first loop through this while loop
                            if iStr == '^' and postfixStack.peek() == '^':
                                postfixStack.push(iStr)
                                pushed = True
                            
                            # Pushes the operator if there is nothing left in the stack or the precedence of the current operator is
                            # greater than that of the top operator
                            elif postfixStack.top == None or precedence[iStr] > precedence[postfixStack.peek()]:
                                postfixStack.push(iStr)
                                pushed = True
                            
                            # if the precedence of the current operator is less than that of the top operator, the top operator
                            # is popped and added to the postFix string
                            elif precedence[iStr] <= precedence[postfixStack.peek()]:
                                postFix += postfixStack.pop() + ' '
        
                    lastWasOperator = True
        
        # loops through postfixStack to add any remaining operators
        empty = False
        while not empty:
            if postfixStack.top == None:
                empty = True
            else:
                postFix += postfixStack.pop() + ' '

        # strips any unecesary spaces before returning
        return postFix.rstrip()


    @property
    def calculate(self):
        '''
            calculate must call _getPostfix
            calculate must create and use a Stack to compute the final result as shown in the video lecture
            
            >>> x=Calculator()
            >>> x.setExpr('4 + 3 - 2')
            >>> x.calculate
            5.0
            >>> x.setExpr('-2 + 3.5')
            >>> x.calculate
            1.5
            >>> x.setExpr('4 + 3.65 - 2 / 2')
            >>> x.calculate
            6.65
            >>> x.setExpr('23 / 12 - 223 + 5.25 * 4 * 3423')
            >>> x.calculate
            71661.91666666667
            >>> x.setExpr(' 2 - 3 * 4')
            >>> x.calculate
            -10.0
            >>> x.setExpr('7 ^ 2 ^ 3')
            >>> x.calculate
            5764801.0
            >>> x.setExpr(' 3 * ( ( ( 10 - 2 * 3 ) ) )')
            >>> x.calculate
            12.0
            >>> x.setExpr('8 / 4 * ( 3 - 2.45 * ( 4 - 2 ^ 3 ) ) + 3')
            >>> x.calculate
            28.6
            >>> x.setExpr('2 * ( 4 + 2 * ( 5 - 3 ^ 2 ) + 1 ) + 4')
            >>> x.calculate
            -2.0
            >>> x.setExpr(' 2.5 + 3 * ( 2 + ( 3.0 ) * ( 5 ^ 2 - 2 * 3 ^ ( 2 ) ) * ( 4 ) ) * ( 2 / 8 + 2 * ( 3 - 1 / 3 ) ) - 2 / 3 ^ 2')
            >>> x.calculate
            1442.7777777777778
            

            # In invalid expressions, you might print an error message, but code must return None, adjust doctest accordingly
            >>> x.setExpr(" 4 + + 3 + 2") 
            >>> x.calculate
            >>> x.setExpr("4  3 + 2")
            >>> x.calculate
            >>> x.setExpr('( 2 ) * 10 - 3 * ( 2 - 3 * 2 ) )')
            >>> x.calculate
            >>> x.setExpr('( 2 ) * 10 - 3 * / ( 2 - 3 * 2 )')
            >>> x.calculate
            >>> x.setExpr(' ) 2 ( * 10 - 3 * ( 2 - 3 * 2 ) ')
            >>> x.calculate
            >>> x.setExpr('( 3.5 ) ( 15 )') 
            >>> x.calculate
            >>> x.setExpr('3 ( 5 ) - 15 + 85 ( 12 )') 
            >>> x.calculate
            >>> x.setExpr("( -2 / 6 ) + ( 5 ( ( 9.4 ) ) )") 
            >>> x.calculate
        '''

        if not isinstance(self.__expr,str) or len(self.__expr)<=0:
            print("Argument error in calculate")
            return None

        calcStack = Stack()   # method must use calcStack to compute the  expression

        # convert self.__expr to postFix notation
        postFix = self._getPostfix(self.__expr)

        # if the expression is invalid, None is returned
        if postFix == None:
            return None

        # loops through the postFix expression to make the calculations 
        postFixLST = postFix.split()
        for i in postFixLST:
            if self._isNumber(i):
                calcStack.push(float(i))
            elif i == '+':
                secondTerm = calcStack.pop()
                firstTerm = calcStack.pop()
                newTop = firstTerm + secondTerm
                calcStack.push(newTop)
            elif i == '-':
                secondTerm = calcStack.pop()
                firstTerm = calcStack.pop()
                newTop = firstTerm - secondTerm
                calcStack.push(newTop)
            elif i == '*':
                secondTerm = calcStack.pop()
                firstTerm = calcStack.pop()
                newTop = firstTerm * secondTerm
                calcStack.push(newTop)
            elif i == '/':
                secondTerm = calcStack.pop()
                firstTerm = calcStack.pop()
                newTop = firstTerm / secondTerm
                calcStack.push(newTop)
            elif i == '^':
                secondTerm = calcStack.pop()
                firstTerm = calcStack.pop()
                newTop = firstTerm ** secondTerm
                calcStack.push(newTop)
        
        return float(calcStack.pop())


#=============================================== Part III ==============================================

class AdvancedCalculator:
    '''
        >>> C = AdvancedCalculator()
        >>> C.states == {}
        True
        >>> C.setExpression('a = 5;b = 7 + a;a = 7;c = a + b;c = a * 0;return c')
        >>> C.calculateExpressions() == {'a = 5': {'a': 5.0}, 'b = 7 + a': {'a': 5.0, 'b': 12.0}, 'a = 7': {'a': 7.0, 'b': 12.0}, 'c = a + b': {'a': 7.0, 'b': 12.0, 'c': 19.0}, 'c = a * 0': {'a': 7.0, 'b': 12.0, 'c': 0.0}, '_return_': 0.0}
        True
        >>> C.states == {'a': 7.0, 'b': 12.0, 'c': 0.0}
        True
        >>> C.setExpression('x1 = 5;x2 = 7 * ( x1 - 1 );x1 = x2 - x1;return x2 + x1 ^ 3')
        >>> C.states == {}
        True
        >>> C.calculateExpressions() == {'x1 = 5': {'x1': 5.0}, 'x2 = 7 * ( x1 - 1 )': {'x1': 5.0, 'x2': 28.0}, 'x1 = x2 - x1': {'x1': 23.0, 'x2': 28.0}, '_return_': 12195.0}
        True
        >>> print(C.calculateExpressions())
        {'x1 = 5': {'x1': 5.0}, 'x2 = 7 * ( x1 - 1 )': {'x1': 5.0, 'x2': 28.0}, 'x1 = x2 - x1': {'x1': 23.0, 'x2': 28.0}, '_return_': 12195.0}
        >>> C.states == {'x1': 23.0, 'x2': 28.0}
        True
        >>> C.setExpression('x1 = 5 * 5 + 97;x2 = 7 * ( x1 / 2 );x1 = x2 * 7 / x1;return x1 * ( x2 - 5 )')
        >>> C.calculateExpressions() == {'x1 = 5 * 5 + 97': {'x1': 122.0}, 'x2 = 7 * ( x1 / 2 )': {'x1': 122.0, 'x2': 427.0}, 'x1 = x2 * 7 / x1': {'x1': 24.5, 'x2': 427.0}, '_return_': 10339.0}
        True
        >>> C.states == {'x1': 24.5, 'x2': 427.0}
        True
        >>> C.setExpression('A = 1;B = A + 9;C = A + B;A = 20;D = A + B + C;return D - A')
        >>> C.calculateExpressions() == {'A = 1': {'A': 1.0}, 'B = A + 9': {'A': 1.0, 'B': 10.0}, 'C = A + B': {'A': 1.0, 'B': 10.0, 'C': 11.0}, 'A = 20': {'A': 20.0, 'B': 10.0, 'C': 11.0}, 'D = A + B + C': {'A': 20.0, 'B': 10.0, 'C': 11.0, 'D': 41.0}, '_return_': 21.0}
        True
        >>> C.states == {'A': 20.0, 'B': 10.0, 'C': 11.0, 'D': 41.0}
        True
        >>> C.setExpression('A = 1;B = A + 9;2C = A + B;A = 20;D = A + B + C;return D + A')
        >>> C.calculateExpressions() is None
        True
        >>> C.states == {}
        True
    '''
    def __init__(self):
        self.expressions = ''
        self.states = {}

    def setExpression(self, expression):
        self.expressions = expression
        self.states = {}

    def _isVariable(self, word):
        '''
            >>> C = AdvancedCalculator()
            >>> C._isVariable('volume')
            True
            >>> C._isVariable('4volume')
            False
            >>> C._isVariable('volume2')
            True
            >>> C._isVariable('vol%2')
            False
        '''
        isValid = True # is True if word is a valid variable name and False if not

        # makes sure the first character in word is a letter
        if word[0].isalpha():
            
            # looks at each letter to determine if it is not an alphanumeric character
            for i in word:
                if i.isalnum():
                    if isValid == True:
                        isValid = True
                else:
                    isValid = False
        else:
            isValid = False
        
        return isValid
                

       

    def _replaceVariables(self, expr):
        '''
            >>> C = AdvancedCalculator()
            >>> C.states = {'x1': 23.0, 'x2': 28.0}
            >>> C._replaceVariables('1')
            '1'
            >>> C._replaceVariables('105 + x')
            >>> C._replaceVariables('7 * ( x1 - 1 )')
            '7 * ( 23.0 - 1 )'
            >>> C._replaceVariables('x2 - x1')
            '28.0 - 23.0'
        '''
        exprLst = expr.split() # splits expr by spaces to look at each term
        newExpr = [] # modifies expr and rebuilds the expression but with the variable values subsituted in
        

        # loops through each term in the expression
        for i in exprLst:

            # if the first character in the term is a letter, it checks if the term is a variable in self.states
            if self._isVariable(i) == True:
                if i in self.states:
                    newExpr.append(self.states[i])
                else:
                    return None
            
            # if the first character is not a letter, it must be a number and is not modified
            else:
                newExpr.append(i)
        

        # loops through newExpr and adds spaces between each term to make it a valid expression in String form
        outputExpr = ""
        for i in newExpr:
            outputExpr += str(i) + " "
        
        return outputExpr.rstrip()



    
    def calculateExpressions(self):

        self.states = {} 
        calcObj = Calculator()     # method must use calcObj to compute each expression
        
        exprDict = {} # stores the progression of the calculations. 
                                    # The key is the line evaluated 
                                    # the value is the current state of self.states after the line is evaluated. 
                                    # the return key holds the final result of self.states after everything is evalueated

        exprLineLst = self.expressions.split(";") # stores each expression in self.expression as a String
        
        returnFound = False
        line = 0
        while line < len(exprLineLst):
            termsLst = exprLineLst[line].split()
            # finds the value of the variable and updates self.states with the first variable's value (i.e. the first line)
            if self._isVariable(termsLst[0]) and termsLst[0] != 'return': # a = 5 or b = a ^ 3 + 4
                varName = termsLst[0]
                rightSideStr = exprLineLst[line][len(varName) + 3:] # string of the right side of the equals sign
                rightSideSubbed = self._replaceVariables(rightSideStr)
                calcObj.setExpr(rightSideSubbed)
                rightSideVal = calcObj.calculate
                self.states[varName] = rightSideVal

            # finds the value of return
            elif termsLst[0] == 'return': # return c or return x1 + x2 * 5
                varName = termsLst[0]
                rightSideStr = exprLineLst[line][7:] # string on the right side of the equals sign
                rightSideSubbed = self._replaceVariables(rightSideStr)
                calcObj.setExpr(rightSideSubbed)
                rightSideVal = calcObj.calculate
                returnFound = True
            else:
                self.states = {}
                return None

                
            if returnFound == False:
                # loop through self.states to copy down the dictionary without referencing the memory address of self.states
                currentStates = {} # holds the current value of self.states
                for i in self.states:
                    currentStates[i] = self.states[i]
                exprDict[exprLineLst[line]] = currentStates
            else:
                # this runs last and is for the return line in the expressions
                exprDict['_return_'] = rightSideVal
            
            line += 1
                        

        return exprDict
