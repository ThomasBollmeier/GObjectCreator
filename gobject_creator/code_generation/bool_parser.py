# coding=UTF-8

"""
This file is part of GObjectCreator.

GObjectCreator is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

GObjectCreator is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with GObjectCreator (see file COPYING). If not, see
<http://www.gnu.org/licenses/>.
"""

def evaluateExpr(inExprStr):
    
    return bool(inExprStr)

class LogicalExpr(object):
    
    def __init__(self, inSimple):
        
        if self.__class__ is LogicalExpr:
            raise AbstractClassError
        
        self.simple = inSimple
        self.negation = False
        
    def isTrue(self, inEvaluator = evaluateExpr):
        
        result = self._isTrue(inEvaluator)
        if self.negation:
            result = not result
            
        return result 

    def _isTrue(self, inEvaluator = evaluateExpr):
        pass
        
    def _toString(self):
        pass
    
    def __str__(self):
        
        result = self._toString()
        if self.negation:
            result = "! ( %s )" % result
            
        return result
        
class LogicalExprSimple(LogicalExpr):
    
    def __init__(self, inExprStr):
        
        LogicalExpr.__init__(self, True)
        self.exprStr = inExprStr

    def _isTrue(self, inEvaluator = evaluateExpr):
        
        return inEvaluator(self.exprStr)
         
    def _toString(self):
        
        return self.exprStr 

class Bool:
    
    AND, OR = range(1, 3)
        
class LogicalExprCompound(LogicalExpr):
    
    def __init__(self, inType = Bool.AND):
        
        LogicalExpr.__init__(self, False)
        self.type = inType
        self.exprs = []
        
    def add(self, inExpr):
        
        self.exprs.append(inExpr)
        
    def _isTrue(self, inEvaluator):
        
        result = None
        for expr in self.exprs:
            if result is None:
                result = expr.isTrue(inEvaluator)
            else:
                if self.type == Bool.AND:
                    result = result and expr.isTrue(inEvaluator)
                else:
                    result = result or expr.isTrue(inEvaluator)
            if (self.type == Bool.AND and not result) or \
               (self.type == Bool.OR and result):
                return result
        
        return result
        
    def _toString(self):
        
        result = ""
        for expr in self.exprs:
            if result:
                if self.type == Bool.AND:
                    result += " && "
                else:
                    result += " || "
            result += "( %s )" % expr

        return result

class BoolParser(object):
    
    def __init__(self,
                 inAndOperator = "and",
                 inOrOperator = "or",
                 inNotOperator = "not"
                 ):
        
        self._and = inAndOperator
        self._or = inOrOperator
        self._not = inNotOperator
        
    def parse(self, inExprStr):
        """
        Parsing-Analyse eines logischen Ausdrucks
        
        --> inExprStr: logischer Ausdruck (string)
        <-- logischer Ausdruckstyp (LogicalExpr)
        
        """
        
        substrs = self._splitWithParentheses(inExprStr, self._or)
        if len(substrs) == 1:
            # keine Oder-Verknüpfung => Und-Verknüpfung prüfen
            substrs = self._splitWithParentheses(inExprStr, self._and)
            if len(substrs) == 1:
                # keine Und-Verknüpfung => Negation prüfen
                substrs = self._splitWithParentheses(inExprStr, self._not, 
                                                     inInclSep=True)
                numSubstrs = len(substrs)
                if numSubstrs == 1:
                    result = LogicalExprSimple(inExprStr)
                    result.negation = False
                elif numSubstrs == 2:
                    result = self.parse(substrs[1])
                    result.negation = True
                else:
                    raise ParseError
            else:
                result = LogicalExprCompound(Bool.AND)
                for substr in substrs:
                    result.add(self.parse(substr))
        else:
            result = LogicalExprCompound(Bool.OR)
            for substr in substrs:
                result.add(self.parse(substr))
    
        return result
    
    def _splitWithParentheses(self, inExprStr, inSep, inSepCaseSensitive = False,
                              inInclSep = False):
        
        if not inSepCaseSensitive:
            separators = self._getCaseVariations(inSep)
        else:
            separators = [inSep] 
        
        level = 0
        curr = ""
        tail = ""
        lenSep = len(inSep)
        substrs = []
        
        exprStr = inExprStr.strip()
        if exprStr[0] == "(" and exprStr[-1] == ")":
            exprStr = exprStr[1:-1]
        
        for ch in exprStr:
            
            if len(tail) == lenSep:
                # Trenner gefunden?
                found = False    
                if tail in separators:
                    # ja -> sicherstellen, dass davor und danach Leerzeichen ist
                    try:
                        lastChar = curr[-1]
                    except IndexError:
                        lastChar = " "
                    if lastChar == " " and ch == " ":
                        found = True
                    
                if not found:
                    curr += tail[0]
                    tail = tail[1:]
                else:
                    if curr:
                        substrs.append(curr)
                        curr = ""
                    if inInclSep:
                        substrs.append(tail)
                    tail = ""
                    
            if ch == "(":
                level += 1
                if level == 1:
                    curr += tail
                    tail = ""
            elif ch == ")":
                level -= 1
            
            if level == 0:
                tail += ch
            else:
                curr += ch
                
        curr += tail
        substrs.append(curr)
        
        return substrs
        
    def _getCaseVariations(self, inStr):
        
        left = ""
        right = inStr
        result = []
        self.__getCaseVariations(left, right, result)
        
        return result
                
    def __getCaseVariations(self, inLeftStr, inRightStr, inOutVariations):
        """
        Ermittelt die Kombinationen, die sich aus einer Zeichenkette
        bei Variation von Groß- und Kleinschreibung ergeben.
        """
        if inRightStr:
            charLower = inRightStr[0].lower()
            charUpper = inRightStr[0].upper()
            rightStr = inRightStr[1:]
            self.__getCaseVariations(inLeftStr + charLower, rightStr, inOutVariations)
            self.__getCaseVariations(inLeftStr + charUpper, rightStr, inOutVariations)
        else:
            if not inLeftStr in inOutVariations:
                inOutVariations.append(inLeftStr)

class AbstractClassError(Exception): pass

class ParseError(Exception): pass
