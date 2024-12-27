import unittest

from errors import Err, guarded


class ErrTestCase(unittest.TestCase):
    def test_constructor(self):
        err = Err("hello world")
        self.assertEqual("test_errors.py:8: hello world", str(err))


class GuardedDecoratorTestCase(unittest.TestCase):
    def test_arg1(self):
        @guarded
        def f(a: int):
            return a

        r1 = f(0)
        self.assertEqual(0, r1)

        r2 = f(Err("error in test"))
        self.assertEqual("error in test", r2.message)

    def test_arg1_reterr(self):
        @guarded
        def f(a: int) -> int | Err:
            if a == 0:
                return Err("error from f")
            return a

        r1 = f(1)
        self.assertEqual(1, r1)

        r2 = f(0)
        self.assertEqual("error from f", r2.message)

        r3 = f(Err("error in test"))
        self.assertEqual("error in test", r3.message)

    def test_arg2(self):
        @guarded
        def f(a: int, b: int) -> int:
            return a + b

        r1 = f(1, 2)
        self.assertEqual(3, r1)

        r2 = f(Err("error in test"), 2)
        self.assertEqual("error in test", r2.message)

    def test_arg2_reterr(self):
        @guarded
        def f(a: int, b: int) -> int | Err:
            if a == 0:
                return Err("error from f")
            return a + b

        r1 = f(1, 2)
        self.assertEqual(3, r1)

        r2 = f(0, 2)
        self.assertEqual("error from f", r2.message)

        r3 = f(Err("error in test"), 2)
        self.assertEqual("error in test", r3.message)

    def test_kwarg1(self):
        @guarded
        def f(a: int, *, k: int) -> int:
            return a + k

        r1 = f(1, k=2)
        self.assertEqual(3, r1)

        r2 = f(Err("error in test"), k=2)
        self.assertEqual("error in test", r2.message)

    def test_kwarg1_reterr(self):
        @guarded
        def f(a: int, *, k: int) -> int | Err:
            if k == 0:
                return Err("error from f")
            return a + k

        r1 = f(1, k=2)
        self.assertEqual(3, r1)

        r2 = f(Err("error in test"), k=2)
        self.assertEqual("error in test", r2.message)

        r3 = f(1, k=0)
        self.assertEqual("error from f", r3.message)

    def test_kwarg2(self):
        @guarded
        def f(a: int, *, k: int, l: int) -> int:
            return a + k + l

        r1 = f(1, k=2, l=3)
        self.assertEqual(6, r1)

        r2 = f(Err("error in test"), k=2, l=3)
        self.assertEqual("error in test", r2.message)

    def test_kwarg2_reterr(self):
        @guarded
        def f(a: int, *, k: int, l: int) -> int | Err:
            if k == 0:
                return Err("error from f")
            return a + k + l

        r1 = f(1, k=2, l=3)
        self.assertEqual(6, r1)

        r2 = f(1, k=0, l=3)
        self.assertEqual("error from f", r2.message)
        r3 = f(Err("error in test"), k=2, l=3)
        self.assertEqual("error in test", r3.message)


if __name__ == '__main__':
    unittest.main()
