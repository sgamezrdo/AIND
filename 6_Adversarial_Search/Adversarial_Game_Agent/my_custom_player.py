from sample_players import DataPlayer
from sample_players import BasePlayer
import random

W, H = 11, 9
#get the weights for the x axis
#the best positions is in the middle
w_list = [i for i in range(int(W/2))]
w_list_weights = [i*0.2 for i in w_list]
all_w_weights =  w_list_weights + [1.] + w_list_weights[::-1]
#get the weights for the y axis
#the best positions is in the middle
h_list = [i for i in range(int(H/2))]
h_list_weights = [i*0.2 for i in h_list]
all_h_weights =  h_list_weights + [1.] + h_list_weights[::-1]

class CustomPlayer(DataPlayer):
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only required method for this project.
    You can modify the interface for get_action by adding named parameters
    with default values, but the function MUST remain compatible with the
    default interface.

    **********************************************************************
    NOTES:
    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.

    - You can pass state forward to your agent on the next turn by assigning
      any pickleable object to the self.context attribute.
    **********************************************************************
    """
    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller will be responsible
        for cutting off the function after the search time limit has expired.

        See RandomPlayer and GreedyPlayer in sample_players for more examples.

        **********************************************************************
        NOTE: 
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        # TODO: Replace the example implementation below with your own search
        #       method by combining techniques from lecture
        #
        # EXAMPLE: choose a random move without any search--this function MUST
        #          call self.queue.put(ACTION) at least once before time expires
        #          (the timer is automatically managed for you)
                # randomly select a move as player 1 or 2 on an empty board, otherwise
        # return the optimal minimax move at a fixed search depth of 3 plies
        if state.ply_count < 2:
            self.queue.put(random.choice(state.actions()))
        else:
            self.queue.put(self.alpha_beta_search(state))
            

    def alpha_beta_search(self, gameState, depth=3):
        """ Return the move along a branch of the game tree that
        has the best possible value.  A move is a pair of coordinates
        in (column, row) order corresponding to a legal move for
        the searching player.
        
        You can ignore the special case of calling this function
        from a terminal state.
        """
     
        
        def min_value(gameState, alpha, beta, depth):
            """ Return the value for a win (+1) if the game is over,
            otherwise return the minimum value over all legal child
            nodes.
            """
            if gameState.terminal_test(): 
                return gameState.utility(self.player_id)
            if depth <= 0: 
                return self.score(gameState)

            v = float("inf")
            for a in gameState.actions():
                v = min(v, max_value(gameState.result(a), alpha, beta, depth - 1))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v

        def max_value(gameState, alpha, beta, depth):
            """ Return the value for a loss (-1) if the game is over,
            otherwise return the maximum value over all legal child
            nodes.
            """
            if gameState.terminal_test(): 
                return gameState.utility(self.player_id)
            if depth <= 0: 
                return self.score(gameState)

            v = float("-inf")
            for a in gameState.actions():
                v = max(v, min_value(gameState.result(a), alpha, beta, depth - 1))
                #print(v)
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v
        
        alpha = float("-inf")
        beta = float("inf")
        best_score = float("-inf")
        best_move = None
        for a in gameState.actions():
            #print(a)
            v = min_value(gameState.result(a), alpha, beta, depth - 1)
            alpha = max(alpha, v)
            if v >= best_score:
                best_score = v
                best_move = a
        return best_move

    def score_base(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - len(opp_liberties)
    
    
    
    def score_positional(self, state):
        own_loc = state.locs[self.player_id]
        #get positions
        x_pos, y_pos = ind2xy(own_loc)
        #return the positional score
        return position_score(x_pos, y_pos)
        
    def avg_positional_score_opp(self, state):
        opp_loc = state.locs[1 - self.player_id]
        opp_liberties = state.liberties(opp_loc)
        opp_pos_scores = [position_score(*ind2xy(libert)) for libert in opp_liberties]
        return -1. * sum(opp_pos_scores) / len(opp_pos_scores)

        
    def score(self, state):
        return self.score_base(state)  #+ 0.25*self.score_positional(state) #+ 0.1*self.avg_positional_score_opp(state)

def position_score(x_pos, y_pos):
    return 0.5*all_w_weights[x_pos] + 0.5*all_h_weights[y_pos]
    
def ind2xy(loc):
    """ Convert from board index value to xy coordinates
    """
    return (loc % (W + 2), loc // (W + 2))
    
   