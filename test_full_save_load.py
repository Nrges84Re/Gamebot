from renpy_bridge import RenPyBridge


print("=== FULL PYTHON SAVE / LOAD TEST ===")

bridge = RenPyBridge()

# --------------------------------------------------
# 1. Initial state
# --------------------------------------------------

bridge.reset()

initial_state = bridge.get_status()

print("\nInitial State:")
print(initial_state)


# --------------------------------------------------
# 2. Apply first decision
# --------------------------------------------------

print("\nApplying choice_1...")

bridge.apply_decision("choice_1")

state_before_save = bridge.get_status()

print("\nState Before Save:")
print(state_before_save)


# --------------------------------------------------
# 3. Save Python Engine state
# --------------------------------------------------

saved_state = bridge.get_state().copy()

print("\nSaved Python State:")
print(saved_state)


# --------------------------------------------------
# 4. Apply another decision
# --------------------------------------------------

print("\nApplying choice_4...")

bridge.apply_decision("choice_4")

state_after_change = bridge.get_status()

print("\nState After Additional Decision:")
print(state_after_change)


# --------------------------------------------------
# 5. Load previous Python state
# --------------------------------------------------

print("\nLoading Saved Python State...")

bridge.load_state(saved_state)

state_after_load = bridge.get_status()

print("\nState After Load:")
print(state_after_load)


# --------------------------------------------------
# 6. Compare
# --------------------------------------------------

if state_after_load == state_before_save:

    print("\n=== FULL PYTHON SAVE / LOAD TEST PASSED ===")

else:

    print("\n=== FULL PYTHON SAVE / LOAD TEST FAILED ===")

    print("\nExpected:")
    print(state_before_save)

    print("\nActual:")
    print(state_after_load)

    raise SystemExit(1)