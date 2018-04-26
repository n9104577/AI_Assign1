# -*- coding: utf-8 -*-
"""
Created on  Feb 27 2018

@author: frederic

Scaffholding code for CAB320 Assignment One

This is the only file that you have to modify and submit for the assignment.

"""

import numpy as np

import itertools

import generic_search as gs

from assignment_one import (TetrisPart, AssemblyProblem, offset_range, display_state, 
                            make_state_canonical, play_solution, 
                            load_state, make_random_state
                            )

# ---------------------------------------------------------------------------

def print_the_team():
    '''
    Print details of the members of your team 
    (full name + student number)
    '''
    
    raise NotImplementedError

#    print('Jake Carmock, 12340001')
#    print('Kallum Strachan, 9703748')

    
# ---------------------------------------------------------------------------
        
def appear_as_subpart(some_part, goal_part):
    '''    
    Determine whether the part 'some_part' appears in another part 'goal_part'.
    
    Formally, we say that 'some_part' appears in another part 'goal_part',
    when the matrix representation 'S' of 'some_part' is a a submatrix 'M' of
    the matrix representation 'G' of 'goal_part' and the following constraints
    are satisfied:
        for all indices i,j
            S[i,j] == 0 or S[i,j] == M[i,j]
            
    During an assembly sequence that does not use rotations, any part present 
    on the workbench has to appear somewhere in a goal part!
    
    @param
        some_part: a tuple representation of a tetris part
        goal_part: a tuple representation of another tetris part
        
    @return
        True if 'some_part' appears in 'goal_part'
        False otherwise    
    '''
   
    # turn the parts into numpy arrays
    some_array = np.array(some_part)
    goal_array = np.array(goal_part)
   
    # get the shape/size of the arrays
    #Height [0] by width [1]    
    some_size = some_array.shape
    goal_size = goal_array.shape
    
    # make sure the goal array is valid
    if(len(goal_size) > 1):
        
        # check to see if the part is smaller than the goal else 
        # there is no point checking
        if some_size[0] <= goal_size[0] and some_size[1] <= goal_size[1]:        
            
            # iterate through the goal part array
            for i in range(0, goal_size[0]):            
                for j in range(0, goal_size[1]-1):    
                    
                    # check if the first one or two values of the part array match the goal array
                    if((some_size[1] == 1 and some_array[0][0] == goal_array[i][j]) or some_array[0][0] == goal_array[i][j] and some_array[0][1] == goal_array[i][j+1]):
                        
                        # if it does pull a slice of the goal array
                        temp = goal_array[i:i+some_size[0], j:j+some_size[1]]     
                        temp = np.array(temp)  
                        
                        # just make sure theyre the same size
                        if temp.size == some_array.size:
                            
                            # pull the zeros from the part array
                            rows,cols = np.where(some_array == 0)   

                            # Then for each location in part array where there is a zero
                            # replace the corresponding value in the temp array with a zero                                        
                            for k in range(0,len(rows)):                            
                                temp.itemset((rows[k],cols[k]), 0)
                                
                                # check the two arrays are equal if so return true else repeat 
                                if np.array_equal(some_array, temp):       
                                    return True                                           
    return False
                
                    
        
    #    a = np.array(some_part)  # HINT


# ---------------------------------------------------------------------------
        
def cost_rotated_subpart(some_part, goal_part):
    '''    
    Determine whether the part 'some_part' appears in another part 'goal_part'
    as a rotated subpart. If yes, return the number of 'rotate90' needed, if 
    no return 'np.inf'
    
    The definition of appearance is the same as in the function 
    'appear_as_subpart'.
                   
    @param
        some_part: a tuple representation of a tetris part
        goal_part: a tuple representation of another tetris part
    
    @return
        the number of rotation needed to see 'some_part' appear in 'goal_part'
        np.inf  if no rotated version of 'some_part' appear in 'goal_part'
    
    '''
    # variable to count number of rotations
    numRotation = 0

    # only 3 rotations for a full 
    some_part_piece = TetrisPart(some_part)
    for i in range(0,4):
        
        # check if some_part appears in goal_part
        if(appear_as_subpart(some_part, goal_part)):
            
            # if yes return roations else rotate the part 90 degrees and check again
            
            return numRotation
        else:
            some_part_piece.rotate90()
            some_part = some_part_piece.get_frozen()
            
            numRotation = numRotation + 1
                
    
    return np.inf
    
    
# ---------------------------------------------------------------------------

class AssemblyProblem_1(AssemblyProblem):
    '''
    
    Subclass of 'assignment_one.AssemblyProblem'
    
    * The part rotation action is not available for AssemblyProblem_1 *

    The 'actions' method of this class simply generates
    the list of all legal actions. The 'actions' method of this class does 
    *NOT* filtered out actions that are doomed to fail. In other words, 
    no pruning is done in the 'actions' method of this class.
        
    '''

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal.  Your subclass's constructor can add
        other arguments."""
        # Call the parent class constructor.
        # Here the parent class is 'AssemblyProblem' 
        # which itself is derived from 'generic_search.Problem'
        super(AssemblyProblem_1, self).__init__(initial, goal, use_rotation=False)
    
    def actions(self, state):
        """
        Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once.
        
        @param
          state : a state of an assembly problem.
        
        @return 
           the list of all legal drop actions available in the 
            state passed as argument.
        
        """
        #
        actions = []        
        part_list = list(state)
        
        # get the number of different combinations
        options = list(itertools.permutations(part_list))
        
        # for each combination get the part above and part under
        for opt in options:
            
            if(len(opt) <= 1):
                return actions
            
            pa = opt[0]
            pu = opt[1]
            
            
            # get the offset range for that combo
            range1 = offset_range(pa,pu)
            
            # then get every append every range to that combo 
            for offset in range(range1[0], range1[1]):
                actions.append((pa, pu, offset))       

#        print("actions")
#        print(np.array(actions))
        #print()
        return list(actions)


    def result(self, state, action):
        """
        Return the state (as a tuple of parts in canonical order)
        that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).
        
        @return
          a state in canonical order
        
        """
        # Here a workbench state is a frozenset of parts        
 
        part_list = list(state)
        
        # pa, pu, offset = action # HINT
        # get each variable from action
        pa, pu, offset = action
        
        # remove pa and pu from the part list(state) to free it up
        part_list.remove(pa)
        part_list.remove(pu)        
        
        # create a new tetris part out of the variables from actions
        # turn it to a tuple of tuples using .get_frozen()
        tetrisPart = TetrisPart(pa, pu, offset).get_frozen()
        
        # append it back to the part_list and return it as a canonical state
        part_list.append(tuple(tetrisPart))
        state = make_state_canonical(part_list)
        #display_state(state)
        
        return state
       

# ---------------------------------------------------------------------------

class AssemblyProblem_2(AssemblyProblem_1):
    '''
    
    Subclass of 'assignment_one.AssemblyProblem'
        
    * Like for AssemblyProblem_1,  the part rotation action is not available 
       for AssemblyProblem_2 *

    The 'actions' method of this class  generates a list of legal actions. 
    But pruning is performed by detecting some doomed actions and 
    filtering them out.  That is, some actions that are doomed to 
    fail are not returned. In this class, pruning is performed while 
    generating the legal actions.
    However, if an action 'a' is not doomed to fail, it has to be returned. 
    In other words, if there exists a sequence of actions solution starting 
    with 'a', then 'a' has to be returned.
        
    '''

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal.  Your subclass's constructor can add
        other arguments."""
        # Call the parent class constructor.
        # Here the parent class is 'AssemblyProblem' 
        # which itself is derived from 'generic_search.Problem'
        super(AssemblyProblem_2, self).__init__(initial, goal)
    
    def actions(self, state):
        """
        Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once.
        
        A candidate action is eliminated if and only if the new part 
        it creates does not appear in the goal state.
        """
        #

        actions = []
        part_list = list(state)
        
        # make sure the goal state is the right format for appear_as_subpart
        goal = self.goal
        goal_array = np.array(goal)
        
        # reshape it 
        goal_size = goal_array.shape
        
        #check the size is valid if it is make sure its not to big
        # and assign it to be the goal_array
        if(len(goal_size) > 1):
            new_goal = np.reshape(goal_array,[goal_size[1],goal_size[2]])
            new_goal_size = new_goal.shape
            goal_size = new_goal_size
            goal_array = np.array(new_goal)
        
        
        
   
        # get every combo
        options = list(itertools.permutations(part_list))
        for opt in options:
            if(len(opt) <= 1):
                return actions
            
            pa = opt[0]
            pu = opt[1]
            
            # get the range of offset for the two parts
            range1 = offset_range(pa,pu)
            for offset in range(range1[0], range1[1]):
                
                # create a tetris part and check it appears in the goal_array
                # if it does append it to the actions list else skip it
                tetrisPart = TetrisPart(pa, pu, offset).get_frozen()
                if(appear_as_subpart(tetrisPart, goal_array)):
                    actions.append((pa, pu, offset))       

#        print("actions")
#        print(np.array(actions))
#        print()
        return list(actions)


# ---------------------------------------------------------------------------

class AssemblyProblem_3(AssemblyProblem_1):
    '''
    
    Subclass 'assignment_one.AssemblyProblem'
    
    * The part rotation action is available for AssemblyProblem_3 *

    The 'actions' method of this class simply generates
    the list of all legal actions including rotation. 
    The 'actions' method of this class does 
    *NOT* filter out actions that are doomed to fail. In other words, 
    no pruning is done in this method.
        
    '''

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal.  Your subclass's constructor can add
        other arguments."""
        # Call the parent class constructor.
        # Here the parent class is 'AssemblyProblem' 
        # which itself is derived from 'generic_search.Problem'
        super(AssemblyProblem_3, self).__init__(initial, goal)
        self.use_rotation = True

    
    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once.
        
        Rotations are allowed, but no filtering out the actions that 
        lead to doomed states.
        
        """
        #
#
        actions = []
        
        part_list = list(state)
        
        options = list(itertools.permutations(part_list))
                
        for opt in options:
            
            if(len(opt) <= 1):
                return actions
            
            pa = opt[0]
            pu = opt[1]            
            
            pa_rotate = TetrisPart(pa)            
            pu_rotate = TetrisPart(pu)
            
            range1 = offset_range(pa,pu)
           
            for offset in range(range1[0], range1[1]):             
                for rotations in range(0,4):
                    pa_rotate.rotate90()                    
                    pa = pa_rotate.get_frozen()
                    
                    for rotationsPu in range(0,4):
                        pu_rotate.rotate90()
                        pu = pu_rotate.get_frozen()     
                        actions.append((pa, pu, offset))  
#            
                     

#        print("actions")
#        actions.append((pa, None, None))
        
        

#        print(np.array(actions))
#        print()
        return list(actions)

        

        
    def result(self, state, action):
        """
        Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).

        The action can be a drop or rotation.        
        """
        # Here a workbench state is a frozenset of parts        
 
        part_list = list(state)
        
        # pa, pu, offset = action # HINT
        # get each variable from action
        pa, pu, offset = action
               
        # find the rotated piece is the state and remove it
        piece_list = [pa, pu]        
        for p in piece_list:
            removed = False
            tetris_p = TetrisPart(p)
            for i in range(0, 4):
                tetris_p.rotate90()
                tetris_frozen = tetris_p.get_frozen()
                for part in part_list:
                    np_tetris = np.array(tetris_frozen)
                    np_part = np.array(part)
                    if(np.array_equal(np_tetris, np_part)):                        
                        part_list.remove(tetris_frozen)
                        
                        removed = True
                        break
                    if(removed == True):
                        break
                if(removed == True):
                    break
   
        
        # create a new tetris part out of the variables from actions
        # turn it to a tuple of tuples using .get_frozen()
        tetrisPart = TetrisPart(pa, pu, offset).get_frozen()
        
        # append it back to the part_list and return it as a canonical state
        part_list.append(tuple(tetrisPart))
        state = make_state_canonical(part_list)
        
#        print("display state")
#        display_state(state)
        
       
        
        return state


# ---------------------------------------------------------------------------

class AssemblyProblem_4(AssemblyProblem_3):
    '''
    
    Subclass 'assignment_one.AssemblyProblem3'
    
    * Like for its parent class AssemblyProblem_3, 
      the part rotation action is available for AssemblyProblem_4  *

    AssemblyProblem_4 introduces a simple heuristic function and uses
    action filtering.
    See the details in the methods 'self.actions()' and 'self.h()'.
    
    '''

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal.  Your subclass's constructor can add
        other arguments."""
        # Call the parent class constructor.
        # Here the parent class is 'AssemblyProblem' 
        # which itself is derived from 'generic_search.Problem'
        super(AssemblyProblem_4, self).__init__(initial, goal)

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once.
        
        Filter out actions (drops and rotations) that are doomed to fail 
        using the function 'cost_rotated_subpart'.
        A candidate action is eliminated if and only if the new part 
        it creates does not appear in the goal state.
        This should  be checked with the function "cost_rotated_subpart()'.
                
        """


        actions = []
        
        # make sure the goal state is the right format for appear_as_subpart
        goal = self.goal
        goal_array = np.array(goal)
        
        # reshape it 
        goal_size = goal_array.shape
        
        #check the size is valid if it is make sure its not to big
        # and assign it to be the goal_array
        if(len(goal_size) > 1):
            new_goal = np.reshape(goal_array,[goal_size[1],goal_size[2]])
            new_goal_size = new_goal.shape
            goal_size = new_goal_size
            goal_array = np.array(new_goal)
            
        part_list = list(state)
        
        options = list(itertools.permutations(part_list))
                
        for opt in options:
            
            if(len(opt) <= 1):
                return actions
            
            pa = opt[0]
            pu = opt[1]            
            
            pa_rotate = TetrisPart(pa)            
            pu_rotate = TetrisPart(pu)
            
            range1 = offset_range(pa,pu)
           
            for offset in range(range1[0], range1[1]):             
                for rotations in range(0,4):
                    pa_rotate.rotate90()                    
                    pa = pa_rotate.get_frozen()
                    
                    for rotationsPu in range(0,4):
                        pu_rotate.rotate90()
                        pu = pu_rotate.get_frozen()   
                        
                        tetrisPart = TetrisPart(pa, pu, offset).get_frozen()
                        if(cost_rotated_subpart(tetrisPart, goal_array) != np.inf):
                              actions.append((pa, pu, offset))

        

        print(np.array(actions))
#        print()
        return list(actions)
        
        
        
    def h(self, n):
        '''
        This heuristic computes the following cost; 
        
           Let 'k_n' be the number of parts of the state associated to node 'n'
           and 'k_g' be the number of parts of the goal state.
          
        The cost function h(n) must return 
            k_n - k_g + max ("cost of the rotations")  
        where the list of cost of the rotations is computed over the parts in 
        the state 'n.state' according to 'cost_rotated_subpart'.
        
        
        @param
          n : node of a search tree
          
        '''
        k_n = 0
        k_g = 0
        return k_n-k_g + 1
        

# ---------------------------------------------------------------------------
        
def solve_1(initial, goal):
    '''
    Solve a problem of type AssemblyProblem_1
    
    The implementation has to 
    - use an instance of the class AssemblyProblem_1
    - make a call to an appropriate functions of the 'generic_search" library
    
    @return
        - the string 'no solution' if the problem is not solvable
        - otherwise return the sequence of actions to go from state
        'initial' to state 'goal'
    
    '''

    print('\n++  busy searching in solve_1() ...  ++\n')
    
    assembly_problem = AssemblyProblem_1(initial, goal) # HINT
    sol = gs.depth_first_graph_search(assembly_problem)
  
    if(sol == None):
        print("no solution")
        return "no solution"
    else:
        print("solutino")
        print(sol.solution()) 
        return sol.solution()

# ---------------------------------------------------------------------------
        
def solve_2(initial, goal):
    '''
    Solve a problem of type AssemblyProblem_2
    
    The implementation has to 
    - use an instance of the class AssemblyProblem_2
    - make a call to an appropriate functions of the 'generic_search" library
    
    @return
        - the string 'no solution' if the problem is not solvable
        - otherwise return the sequence of actions to go from state
        'initial' to state 'goal'
    
    '''

    print('\n++  busy searching in solve_2() ...  ++\n')
    assembly_problem = AssemblyProblem_2(initial, goal) # HINT
    sol = gs.depth_first_graph_search(assembly_problem)
  
    if(sol == None):
        print("no solution")
        return "no solution"
    else:
        
        print(sol.solution()) 
        return sol.solution()
    

# ---------------------------------------------------------------------------
        
def solve_3(initial, goal):
    '''
    Solve a problem of type AssemblyProblem_3
    
    The implementation has to 
    - use an instance of the class AssemblyProblem_3
    - make a call to an appropriate functions of the 'generic_search" library
    
    @return
        - the string 'no solution' if the problem is not solvable
        - otherwise return the sequence of actions to go from state
        'initial' to state 'goal'
    
    '''

    print('\n++  busy searching in solve_3() ...  ++\n')
    assembly_problem = AssemblyProblem_3(initial, goal) # HINT
    
    sol = gs.depth_first_graph_search(assembly_problem)
  
    if(sol == None):
        print("no solution")
        return "no solution"
    else:
        print("solution")
        print(sol.solution()) 
        return sol.solution()
    
# ---------------------------------------------------------------------------
        
def solve_4(initial, goal):
    '''
    Solve a problem of type AssemblyProblem_4
    
    The implementation has to 
    - use an instance of the class AssemblyProblem_4
    - make a call to an appropriate functions of the 'generic_search" library
    
    @return
        - the string 'no solution' if the problem is not solvable
        - otherwise return the sequence of actions to go from state
        'initial' to state 'goal'
    
    '''

    #         raise NotImplementedError
    print('\n++  busy searching in solve_4() ...  ++\n')
    assembly_problem = AssemblyProblem_4(initial, goal) # HINT
    sol = gs.astar_graph_search(assembly_problem, assembly_problem.h(0))
    
    if(sol == None):
        print("no solution")
        return "no solution"
    else:
        print("solution")
        print(sol.solution()) 
        return sol.solution()
# ---------------------------------------------------------------------------


    
if __name__ == '__main__':
    pass
    
