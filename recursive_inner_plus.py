def recursive_inner_plus(input_list):
    loop_list = input_list
    for i in loop_list:
        if isinstance(i, list):
            return recursive_inner_plus(i)
    loop_list_plus = []
    for i in loop_list:
        loop_list_plus.append(i + 1)
    return loop_list_plus

if __name__ == "__main__":
    user_input_str = input("Enter a nested list (e.g., [1, 2, [3, 4, [5, 6]]]): ")
    
    try:
        user_list = eval(user_input_str)
        
        if isinstance(user_list, list):
            result = recursive_inner_plus(user_list)
            print(f"The innermost list + 1 is: {result}")
        else:
            print("Error: The input is not a valid list.")
            
    except (SyntaxError, NameError, TypeError) as e:
        print(f"Error: Invalid list format.")