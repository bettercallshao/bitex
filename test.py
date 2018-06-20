import bitex
import sys

assert(bitex.get_digits(0) == 8)
assert(bitex.get_digits(8) == 8)
assert(bitex.get_digits(256) == 16)
assert(bitex.get_digits(257) == 16)
assert(bitex.get_digits(65536) == 24)

bitex.run(sys.argv[1], sys.argv[2])
