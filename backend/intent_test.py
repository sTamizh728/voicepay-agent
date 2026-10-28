from intent import understand

tests = [
    "Send $20 to Sam",
    "hey can you pay priya fifteen dollars",
    "show me my last payments",
    "send money to Sam",   # no amount - should ask, not guess
]

for text in tests:
    print(text, "->", understand(text))