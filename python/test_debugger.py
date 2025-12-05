from debugger import main

# Test the main function with dummy arguments
try:
    result = main({})
    print("Test Result:")
    print(f"Type: {type(result)}")
    print(f"Content: {result}")
    print("Test passed!")
except Exception as e:
    print(f"Test failed with error: {e}")
