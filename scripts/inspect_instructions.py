import pickle
import Instruction
import Microarchitecture

instructions, loops, states = pickle.load(open('../logs/openssl/vuln/1000/0xaa/uarch.pickle', 'rb')) 
