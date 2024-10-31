import streamlit as st

import math
#import sympy as sp
from sympy import solve
from sympy import Eq
from sympy import symbols
from fractions import Fraction


class Separate:
    # sets up the class
    def __init__(self, equation):
        self.equation = equation  # Store the equation as an instance variable
        self.invalid=False
        self.isInvalidReason = ""

    # checks if the equation is invalid. if it is, it prints general error
    def isInvalid(self):
        self.invalid=True
        return self.isInvalidReason
        #if (self.equation.count('=') != 1):
         #   return "Has too many =. Please try again"

    # separates the sides of the equation using the = into an array and returns it. if there is more than one equals sign it returns has too many equal signs
    def sides(self):
        if (self.equation.count('=') != 1):
            #self.isInvalidReason = "Has more or less than 1 =. Please try again."
            #return self.isInvalid()
            st.write("Has more or less than 1 =. Please try again.")
            self.invalid = True
        equation = self.equation.split('=')
       # if (len(equation) > 2):
        #    return "Has too many =. Please try again"
        #print(equation)
        if(self.invalid==False):
            return equation
        else:
            self.invalid=True
            return self.invalid

    # this separates the separated side version into further separations of molecules while maintaining the separation of the sides in a nested array
    def molecules(self):
        if (self.invalid==True):
            return self.invalid
        equation = self.sides()
        if(self.invalid==True):
            return self.invalid
        # Call sides method to get the sides
        if(equation[0][-1]=='+'):
            st.write("Side ends with a +. Invalid")
            self.invalid = True
            return self.invalid
        if(equation[1][-1]=='+'):
            st.write("Side ends with a +. Invalid")
            self.invalid = True
            return self.invalid
        equation[0] = equation[0].split('+')
        if(equation[0][-1]=='+'):
            st.write("Side ends with a +. Invalid")
            self.invalid = True
            return self.invalid
        equation[1] = equation[1].split('+')
        
        #print(equation)
        if(self.invalid==True):
            return self.invalid
        return equation

    def isElement(self, potElementString):
        elements = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne","Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca","Sc", "Ti", "V", "Cr", "Mn", "Fe", "Ni", "Co", "Cu", "Zn","Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"]
        numEls = len(elements)
        #x = 0
        elementFound = False
        for x in range(len(elements)):
            if potElementString == elements[x]:
                #result = print("It's an Element, in fact, it is: ", elements[x])
                elementFound = True
                #print("I am stuck in the loop!")
            #x+=1
        if elementFound==False:
            #print("The element", potElementString, "does not exist. Please try again.")
            #self.isInvalidReason = "The element" + potElementString+ "does not exist. Please try again."
            #return self.isInvalid()
            st.write("The element" + potElementString+ "does not exist. Please try again.")
            self.invalid=True
            return self.invalid
            
       # else:
        #    isInvalidReason = "I'm sorry, I do  not understand that. Please try again: " + potElementString
         #   return self.isInvalid()
            #x+=1
        return elementFound

    # This separates it into elements while keeping the separations of the molecules and sides in a nested array
    def elements(self):
        if(self.invalid):
            return self.invalid
        equation = self.molecules()# Call molecules to get the separated molecules
        if(self.invalid):
            return self.invalid
        length_equation = len(equation)

        # Iterate over the sides of the equation
        for side in range(length_equation):
            # Iterate over the molecules on each side
            len_side = len(equation[side])
            for mol in range(len_side):
                parsed_mol = []
                mol_len = len(equation[side][mol])
                letter = 0

                # Parse the molecule letter by letter
                while letter < mol_len:
                    # Handle numeric values (coefficients or subscripts)
                    if equation[side][mol][letter].isnumeric():
                        whole_num = ""
                        while letter < mol_len and equation[side][mol][letter].isnumeric():
                            whole_num += equation[side][mol][letter]
                            letter += 1  # increment letter directly
                        #print("Number: ", whole_num)
                        parsed_mol.append(whole_num)

                    # Handle elements (letters)
                    elif equation[side][mol][letter].isalpha():
                        if equation[side][mol][letter].isupper():  # Capital letter, start of an element
                            if letter + 1 < mol_len and equation[side][mol][letter + 1].islower():
                                # Two-letter element (e.g., "He")
                                potE = equation[side][mol][letter] + equation[side][mol][letter + 1]
                                letter += 2  # skip both letters
                            else:
                                # One-letter element (e.g., "H")
                                potE = equation[side][mol][letter]
                                letter += 1  # skip the one letter

                            # Check if it's a valid element
                            if self.isElement(potE):  # Changed to self.isElement
                                #print("We got an element!: ", potE)
                                parsed_mol.append(potE)
                            else:
                                self.invalid=True
                                st.write("We have an error! Error Causer: "+ potE)
                                return self.invalid

                        # Check if there is a numeric subscript following the element
                        if letter < mol_len and equation[side][mol][letter].isnumeric():
                            subscript = ""
                            while letter < mol_len and equation[side][mol][letter].isnumeric():
                                subscript += equation[side][mol][letter]
                                letter += 1
                            parsed_mol.append(subscript)

                    # Handle parentheses
                    elif equation[side][mol][letter] == '(':
                        #print("It's a (")
                        #parsed_mol.append('(')
                        letter += 1
                        self.isInvalidReason = "Sorry, we do not handle equations with parentheses at this time."
                        st.write(self.isInvalidReason)
                        
                        #return false
                    elif equation[side][mol][letter] == ')':
                        #print("It's a )")
                        #parsed_mol.append(')')
                        letter += 1
                        isInvalidReason = "Sorry, we do not handle equations with parentheses at this time."
                        st.write(isInvalidReason)
                     
                        

                    # Handle unexpected characters
                    else:
                        #print("Unexpected character: ", equation[side][mol][letter])
                        st.write("Unexpected character: ", equation[side][mol][letter], ". Will ignore")
                        letter += 1

                # Replace the molecule with its parsed version
                equation[side][mol] = parsed_mol

        #print("")
        return equation  # Return parsed equation

    def elementCount(self):
        equation = self.elements()  # Call elements to get parsed elements
  # Return empty if invalid equation
        elements0 = []
        elements1 = []
        side0 = equation[0]
        side1 = equation[1]
        
        # Collect unique elements from side0
        for mol in side0:
            for el in mol:
                if el.isalpha() and el not in elements0:
                    elements0.append(el)  # Append only if it's unique

        # Collect unique elements from side1
        for mol in side1:
            for el in mol:
                if el.isalpha() and el not in elements1:
                    elements1.append(el)  # Append only if it's unique

        if (sorted(elements0) == sorted(elements1)):
            #print("Same: ", elements0)
            #print("There are ", len(elements0), "elements")
            return elements0
        else:
            st.write("Equation needs to have the same elements on both sides. Error")
            #print(elements0, "!=", elements1)
            self.invalid=True
            return self.invalid

    def elementSolve(self):
        if(self.invalid):
            return self.invalid
        equation = self.elements()  # Call elements to get parsed elements
        #print(equation)
        if(self.invalid):
            return self.invalid
        side0 = equation[0]
        side1 = equation[1]

        num_elements = self.elementCount()  # Number of unique elements (rows)
        if(num_elements == True):
        #if not num_elements:
            #st.write("Element count failed")
            return True# Handle no valid elements case
        
        totalCol = len(side0) + len(side1)  # Total number of molecules (columns)
       # print("Total columns = ", totalCol)
        if(self.invalid==True):
           st.write(self.invalid)
           return self.invalid
        totalRow = len(num_elements)
        # sympy matrix solving does not work for chemical equations who have two or more molecules than the num of elements
        if((totalRow+1)<(totalCol)):
            invalid=True
            return invalid

        # Initialize matrix with zeros
        totalMatrix = [[0 for _ in range(totalCol)] for _ in range(totalRow)]
        curEl = 0
        for side in range(2):
            for col in range(len(equation[side])):
                for el in range(len(equation[side][col])):
                    for row in range(len(num_elements)):
                        if equation[side][col][el] == num_elements[row]:
                            if (equation[side][col][el] == equation[side][col][-1]):
                                totalMatrix[row][len(side0) * side + col] += 1
                            elif (el + 1 < len(equation[side][col]) and equation[side][col][el + 1].isnumeric()):
                                totalMatrix[row][len(side0) * side + col] += int(equation[side][col][el + 1])
                            elif (el + 1 < len(equation[side][col]) and equation[side][col][el + 1].isalpha()):
                                totalMatrix[row][len(side0) * side + col] += 1
                            else:
                                st.write("I'm unsure what to do")
                                self.invalid = True
                                return self.invalid
                #print(totalMatrix)

        # Make matrix square
        while len(totalMatrix) != len(totalMatrix[0]):
            newRow = []
            if (totalRow > totalCol):
                for i in range(totalRow):
                    totalMatrix[i].append(0)
            elif (totalCol > totalRow):
                for i in range(totalCol):
                    newRow.append(0)
                totalMatrix.append(newRow)

        # Negate second side
        for i in range(totalRow):
            for j in range(totalCol // 2, totalCol):
                totalMatrix[i][j] = -totalMatrix[i][j]
        
        # Define the coefficients as symbols
        stringVariables = ''
        for i in range(totalCol):
            stringVariables += "c" + str(i) + ' '
        symbol = symbols(stringVariables)

        # Initialize a list to store the equations
        equations = []

        # Iterate over each row in the matrix to create equations
        for row in totalMatrix:
            constant = row[-1]  # The last element in the row represents the constant (right side of the equation)
            coefficients = row[:-1]  # Coefficients for each variable (excluding the last one)
        
            # Create the equation using the dot product
            equationw = Eq(sum(coef * sym for coef, sym in zip(coefficients, symbol)), constant)
            equations.append(equationw)  # Append the equation to the list

        # Solve the system of equations
        solution = solve(equations, symbol)
        #print("Solution = ", solution)
        const = 1
        solutionArray = list(solution.values())
        for i in range(len(solutionArray)):
            solutionArray[i] = abs(solutionArray[i])
        for j in range(len(solutionArray)):
            fracJ = Fraction(solutionArray[j])
            if solutionArray[j]<1/const:
                const = fracJ.denominator
        #print(solutionArray)
        for k in range(len(solutionArray)):
            solutionArray[k]*=const
        #print(solutionArray)
        solutionArray.append(const)
        

        solvedEquation = ""
        #turns the solved equation matrix back into a string equation
        for side in range(len(equation)):
            for mol in range(len(equation[side])):
                solvedEquation += str(solutionArray[mol + side * len(equation[0])])
                for el in range(len(equation[side][mol])):
                    if(equation[side][mol][el].isnumeric()):
                        solvedEquation+="_{"
                        solvedEquation+=equation[side][mol][el]
                        solvedEquation+="}"
                    else:
                        solvedEquation+=equation[side][mol][el]
                        
                if(mol!=len(equation[side])-1):
                    solvedEquation += " + "  # Add spacing between molecules
            if(side==0):
                solvedEquation+= " = "
                
        #turns the equation into latex to make it easier to read
        solvedEquation = solvedEquation.replace("+  ", "")
        solvedEquation = solvedEquation.replace("=", "\\longrightarrow")
        
        #turns the solution into latex
        st.latex(r""" """ +solvedEquation+""" """)
       
        return solvedEquation
        





st.write("""
Stoichiometric Equation Solver
""")
with st.form(key="myForm"):
    userEquation = st.text_input("Insert your chemical equation here", "H+O=H2O")
    #separate = Separate(userEquation)
    st.form_submit_button("Solve")
    
separate = Separate(userEquation)


userEquation = separate.elementSolve()
solution =  userEquation
#print(solution)


