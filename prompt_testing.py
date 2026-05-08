with open("prompts/describe_prompt.txt", "r") as f:
    prompt = f.read()

test_inputs = [
    "Weak password policy",
    "No encryption used",
    "Shared user accounts",
    "No backup system",
    "No audit logs"
]

for i, user_input in enumerate(test_inputs, 1):
    final_prompt = prompt.replace("{user_input}", user_input)

    print(f"\n===== TEST {i} =====")
    print(final_prompt)