import unittest
from textwrap import dedent
from representer import Representer
from representer.utils import reformat


class RepresenterNormalizationTest(unittest.TestCase):
    def normalize_code(self, source: str) -> str:
        """
        Normalize source to generated code.
        """
        representer = Representer(source)
        print("\n\n")
        print(representer.dump_tree())
        representer.normalize()
        print(representer.dump_tree())

        return representer.dump_code()

    def assertCodeEqual(self, first, second, msg=None):
        """
        Assert that the pieces of code are equal, after formatting.
        """
        received = self.normalize_code(dedent(first))
        expected = reformat(dedent(second))
        self.assertEqual(received, expected, msg)

    def test_module_empty(self):
        before = ""
        expect = before
        self.assertCodeEqual(before, expect)

    def test_module_comments_ignored(self):
        before = """\
                # comment
                # comment
                """
        expect = ""
        self.assertCodeEqual(before, expect)

    def test_module_docstring_ignored(self):
        before = '''\
                """
                Module level docstring
                """
                '''
        expect = ""
        self.assertCodeEqual(before, expect)

    def test_import(self):
        before = """\
                import mod
                import moda, modb
                mod.name + modea.namea / modeb.nameb
                """
        expect = before
        self.assertCodeEqual(before, expect)

    def test_import_as(self):
        before = """\
                import mod as name
                import moda as namea, modb as nameb
                name + namea / nameb
                """
        expect = """\
                import mod as PLACEHOLDER_0
                import moda as PLACEHOLDER_1, modb as PLACEHOLDER_2
                PLACEHOLDER_0 + PLACEHOLDER_1 / PLACEHOLDER_2
                """
        self.assertCodeEqual(before, expect)

    def test_from_import(self):
        before = """\
                from mod import name
                from modb import namea, nameb
                name + namea / nameb
                """
        expect = before
        self.assertCodeEqual(before, expect)

    def test_from_import_star(self):
        before = """\
                from mod import *
                print(star_name)
                print(star_name.attribute)
                """
        expect = before
        self.assertCodeEqual(before, expect)

    def test_from_import_as(self):
        before = """\
                from mod import name as aname
                from modb import namea as anamea, nameb as anameb
                aname + anamea / anameb
                """
        expect = """\
                from mod import name as PLACEHOLDER_0
                from modb import namea as PLACEHOLDER_1, nameb as PLACEHOLDER_2
                PLACEHOLDER_0 + PLACEHOLDER_1 / PLACEHOLDER_2
                """
        self.assertCodeEqual(before, expect)

    def test_with(self):
        before = """\
                with open("file.txt", "r"):
                    pass
                """
        expect = before
        self.assertCodeEqual(before, expect)

    def test_with_as(self):
        before = """\
                with open("in", "r") as src, open("out", "w") as dst:
                    dst.write(src.read())
                """
        expect = """\
                with open("in", "r") as PLACEHOLDER_0, open("out", "w") as PLACEHOLDER_1:
                    PLACEHOLDER_1.write(PLACEHOLDER_0.read())
                """
        self.assertCodeEqual(before, expect)

    def test_try_except(self):
        before = """\
                try:
                    raise TypeError from ValueError("foo")
                except (TypeError, ValueError):
                    sys.exit(2)
                else:
                    sys.exit(0)
                finally:
                    sys.exit(1)
                """
        expect = before
        self.assertCodeEqual(before, expect)

    def test_try_except_as(self):
        before = """\
                try:
                    raise TypeError from ValueError("foo")
                except (TypeError, ValueError) as err:
                    print(err)
                    sys.exit(2)
                else:
                    sys.exit(0)
                finally:
                    sys.exit(1)
                """
        expect = """\
                try:
                    raise TypeError from ValueError("foo")
                except (TypeError, ValueError) as PLACEHOLDER_0:
                    print(PLACEHOLDER_0)
                    sys.exit(2)
                else:
                    sys.exit(0)
                finally:
                    sys.exit(1)
                """
        self.assertCodeEqual(before, expect)

    def test_with_list_comprehension(self):
        before = "[i + 1 for i in range(5) if not i % 2]"
        expect = (
            "[(PLACEHOLDER_0 + 1) for PLACEHOLDER_0 in range(5)"
            "if not PLACEHOLDER_0 % 2]"
        )
        self.assertCodeEqual(before, expect)

    def test_with_set_comprehension(self):
        before = "{i + 1 for i in range(5) if not i % 2}"
        expect = (
            "{(PLACEHOLDER_0 + 1) for PLACEHOLDER_0 in range(5)"
            "if not PLACEHOLDER_0 % 2}"
        )
        self.assertCodeEqual(before, expect)

    def test_with_generator_comprehension(self):
        before = "(i + 1 for i in range(5) if not i % 2)"
        expect = (
            "(PLACEHOLDER_0 + 1 for PLACEHOLDER_0 in range(5)"
            "if not PLACEHOLDER_0 % 2)"
        )
        self.assertCodeEqual(before, expect)

    def test_with_dict_comprehension(self):
        before = "{k: None for k in range(5) if not k % 2}"
        expect = (
            "{PLACEHOLDER_0 : None for PLACEHOLDER_0 in range(5)"
            "if not PLACEHOLDER_0 % 2}"
        )
        self.assertCodeEqual(before, expect)

    def test_with_list_compound_comprehension(self):
        before = "[i + n for i in range(5) for n in range(5) if not i % 2]"
        expect = (
            "[(PLACEHOLDER_0 + PLACEHOLDER_1) for PLACEHOLDER_0 in range(5)"
            "for PLACEHOLDER_1 in range(5) if not PLACEHOLDER_0 % 2]"
        )
        self.assertCodeEqual(before, expect)

    def test_with_set_compound_comprehension(self):
        before = "{i + n for i in range(5) for n in range(5) if not i % 2}"
        expect = (
            "{(PLACEHOLDER_0 + PLACEHOLDER_1) for PLACEHOLDER_0 in range(5)"
            "for PLACEHOLDER_1 in range(5) if not PLACEHOLDER_0 % 2}"
        )
        self.assertCodeEqual(before, expect)

    def test_with_generator_compound_comprehension(self):
        before = "(i + n for i in range(5) for n in range(5) if not i % 2)"
        expect = (
            "(PLACEHOLDER_0 + PLACEHOLDER_1 for PLACEHOLDER_0 in range(5)"
            "for PLACEHOLDER_1 in range(5) if not PLACEHOLDER_0 % 2)"
        )
        self.assertCodeEqual(before, expect)

    def test_with_dict_compound_comprehension(self):
        before = "{k: v for k in range(5) for v in range(5) if not k % 2}"
        expect = (
            "{PLACEHOLDER_0 : PLACEHOLDER_1 for PLACEHOLDER_0 in range(5)"
            "for PLACEHOLDER_1 in range(5) if not PLACEHOLDER_0 % 2}"
        )
        self.assertCodeEqual(before, expect)

    def test_for_loop(self):
        before = """\
                for name in range(21):
                    print(name + 1)
                """
        expect = """\
                for PLACEHOLDER_0 in range(21):
                    print(PLACEHOLDER_0 + 1)
                """
        self.assertCodeEqual(before, expect)

    def test_for_loop_with_expansion(self):
        before = """\
                for idx, item in enumerate(range(21)):
                    print(idx, item)
                """
        expect = """\
                for PLACEHOLDER_0, PLACEHOLDER_1 in enumerate(range(21)):
                    print(PLACEHOLDER_0, PLACEHOLDER_1)
                """
        self.assertCodeEqual(before, expect)

    def test_i_am_the_walrus(self):
        before = """\
                while name := True:
                    print(name)
                """
        expect = """\
                while (PLACEHOLDER_0 := True):
                    print(PLACEHOLDER_0)
                """
        self.assertCodeEqual(before, expect)

    def test_simple_assignment(self):
        before = """\
                x = 10
                y = x + 10
                x = x + y
                x, y = y, x
                """
        expect = """\
                PLACEHOLDER_0 = 10
                PLACEHOLDER_1 = PLACEHOLDER_0 + 10
                PLACEHOLDER_0 = PLACEHOLDER_0 + PLACEHOLDER_1
                PLACEHOLDER_0, PLACEHOLDER_1 = PLACEHOLDER_1, PLACEHOLDER_0
                """
        self.assertCodeEqual(before, expect)

    def test_augmented_assignment(self):
        before = """\
                x = 10
                y = x + 10
                x += y
                y *= 0
                """
        expect = """\
                PLACEHOLDER_0 = 10
                PLACEHOLDER_1 = PLACEHOLDER_0 + 10
                PLACEHOLDER_0 += PLACEHOLDER_1
                PLACEHOLDER_1 *= 0
                """
        self.assertCodeEqual(before, expect)

    def test_def_functions(self):
        before = """\
                def func(posarg, defarg=None, *varargs, **nameargs):
                    '''
                    Docstrings are ignored.
                    '''
                    # comments are ignored
                    with func() as name:
                        for item in name:
                            print(item)
                    return item
                """
        expect = """\
                def PLACEHOLDER_0(PLACEHOLDER_1, PLACEHOLDER_2=None, 
                                  *PLACEHOLDER_3, **PLACEHOLDER_4):
                    with PLACEHOLDER_0() as PLACEHOLDER_5:
                        for PLACEHOLDER_6 in PLACEHOLDER_5:
                            print(PLACEHOLDER_6)
                    return PLACEHOLDER_6
                """
        self.assertCodeEqual(before, expect)

    def test_async_def_functions(self):
        before = """\
                async def afunc(posarg, defarg=None, *varargs, **nameargs):
                    '''
                    Docstrings are ignored
                    '''
                    # comments are ignored
                    async with afunc() as aname:
                        async for item in aname:
                            print(item)
                    await afunc()
                """
        expect = """\
                async def PLACEHOLDER_0(PLACEHOLDER_1, PLACEHOLDER_2=None, 
                                        *PLACEHOLDER_3, **PLACEHOLDER_4):
                    async with PLACEHOLDER_0() as PLACEHOLDER_5:
                        async for PLACEHOLDER_6 in PLACEHOLDER_5:
                            print(PLACEHOLDER_6)
                    await PLACEHOLDER_0()
                """
        self.assertCodeEqual(before, expect)


    def test_class_def_no_inheritance(self):
        before = """\
                class Foo:
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
                """
        expect = """\
                 class PLACEHOLDER_0:
                     PLACEHOLDER_1 = 2
                
                     def PLACEHOLDER_2(
                         self, PLACEHOLDER_3, PLACEHOLDER_4=None, *PLACEHOLDER_5, **PLACEHOLDER_6
                     ):
                         self.PLACEHOLDER_7 = self.PLACEHOLDER_1 + 2
                """
        self.assertCodeEqual(before, expect)


    def test_class_def_no_inheritance(self):
        before = """\
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
                """
        expect = """\
                class PLACEHOLDER_0: pass

                class PLACEHOLDER_1(PLACEHOLDER_0):
                    PLACEHOLDER_2 = 2
                
                    def PLACEHOLDER_3(
                        self, PLACEHOLDER_4, PLACEHOLDER_5=None, *PLACEHOLDER_6, **PLACEHOLDER_7
                    ):
                        self.PLACEHOLDER_8 = self.PLACEHOLDER_2 + 2
                """
        self.assertCodeEqual(before, expect)

    @unittest.skip("TODO: HANDLE METACLASS ASSIGNMENT")
    def test_class_with_metaclass(self):
        before = """\
                from abc import ABCMeta

                class MyABC(metaclass=ABCMeta):
                    pass
                """
        expect = """\
                from abc import ABCMeta

                class PLACEHOLDER_0(metaclass=ABCMeta):
                    pass
                """
        self.assertCodeEqual(before, expect)


if __name__ == "__main__":
    unittest.main()
