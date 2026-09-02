from renpy_bridge import RenPyBridge


print("=== RenPy / Python Connection Test ===")

bridge = RenPyBridge()

print("\nBefore:")
print(bridge.get_status())

print("\nApplying choice_1...")

bridge.apply_decision("choice_1")

print("\nAfter choice_1:")
print(bridge.get_status())

print("\nResult:")
print(bridge.get_result())

print("\n=== CONNECTION TEST PASSED ===")