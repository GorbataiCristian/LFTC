import copy

FA_INPUT = 'FA_integer.in'

class Transition:
    def __init__(self, state_from, state_to, value):
        self.state_from = state_from
        self.state_to = state_to
        self.value = value

    def getStateFrom(self):
        return self.state_from

    def getStateTo(self):
        return self.state_to

    def setStateFrom(self, state):
        self.state_from = state

    def setStateTo(self, state):
        self.state_to = state

    def getValue(self):
        return self.value

    def __str__(self):
        return str(self.state_from) + ' -> ' + \
            str(self.state_to) + '(' + \
            str(self.value) + ')'

class FiniteAutomata:
    def __init__(self, transitions, initial_state, final_states):
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

    def getTransitions(self):
        return self.transitions

    def getFinalStates(self):
        return self.final_states

    def getInitialState(self):
        return self.initial_state

    def getTransitionsFromState(self, state):
        transitions = []
        for transition in self.transitions:
            if transition.getStateFrom() == state:
                transitions.append(transition)
        return transitions

    def checkIfFinalState(self, state):
        return state in self.final_states

    def checkSequence(self, sequence):
        starting_sequence = sequence
        current_state = self.initial_state

        while sequence:
            possible_transitions = self.getTransitionsFromState(current_state)
            found = False
            for transition in possible_transitions:
                if sequence.find(transition.getValue()) == 0:
                    current_state = transition.getStateTo()
                    sequence = sequence[len(transition.getValue()):]
                    if sequence == "":
                        if transition.getStateTo() in self.final_states:
                            # print('valid sequence:', starting_sequence)
                            return True
                        else:
                            # print('invalid sequence:', starting_sequence)
                            return False

                    found = True
                    break
            if not found:
                # print('invalid sequence:', starting_sequence)
                return False

    def getStates(self):
        states = []
        for transition in self.transitions:
            if transition.getStateFrom() not in states:
                states.append(transition.getStateFrom())
            if transition.getStateTo() not in states:
                states.append(transition.getStateTo())
        return states

    def getAlphabet(self):
        alphabet = []
        for transition in self.transitions:
            characters = list(transition.getValue())
            for char in characters:
                if char not in alphabet:
                    alphabet.append(char)
        return alphabet


    def __str__(self):
        transitions = copy.deepcopy(self.transitions)
        for transition in transitions:
            if transition.getStateFrom() == self.initial_state:
                transition.setStateFrom(">" + str(transition.getStateFrom()))
            if transition.getStateFrom() in self.final_states:
                transition.setStateFrom("*" + str(transition.getStateFrom()))
            if transition.getStateTo() in self.final_states:
                transition.setStateTo("*" + str(transition.getStateTo()))

        string_builder = ""
        for transition in transitions:
            string_builder += str(transition) + '\n'
        return string_builder[:-1]


def read_FA_file(FA_file):
    transitions = []
    initial_state = None
    final_states = []
    with open(FA_file) as fa:
        for line in fa:
            line = line.split()
            state1 = line[0]
            state2 = line[1]
            value = line[2]

            # > for initial states
            if state1[0] == '>':
                if len(state1) == 1:
                    print(f'FA error -- invalid initial: "{state1}"')
                    return None
                state1 = state1[1:]
                if initial_state is not None and initial_state != state1:
                    print("FA error -- you cannot have more than 1 initial state")
                    return None
                initial_state = state1

            if state1[0] == '*':
                if len(state1) == 1:
                    print(f'FA error -- invalid starting: "{state1}"')
                    return None
                state1 = state1[1:]

            # * for final states
            if state2[0] == '*':
                if len(state2) == 1:
                    print(f'FA error -- invalid final: "{state1}"')
                    return None
                state2 = state2[1:]

                if state2 not in final_states:
                    final_states.append(state2)

            transitions.append(Transition(state1, state2, value))

    return FiniteAutomata(transitions, initial_state, final_states)


def menu_help():
    print("help : menu")
    print("1 : set of states")
    print("2 : alphabet")
    print("3 : all transitions")
    print("4 : set of final states")
    print("exit : quit")

def menu_run(FA):
    menu_help()
    while True:
        cmd = input("insert command>>>")
        if cmd == '1':
            print(FA.getStates())
        elif cmd == '2':
            print(FA.getAlphabet())
        elif cmd == '3':
            print([str(e) for e in FA.getTransitions()])
        elif cmd == '4':
            print(FA.getFinalStates())
        elif cmd == 'help':
            menu_help()
        elif cmd == 'exit':
            return

if __name__ == "__main__":
    FA = read_FA_file(FA_INPUT)
    menu_run(FA)



