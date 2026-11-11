
import json
from pathlib import Path
import copy



#validation function

# Validation function
def validate(data):

    #below conditional booleans check to ensure that each part of the DFA is correct and labeled properly

    #all data present checks to ensure all data fields are present and not missing
    all_data_present = False

    #this checks to ensure that the data within the data fields are correct
    data_correct = False

    #this checks to make sure the start state is within the list of states
    valid_start_state = False

    #this checks to ensure that the accept states are within the list of states
    valid_accept_state = False

    #this checks to make sure all transitions are correct (ie. no transitions into non-existent states, etc.)
    valid_transitions = False


    if ("states" in data
        and "alphabet" in data
        and "start_state" in data
        and "accept_states" in data
        and "transitions" in data):
        all_data_present = True
    else:
        return False


    #checks to ensure all data values are of the correct type
    states_type_correct = isinstance(data["states"], list)
    alphabet_type_correct = isinstance(data["alphabet"], list)
    start_type_correct = isinstance(data["start_state"], str)
    accept_type_correct = isinstance(data["accept_states"], list)
    transitions_type_correct = isinstance(data["transitions"], dict)

    #checks to ensure data is in the correct formats
    data_correct = (
    states_type_correct
    and alphabet_type_correct
    and start_type_correct
    and accept_type_correct
    and transitions_type_correct
)
    if not data_correct:
        return False

    #for loop to check that the start state is within the list of state. 
    for state in data["states"]:

        #if it is, break the loop and set as true
        if state == data["start_state"]:
            valid_start_state = True
            break

    #if not, return false
    if not valid_start_state:
        return False

    #reuses the logic for the check for the start state.
    valid_accept_state = True

    #checks to make sure there are no invalid states (ie. accept states outside the list of states)
    for accept_state in data["accept_states"]:

        #if a state is invalid, set as False. If not, we continue on
        if accept_state not in data["states"]:
            valid_accept_state = False
            break

    if not valid_accept_state:
        return False

    valid_transitions = True

    #checks to ensure all transitions for each state is valid (ie. a state does not transition into a non-existent state)
    for state, transitions in data["transitions"].items():

        #if the source state is not within the list of states, we set as false
        if state not in data["states"]:
            valid_transitions = False
            break

        for symbol, destination in transitions.items():
            #if a state references a non-existent symbol during a transition, we also set as false
            if symbol not in data["alphabet"]:
                valid_transitions = False
                break

            #if a state transitions into a non-existent state, we set as false
            if destination not in data["states"]:
                valid_transitions = False
                break

        if not valid_transitions:
            break
    #exit and return false if transitions fail. Otherwise, set valid_transitions as true
    if not valid_transitions:
        return False

    
    # Checks that every state has a transition for every symbol within the alphabet
    for state in data["states"]:

        #checks to ensure the source state actually exists
        if state not in data["transitions"]:
            valid_transitions = False
            break

        #makes sure all alphabet symbols have a corresponding transition
        for symbol in data["alphabet"]:

            if symbol not in data["transitions"][state]:
                valid_transitions = False
                break

        if not valid_transitions:
            break

    if not valid_transitions:
        return False

    #if all checks pass, return True. Otherwalse, false
    if (all_data_present
    and data_correct
    and valid_start_state
    and valid_accept_state
    and valid_transitions):
        return True

    return False

# Reads the input DFA
try:
    #hardcoded name for now
    with open("input_dfa.json", "r") as file:
        data = json.load(file)

# if the DFA is invalid or does not exist, print an exception
except json.JSONDecodeError:
    print("[ERROR] Invalid JSON formatting.")

except FileNotFoundError:
    print("[ERROR] Input file not found.")

#put an else here for "graceful error handling" (code freaks out if we dont do this)
else:

# LOGIC

    # Checks for valid DFA
    is_valid = validate(data)


    #if not valid, print an error
    if not is_valid:
        print("[ERROR] Invalid DFA.")

    #if the DFA is valid, perform the logic and print the complement
    else:

        #copy the original dfa (by this point the dfa has a valid structure so we only need to change one of the fields)
        complement_dfa = copy.deepcopy(data)

        #stores all unique states not in the original accepting states (ie. its complement)
        complement_accept_states = []

        for state in data["states"]:
            #adds any states outside the original accepting states into the list of complement states 
            if state not in data["accept_states"]:
                complement_accept_states.append(state)

        #replace the original accepting states with its complement
        complement_dfa["accept_states"] = complement_accept_states

        # Prints a formatted message showing the original vs. changed DFA
        print("Original DFA:")
        print(json.dumps(data, indent=4))
        print()

        print("Complement DFA:")
        print(json.dumps(complement_dfa, indent=4))
        print()

        #saves the output dfa within the same directory
        with open("output_dfa.json", "w") as file:
            json.dump(complement_dfa, file, indent=4)
