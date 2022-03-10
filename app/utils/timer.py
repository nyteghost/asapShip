from threading import Timer 


class LoopStopper: 
 
    def __init__(self, seconds): 
        self._loop_stop = False 
        self._seconds = seconds 

    def _stop_loop(self): 
        self._loop_stop = True 

    def run( self, generator_expression, task): 
        """ Execute a task a number of times based on the generator_expression""" 
        t = Timer(self._seconds, self._stop_loop) 
        t.start() 
        for i in generator_expression: 
            task(i) 
            if self._loop_stop: 
                break 
        t.cancel() # Cancel the timer if the loop ends ok. 
 
ls = LoopStopper( 5) # 5 second timeout 
ls.run( range(1000000), print) # print numbers from 0 to 999999 