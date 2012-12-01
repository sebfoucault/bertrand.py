import pprint
from collections import deque

class DequeEx:
    
    def __init__(self,smart):
        self._values_keys = {};
        self._deque = deque()
    
    def __len__(self):
        return len(self._deque)
    
    def popleft(self):
        return self._deque.popleft()
        
    def append(self, state):
    
        svalues = state.values[:]
        svalues.sort()
        svalues_keys = self._get_key(svalues)
        
        if (svalues_keys in self._values_keys):
            pass
        else: 
            self._values_keys[svalues_keys] = True
            self._deque.append(state)
    
    def extend(self, states):
        for state in states:
            self.append(state)
        
    def _get_key(self,list):
        k = ""
        for i in list:
            k = k + ";" + str(i)
        return k            

class Problem:
    
    def __init__(self, values, target):
        self.values = values
        self.target = target
        
    def __repr__(self):
        return """"{ target:%s, values:%s"}""" \
            %(str(self.target), repr(self.values))

class State: 
    
    def __init__(self, problem, values, operations):
        self.problem = problem
        self.operations = operations
        self.values = values   
    
    def is_solved(self):
        return len( [x for x in self.values if x == self.problem.target] ) > 0
    
    def __repr__(self):
        return """{problem: %s, values: %s, operations: %s}""" \
            %(repr(self.problem), repr(self.values), repr(self.operations))
            
            
class Operation:

    def __init__(self, symbol, commutative, computator, validator):
        self.symbol = symbol
        self._computator = computator
        self._validator = validator
        self.commutative = commutative
            
    def compute(self, a, b):
        return self._computator(a,b)
    
    def validate(self, a, b):
        return self._validator(a,b)


class OperationInstance:
    
    def __init__(self, operation, o1, o2, result ):
        self.operation = operation
        self.operand1 = o1
        self.operand2 = o2
        self.result = result
        
    def __repr__(self):
        return """%s%s%s=%s""" \
            %(str(self.operand1), self.operation.symbol, str(self.operand2), \
                str(self.result))
    

def operations():
    
    def mul(a,b): return a*b    
    def mulCheck(a,b): return True 
    
    def div(a,b): return a/b
    def divCheck(a,b): return a > b and a % b == 0 and b!=0
        
    def add(a,b): return a+b
    def addCheck(a,b): return True
        
    def sub(a,b): return a-b
    def subCheck(a,b): return a>b
    
    return [
        Operation("*", True, mul, mulCheck),
        Operation("/", False, div, divCheck),
        Operation("+", True, add, addCheck),
        Operation("-", False, sub, subCheck)
    ]


class Solver:
    
    def __init__(self, problem):
        self._problem = problem
        self._ops = operations()

        
    def solve(self, options):
    
        init_state = State(self._problem, list(self._problem.values),[])
        self._states = DequeEx(True)
        self._states.append( init_state)
        
        while (len(self._states) != 0):
            
            cur_state = self._states.popleft()
            
            if (cur_state.is_solved()):
                return cur_state.operations
                
            alt_states = self._combinate(cur_state, options)
            self._states.extend(alt_states)
        
        return None                


    def _combinate(self, state, options):
        
        newStates = []
         
        for i in range(len(state.values)):
            for j in range(len(state.values)):
                if i==j:
                    continue
                op1 = state.values[i]
                op2 = state.values[j]
                for o in self._ops:
                    
                    if options['optCommutative'] == True and o.commutative and i > j:
                        continue
                    if o.validate(op1, op2) == False:
                        continue
                    
                    r = o.compute(op1, op2)
            
                    newValues = [state.values[k] 
                                 for k in range(len(state.values)) 
                                 if i != k and j != k]
                    newValues.append(r)
                    
                    newOperations = []
                    newOperations.extend(state.operations)
                    newOperations.append(OperationInstance(o, op1, op2, r))   
                        
                    newState = State(state.problem, newValues, newOperations)            
                    newStates.append(newState)        
        
        return newStates


p1 = Problem( [1,4,6,10,25,75], 911 )
solver = Solver(p1)
solution  = solver.solve( {'optCommutative':True} )
print(solution)
