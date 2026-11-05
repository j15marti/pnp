from decimal import Decimal

a = 9007199254740992
b = a + 1
assert a != b
assert float(a) == float(b)
assert (a, -b) != (a, -a)
print('Exact integers distinguish source variables; floating conversion does not.')
