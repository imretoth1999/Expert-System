#!/usr/bin/python
import sys

class Nod:
    def __init__(self, name, rule):
        self.name = name;
        self.rules = [];
        self.found = -2;
        self.addRule(rule);
    def addRule(self, rule):
        if rule not in self.rules:
            self.rules.append(rule)

class ExpertSystem:
    def __init__(self,d):
        self.__destinatie = d
        self.__necunoscute = []
        self.__noduri = {}
        self.__propozitii = None
        self.__cerinta = None
        self.__contradictii = ""
        try:
            prop = False
            cerinta = False
            with open(d) as fisier:
                linii = fisier.readlines()
                for linie in linii:
                    linie = linie.strip()
                    if '#' in linie:
                        linie = linie.split('#')[0].strip()
                    if  linie != '\n' and linie != '':
                        if linie[0] == '=':
                            if prop:
                                print "We already have first order logic facts"
                                exit()
                            self.__propozitii = linie.split('=')[1].replace(" ","").strip()
                            for c in self.__propozitii:
                                if not (c and c.isalpha() and c.isupper()):
                                    print "Not a valid char"
                                    exit()
                            prop = True
                            self.__propozitii='1'+self.__propozitii
                        elif linie[0] == '?':
                            if not prop:
                                print "No first order logic facts found"
                                exit()
                            if cerinta:
                                print "We already have the requests"
                                exit()
                            self.__cerinta = linie.split('?')[1].replace(" ","").strip()
                            for c in self.__cerinta:
                                if not (c and c.isalpha() and c.isupper()):
                                    print "The character is not valid"
                                    exit()  
                            cerinta = True
                        else:
                            if "=>" in linie:
                                formula = linie.split("=>")[0].strip()
                                formula = "(" + formula + ")"
                                dreapta = linie.split("=>")[1].strip()
                                corect = False
                                if not self.greseala(dreapta,corect):
                                    print "Error in the right side"
                                    exit()
                                corect = True
                                if not self.greseala(formula,corect):
                                    print "Error in the left side"
                                    exit()
                                formula =self.addp(formula)
                                p,n = self.getValueName(dreapta)
                                for name in p:
                                    if name in self.__noduri:
                                        self.__noduri[name].addRule(formula)
                                    else:
                                        self.__noduri[name] = Nod(name,formula)
                                formula = "(!" + formula + ")"
                                for name in n:
                                    if name in self.__noduri:
                                        self.__noduri[name].addRule(formula)
                                    else:
                                        self.__noduri[name] = Nod(name,formula)
                            else:
                                print "No => found in the line"
                                exit()
        except IOError:
            print "Error while opening the file"
            exit()
        return
                                    
    def greseala(self,linie,corect):
        linie = linie.replace(" ","")
        if linie == "\n" and linie == "":
            return False
        nrbrackets = 0
        prevF = None
        for c in linie:
            if c == '(':
                if prevF and prevF.isupper() and prevF.isalpha():
                    return False
                nrbrackets+=1
            elif c == ')':
                if nrbrackets <= 0:
                    return False
                if not (prevF and prevF.isupper() and prevF.isalpha()) and not prevF == ')':
                    return False
                nrbrackets-=1
            elif c == '!':
                if prevF and prevF.isalpha() and prevF.isupper():
                    return False
            elif c == '+':
                if not ( prevF and prevF.isupper() and prevF.isalpha()) and not prevF == ')':
                    return False
            elif corect and c == '|':
                if not  (prevF and prevF.isupper() and prevF.isalpha()):
                    return False
            elif corect and c == '^':
                if not ( prevF and prevF.isupper() and prevF.isalpha()):
                    return False
            elif c and c.isupper() and c.isalpha:
                if prevF and prevF.isalpha() and prevF.isupper():
                    return False
            else:
                return False
            prevF = c
        if nrbrackets > 0 or prevF == '!':
            return False
        return True
           
    def addp(self,formula):
        i = 0
        while i < len(formula):
            if formula[i] == '!':
                i+=1
                j = i
                if not formula[i].isalpha():
                    k = 0
                    while j <len(formula):
                        if formula[j] == '(':
                            k+=1
                        elif formula[j] == ')':
                            k-=1
                            if k == 0:
                                break
                        j+=1
                formula = formula[:j+1] + ')' + formula[j+1:]
                formula = formula[:i-1] + '(' + formula[i-1:]
            i+=1
        formula = self.addop(formula,'+')
        formula = self.addop(formula,'|')
        formula = self.addop(formula,'^')
        
        return formula
    def addop(self, formula, op):
        i = 0
        while i < len(formula):
            if formula[i] == op:
                left = i
                right = i
                i += 1
                counter = 0
                while left > 0:
                    if formula[left] == ")":
                        counter += 1
                    elif formula[left] == "(":
                        counter -= 1
                        if counter == 0:
                            break
                    elif formula[left].isalpha() and counter == 0:
                        break
                    left -= 1
                while right < len(formula):
                    if formula[right] == "(":
                        counter += 1
                    elif formula[right] == ")":
                        counter -= 1
                        if counter == 0:
                            break
                    elif formula[right].isalpha() and counter == 0:
                        break
                    right += 1
                formula = formula[:right + 1] + ')' + formula[right+1:]
                formula = formula[:left - 1] + '(' + formula[left- 1:]
            i += 1
        return formula
    def getValueName(self,r):
        r = r.replace(" ","")
        pos = []
        pnegation = []
        negation = []
        paranthesis = 0
        previous = None
        for c in r:
            if c == '(':
                paranthesis+=1
                if previous == '!':
                    pnegation.append(paranthesis)
            elif c == ')':
                if paranthesis in pnegation:
                    pnegation.remove(paranthesis)
                paranthesis -= 1
            elif c.isalpha():
                negations = len(pnegation)
                if previous == '!':
                    negations +=1
                if negations % 2 == 0:
                    pos.append(c)
                else:
                    negation.append(c)
            previous = c
        return pos, negation
    def calcul(self,e):
        stanga = e[0]
        neg = False
        val = []
        sval = []
        op = []
        dreapta = e[1:]
        if stanga == '!':
            neg = True
            stanga = e[1]
            dreapta = e[2:]
        rezstanga = self.prelucrare(stanga)
        val.append(rezstanga);
        if (neg):
            rezstanga = not rezstanga
        sval.append(neg)
        while True:
            neg = False
            if dreapta != "":
                op1 = dreapta[0]
                op.append(op1)
                inceput = dreapta[1]    
                dreapta = dreapta[2:]
            else:
                break
            if inceput == '!':
                neg = True
                inceput = dreapta[0]
                dreapta = dreapta[1:]
            rezdreapta = self.prelucrare(inceput)
            val.append(rezdreapta)
            if neg:
                rezdreapta = not rezdreapta
            sval.append(neg)
            if op1 == "+":
                rezstanga = rezstanga and rezdreapta
            if op1 == "|":
                rezstanga = rezstanga or rezdreapta
            if op1 == "^":
                rezstanga = (not rezstanga and rezdreapta) or (not rezdreapta and rezstanga)
        return rezstanga
    
    def prelucrare(self,q):
        if q in self.__necunoscute:
            print "Impossible solution!"
            exit()
        else:
            self.__necunoscute.append(q)
        if q in self.__propozitii:
            self.__necunoscute.remove(q)
            return True
        elif q in self.__contradictii:
            if q not in self.__contradictii:
                self.__contradictii+=q
            self.__necunoscute.remove(q)
            return False
        elif q in self.__noduri:
            for r in self.__noduri[q].rules:
                r = r.replace(" ","")
                while "(" in r:
                    cp = r.find(")")
                    op = r.rfind('(',0,cp)
                    e = r[op + 1:cp]
                    c = self.calcul(e)
                    func = r[0:op]
                    if c:
                        func += '1'
                    else:
                        func += '0'
                    r = func + r[cp+1:]
                if r == "1":
                    if q not in self.__propozitii:
                        self.__propozitii += q
                    self.__necunoscute.remove(q)
                    return True
            if q not in self.__contradictii:
                self.__contradictii+=q
            self.__necunoscute.remove(q)
            return False
        else:
            if q not in self.__contradictii:
                self.__contradictii += q
            self.__necunoscute.remove(q)
            return False
    def solution(self):
        for i,q in enumerate(self.__cerinta):
            res = self.prelucrare(q)
            print "For the sentence ",q,"the result is: ",res
if	len(sys.argv) < 2:
	print "No file given!Try again"
	exit()
else:
	first_order_logic = ExpertSystem(sys.argv[1])
	first_order_logic.solution()
