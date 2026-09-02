from renpy_bridge import RenPyBridge


choices = [
    "choice_1",
    "choice_2",
    "choice_3",
    "choice_4",
    "choice_5",
    "choice_6",
    "choice_7",
    "choice_8",
    "choice_9",
    "choice_10",
    "choice_11",
    "choice_12",
]


print("=== ALL 12 CHOICES TEST ===")

bridge = RenPyBridge()

for choice in choices:

    bridge.reset()

    before = bridge.get_status()

    after = bridge.apply_decision(choice)

    result = bridge.get_result()

    print()
    print("--------------------------------")
    print("Testing:", choice)
    print("Before:", before)
    print("After :", after)
    print("Result:", result)


print()
print("=== ALL 12 CHOICES TEST PASSED ===")