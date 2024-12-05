class Pastry:
    def accept(self, visitor):
        """Route to the correct method in the visitor."""
        raise NotImplementedError("Subclasses must implement this method.")


class Beignet(Pastry):
    def accept(self, visitor):
        visitor.visit_beignet(self)

class Cruller(Pastry):
    def accept(self, visitor):
        visitor.visit_cruller(self)

class PastryVisitor:
    def visit_beignet(self, beignet):
        raise NotImplementedError("Subclasses must implement this method.")
    
    def visit_cruller(self, cruller):
        raise NotImplementedError("Subclasses must implement this method.")

class CookVisitor(PastryVisitor):
    def visit_beignet(self, beignet):
        print("Cooking a beignet!")

    def visit_cruller(self, cruller):
        print("Cooking a cruller!")

beignet = Beignet()
cruller = Cruller()

cook_visitor = CookVisitor()

# The accept method calls the correct visitor method dynamically.
beignet.accept(cook_visitor)  # Output: Cooking a beignet!
cruller.accept(cook_visitor)  # Output: Cooking a cruller!
