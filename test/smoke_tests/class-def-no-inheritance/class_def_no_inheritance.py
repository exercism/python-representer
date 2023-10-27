class Bar: pass

class Foo(Bar):
    '''
    Docstrings are ignored.
    '''
    class_attr = 2

    def method(self, posarg, defarg=None, *varargs, **nameargs):
        '''
        Docstrings are ignored.
        '''
        # comments are ignored
        self.instance_attr = self.class_attr + 2 # not self is preserved
