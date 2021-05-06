import collections as col
import sys


class DFA:
    def __init__(self, dicts, final_states, alpha):
        self.dicts = dicts
        self.final_states = final_states
        self.alpha = alpha

    def __str__(self): 
        str_out = str(len(self.dicts)) + "\n"
        for i in self.final_states:
            str_out += str(i) + " "
        str_out += "\n"
        for i in range(0, len(self.dicts)):
            for ch in self.alpha:
                str_out += str(i) + " " + str(ch) + " " + str(self.dicts[i][ch]) + "\n"
        return str_out

class NFA:
    def __init__(self, dicts, final_states, alpha):
        self.dicts = dicts
        self.final_states = final_states
        self.alpha = alpha

    def __str__(self): 
        str_out = str(self.alpha) + "\n"
        for i in range(0, len(self.dicts)):
            str_out += "Din starea " + str(i) + " am tranzitiile: " + str(self.dicts[i]) + "\n"
        return str_out
            

def read_nfa(inp):
    alpha = set()
    nr_states = int(inp.readline())
    final_states = list(map(int, inp.readline().split()))
    dicts = []
    for i in range(0, nr_states):
        dicts.append({})
    input_line = inp.readline()
    while True:
        if input_line == "":
            break
        line = list(input_line.split())
        if len(line) == 0:
            break
        dict_crt = dicts[int(line[0])]
        alpha.add(line[1])
        dict_crt[line[1]] = ""

        for i in range(2, len(line)):
            dict_crt[line[1]] += line[i] + " "
        input_line = inp.readline()

    ret = NFA(dicts, final_states, alpha)
    return ret

def id_to_states(id):
    return list(map(int, id.split()))

def states_to_id(states):
    l = sorted(set(states))
    r = ""
    for i in range(0, len(l)):
        r += str(l[i]) + " " 
    return r

def eps_closure(state, nfa):
    rez = [state]
    set_state = nfa.sets[state]
    next_states_id = set_state["eps"]
    next_states = id_to_states(next_states_id)
    rez.append(next_states)

    #de continuat

    

def transform(nfa):
    NFA_final = nfa.final_states
    NFA_dicts = nfa.dicts
    NFA_alpha = nfa.alpha

    DFA_final = []
    DFA_dicts = []
    DFA_alpha = NFA_alpha
    if "eps" in DFA_alpha:
        DFA_alpha.remove("eps")

    DFA_states = ["0 "]  #i este starea care are tagul DFA_state[i]
    DFA_nr_states = 1
    i = 0
    while i < DFA_nr_states:
        DFA_dicts.append({})
        crt_dict = DFA_dicts[i]
        state_id = DFA_states[i]
        if state_id == "sink":
            for ch in DFA_alpha:
                crt_dict[ch] = i
            i += 1
            continue
        
        states = id_to_states(state_id)

        for j in states:
            if j in NFA_final:
                DFA_final.append(i)
                break
        
        for ch in DFA_alpha:
            next_state = ""
            for j in states:
                NFA_state_dict = NFA_dicts[j]
                if ch in NFA_state_dict:
                    next_state += NFA_state_dict[ch]
            next_state = states_to_id(id_to_states(next_state))
            if next_state == "":
                next_state = "sink"
            if next_state in DFA_states:
                crt_dict[ch] = DFA_states.index(next_state) 
            else:
                DFA_states.append(next_state)
                crt_dict[ch] = DFA_nr_states
                DFA_nr_states += 1
        i += 1
    
    rez = DFA(DFA_dicts, DFA_final, DFA_alpha)
    return rez


#parametrii din linia de comanda
arg1 = sys.argv[1]
arg2 = sys.argv[2]

#print(arg1)

#fisierul de input
inp = open(arg1, "r")

n = read_nfa(inp)

inp.close()

#fisierul output prima data pornit cu w sa fiu sigur ca e gol
open(arg2, "w").close
#apoi append
out = open(arg2, "a")

out.write(str(transform(n)))

out.close()



