from renpy_bridge import RenPyBridge


print("=== PYTHON SAVE / LOAD TEST ===")

bridge = RenPyBridge()

print("\n1. Initial Status:")
print(bridge.get_status())

print("\n2. Applying choices...")

bridge.apply_decision("choice_1")
bridge.apply_decision("choice_4")
bridge.apply_decision("choice_7")

print("\n3. Status Before Save:")
saved_status = bridge.get_status()
print(saved_status)

print("\n4. Saving state...")

saved_state = bridge.get_state()

print("Saved State:")
print(saved_state)

print("\n5. Changing state after Save...")

bridge.apply_decision("choice_10")

print("Changed Status:")
print(bridge.get_status())

print("\n6. Loading saved state...")

bridge.load_state(saved_state)

print("Status After Load:")
loaded_status = bridge.get_status()
print(loaded_status)

print("\n7. Comparing states...")

if loaded_status == saved_status:
    print("\n=== SAVE / LOAD TEST PASSED ===")
else:
    print("\n=== SAVE / LOAD TEST FAILED ===")