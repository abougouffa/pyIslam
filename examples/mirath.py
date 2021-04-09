from pyIslam.mirath import Mirath

print("\n---Testing Mirath---\n")

test = Mirath()
test.add_relative("wife")
test.add_relative("father")
test.add_relative("maternal_grandmother")
test.add_relative("mother")
test.add_relative("paternal_grandmother")
test.add_relative("sister")
test.add_relative("brother")
test.add_relative("maternal_brother", 3)
test.add_relative("son")
test.calculate_mirath()
# test.display_shares()
