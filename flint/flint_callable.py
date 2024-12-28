from abc import ABC, abstractmethod
import time

class FlintCallable(ABC):
    
    @abstractmethod
    def arity(self) -> int:
        """
        Returns the number of arguments the callable expects
        """
        pass
    
    @abstractmethod
    def call(self, interpreter, arguments) -> object:
        """
        Excutes the callable with the given interpreter and arguments
        """
        pass
    
    
    @abstractmethod
    def to_string(self) -> str:
        """
        Returns the string representation of the callable
        """
        pass
    
    
#############################
# Native functions in Flint #
#############################

class ClockCallable(FlintCallable):
    def arity(self):
        return 0
    
    def call(self, interpreter, arguments):
        current_time = time.time()  # Returns time in seconds since the epoch
        return current_time
    
    def to_string(self):
        return "<native fn>"

