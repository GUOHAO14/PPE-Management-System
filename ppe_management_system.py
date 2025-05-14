from datetime import date
from datetime import datetime


def count_file_length(file):  # function that counts how many lines of content there are in a file
    file.seek(0)
    return sum(1 for line in file if line.strip())


def username_registration():  # prompt for unique username
    while True:  # repeat until con_user suffices constraint
        with open("controller.txt", "r") as file:  # retrieve all existing records
            con_user = input("""Enter username for registration
>>> """).strip()
            acc_list = file.readlines()
            # even index is username, odd index is password
            # locate all even index items from acc_list and add in user_list
            user_list = [user.removesuffix("\n") for user in acc_list if acc_list.index(user) % 2 == 0]
            if con_user in user_list:  # new username cannot be the same with old ones
                print(f"\"{con_user}\" has already been taken. Register a new one.")
            else:
                return con_user  # also ends loop


def password_registration():  # prompt for password & check length
    con_pass = ""
    while len(con_pass) < 8:  # loop until password is more than/equal to 8 characters
        con_pass = input("""Enter password of 8 or more characters
>>> """)
        if len(con_pass) < 8:  # display error message --> continue loop
            print("Password must be 8 or more characters for stronger security.")
    return con_pass


def controller_registration():
    # register controller username & password, if startup signal from check_files_status() is 0
    try:  # when controller.txt is readable (exist)
        with open("controller.txt", "r") as file:
            file_length = count_file_length(file)
            # each controller has one username and one password
            # must be 8 lines in controller.txt
            if file_length != 8:  # controller.txt is incomplete
                print("Controller registration is incomplete.")
                print("\n**Register Controller Username & Password**")

                # to determine number of needed controller registration left
                with open("controller.txt", "a+") as file:
                    register_count = (8 - file_length) / 2

                    # based on register_count, inform user how many registrations are left
                    # prompt input
                    if register_count in range(1, 5):
                        while file_length != 8:
                            file_length = count_file_length(file)
                            register_count = int((8 - file_length) / 2)

                            # display effect
                            if register_count > 1:
                                print(f"\n{register_count} controllers registrations remaining.")
                            elif register_count == 1:
                                print(f"\n{register_count} controller registration remaining.")

                            # prompt for username
                            con_user = username_registration()
                            # prompt for password
                            con_pass = password_registration()

                            # declare variable with an initial value
                            confirm_register = "0"
                            # loop until user decides to save
                            # some branch will force stop, such as to exit program
                            while confirm_register != "1":
                                print(f"\nController username: {con_user}\nController password: {con_pass}\n")
                                confirm_register = input("""1 Save Controller
2 Change Username or Password
3 Save & Exit Controller Registration
4 Don't Save
5 Don't Save & Exit Controller Registration
Enter 1, 2, 3, 4 or 5
>>> """)
                                if confirm_register == "1":
                                    file.write(f"{con_user}\n")
                                    file.write(f"{con_pass}\n")  # save data
                                    print("\nUsername & Password saved.")
                                    # move on to next account prompt

                                elif confirm_register == "2":
                                    change_what = ""
                                    # stop looping when input is correct
                                    while change_what not in ["1", "2", "3"]:
                                        # change username or password
                                        change_what = input("""\n1 Change Username
2 Change Password
3 back (No Changes)
Enter 1, 2 or 3
>>> """)
                                        if change_what == "1":  # calls username function
                                            con_user = username_registration()
                                        elif change_what == "2":  # calls password function
                                            con_pass = password_registration()
                                        elif change_what == "3":
                                            pass  # return to previous loop
                                        else:
                                            print("Invalid input. Try again.")

                                elif confirm_register == "3":  # save data
                                    file.write(f"{con_user}\n")
                                    file.write(f"{con_pass}\n")
                                    print("\nUsername & Password saved.\n")
                                    exit()  # exit program

                                elif confirm_register == "4":
                                    dont_save = input("""\nData discarded. Do you want to
1 Continue registration?
2 Exit registration?
Enter 1 or 2
>>> """)
                                    if dont_save == "1":
                                        break  # break loop & proceed to new registration
                                    elif dont_save == "2":
                                        exit()  # stop program
                                    else:
                                        print("Invalid input. Try again.")

                                elif confirm_register == "5":
                                    print("Data discarded.")
                                    exit()  # another way to exit program

                                else:
                                    print("Invalid input. Try again.")

                            file_length = count_file_length(file)  # update file length

                        print("\n**Controller registration complete.**\n")
                        con_signal = 1
                        # signal indicating registration is complete
                        return con_signal

                    elif register_count == 0:
                        # only for displaying message
                        print("\"controller.txt\" is empty...")
                    else:
                        # handle anomalies in file
                        # such as file length is an odd number, or more than 8
                        print("Invalid file length in \"controller.txt\" file.\nResetting file content...")
                        with open("controller.txt", "w"):
                            con_signal = 0
                            return con_signal
            else:  # skip registration because already complete
                con_signal = 1
                return con_signal

    except FileNotFoundError:  # when file does not exist
        print(f"File named \"controller.txt\" does not exist.\nCreating \"controller.txt\" file...")
        with open("controller.txt", "w"):  # create file
            con_signal = 0
            return con_signal  # signalling to loop back function


def get_file_check(file_name):
    return file_check.get(file_name, 0)  # Default to 0 if file_name is not found


def read_existing_keys(file_name, data_list):  # Initialize an empty dictionary to store existing keys.
    existing_keys = {}
    try:
        with open(file_name, "r") as file:
            data = file.read().strip().split('\n')
            for i in range(0, len(data), len(data_list)):  # read through the data list in chunks the size of data_list.
                entry = data[i:i + len(data_list)]  # slice the data to get the current entry.
                for idx, key in enumerate(entry):  # read through each element in the entry.
                    key = key.strip()
                    if idx in existing_keys:  # if the index already exists in the dictionary,add the key to the set.
                        existing_keys[idx].add(key)
                    else:
                        existing_keys[idx] = {key}  # if not, create a new set at that index with the key as its first element.
    except FileNotFoundError:
        pass
    return existing_keys


def read_codes_from_file(file_name, index, data_list):  # create an empty set to store the codes.
    codes = set()
    try:
        with open(file_name, "r") as file:
            data = file.read().strip().split('\n')
            for i in range(index, len(data), len(data_list)):
                # read through the data list starting from the specified index,read the list in increments of the size of data_list.
                codes.add(data[i].strip())
    except FileNotFoundError:
        pass
    return codes


def enter_inventory_data(data_list, file_name, add_signal="0"):
    # Read item codes from PPE list
    ppe_item_codes = read_codes_from_file("ppe.txt", ppe_list.index("item code"), ppe_list)

    # Read supplier codes from Supplier list
    supplier_codes = read_codes_from_file("supplier.txt", supplier_list.index("supplier code"), supplier_list)

    # Read hospital codes from Hospital list
    hospital_codes = read_codes_from_file("hospital.txt", hospital_list.index("hospital code"), hospital_list)

    file_check_count = get_file_check(file_name)  # Get the number of lines expected from the dictionary
    # Read through all existing keys from each list and set them as unique ids
    existing_keys = read_existing_keys(file_name, data_list)
    unique_ids = existing_keys

    id_indices = [data_list.index(key) for key in
                  ['supplier code', 'hospital code', 'item code', 'distribution code', 'supply code'] if
                  key in data_list]

    filtered_fields = [item for item in data_list if
                       'quantity' in item or 'day' in item or 'year' in item or 'month' in item]

    # Set to track unique item codes in the current session
    used_item_codes = set()
    while True:
        try:
            with (open(file_name, "a+") as file):
                file.seek(0)  # Move the file pointer to the start of the file to read its contents.
                file_length = count_file_length(file)  # Count the number of lines or entries in the file.
                # Check if the file size fulfills the required amount.
                if file_check_count is not None and file_length < file_check_count:
                    print(f"{file_name} is incomplete")
                fourth_d_s = "0"  # declare variable
                filler = "1"
                # Continue prompting the user for input until the file meets the required line count
                # add_signal == "1" tells the program that it is used for Update Inventory functionality
                # behaves differently compared to Initial Inventory Creation
                # fourth_d_s == "1" allows one additional loop (4th) for hospital or supplier data entry
                while file_check_count is None or file_length < file_check_count or add_signal == "1" or fourth_d_s == "1":
                    print(f"\nEnter {', '.join(data_list)} (each value on a new line).")

                    if "ppe quantity" in data_list and add_signal == "0":
                        # Provide notes for ppe quantity units
                        print("Note: PPE Quantity (units) is set as 100 (default).")

                    if file_name in ["ppe.txt", "hospital.txt", "supplier.txt"] and add_signal == "0":
                        # Provide additional instructions based on the specific file being edited.
                        print(f"Type 'exit' to quit.")

                    if file_name in ["distribution.txt", "supply.txt"]:
                        print(f"Enter \"back\" to return to previous page.")

                    # Initialize empty lists to store the entered values if any errors encountered.
                    values = []
                    errors = []
                    stop_signal = "0"  # Default stop signal is "0" (indicating to continue entering values).
                    for field in data_list:
                        if file_name in ["supplier.txt", "hospital.txt", "distribution.txt"] or (
                                file_name == "ppe.txt" and field != "ppe quantity") or (
                                file_name == "supply.txt" and field != "supplier code") or add_signal == "1":
                            while True:
                                value = input(f"{field}: ").strip().lower()

                                if file_name in ["ppe.txt", "hospital.txt", "supplier.txt"]:
                                    if value == 'exit':  # exit program during initial creation
                                        exit()
                                if file_name in ["distribution.txt", "supply.txt"]:
                                    if value == "back":  # exit during Add (Update) functionality session
                                        stop_signal = "1"
                                        filler = "0"
                                        break

                                # Remove internal spaces for specific fields
                                if field in ['item code', 'supplier code', 'hospital code', 'distribution code',
                                             'supply code']:
                                    value = value.replace(" ", "").upper()
                                values.append(value.upper())
                                break
                        if stop_signal == "1":  # user stops entering data (Add)
                            break

                        if file_name == "supply.txt" and field == "supplier code":
                            ppe = values[1]  # Retrieve the item (PPE) from the values list. It is assumed to be at index 1.
                            try:
                                sr_index = ItemCodeList.index(ppe)  # Find the index of the item in the ItemCodeList, which presumably contains codes or identifiers for items.
                                value = ItemSrCodeList[sr_index]  # Use the retrieved index to find the corresponding supplier code from the ItemSrCodeList.
                                values.append(value)  # Append the retrieved supplier code to the `values` list, which will be used for saving data later.
                                print(f"{field}: {value}")
                            except ValueError:
                                print("Invalid item. Session aborted.")
                                stop_signal = "1"
                                filler = "0"
                                break


                        if file_name == "ppe.txt" and field == "ppe quantity" and add_signal == "0":
                            value = "100"
                            values.append(value)

                    if stop_signal != "1":  # Check errors in data
                        print(f"\nData to be entered into {file_name}:")
                        for value_index, value in enumerate(values):
                            print(f"{data_list[value_index]}: {value}")

                        # Clear previous errors
                        errors.clear()

                        # Check for uniqueness and other validations
                        for i in range(len(data_list)):
                            expected_type = data_list[i]
                            value = values[i]

                            # Ensure primary key does not repeat
                            if value in existing_keys.get(0, set()):
                                errors.append(
                                    f"Error: '{value}' for {expected_type} already exists. Please enter a unique value.")

                            # Validate integer fields
                            if expected_type in filtered_fields:
                                try:
                                    value = int(value)
                                    values[i] = value
                                except ValueError:
                                    errors.append(f"Error: '{value}' should be an integer for {expected_type}.")

                            # Validate against lists
                            if (
                                    file_name == "distribution.txt" or file_name == "supply.txt") and expected_type == "item code":
                                if value not in ppe_item_codes:
                                    errors.append(
                                        f"Error: '{value}' is not a valid item code. "
                                        f"Please enter a valid item code from ppe.txt.")

                            if file_name == "distribution.txt" and expected_type == 'hospital code':
                                if value not in hospital_codes:
                                    errors.append(
                                        f"Error: '{value}' is not a valid hospital code. "
                                        f"Please enter a valid hospital code from hospital.txt.")

                            if (
                                    file_name == "ppe.txt" or file_name == "supply.txt") and expected_type == 'supplier code':
                                if value not in supplier_codes:
                                    errors.append(
                                        f"Error: '{value}' is not a valid supplier code. "
                                        f"Please enter a valid supplier code from supplier.txt.")

                        if file_name == "distribution.txt" or file_name == "supply.txt":
                            if type(values[3]) is int and values[3] not in range(2020, 2025):  # limit year range
                                    errors.append("Error: Year out of range (must be 2020-2024).")
                            if type(values[4]) is int:
                                if values[4] not in range(1, 13):  # a year has 12 months
                                    errors.append("Error: Invalid month (must be 1-12).")
                                else:
                                    if type(values[5]) is int:
                                        if values[4] in [1, 3, 5, 7, 8, 10, 12]:
                                            if values[5] not in range(1, 32):
                                                errors.append(f"Error: Invalid day (must be 1-31).")
                                        if values[4] in [4, 6, 9, 11]:
                                            if values[5] not in range(1, 31):
                                                errors.append(f"Error: Invalid day (must be 1-30).")
                                        if values[4] == 2:
                                            if values[5] not in range(1, 30):
                                                errors.append(f"Error: Invalid day (must be 1-29).")
                        if errors:
                            print("\n".join(errors))  # Display all errors
                            print("Invalid Data.")
                            continue

                        if file_name == "distribution.txt" or file_name == "supply.txt":
                            # Extract the item (PPE) being transacted and its quantity from the input values.
                            transact_ppe = values[1]
                            transact_quan = int(values[6])
                            ppe_index = ItemCodeList.index(transact_ppe)  # Find the index of the item in the item list.
                            current_quan = int(ItemQuantityList[ppe_index])  # Get the current quantity of the item from the quantity list.
                            if file_name == "distribution.txt":
                                new_quan = current_quan - transact_quan  # Calculate the new quantity after distribution.
                                if new_quan < 0:
                                    print(
                                        f"\nSpecified unit quantity ({transact_quan}) of {transact_ppe} cannot be distributed."
                                        f"\nCurrent Stock: {current_quan} *INSUFFICIENT*")
                                    return new_quan, ppe_index
                                else:
                                    print(f"\nCurrent Stock: {current_quan}    After Distribution: {new_quan}")
                            elif file_name == "supply.txt":
                                new_quan = current_quan + transact_quan
                                print(f"\nCurrent Stock: {current_quan}    After Supply: {new_quan}")

                        while True:
                            save_data = input(
                                f"Confirm entry? (type \"yes\" or click enter to confirm, type \"no\" to cancel)\n>>> ").lower()

                            if save_data in ["yes", ""]:
                                for value in values:
                                    value = str(value)
                                    file.write(value + "\n")
                                    # prevents 5th or more loop when entering data for hospital or supplier
                                    fourth_d_s = "0"

                                # Update existing_keys and unique_ids after writing data
                                for i in id_indices:
                                    if i in existing_keys:
                                        existing_keys[i].add(values[i].strip())
                                    else:
                                        existing_keys[i] = {values[i].strip()}

                                if file_name == "ppe.txt":
                                    used_item_codes.add(values[0].strip())  # Add item code to used_item_codes

                                if file_name in ["distribution.txt", "supply.txt"]:
                                    for j, field in enumerate(data_list):
                                        if field in ['item code', 'supplier code']:
                                            unique_ids.setdefault(field, set()).add(values[j].strip())

                                print("Data entry successful.")
                                break

                            elif save_data == "no":
                                print("Data not entered.")
                                if file_check_count is None:
                                    # special signal for when updating distribution & supply file
                                    # return exact
                                    return save_data, ppe_index
                                break

                            else:
                                print("Invalid input.")

                    file_length = count_file_length(file)
                    if (file_name == "hospital.txt" or file_name == "supplier.txt") and file_length == 6:
                        choice = input(
                            f"Do you want to enter the fourth record for {file_name}?\n(yes/no) >>> ").strip().lower()
                        if choice == "yes":
                            fourth_d_s = "1"  # indicate another data entry loop for hospital or supply
                        elif choice == "no":
                            pass
                        else:
                            print("Invalid input.")
                    if file_check_count is None:  # distribution & supply file
                        if stop_signal == "1":
                            if filler != "0":
                                filler = "-1"
                            # no data added for said files
                            return stop_signal, filler
                        return new_quan, ppe_index  # break loop for distribution & supply file, return new quantity

                    if add_signal == "1" and fourth_d_s != "1":
                        return True

                if add_signal != "1":
                    print(f"{file_name} is complete.")
                    return False  # Indicate that data entry is complete for this file


        except FileNotFoundError:
            print(f"\nCreating {file_name}...")
            with open(file_name, "w"):
                pass


def boot_system():
    # make sure mandatory files exist and filled up
    # if yes, initiate main inventory management system
    print("Booting system...\n")
    print("Initiating system files...\n")

    con_signal = 0
    while con_signal == 0:
        con_signal = controller_registration()
    # only move on to following code if con_signal = 1
    # which means controller.txt is complete
    print("All controllers are set up.\n")

    # check supplier.txt or enter supplier data
    enter_inventory_data(supplier_list, "supplier.txt")

    # check hospital.txt or enter hospital data
    enter_inventory_data(hospital_list, "hospital.txt")

    # check ppe.txt or enter ppe data
    enter_inventory_data(ppe_list, "ppe.txt")

    # create distribution.txt and supply.txt file if do not exist
    # if exist, do not affect data
    open("distribution.txt", "a").close()
    open("supply.txt", "a").close()
    # all files exist with required data
    print("All inventory files are set up.\n")
    print("Proceeding to main system...\n")


def stock_display(file_name):  # display stock when updating supply & distribution data
    print("\nPPE TABLE", end="")
    for up_index, item_code in enumerate(ItemCodeList):  # retrieve item code & corresponding quantity
        item_name = ItemNameList[up_index]
        quantity = ItemQuantityList[up_index]
        print(
            f"\n{item_code} -  {item_name}{" " * (26 - len(item_code) - len(item_name) - len(str(quantity)))}{quantity} units",
            end="")
        if file_name == "supply.txt":
            sr_code = ItemSrCodeList[up_index]  # supplier code for each item
            sr_idx = SrCodeList.index(sr_code)
            sr_name = SrNameList[sr_idx]  # supplier name found
            print(f"     < supplied by >     [{sr_code} -  {sr_name}]", end="")
    print("")
    if file_name == "distribution.txt":
        print("\nHOSPITAL TABLE")
        for hos_code, hos_name in zip(HosCodeList, HosNameList):  # retrieve hospital code & its name
            print(f"{hos_code} -  {hos_name}")


def update_ppe_hos_sr_inventory(data_list, file_name):
    # when adding data for ppe.txt, hospital.txt or supplier.txt
    add_signal = "1"
    while True:  # for users who want to add data again
        if file_name == "hospital.txt" or file_name == "supplier.txt":
            with open(file_name, "r") as file:
                file_len = len(file.readlines())  # retrieve number of lines
                if file_len == 8:  # file already has 4 records (maximum)
                    print("Maximum file length reached (4). Data addition not allowed.")
                    break  # exit Update functionality
        enter_inventory_data(data_list, file_name, add_signal=add_signal)
        # if the 2 files has 3 records only
        if file_name == "hospital.txt" or file_name == "supplier.txt":
            break  # having 4 records, no point to loop Update functionality
        if file_name == "ppe.txt":  # limitless records
            up_more = input(f"\nDo you want to enter more data for {file_name}?\n(yes/no) >>> ").strip().lower()
            if up_more == "yes":
                pass  # add more data, back to loop
            elif up_more == "no":
                break  # exit Update functionality
            else:  # other input
                print("Invalid input.")


def update_dis_sup_inventory(data_list, file_name):
    # when adding data for distribution.txt or supply.txt
    while True:
        stock_display(file_name)  # display current stock
        new_quan, quan_idx = enter_inventory_data(data_list, file_name)  # add data

        if new_quan == "1" and quan_idx == "-1":  # special signal to return to previous page
            break  # exit current loop
        else:
            if type(new_quan) is int and new_quan >= 0:  # valid data that can be added
                ItemQuantityList[quan_idx] = str(new_quan)
                save_item()  # save quantity change in ppe file
                stock_display(file_name)  # display updated stock
            else:
                # "no" is returned from enter_inventory_data function
                # do nothing with it, no new quantity updated
                pass
            # once data saved, option for another data entry session
            up_more = ""
            while up_more != "yes" and up_more != "no":
                up_more = input(f"\nDo you want to enter more data for {file_name}?\n(yes/no) >>> ").strip().lower()
                if up_more == "yes":
                    break  # prompt for data entry again
                elif up_more == "no":
                    break  # breaks loop, go back to previous loop (previous page)
                else:  # handle invalid input
                    print("Invalid input.")
            if up_more == "no":
                break


def display_login_prompt():
    # Prompt the user to enter their admin username and password
    Input_username = input('\nEnter admin username: ')
    Input_password = input('Enter admin password: ')
    # Return the entered username and password
    return Input_username, Input_password


def Validate_credentials(Username, Password):
    # Initialize empty lists to store controller data
    Controller_list = []
    User_list = []
    Pass_list = []

    with open('controller.txt', 'r') as file:
        # Open the 'controller.txt' file in read mode
        for line in file:
            if line == "\n":
                # Skip empty lines
                pass
            else:
                Controller_list.append(line.strip())
                # Add each line to the controller list after stripping whitespace

    for Index, Item in enumerate(Controller_list):
        # Separate usernames and passwords into different lists
        if Index % 2 == 0:
            User_list.append(Item)
        else:
            Pass_list.append(Item)

    if Username in User_list:
        # Check if the entered username is in the list of usernames
        Admin_index = User_list.index(Username)
        # Get the index of the username
        if Password == Pass_list[Admin_index]:
            # Check if the password at the corresponding index matches the entered password
            return True
        else:
            return False
    else:
        return False


def admin_login():
    # Print a welcome message
    print("**Welcome to Admin Login**")

    # Initialize login attempt counter
    Login_attempts = 0
    # Define maximum number of allowed attempts
    Max_attempts = 3
    # Loop until the maximum attempts are reached
    while Login_attempts < Max_attempts:
        # Prompt the user to enter their login credentials
        Username, Password = display_login_prompt()

        # Validate the entered credentials
        if Validate_credentials(Username, Password) is True:
            # Print a welcome message if credentials are valid
            print(f'Welcome back, Admin {Username}.')
            return True
        else:
            # Print an error message and increment the attempt counter if credentials are invalid
            print('Invalid Username or Password, please try again.')
            Login_attempts += 1

    # If maximum attempts are reached, deny access and exit
    if Login_attempts >= Max_attempts:
        print('Max attempts reached; Access denied.')
        exit()


def ffind():  # prompt user to choose which file to search
    find = input("""\nChoose Inventory to View, Search & Track
    1: Item
    2: Supplier
    3: Hospital
    4: Supply
    5: Distribution
    6: back
Enter choice (number from 1 to 6): """).lower().replace(" ", "")
    return find


def Iprovide():  # prompt user what can provide to search for item file
    provide = input("""\nVIEW PERSONAL PROTECTIVE EQUIPMENT (PPE) DATA
    1: Display ALL Records.
OR Display specific record by providing-
    2: Item code
    3: Item name
    4: Item quantity
    5: Supplier code
    6: Supplier name
    7: Hospital code
    8: Hospital name
Type 'exit' to quit
Enter choice (number from 1 to 8): """).lower().replace(" ", "")
    return provide


def Srprovide():  # prompt user what can provide to search for supplier file
    provide = input("""\nVIEW SUPPLIER DATA
    1: Display ALL Records
OR Display specific record by providing-
    2: Item code
    3: Item name
    4: Supplier code
    5: Supplier name
    6: Supply code
    7: Supply date
Type 'exit' to quit
Enter choice (number from 1 to 7): """).lower().replace(" ", "")
    return provide


def Hprovide():  # prompt user what can provide to search for hospital file
    provide = input("""\nVIEW HOSPITAL DATA
    1: Display ALL Records
OR Display specific record by providing-
    2: Hospital code
    3: Hospital name
    4: Distribution code
    5: Distribution date
Type 'exit' to quit
Enter choice (number from 1 to 5): """).lower().replace(" ", "")
    return provide


def Sprovide():  # prompt user what can provide to search for supply file
    provide = input("""\nVIEW SUPPLY TRANSACTIONS
    1: Display ALL Records
OR Display specific record by providing-
    2: Item code
    3: Item name
    4: Supplier code
    5: Supplier name
    6: Supply code
    7: Supply date
    8: Supply quantity
Type 'exit' to quit
Enter choice (number from 1 to 8): """).lower().replace(" ", "")
    return provide


def Dprovide():  # prompt user what can provide to search for distribution file
    provide = input("""\nVIEW DISTRIBUTION TRANSACTIONS
    1: Display ALL Records
    2: Distribution for Specific Item (Summary)
OR Display specific record by providing-
    3: Item code
    4: Item name
    5: Hospital code
    6: Hospital name
    7: Distribution code
    8: Distribution date
    9: Distribution quantity
Type 'exit' to quit
Enter choice (number from 1 to 9): """).lower().replace(" ", "")
    return provide


def CAns():  # prompt user for information about code and number
    ans = input("Please enter the information: ").upper().replace(" ", "")
    return ans


def NAns():  # prompt user for information about name
    ans = input("Please enter the information: ").upper().strip()
    return ans


def fselect(ans):  # prompt user to select the range of quantity
    select = input(f"""\nPlease choose one
    1: greater than {ans}
    2: lesser than {ans}
    3: equal to {ans}
Enter the code: """).lower().replace(" ", "")
    return select


def showItem(index):  # display item file
    show = []
    show.append(ItemCodeList[index])
    show.append(ItemNameList[index])
    show.append(ItemQuantityList[index])
    show.append(ItemSrCodeList[index])
    print(show)


def showSr(index):  # display supplier file
    show = []
    show.append(SrCodeList[index])
    show.append(SrNameList[index])
    print(show)


def showHos(index):  # display hospital file
    show = []
    show.append(HosCodeList[index])
    show.append(HosNameList[index])
    print(show)


def showSup(index):  # display supply file
    show = []
    show.append(SupCodeList[index])
    show.append(SupItemCodeList[index])
    show.append(SupSrCodeList[index])
    show.append(SupQuantityList[index])
    show.append(FSupDateList[index])
    print(show)


def showDis(index):  # display distribution file
    show = []
    show.append(DisCodeList[index])
    show.append(DisItemCodeList[index])
    show.append(DisHosCodeList[index])
    show.append(DisQuantityList[index])
    show.append(FDisDateList[index])
    print(show)


def distribution_summary(ans, year=None, month=None):
    hos_display = [hos_code for hos_code in HosCodeList]
    quantity_display = [0 for length in HosCodeList]
    for dis_idx in range(len(DisCodeList)):  # match item code with item code list for every distribution
        if ans == DisItemCodeList[dis_idx]:
            # match year, month with year list and month list if year, month exist
            if (year is None and month is None) or (year == DisYearList[dis_idx] and month == DisMonthList[dis_idx]):
                dis_hos = DisHosCodeList[dis_idx]
                quantity = int(DisQuantityList[dis_idx])
                for hos_idx, hos_code in enumerate(HosCodeList):
                    if hos_code == dis_hos:  # add quantity into quantity display if all criteria meet
                        quantity_display[hos_idx] += quantity
    item_name = ItemNameList[ItemCodeList.index(ans)]
    print(f"\nHospital Distribution Quantity for PPE - {ans} ({item_name})")  # display total quantity
    for hos_code, quantity in zip(hos_display, quantity_display):
        print(f"{hos_code} :   {quantity} units")


def search(ItemQuantityList):
    while True:
        find = ffind()
        if find == "6":
            break
        elif find == "1":  # item file
            provide = Iprovide()
            if provide == "exit":
                break
            elif provide == "1":  # display all item file
                choose = input("""\nPlease choose one
    1: Show in ascending order
    2: Show in descending order
    3: Show in original order
Enter the code: """).lower().replace(" ", "")  # prompt user to choose order
                if choose in ["1", "2", "3"]:
                    if choose == "1":
                        SList = sorted(ItemCodeList)  # sort item code in ascending order
                    elif choose == "2":
                        SList = sorted(ItemCodeList, reverse=True)  # sort item code in descending order
                    elif choose == "3":
                        SList = ItemCodeList  # item code in original order
                    for x in SList:
                        index = ItemCodeList.index(x)  # use index of sorted item code to find other item details
                        showItem(index)
                else:
                    print("Invalid")
            elif provide == "2":
                ans = CAns()  # prompt user for item code
                if ans in ItemCodeList:
                    index = ItemCodeList.index(ans)  # use index of item code to find item details
                    showItem(index)
                else:
                    print("Invalid")
            elif provide == "3":
                ans = NAns()  # prompt user for item name
                if ans in ItemNameList:
                    index = ItemNameList.index(ans)  # use index of item name to find item details
                    showItem(index)
                else:
                    print("Invalid")
            elif provide == "4":
                ans = CAns()  # prompt user for item quantity
                try:
                    ans = int(ans)  # ensure input is integer
                except ValueError:
                    print("Invalid")
                else:
                    select = fselect(ans)  # prompt user for quantity range
                    if select in ["1", "2", "3"]:
                        # add the index of item quantity that meet the criteria into index list
                        if select == "1":
                            index = [index for index, x in enumerate(ItemQuantityList) if int(x) > int(ans)]
                        elif select == "2":
                            index = [index for index, x in enumerate(ItemQuantityList) if int(x) < int(ans)]
                        elif select == "3":
                            index = [index for index, x in enumerate(ItemQuantityList) if int(x) == int(ans)]
                        if index == []:
                            print("No matching data.")
                        else:
                            for index in index:  # use the index to find item details
                                showItem(index)
                    else:
                        print("Invalid")
            elif provide == "5":
                ans = CAns()  # prompt user for supplier code
                if ans in ItemSrCodeList:
                    # add the index of supplier code same as input into index list
                    index = [index for index, x in enumerate(ItemSrCodeList) if x == ans]
                    for index in index:  # use the index to find other details
                        showItem(index)
                else:
                    print("Invalid")
            elif provide == "6":
                ans = NAns()  # prompt user for supplier name
                if ans in SrNameList:
                    # use supplier name to find supplier code
                    index = SrNameList.index(ans)
                    pk = SrCodeList[index]
                    # use supplier code to find index of item list
                    index = [index for index, x in enumerate(ItemSrCodeList) if x == pk]
                    for index in index:  # use index of item list to find item details
                        showItem(index)
                else:
                    print("Invalid")
            elif provide == "7":
                ans = CAns()  # prompt user for hospital code
                if ans in DisHosCodeList:
                    # use hospital code to find index of distribution list
                    index = [index for index, x in enumerate(DisHosCodeList) if x == ans]
                    pk = []
                    for x in index:
                        pk.append(DisItemCodeList[x])  # use index of distribution list to find item code
                    index = []
                    for x in pk:
                        index.append(ItemCodeList.index(x))  # use item code to find index of item list
                    for index in index:  # use index of item list to find item details
                        showItem(index)
                else:
                    print("Invalid")
            elif provide == "8":
                ans = NAns()  # prompt user for hospital name
                if ans in HosNameList:
                    # use hospital name to find hospital code
                    index = HosNameList.index(ans)
                    pk = HosCodeList[index]
                    if pk in DisHosCodeList:
                        # use hospital code to find index of distribution list
                        index = [index for index, x in enumerate(DisHosCodeList) if x == pk]
                        pk = []
                        for x in index:
                            pk.append(DisItemCodeList[x])  # use index of distribution list to find item code
                        index = []
                        # use item code to find item details
                        for x in pk:
                            index.append(ItemCodeList.index(x))
                        for index in index:
                            showItem(index)
                    else:
                        print("Doesn't have any relevant item")
                else:
                    print("Invalid")
            else:
                print("Invalid")

        elif find == "2":  # supplier file
            provide = Srprovide()
            if provide == "exit":
                break
            elif provide == "1":
                for index, x in enumerate(SrCodeList):  # display all supplier file
                    showSr(index)
            elif provide == "2":
                ans = CAns()  # prompt user for item code
                if ans in ItemCodeList:
                    index = ItemCodeList.index(ans)  # use index of item code to find supplier code
                    pk = ItemSrCodeList[index]
                    index = SrCodeList.index(pk)  # use supplier code to find supplier details
                    showSr(index)
                else:
                    print("Invalid")
            elif provide == "3":
                ans = NAns()  # prompt user for item name
                if ans in ItemNameList:
                    index = ItemNameList.index(ans)  # use index of item name to find supplier code
                    pk = ItemSrCodeList[index]
                    index = SrCodeList.index(pk)  # use supplier code to find supplier details
                    showSr(index)
                else:
                    print("Invalid")
            elif provide == "4":
                ans = CAns()  # prompt user for supplier code
                if ans in SrCodeList:
                    index = SrCodeList.index(ans)  # use supplier code to find supplier details
                    showSr(index)
                else:
                    print("Invalid")
            elif provide == "5":
                ans = NAns()  # prompt user for supplier name
                if ans in SrNameList:
                    index = SrNameList.index(ans)  # use index of supplier name to find supplier details
                    showSr(index)
                else:
                    print("Invalid")
            elif provide == "6":
                ans = CAns()  # prompt user for supply code
                if ans in SupCodeList:
                    index = SupCodeList.index(ans)  # use index of supply code to find supplier code
                    pk = SupSrCodeList[index]
                    index = SrCodeList.index(pk)  # use supplier code to find supplier details
                    showSr(index)
                else:
                    print("Invalid")
            elif provide == "7":
                try:
                    year, month, day = input("""\nPlease enter the date in number, split by comma (year, month, date)
: """).replace(" ", "").split(",")  # prompt user for date
                    # ensure date is in integer
                    year = int(year)
                    month = int(month)
                    day = int(day)
                except ValueError:
                    print("Invalid")
                else:
                    try:
                        ans = date(year, month, day)  # ensure that date is in date format
                    except ValueError:
                        print("Invalid")
                    else:
                        select = fselect(ans)  # prompt user for date range
                        if select in ["1", "2", "3"]:
                            # add the index of supply date that meet the criteria into index list
                            if select == "1":
                                index = [index for index, x in enumerate(SupDateList) if x > ans]
                            elif select == "2":
                                index = [index for index, x in enumerate(SupDateList) if x < ans]
                            elif select == "3":
                                index = [index for index, x in enumerate(SupDateList) if x == ans]
                            if index == []:
                                print("No matching data.")
                            else:
                                pk = []
                                for x in index:
                                    pk.append(SupSrCodeList[x])  # use the index to find supplier code
                                index = []
                                for x in pk:
                                    index.append(SrCodeList.index(x))  # use supplier code to find supplier details
                                for index in index:
                                    showSr(index)
                        else:
                            print("Invalid")
            else:
                print("Invalid")

        elif find == "3":  # hospital file
            provide = Hprovide()
            if provide == "exit":
                break
            elif provide == "1":
                for index, x in enumerate(HosCodeList):  # display all hospital file
                    showHos(index)
            elif provide == "2":
                ans = CAns()  # prompt user for hospital code
                if ans in HosCodeList:
                    index = HosCodeList.index(ans)  # use hospital code to find hospital details
                    showHos(index)
                else:
                    print("Invalid")
            elif provide == "3":
                ans = NAns()  # prompt user for hospital name
                if ans in HosNameList:
                    index = HosNameList.index(ans)  # use index of hospital name to find hospital details
                    showHos(index)
                else:
                    print("Invalid")
            elif provide == "4":
                ans = CAns()  # prompt user for distribution code
                if ans in DisCodeList:
                    # use index of distribution code to find hospital code
                    index = DisCodeList.index(ans)
                    pk = DisHosCodeList[index]
                    index = HosCodeList.index(pk)  # use hospital code to find hospital details
                    showHos(index)
                else:
                    print("Invalid")
            elif provide == "5":
                try:
                    year, month, day = input("""\nPlease enter the date in number, split by comma (year, month, date)
: """).replace(" ", "").split(",")  # prompt user for date
                    # ensure date in integer
                    year = int(year)
                    month = int(month)
                    day = int(day)
                except ValueError:
                    print("Invalid")
                else:
                    try:
                        ans = date(year, month, day)  # ensure date in date format
                    except ValueError:
                        print("Invalid")
                    else:
                        select = fselect(ans)  # prompt user for date range
                        if select in ["1", "2", "3"]:
                            # add the index of date that meet the criteria into index list
                            if select == "1":
                                index = [index for index, x in enumerate(DisDateList) if x > ans]
                            elif select == "2":
                                index = [index for index, x in enumerate(DisDateList) if x < ans]
                            elif select == "3":
                                index = [index for index, x in enumerate(DisDateList) if x == ans]
                            if index == []:
                                print("No matching data.")
                            else:
                                pk = []
                                for x in index:
                                    pk.append(DisHosCodeList[x])  # use index of date to find hospital code
                                index = []
                                for x in pk:
                                    index.append(HosCodeList.index(x))  # use hospital code to find hospital details
                                for index in index:
                                    showHos(index)
                        else:
                            print("Invalid")
            else:
                print("Invalid")

        elif find == "4":  # supply file
            provide = Sprovide()
            if provide == "exit":
                break
            elif provide == "1":  # search all supply file
                if SupCodeList == []:
                    print("No data available at this moment.")
                else:
                    for index, x in enumerate(SupCodeList):
                        showSup(index)
            elif provide == "2":
                ans = CAns()  # prompt user for item code
                if ans in SupItemCodeList:
                    # use index of item code to find supply details
                    index = [index for index, x in enumerate(SupItemCodeList) if x == ans]
                    for index in index:
                        showSup(index)
                else:
                    print("Invalid")
            elif provide == "3":
                ans = NAns()  # prompt user for item name
                if ans in ItemNameList:
                    index = ItemNameList.index(ans)  # use index of item name to find item code
                    pk = ItemCodeList[index]
                    if pk in SupItemCodeList:
                        # use index of item code to find supply details
                        index = [index for index, x in enumerate(SupItemCodeList) if x == pk]
                        for index in index:
                            showSup(index)
                    else:
                        print("Doesn't have any relevant distribution")
                else:
                    print("Invalid")
            elif provide == "4":
                ans = CAns()  # prompt user for supplier code
                if ans in SupSrCodeList:
                    # use index of supplier code to find supply details
                    index = [index for index, x in enumerate(SupSrCodeList) if x == ans]
                    for index in index:
                        showSup(index)
                else:
                    print("Invalid")
            elif provide == "5":
                ans = NAns()  # prompt user for supplier name
                if ans in SrNameList:
                    index = SrNameList.index(ans)  # use index of supplier name to find supplier code
                    pk = SrCodeList[index]
                    if pk in SupSrCodeList:
                        # use index of supplier code to find supply details
                        index = [index for index, x in enumerate(SupSrCodeList) if x == pk]
                        for index in index:
                            showSup(index)
                    else:
                        print("Doesn't have any relevant distribution")
                else:
                    print("Invalid")
            elif provide == "6":
                ans = CAns()  #prompt user for supply code
                if ans in SupCodeList:
                    index = SupCodeList.index(ans)  # use supply code to find supply details
                    showSup(index)
                else:
                    print("Invalid")
            elif provide == "7":
                try:
                    year, month, day = input("""\nPlease enter the date in number, split by comma (year, month, date)
: """).replace(" ", "").split(",")  # prompt user for date
                    # ensure that date is integer
                    year = int(year)
                    month = int(month)
                    day = int(day)
                except ValueError:
                    print("Invalid")
                else:
                    try:
                        ans = date(year, month, day)  # ensure that date is in date format
                    except ValueError:
                        print("Invalid")
                    else:
                        select = fselect(ans)  # prompt user for date range
                        if select in ["1", "2", "3"]:
                            # add index of date that meet the criteria into index list
                            if select == "1":
                                index = [index for index, x in enumerate(SupDateList) if x > ans]
                            elif select == "2":
                                index = [index for index, x in enumerate(SupDateList) if x < ans]
                            elif select == "3":
                                index = [index for index, x in enumerate(SupDateList) if x == ans]
                            if index == []:
                                print("No matching data.")
                            else:
                                for index in index:  # use index of date to find supply details
                                    showSup(index)
                        else:
                            print("Invalid")
            elif provide == "8":
                choose = input("""\nPlease choose one
    1: separate all transaction
    2: combine transaction with same supplier
    3: combine transaction with the same item and supplier
Enter the code: """).lower().replace(" ", "")  # prompt user for combination
                if choose == "1":
                    ans = CAns()  # prompt user for supply quantity
                    try:
                        ans = int(ans)  # ensure that quantity is integer
                    except ValueError:
                        print("Invalid")
                    else:
                        select = fselect(ans)  # prompt user for quantity range
                        if select in ["1", "2", "3"]:
                            # add the index of quantity that meet criteria into index list
                            if select == "1":
                                index = [index for index, x in enumerate(SupQuantityList) if int(x) > int(ans)]
                            elif select == "2":
                                index = [index for index, x in enumerate(SupQuantityList) if int(x) < int(ans)]
                            elif select == "3":
                                index = [index for index, x in enumerate(SupQuantityList) if int(x) == int(ans)]
                            if index == []:
                                print("No matching data.")
                            else:
                                for index in index:  # use index of quantity to find supply details
                                    showSup(index)
                        else:
                            print("Invalid")
                elif choose == "2":
                    ans = CAns()
                    try:
                        ans = int(ans)
                    except ValueError:
                        print("Invalid")
                    else:
                        select = fselect(ans)
                        if select in ["1", "2", "3"]:
                            # add supply quantity and supplier code to the same list
                            SrQuantityList = []
                            for x, y in zip(SupSrCodeList, SupQuantityList):
                                y = int(y)
                                SrQuantityList.append((x, y))
                            # add supply quantity with the same supplier together by using dictionary
                            SrSum = {}
                            for code, quantity in SrQuantityList:
                                if code in SrSum:
                                    SrSum[code] += quantity
                                else:
                                    SrSum[code] = quantity
                            SrSum = list(SrSum.items())  # change dictionary back to list
                            # add the supplier code that total quantity meet criteria into pk list
                            if select == "1":
                                pk = [code for code, quantity in SrSum if int(quantity) > int(ans)]
                            elif select == "2":
                                pk = [code for code, quantity in SrSum if int(quantity) < int(ans)]
                            elif select == "3":
                                pk = [code for code, quantity in SrSum if int(quantity) == int(ans)]
                            if pk == []:
                                print("No matching data.")
                            else:
                                for x in pk:
                                    # use index of supplier code to find supply details
                                    index = [index for index, y in enumerate(SupSrCodeList) if y == x]
                                    for index in index:
                                        showSup(index)
                                    for item in SrSum:  # display the total quantity
                                        if item[0] == x:
                                            print(item)
                                            break
                        else:
                            print("Invalid")
                elif choose == "3":
                    ans = CAns()
                    try:
                        ans = int(ans)
                    except ValueError:
                        print("Invalid")
                    else:
                        select = fselect(ans)
                        if select in ["1", "2", "3"]:
                            # add supplier code, item code and supply quantity into the same list
                            CQuantityList = []
                            for x, y, z in zip(SupSrCodeList, SupItemCodeList, SupQuantityList):
                                z = int(z)
                                CQuantityList.append((x, y, z))
                            # add supply quantity with the same supplier code, item code together using dictionary
                            CSum = {}
                            for SrCode, ICode, quantity in CQuantityList:
                                if (SrCode, ICode) in CSum:
                                    CSum[SrCode, ICode] += quantity
                                else:
                                    CSum[SrCode, ICode] = quantity
                            CSum = list(CSum.items())  # change dictionary back to list
                            # add supplier code, item code that meet criteria into pk list
                            if select == "1":
                                pk = [(SrCode, ICode) for (SrCode, ICode), quantity in CSum if int(quantity) > int(ans)]
                            elif select == "2":
                                pk = [(SrCode, ICode) for (SrCode, ICode), quantity in CSum if int(quantity) < int(ans)]
                            elif select == "3":
                                pk = [(SrCode, ICode) for (SrCode, ICode), quantity in CSum if
                                      int(quantity) == int(ans)]
                            if pk == []:
                                print("No matching data.")
                            else:
                                for SrCode, ICode in pk:
                                    CCode = []
                                    # use index of supplier code, item code to find supply details
                                    for x, y in zip(SupSrCodeList, SupItemCodeList):
                                        CCode.append((x, y))
                                    index = [index for index, z in enumerate(CCode) if z == (SrCode, ICode)]
                                    for index in index:
                                        showSup(index)
                                    for item in CSum:  # display the total quantity
                                        if item[0] == (SrCode, ICode):
                                            print(item)
                                            break
                        else:
                            print("Invalid")
                else:
                    print("Invalid")
            else:
                print("Invalid")

        elif find == "5":  # distribution file
            provide = Dprovide()
            if provide == "exit":
                break
            elif provide == "1":  # search all distribution file
                if DisCodeList == []:
                    print("No data available at this moment.")
                else:
                    for index, x in enumerate(DisCodeList):
                        showDis(index)
            elif provide == "2":
                ans = input("Please enter the Item Code: ").upper().replace(" ", "")
                if ans in ItemCodeList:
                    user_choice = input("Date Range\n1: All time\n2: Specific Year and Month\nEnter 1 or 2 >>> ")
                    if user_choice == "1":
                        distribution_summary(ans)
                    elif user_choice == "2":
                        year, month = prompt_year_month()
                        distribution_summary(ans, year, month)
                else:
                    print("Invalid input")
            elif provide == "3":
                ans = CAns()  # prompt user for item code
                if ans in DisItemCodeList:  # use index of item code to find distribution details
                    index = [index for index, x in enumerate(DisItemCodeList) if x == ans]
                    for index in index:
                        showDis(index)
                else:
                    print("Invalid")
            elif provide == "4":
                ans = NAns()  # prompt user for item name
                if ans in ItemNameList:
                    index = ItemNameList.index(ans)  # use index of item name to find item code
                    pk = ItemCodeList[index]
                    if pk in DisItemCodeList:  # use index of item code to find distribution details
                        index = [index for index, x in enumerate(DisItemCodeList) if x == pk]
                        for index in index:
                            showDis(index)
                    else:
                        print("Doesn't have any relevant distribution")
                else:
                    print("Invalid")
            elif provide == "5":
                ans = CAns()  # prompt user for hospital code
                if ans in DisHosCodeList:  # use index of hospital code to find distribution details
                    index = [index for index, x in enumerate(DisHosCodeList) if x == ans]
                    for index in index:
                        showDis(index)
                else:
                    print("Invalid")
            elif provide == "6":
                ans = NAns()  # prompt user for hospital name
                if ans in HosNameList:
                    index = HosNameList.index(ans)  # use index of hospital name to find hospital code
                    pk = HosCodeList[index]
                    if pk in DisHosCodeList:  # use index of hospital code to find distribution details
                        index = [index for index, x in enumerate(DisHosCodeList) if x == pk]
                        for index in index:
                            showDis(index)
                    else:
                        print("Doesn't have any relevant distribution")
                else:
                    print("Invalid")
            elif provide == "7":
                ans = CAns()  # prompt user for distribution code
                if ans in DisCodeList:
                    index = DisCodeList.index(ans)  # use distribution code to find distribution details
                    showDis(index)
                else:
                    print("Invalid")
            elif provide == "8":
                try:
                    year, month, day = input("""\nPlease enter the date in number, split by comma (year, month, date)
: """).replace(" ", "").split(",")  # prompt user for date
                    # ensure that date is in integer
                    year = int(year)
                    month = int(month)
                    day = int(day)
                except ValueError:
                    print("Invalid")
                else:
                    try:
                        ans = date(year, month, day)  # ensure that date is in date format
                    except ValueError:
                        print("Invalid")
                    else:
                        select = fselect(ans)  # prompt user for date range
                        # add index of date that meet the criteria into index list
                        if select in ["1", "2", "3"]:
                            if select == "1":
                                index = [index for index, x in enumerate(DisDateList) if x > ans]
                            elif select == "2":
                                index = [index for index, x in enumerate(DisDateList) if x < ans]
                            elif select == "3":
                                index = [index for index, x in enumerate(DisDateList) if x == ans]
                            if index == []:
                                print("No matching data.")
                            else:
                                for index in index:  # use the index to find distribution details
                                    showDis(index)
                        else:
                            print("Invalid")
            elif provide == "9":
                choose = input("""\nPlease choose one
    1: separate all transaction
    2: combine transaction with same hospital
    3: combine transaction with same item
    4: combine transaction with the same item and hospital
Enter the code: """).lower().replace(" ", "")  # prompt user for combination
                if choose == "1":
                    ans = CAns()  # prompt user for quantity
                    try:
                        ans = int(ans)
                    except ValueError:
                        print("Invalid")
                    else:
                        select = fselect(ans)  # prompt user for quantity range
                        # add index of quantity that meet criteria into index list
                        if select in ["1", "2", "3"]:
                            if select == "1":
                                index = [index for index, x in enumerate(DisQuantityList) if int(x) > int(ans)]
                            elif select == "2":
                                index = [index for index, x in enumerate(DisQuantityList) if int(x) < int(ans)]
                            elif select == "3":
                                index = [index for index, x in enumerate(DisQuantityList) if int(x) == int(ans)]
                            if index == []:
                                print("No matching data.")
                            else:
                                for index in index:  # use the index to find distribution details
                                    showDis(index)
                        else:
                            print("Invalid")
                elif choose == "2":
                    ans = CAns()
                    try:
                        ans = int(ans)
                    except ValueError:
                        print("Invalid")
                    else:
                        select = fselect(ans)
                        if select in ["1", "2", "3"]:
                            # combine hospital code and distribution quantity into the same list
                            HosQuantityList = []
                            for x, y in zip(DisHosCodeList, DisQuantityList):
                                y = int(y)
                                HosQuantityList.append((x, y))
                            # add distribution quantity with the same hospital code together using dictionary
                            HosSum = {}
                            for code, quantity in HosQuantityList:
                                if code in HosSum:
                                    HosSum[code] += quantity
                                else:
                                    HosSum[code] = quantity
                            HosSum = list(HosSum.items())  # change back to list format
                            # add hospital code that total quantity meet criteria into pk list
                            if select == "1":
                                pk = [code for code, quantity in HosSum if int(quantity) > int(ans)]
                            elif select == "2":
                                pk = [code for code, quantity in HosSum if int(quantity) < int(ans)]
                            elif select == "3":
                                pk = [code for code, quantity in HosSum if int(quantity) == int(ans)]
                            if pk == []:
                                print("No matching data.")
                            else:
                                for x in pk:  # use index of hospital code to find distribution details
                                    index = [index for index, y in enumerate(DisHosCodeList) if y == x]
                                    for index in index:
                                        showDis(index)
                                    for item in HosSum:  # display total distribution quantity
                                        if item[0] == x:
                                            print(item)
                                            break
                        else:
                            print("Invalid")
                elif choose == "3":
                    ans = CAns()
                    try:
                        ans = int(ans)
                    except ValueError:
                        print("Invalid")
                    else:
                        select = fselect(ans)
                        if select in ["1", "2", "3"]:
                            # combine item code and distribution quantity into same list
                            ItemQuantityList = []
                            for x, y in zip(DisItemCodeList, DisQuantityList):
                                y = int(y)
                                ItemQuantityList.append((x, y))
                            # add distribution quantity with the same item code together using dictionary
                            ItemSum = {}
                            for code, quantity in ItemQuantityList:
                                if code in ItemSum:
                                    ItemSum[code] += quantity
                                else:
                                    ItemSum[code] = quantity
                            ItemSum = list(ItemSum.items())
                            # add the hospital code that total quantity that meet criteria into pk list
                            if select == "1":
                                pk = [code for code, quantity in ItemSum if int(quantity) > int(ans)]
                            elif select == "2":
                                pk = [code for code, quantity in ItemSum if int(quantity) < int(ans)]
                            elif select == "3":
                                pk = [code for code, quantity in ItemSum if int(quantity) == int(ans)]
                            if pk == []:
                                print("No matching data.")
                            else:
                                for x in pk:  # use the index to find distribution details
                                    index = [index for index, y in enumerate(DisItemCodeList) if y == x]
                                    for index in index:
                                        showDis(index)
                                    for item in ItemSum:  # display total distribution quantity
                                        if item[0] == x:
                                            print(item)
                                            break
                        else:
                            print("Invalid")
                elif choose == "4":
                    ans = CAns()
                    try:
                        ans = int(ans)
                    except ValueError:
                        print("Invalid")
                    else:
                        select = fselect(ans)
                        if select in ["1", "2", "3"]:
                            # combine hospital code, item code and distribution quantity into same list
                            CQuantityList = []
                            for x, y, z in zip(DisHosCodeList, DisItemCodeList, DisQuantityList):
                                z = int(z)
                                CQuantityList.append((x, y, z))
                            # add the distribution quantity with the same hospital code and item code together
                            CSum = {}
                            for HosCode, ICode, quantity in CQuantityList:
                                if (HosCode, ICode) in CSum:
                                    CSum[HosCode, ICode] += quantity
                                else:
                                    CSum[HosCode, ICode] = quantity
                            CSum = list(CSum.items())
                            # add the hospital code, item code that total quantity meet criteria into pk list
                            if select == "1":
                                pk = [(HosCode, ICode) for (HosCode, ICode), quantity in CSum if
                                      int(quantity) > int(ans)]
                            elif select == "2":
                                pk = [(HosCode, ICode) for (HosCode, ICode), quantity in CSum if
                                      int(quantity) < int(ans)]
                            elif select == "3":
                                pk = [(HosCode, ICode) for (HosCode, ICode), quantity in CSum if
                                      int(quantity) == int(ans)]
                            if pk == []:
                                print("No matching data.")
                            else:
                                for HosCode, ICode in pk:
                                    # use index of hospital code, item code to find distribution details
                                    CCode = []
                                    for x, y in zip(DisHosCodeList, DisItemCodeList):
                                        CCode.append((x, y))
                                    index = [index for index, z in enumerate(CCode) if z == (HosCode, ICode)]
                                    for index in index:
                                        showDis(index)
                                    for item in CSum:
                                        if item[0] == (HosCode, ICode):  # display total quantity
                                            print(item)
                                            break
                        else:
                            print("Invalid")
                else:
                    print("Invalid")
            else:
                print("Invalid")
        else:
            print("Invalid")


def save_item():
    with open("ppe.txt", "w") as file:
        for x in range(len(ItemCodeList)):
            file.write(ItemCodeList[x])
            file.write("\n" + ItemNameList[x])
            file.write("\n" + ItemQuantityList[x])
            file.write("\n" + ItemSrCodeList[x] + "\n")


def save_supplier():
    with open("supplier.txt", "w") as file:
        for x in range(len(SrCodeList)):
            file.write(SrCodeList[x])
            file.write("\n" + SrNameList[x] + "\n")


def save_hospital():
    with open("hospital.txt", "w") as file:
        for x in range(len(HosCodeList)):
            file.write(HosCodeList[x])
            file.write("\n" + HosNameList[x] + "\n")


def save_distribution():
    with open("distribution.txt", "w") as file:
        for x in range(len(DisCodeList)):
            file.write(DisCodeList[x])
            file.write("\n" + DisItemCodeList[x])
            file.write("\n" + DisHosCodeList[x])
            file.write("\n" + DisYearList[x])
            file.write("\n" + DisMonthList[x])
            file.write("\n" + DisDayList[x])
            file.write("\n" + DisQuantityList[x] + "\n")


def save_supply():
    with open("supply.txt", "w") as file:
        for x in range(len(SupCodeList)):
            file.write(SupCodeList[x])
            file.write("\n" + SupItemCodeList[x])
            file.write("\n" + SupSrCodeList[x])
            file.write("\n" + SupYearList[x])
            file.write("\n" + SupMonthList[x])
            file.write("\n" + SupDayList[x])
            file.write("\n" + SupQuantityList[x] + "\n")


def replace():
    while True:
        ans = input("""\nData from WHICH FILE are you going to replace?
    1: Item File
    2: Distribution File
    3: Supply File
    4: Hospital File
    5: Supplier File
Type 'back' to exit
Enter the code: """).lower().replace(" ", "")
        if ans == "back":
            break
        elif ans == "1":
            while True:
                item_choice = input("""\nWhat are you trying to update?
    1: Item Name
    2: Item Quantity
Type 'back' to return
Enter the code: """).lower().replace(" ", "")
                if item_choice == "back":
                    break
                elif item_choice == "1":
                    for index, x in enumerate(ItemCodeList):
                        showItem(index)
                    while True:
                        code = input("What item code (type 'back' to return): ").upper().replace(" ", "")
                        if code.lower() == "back":
                            break
                        elif code in ItemCodeList:
                            while True:
                                new_name = input("Enter new name (type 'back' to return): ").upper().strip()
                                if new_name.lower() == "back":
                                    break
                                elif new_name in ItemNameList:
                                    print("Already exist, please try again")
                                else:
                                    try:
                                        int(new_name)
                                    except ValueError:
                                        index = ItemCodeList.index(code)
                                        ItemNameList[index] = new_name
                                        save_item()
                                        for index, x in enumerate(ItemCodeList):
                                            showItem(index)
                                        print(f"Updated name: {new_name}")
                                        break
                                    else:
                                        print("Invalid item name")
                        else:
                            print("Invalid item code")
                elif item_choice == "2":
                    for index, x in enumerate(ItemCodeList):
                        showItem(index)
                    while True:
                        code = input("What item code (type 'back' to return): ").upper().replace(" ", "")
                        if code.lower() == "back":
                            break
                        elif code in ItemCodeList:
                            while True:
                                new_quantity = input("Enter new quantity (type 'back' to return): ").replace(" ", "")
                                if new_quantity.lower() == "back":
                                    break
                                else:
                                    try:
                                        new_quantity = int(new_quantity)
                                    except ValueError:
                                        print("Invalid quantity")
                                    else:
                                        if new_quantity < 0:
                                            print("Invalid quantity")
                                        else:
                                            index = ItemCodeList.index(code)
                                            ItemQuantityList[index] = str(new_quantity)
                                            save_item()
                                            for index, x in enumerate(ItemCodeList):
                                                showItem(index)
                                            print(f"Updated quantity: {new_quantity}")
                                            break
                        else:
                            print("Invalid item code")
                else:
                    print("Invalid code")

        elif ans == "2":
            while True:
                dist_choice = input("""\nWhat you trying to update
    1: Distribution Quantity
    2: Distribution Date
Type 'back' to return
Enter the code: """).lower().replace(" ", "")
                if dist_choice == "back":
                    break
                elif dist_choice == "1":
                    for index, x in enumerate(DisCodeList):
                        showDis(index)
                    while True:
                        code = input("What Distribution Code (type 'back' to return): ").upper().replace(" ", "")
                        if code.lower() == "back":
                            break
                        elif code in DisCodeList:
                            while True:
                                new_quantity = input("Enter new quantity (type 'back' to return): ").replace(" ", "")
                                if new_quantity.lower() == "back":
                                    break
                                else:
                                    try:
                                        new_quantity = int(new_quantity)
                                    except ValueError:
                                        print("Invalid quantity")
                                    else:
                                        if new_quantity < 0:
                                            print("Invalid quantity")
                                        else:
                                            index = DisCodeList.index(code)
                                            quantity = DisQuantityList[index]
                                            DisQuantityList[index] = str(new_quantity)
                                            if new_quantity > int(quantity):
                                                different = int(new_quantity) - int(quantity)
                                                pk = DisItemCodeList[index]
                                                index = ItemCodeList.index(pk)
                                                item_quantity = int(ItemQuantityList[index]) - int(different)
                                                if item_quantity < 0:
                                                    print("Item quantity not enough")
                                                else:
                                                    ItemQuantityList[index] = str(item_quantity)
                                            elif new_quantity < int(quantity):
                                                different = int(quantity) - int(new_quantity)
                                                pk = DisItemCodeList[index]
                                                index = ItemCodeList.index(pk)
                                                ItemQuantityList[index] = str(
                                                    int(ItemQuantityList[index]) + int(different))
                                            save_distribution()
                                            save_item()
                                            for index, x in enumerate(DisCodeList):
                                                showDis(index)
                                            print(f"Updated quantity: {new_quantity}")
                                            break
                        else:
                            print("Invalid distribution code")
                elif dist_choice == "2":
                    for index, x in enumerate(DisCodeList):
                        showDis(index)
                    while True:
                        code = input("What Distribution Code (type 'back' to return): ").upper().replace(" ", "")
                        if code.lower() == "back":
                            break
                        elif code in DisCodeList:
                            try:
                                new_year, new_month, new_day = input("""Please enter new date in number, split by comma (year, month, date)
: """).replace(" ", "").split(",")
                                year = int(new_year)
                                month = int(new_month)
                                day = int(new_day)
                            except ValueError:
                                print("Invalid date")
                            else:
                                try:
                                    new_date = date(year, month, day)
                                except ValueError:
                                    print("Invalid date")
                                else:
                                    index = DisCodeList.index(code)
                                    DisYearList[index] = new_year
                                    DisMonthList[index] = new_month
                                    DisDayList[index] = new_day
                                    DisDateList[index] = new_date
                                    Fnew_date = new_date.strftime('%Y-%m-%d')
                                    FDisDateList[index] = Fnew_date
                                    save_distribution()
                                    for index, x in enumerate(DisCodeList):
                                        showDis(index)
                                    print(f"Updated date: {Fnew_date}")
                        else:
                            print("Invalid distribution code")
                else:
                    print("Invalid code")

        elif ans == "3":
            while True:
                supply_choice = input("""\nWhat you trying to update?
    1: Supply Quantity
    2: Supply Date
Type 'back' to return
Enter the code: """).lower().replace(" ", "")
                if supply_choice == "back":
                    break
                elif supply_choice == "1":
                    for index, x in enumerate(SupCodeList):
                        showSup(index)
                    while True:
                        code = input("What Supply Code (type 'back' to return): ").upper().replace(" ", "")
                        if code.lower() == "back":
                            break
                        elif code in SupCodeList:
                            while True:
                                new_quantity = input("Enter new quantity (type 'back' to return): ").replace(" ", "")
                                if new_quantity.lower() == "back":
                                    break
                                else:
                                    try:
                                        new_quantity = int(new_quantity)
                                    except ValueError:
                                        print("Invalid quantity")
                                    else:
                                        if new_quantity < 0:
                                            print("Invalid quantity")
                                        else:
                                            index = SupCodeList.index(code)
                                            quantity = DisQuantityList[index]
                                            SupQuantityList[index] = str(new_quantity)
                                            if new_quantity > int(quantity):
                                                different = int(new_quantity) - int(quantity)
                                                pk = SupItemCodeList[index]
                                                index = ItemCodeList.index(pk)
                                                ItemQuantityList[index] = str(
                                                    int(ItemQuantityList[index]) + int(different))
                                            elif new_quantity < int(quantity):
                                                different = int(quantity) - int(new_quantity)
                                                pk = SupItemCodeList[index]
                                                index = ItemCodeList.index(pk)
                                                item_quantity = int(ItemQuantityList[index]) - int(different)
                                                if item_quantity < 0:
                                                    print("Item quantity not enough")
                                                else:
                                                    ItemQuantityList[index] = str(item_quantity)
                                            save_supply()
                                            save_item()
                                            for index, x in enumerate(SupCodeList):
                                                showSup(index)
                                            print(f"Updated quantity: {new_quantity}")
                                            break
                        else:
                            print("Invalid supply code")
                elif supply_choice == "2":
                    for index, x in enumerate(SupCodeList):
                        showSup(index)
                    while True:
                        code = input("What Supply Code (type 'back' to return): ").upper().replace(" ", "")
                        if code.lower() == "back":
                            break
                        elif code in SupCodeList:
                            try:
                                new_year, new_month, new_day = input("""Please enter new date in number, split by comma (year, month, date)
: """).replace(" ", "").split(",")
                                year = int(new_year)
                                month = int(new_month)
                                day = int(new_day)
                            except ValueError:
                                print("Invalid date")
                            else:
                                try:
                                    new_date = date(year, month, day)
                                except ValueError:
                                    print("Invalid")
                                else:
                                    index = SupCodeList.index(code)
                                    SupYearList[index] = new_year
                                    SupMonthList[index] = new_month
                                    SupDayList[index] = new_day
                                    SupDateList[index] = new_date
                                    Fnew_date = new_date.strftime('%Y-%m-%d')
                                    FSupDateList[index] = Fnew_date
                                    save_supply()
                                    for index, x in enumerate(SupCodeList):
                                        showSup(index)
                                    print(f"Updated date: {Fnew_date}")
                        else:
                            print("Invalid supply code")
                else:
                    print("Invalid code")

        elif ans == "4":
            for index, x in enumerate(HosCodeList):
                showHos(index)
            while True:
                code = input("""You only can update Hospital Name
What Hospital Code (type 'back' to return): """).upper().replace(" ", "")
                if code.lower() == "back":
                    break
                elif code in HosCodeList:
                    while True:
                        new_hospital_name = input("Enter new name (type 'back' to return): ").upper().strip()
                        if new_hospital_name.lower() == "back":
                            break
                        elif new_hospital_name in HosNameList:
                            print("Already exist, please try again")
                        else:
                            try:
                                int(new_hospital_name)
                            except ValueError:
                                index = HosCodeList.index(code)
                                HosNameList[index] = new_hospital_name
                                save_hospital()
                                for index, x in enumerate(HosCodeList):
                                    showHos(index)
                                print(f"Updated hospital name: {new_hospital_name}")
                                break
                            else:
                                print("Invalid hospital name")
                else:
                    print("Invalid hospital code")

        elif ans == "5":
            for index, x in enumerate(SrCodeList):
                showSr(index)
            while True:
                code = input("""You only can update Supplier Name
What Supplier Code (type 'back' to return): """).upper().replace(" ", "")
                if code.lower() == "back":
                    break
                elif code in SrCodeList:
                    while True:
                        new_supplier_name = input("Enter new name (type 'back' to return): ").upper().strip()
                        if new_supplier_name.lower() == "back":
                            break
                        elif new_supplier_name in SrNameList:
                            print("Already exist, please try again")
                        else:
                            try:
                                int(new_supplier_name)
                            except ValueError:
                                index = SrCodeList.index(code)
                                SrNameList[index] = new_supplier_name
                                save_supplier()
                                for index, x in enumerate(SrCodeList):
                                    showSr(index)
                                print(f"Updated supplier name: {new_supplier_name}")
                                break
                            else:
                                print("Invalid supplier name")
                else:
                    print("Invalid supplier code")
        else:
            print("Invalid code")


def delete_record(lists, index):
    for lst in lists:
        del lst[index]


def remove():
    while True:  # loop for remove
        ans = input("""\nWhich file's data are you going to delete?
    1: Distribution File
    2: Supply File
Type 'back' to exit
Enter the code: """).lower().replace(" ", "")  # prompt user on what file they wanna delete
        if ans == "back":  # return to previous menu
            break

        elif ans == "1":  # Distribution
            for index, x in enumerate(DisCodeList): #
                showDis(index)  # Display distribution.txt
            while True:
                # Prompt user to enter code/primary key for removal
                code_to_delete = input("Enter distribution code to delete (or 'back' to return): ").upper().replace(" ",
                                                                                                                    "")
                if code_to_delete.lower() == "back":  # return to previous menu
                    break
                elif code_to_delete in DisCodeList:
                    index = DisCodeList.index(code_to_delete)  # ensure data is in the list
                    showDis(index)
                    # confirmation for removal
                    confirm = input("Do you sure want to delete the whole record? (yes/no)\n>>> ").lower().replace(" ",
                                                                                                                   "")
                    if confirm == "yes":
                        quantity = DisQuantityList[index]
                        pk = DisItemCodeList[index]
                        delete_record(
                            [DisCodeList, DisItemCodeList, DisHosCodeList, DisYearList, DisMonthList, DisDayList,
                             DisQuantityList, DisDateList, FDisDateList], index)  # Removal process
                        index = ItemCodeList.index(pk)
                        ItemQuantityList[index] = str(int(ItemQuantityList[index]) + int(quantity))  # calculation of quatity in item
                        save_distribution()  # saving new data/list in distribution.txt
                        save_item()  # saving new data/list in item.txt
                        for index, x in enumerate(DisCodeList):
                            showDis(index)
                        print(f"Deleted distribution record with code: {code_to_delete}")  # Display new list after removal
                    elif confirm == "no":
                        break  # return to loop prompt user distribution removal
                    else:
                        print("Invalid")  # user input other than yes/no
                else:
                    print("Invalid code")  # input is not in the primary key in distribution.txt

        elif ans == "2":  # Supply
            for index, x in enumerate(SupCodeList):
                showSup(index)  # display supply.txt
            while True:  # loop for supply removal
                # prompt user for code/ prmary key in supply for removal
                code_to_delete = input("Enter supply code to delete (or 'back' to return): ").upper().replace(" ", "")
                if code_to_delete.lower() == "back":
                    break  # return to previous menu
                elif code_to_delete in SupCodeList:
                    index = SupCodeList.index(code_to_delete)  # ensure primary key in list
                    showSup(index)  # display supply.txt
                    quantity = SupQuantityList[index]
                    pk = SupItemCodeList[index]
                    index1 = ItemCodeList.index(pk)
                    item_quantity = int(ItemQuantityList[index1]) - int(quantity)  # calcalation on total quatity in item.txt
                    if item_quantity < 0:
                        print("Item quantity not enough")  # ensure that quatity in item.txt is above 0
                    else:
                        confirm = input("Do you sure want to delete the whole record? (yes/no)\n>>> ").lower().replace(
                            " ", "")  # confirmation of removal
                        if confirm == "yes":
                            delete_record(
                                [SupCodeList, SupItemCodeList, SupSrCodeList, SupYearList, SupMonthList, SupDayList,
                                 SupQuantityList, SupDateList, FSupDateList], index)  # removal process for supply
                            ItemQuantityList[index1] = str(item_quantity)
                            save_supply()  # saving changes in supply.txt
                            save_item()  # saving quatity changes in item.txt
                            for index, x in enumerate(SupCodeList):
                                showSup(index)  # display new supply.txt after removal
                            print(f"Deleted supply record with code: {code_to_delete}")
                        elif confirm == "no":
                            break  # return to loop for supply removal
                        else:
                            print("Invalid")  # display when user input is other than yes/no
                else:
                    print("Invalid code")  # display when user input is not primary key in supply
        else:
            print("Invalid code")  # display when user input is other than 1 , 2 or back


def add():
    while True:  # loops for when input is invalid or back from other branches
        # chooses which file to add (update) data
        add_option = input("""\nADD DATA OPTIONS
1: Item (PPE)
2: Hospital
3: Supplier
4: Distribution
5: Supply
6: back
Enter 1, 2, 3, 4, 5, or 6
>>> """)

        if add_option == "1":
            update_ppe_hos_sr_inventory(ppe_list, "ppe.txt")
        elif add_option == "2":
            update_ppe_hos_sr_inventory(hospital_list, "hospital.txt")
        elif add_option == "3":
            update_ppe_hos_sr_inventory(supplier_list, "supplier.txt")

        # additional access point for Update functionality for distribution.txt & supply.txt
        elif add_option == "4":  # same function used in Update
            update_dis_sup_inventory(distribution_list, "distribution.txt")
        elif add_option == "5":  # same function used in Update
            update_dis_sup_inventory(supply_list, "supply.txt")

        elif add_option == "6":
            break  # breaks add option loop and return to amendment loop
        else:
            print("Invalid input. Try again.")


def prompt_year_month():
    # prompts dates that are used to specify report date
    while True:
        try:  # correct input
            report_year, report_month = input(
                "\nEnter YEAR (20xx) and MONTH (1-12) of the report\n(separate with comma (,) >>> ").split(",")
            report_year = int(report_year)
            report_month = int(report_month)
            if report_year not in range(2020, 2025):  # limit year range
                print("Error - Year out of range (2020-2024).")
            # use "if" instead of "elif"
            # because 1st and 2nd condition can happen simultaneously
            if report_month not in range(1, 13):  # a year has 12 months
                print("Error - Invalid month.")
            if report_year in range(2020, 2025) and report_month in range(1, 13):  # valid year-month
                report_year = str(report_year)
                report_month = str(report_month)
                # convert string to simplify print statement
                return report_year, report_month
        except ValueError:
            # handle errors when input cannot unpack into 2 values
            # handle error when input cannot be converted into integers
            print(
                "Invalid input.\n1. Use numbers to represent Year and Month.\n2. Separate year and month with a comma.")


def ppe_supply_report():
    # generate report which summarises supply transactions
    # ppe supplied by each supplier and its amount
    report_year, report_month = prompt_year_month()  # obtain year & month of report
    # declare list for append()
    sr_display_list = []
    ppe_display_list = []
    quantity_display_list = []

    # list out all ppe_ID from ItemCodeList, extracted from ppe.txt
    for ppe_index, ppe in enumerate(ItemCodeList):
        sr_ID = ItemSrCodeList[ppe_index]
        # stores ppe in a nested list, before in outer list
        # because one supplier can supply more than one ppe
        temporary_ppe_display_list = [ppe]

        # locate quantity of ppe supplied
        total_quantity = 0
        for sup_index, sup_ID in enumerate(SupCodeList):
            quantity = SupQuantityList[sup_index]
            if SupItemCodeList[sup_index] == ppe:
                if SupYearList[sup_index] == report_year and SupMonthList[sup_index] == report_month:
                    # if item same as ppe
                    # adds quantity together
                    total_quantity += int(quantity)
        # follows ppe to have nested list first
        # to simplify display code
        temporary_quan_list = [total_quantity]

        if sr_ID not in sr_display_list:
            # appends all in list
            # ready to be displayed
            sr_display_list.append(sr_ID)
            ppe_display_list.append(temporary_ppe_display_list)
            quantity_display_list.append(temporary_quan_list)
        # if same supplier (already exist in supplier display list)
        elif sr_ID in sr_display_list:
            # if same supplier (already exist in supplier display list)
            # append second ppe in existing nested list
            # index of nested list == index of supplier ID
            sr_index = sr_display_list.index(sr_ID)
            ppe_display_list[sr_index].append(ppe)
            quantity_display_list[sr_index].append(total_quantity)

    # simple if-else for clear & nice output
    if int(report_month) in range(1, 10):
        report_month = "0" + report_month
    else:
        pass
    print(f"\n{report_year}-{report_month} SUPPLY REPORT")

    # code below is used to generate output in the form of a table
    # define column length and table length
    total_quan_sum = []  # will contain total supply quantity for each ppe
    sr_ID_len = 18
    ppe_ID_len = 13
    quantity_len = 18
    quan_sum_len = 35
    table_length = sr_ID_len + ppe_ID_len + quantity_len + quan_sum_len
    # cleanly display report in table form
    print("-" * table_length)
    # column width: 17, 12, 12
    print("| Supplier_ID     | ppe_ID     | Quantity (unit) | Total Quantity Supplied (units) |")
    print("-" * table_length)
    for num in range(len(sr_display_list)):  # display all existing suppliers
        sr_display = sr_display_list[num]  # "for" loop for this specific supplier
        ppe_display = ppe_display_list[num]  # locate the ppe supplied
        ppe_quantity = quantity_display_list[num]  # locate the quantity of ppe supplied
        quan_sum = sum(quantity_display_list[num])
        total_quan_sum.append(quan_sum)
        # var named as "xx_gap" --> for display purpose
        # calculate the spaces needed to be printed after displaying a data value
        # do not affect output data
        sr_gap = sr_ID_len - 2 - len(sr_display)
        quan_sum_gap = quan_sum_len - 3 - len(str(quan_sum))
        ppe_gap = ppe_ID_len - 2 - len(ppe_display[0])
        quantity_gap = quantity_len - 2 - len(str(ppe_quantity[0]))
        # display effect
        print(
            f"| {sr_display}{" " * sr_gap}| {ppe_display[0]}{" " * ppe_gap}| {ppe_quantity[0]}{" " * quantity_gap}| {quan_sum}{" " * (quan_sum_gap)}|")

        if len(ppe_display) > 1:  # different display effect if supplier supplies more than 1 ppe
            print(
                f"|{" " * (sr_ID_len - 1)}|{"-" * (ppe_ID_len - 1)}|{"-" * (quantity_len - 1)}|{" " * (quan_sum_len - 2)}|")
            ppe_display_len = len(ppe_display)

            for index in range(1, ppe_display_len):  # locate other ppe and its quantity with "index"
                ppe_gap = ppe_ID_len - 2 - len(ppe_display[index])
                quantity_gap = quantity_len - 2 - len(str(ppe_quantity[index]))
                print(
                    f"|{" " * (sr_ID_len - 1)}| {ppe_display[index]}{" " * ppe_gap}| {ppe_quantity[index]}{" " * quantity_gap}|{" " * (quan_sum_len - 2)}|")

                if index != ppe_display_len - 1:
                    print(
                        f"|{" " * (sr_ID_len - 1)}|{"-" * (ppe_ID_len - 1)}|{"-" * (quantity_len - 1)}|{" " * (quan_sum_len - 2)}|")
        print("-" * table_length)
    # calculate sum of all ppe quantity and display it
    print(f"{" " * (table_length - quan_sum_len - 6)}Total:  {sum(total_quan_sum)}")


def ppe_distribution_report():
    # hosp_code, ppe code, quantity
    # total distribution quantity
    report_year, report_month = prompt_year_month()  # obtain year & month of report
    # declare list used for display
    quantity_display_list = []

    for hos_ID in HosCodeList:  # run through all hospitals
        nested_quantity_list = []
        for loop in range(len(ItemCodeList)):
            nested_quantity_list.append(0)  # default quantity for each ppe

        for dis_index, dis_ID in enumerate(DisCodeList):  # run through all distribution transactions
            # check if year-month of current distribution transaction matches user input
            if DisYearList[dis_index] == report_year and DisMonthList[dis_index] == report_month:
                # check if hospital of current distribution transaction equals to main "for" loop's hospital
                if DisHosCodeList[dis_index] == hos_ID:
                    quantity = DisQuantityList[dis_index]  # retrieve distribution quantity
                    ppe_index = ItemCodeList.index(DisItemCodeList[dis_index])
                    # index of item in ItemCodeList corresponds to index of quantity in nested_quantity_list
                    # add quantity in the right index that belongs to the item
                    nested_quantity_list[ppe_index] += int(quantity)
        # finish checking all distributions for one hospital
        quantity_display_list.append(nested_quantity_list)

    # simple if-else for clear & nice output
    if int(report_month) in range(1, 10):
        report_month = "0" + report_month
    else:
        pass
    print(f"\n{report_year}-{report_month} DISTRIBUTION REPORT")

    # display effect
    # var named "xx_len" do not affect final output value
    # determines blank spaces needed to be printed -> only for good-looking display
    ppe_len = len(ItemCodeList)
    ppe_char_len = 0
    for ppe in ItemCodeList:
        ppe_char_len += len(ppe)
    table_len = 17 + (ppe_char_len + (ppe_len - 1) * 7) + 26
    # display effect for a table
    print(f"{"-" * table_len}")
    print(
        f"| Hospital_ID  | Quantity (unit) per ppe_ID{" " * (ppe_char_len + (ppe_len - 1) * 7 - 26)}     | Total PPE         |")
    print(f"|{" " * 14}|-{"-" * (ppe_char_len + (ppe_len - 1) * 7)}-----| Quantity (unit)   |")
    print(f"|{" " * 14}| {("     | ").join(ItemCodeList)}     |{" " * 19}|")
    print(f"{"-" * table_len}")

    total_quan_sum = []  # later contains total ppe obtained by each hospital
    for hos_index, hos_ID in enumerate(HosCodeList):  # displays for every hospital
        quantity_sum = sum(quantity_display_list[hos_index])  # total ppe obtained by the hospital
        total_quan_sum.append(quantity_sum)
        quan_sum_len = len(str(quantity_sum))
        print(f"| {hos_ID}{" " * (13 - len(hos_ID))}|", end="")
        for ppe_index, ppe in enumerate(ItemCodeList):  # unpack ppe to be displayed
            # locates the quantity of current ppe in nested loop, based on the current hospital in main loop
            ppe_quantity = quantity_display_list[hos_index][ppe_index]
            quan_char_len = len(str(ppe_quantity))
            # display effect
            print(f" {ppe_quantity}{" " * (7 - quan_char_len)}|", end="")
        print(f" {quantity_sum}{" " * (18 - quan_sum_len)}|")
        print(f"{"-" * table_len}")
    # calculate total ppe obtained by all hospitals
    print(f"{" " * (table_len - 27)}Total:  {sum(total_quan_sum)}")


def overall_transaction_report():
    # display all distribution & supply transactions
    report_year, report_month = prompt_year_month()  # obtain year & month of report
    transaction_list = []  # overall list to store transactions

    for dis_index, dis_ID in enumerate(DisCodeList):  # distributions that match the year-month
        if DisYearList[dis_index] == report_year and DisMonthList[dis_index] == report_month:
            distribution_list = [DisCodeList[dis_index], DisItemCodeList[dis_index], DisHosCodeList[dis_index],
                                 DisQuantityList[dis_index], FDisDateList[dis_index]]
            # store distribution transactions (nested list) in overall list
            transaction_list.append(distribution_list)

    for sup_index, sup_ID in enumerate(SupCodeList):  # supply that match the year-month
        if SupYearList[sup_index] == report_year and SupMonthList[sup_index] == report_month:
            supply_list = [SupCodeList[sup_index], SupItemCodeList[sup_index], SupSrCodeList[sup_index],
                           SupQuantityList[sup_index], FSupDateList[sup_index]]
            # store supply transactions (nested list) in overall list
            transaction_list.append(supply_list)

    while True:  # loop when input is invalid
        # prompt for arrangement order
        order_prompt = input("\nSort transactions according to date\n1: Ascending\n2: Descending\nEnter 1 or 2 >>> ")
        if order_prompt == "1":
            order = False  # descending order of date
            break
        elif order_prompt == "2":
            order = True  # ascending order of date
            break
        else:
            print("Invalid input. Try again.")

    # use sorted() to sort according to date in specified order
    # sort based on key specified, which is date
    # parse date which is the last item of every transaction to given format of datetime
    sorted_transactions = sorted(transaction_list, key=lambda record: datetime.strptime(record[4], "%Y-%m-%d"),
                                 reverse=order)

    # display effect
    if int(report_month) in range(1, 10):
        report_month = "0" + report_month
    else:
        pass

    # display effect
    print(f"\n{report_year}-{report_month} OVERALL TRANSACTION REPORT")
    print(f"{"-" * 95}")
    print(f"| Distribution Code(D) /  | PPE Code | Hospital Code (HOS) /  | Quantity (Units) | Date       |")
    print(f"| Supply Code (S)         |          | Supplier Code (SR)     |                  |            |")
    print(f"{"-" * 95}")
    stock_flow = 0  # default
    # unpack each nested list from overall list
    for dis_sup_code, item_code, sr_hos_code, quantity, trans_date in sorted_transactions:
        display_quantity = ""
        if dis_sup_code[0] == "D":  # identified as distribution = decrease in stock, hence "-" for display
            stock_flow -= int(quantity)
            display_quantity = "- " + quantity
        elif dis_sup_code[0] == "S":  # identified as supply = increase in stock, hence "+" for display
            stock_flow += int(quantity)
            display_quantity = "+ " + quantity
        # display effect for each transaction
        print(f"| {dis_sup_code}{" " * (24 - len(dis_sup_code))}| {item_code}{" " * (9 - len(item_code))}| "
              f"{sr_hos_code}{" " * (23 - len(sr_hos_code))}| {display_quantity}{" " * (15 - len(quantity))}| "
              f"{trans_date} |")
        print(f"{"-" * 95}")

    # display effect for overall stock flow
    str_stock_flow = "0"
    if stock_flow > 0:  # positive flow
        str_stock_flow = "+ " + str(stock_flow)
    elif stock_flow < 0:  # negative flow
        str_stock_flow = "- " + str(stock_flow).removeprefix("-")
    elif stock_flow == 0:
        str_stock_flow = str(stock_flow)
    print(f"{" " * 51}Stock Flow:  {str_stock_flow}{" " * (20 - len(str_stock_flow))}")


def user_navigation():
    loop = 0
    while loop == 0:
        back_opt = input("\n1: Back to Generate Reports page\n2: Back to Main Menu\nEnter 1 or 2\n>>> ")
        if back_opt == "1":
            loop += 1  # break prompt loop and return to reports loop
            return back_opt
        elif back_opt == "2":
            loop += 1
            return back_opt
        else:
            print("Invalid input. Try again.")  # loops for correct answer


# Define lists for different types of data
supplier_list = ["supplier code", "supplier name"]
ppe_list = ["item code", "ppe name", "ppe quantity", "supplier code"]
hospital_list = ["hospital code", "hospital name"]
distribution_list = ["distribution code", "item code", "hospital code", "distribution year", "distribution month",
                     "distribution day", "distribution quantity"]
supply_list = ["supply code", "item code", "supplier code", "supply year", "supply month", "supply day",
               "supply quantity"]

# Define the file check dictionary to specify the number of lines expected in each file
file_check = {
    "ppe.txt": 24,  # Expected number of lines for PPE data
    "hospital.txt": 6,  # Expected number of lines for Hospital data
    "supplier.txt": 6,  # Expected number of lines for Supplier data
    "distribution.txt": None,  # Expected number of lines for Distribution data
    "supply.txt": None  # Expected number of lines for Supply data
}
boot_system()
print("**PERSONAL PROTECTIVE EQUIPMENT INVENTORY MANAGEMENT SYSTEM**")
if admin_login() is True:
    index = 0
    ans = 0
    # read all 5 files for data
    # data stored in list to be used in functionalities
    with open("ppe.txt", "r") as item:
        line = [x.strip() for x in item.readlines()]
        ItemCodeList = line[0::4]
        ItemNameList = line[1::4]
        ItemQuantityList = line[2::4]
        ItemSrCodeList = line[3::4]

    with open("supplier.txt", "r") as supplier:
        line = [x.strip() for x in supplier.readlines()]
        SrCodeList = line[0::2]
        SrNameList = line[1::2]

    with open("hospital.txt", "r") as hospital:
        line = [x.strip() for x in hospital.readlines()]
        HosCodeList = line[0::2]
        HosNameList = line[1::2]

    with (open("distribution.txt", "r") as distribution):
        line = [x.strip() for x in distribution.readlines()]
        DisCodeList = line[0::7]
        DisItemCodeList = line[1::7]
        DisHosCodeList = line[2::7]
        DisYearList = line[3::7]
        DisMonthList = line[4::7]
        DisDayList = line[5::7]
        DisQuantityList = line[6::7]
        DisDateList = []
        for x, y, z in zip(DisYearList, DisMonthList, DisDayList):
            x = int(x)
            y = int(y)
            z = int(z)
            DisDateList.append(date(x, y, z))
        FDisDateList = [d.strftime('%Y-%m-%d') for d in DisDateList]

    with (open("supply.txt", "r") as supply):
        line = [x.strip() for x in supply.readlines()]
        SupCodeList = line[0::7]
        SupItemCodeList = line[1::7]
        SupSrCodeList = line[2::7]
        SupYearList = line[3::7]
        SupMonthList = line[4::7]
        SupDayList = line[5::7]
        SupQuantityList = line[6::7]
        SupDateList = []
        for x, y, z in zip(SupYearList, SupMonthList, SupDayList):
            x = int(x)
            y = int(y)
            z = int(z)
            SupDateList.append(date(x, y, z))
        FSupDateList = [d.strftime('%Y-%m-%d') for d in SupDateList]

    # Main Menu
    while True:  # loops back when input is invalid or back from other branches
        # user chooses what to do
        user_path = input("""\nINVENTORY MANAGEMENT FUNCTIONALITIES
1: Update Item Inventory
2: View, Search & Track Inventory
3: Amend Inventory
4: Generate Reports
5: Exit Program
Enter 1, 2, 3, 4, or 5
>>> """)
        if user_path == "1":  # View, Search & Track Inventory
            while True:  # loops for when input is invalid or back from other branches
                # user chooses which file to update
                update_option = input("""\nUPDATE ITEM INVENTORY OPTIONS
1: Distribution Transactions
2: Supply Transactions
3: back
Enter 1, 2, or 3
>>> """)
                if update_option == "1":  # distribution
                    update_dis_sup_inventory(distribution_list, "distribution.txt")
                elif update_option == "2":  # supply
                    update_dis_sup_inventory(supply_list, "supply.txt")
                elif update_option == "3":
                    break  # breaks Update loop and return to Main Menu loop
                else:
                    print("Invalid input. Try again.")

        elif user_path == "2":  # Update Transactions functionality
            search(ItemQuantityList)

        elif user_path == "3":  # Amendment - Replace, add (update) , delete
            while True:  # loops for when input is invalid or back from other branches
                # user chooses to the type of change being made
                change_option = input("""\nINVENTORY AMENDMENT OPTIONS
1: Replace Data 
2: Add Data
3: Delete Data
4: back
Enter 1, 2, 3, or 4
>>> """)
                if change_option == "1":
                    replace()  # change current data with new data
                elif change_option == "2":
                    add()  # add record (or known as update)
                elif change_option == "3":
                    remove()  # delete certain record
                elif change_option == "4":
                    break  # breaks Amendment loop and return to Main Menu loop
                else:
                    print("Invalid input. Try again.")

        elif user_path == "4":  # Generate Transaction Reports
            while True:  # loops for when input is invalid or back from other branches
                back_opt = "0"
                report_option = input("""\nREPORT GENERATION OPTIONS
1: PPE Distribution Report
2: PPE Supply Report
3: Overall Transaction Report
4: back
Enter 1, 2, 3, or 4
>>> """)
                if report_option == "1":  # ppe distribution for hospitals
                    ppe_distribution_report()
                    back_opt = user_navigation()  # back to menu signal

                if report_option == "2":  # supply provided by suppliers
                    ppe_supply_report()
                    back_opt = user_navigation()  # back to menu signal

                if report_option == "3":  # all distributions and supplies made
                    overall_transaction_report()
                    back_opt = user_navigation()  # back to menu signal

                if back_opt == "2" or report_option == "4":
                    break  # signals to exit Generate Reports loop

                if back_opt == "1":
                    pass  # return to start of loop

                else:  # invalid & loops back to prompting
                    print("Invalid input.")

        elif user_path == "5":  # End program
            print("Have a nice day!")
            exit()  # stop running

        else:  # reminder for invalid input
            print("Invalid input. Try again.")
