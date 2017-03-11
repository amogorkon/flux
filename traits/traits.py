
class Trait:
    def visit(self, obj):
        obj.do()
        
class foo(Trait):
    pass

class bar(Trait):
    pass

class baz(Trait):
    pass