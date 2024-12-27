from abc import ABC, abstractmethod

class FlintCallable:
    
    @abstractmethod
    def arity(self) -> int:
        """
        Returns the number of arguments the callable expects
        """
        pass
    
    @abstractmethod
    def call(self, interpreter, arguments):
        """
        Excutes the callable with the given interpreter and arguments
        """
        pass
