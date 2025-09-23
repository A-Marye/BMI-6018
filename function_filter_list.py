def function_filter_list(input_list, input_integer):
    return [i for i in input_list if i <= input_integer]

def is_ascending(input_list):
    return input_list == sorted(input_list)

if __name__ == "__main__":
    user_input_str = input("Enter a nested list (e.g., [1, 2, [3, 4, [5, 6]]]): ")
    user_integer_str = input("Enter an integer to filter by (e.g., 6): ")
    
    try:
        user_list = eval(user_input_str)
        user_integer = int(user_integer_str)
        
        if isinstance(user_list, list):
            result = function_filter_list(user_list, user_integer)
            print(f"The filtered list is: {result}")
        elif not is_ascending(user_list):
            print("Error: The input is not a valid list.")
        else:
            print("Error: The input is not a valid list.")
            
    except (SyntaxError, NameError, TypeError) as e:
        print(f"Error: Invalid list format.")