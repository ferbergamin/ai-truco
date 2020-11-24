import numpy as np
import csv

weigths1 = np.array([[1.79376379, -1.76743326],
                    [-11.41509836,11.63501476],
                    [8.51850981,-8.29926651],
                    [-0.5696793,0.55177093]])

weigths2 = np.array([[14.50249387],
                    [-13.8153545]])
class Neuron:
    def __init__(self, entries: list):
        self.entries = np.array(entries)
        self.archive = open('memory.csv', 'a+', newline="\n")
        self.writer = csv.DictWriter(self.archive, fieldnames=['who_m_f','card_table','cards_in_hand_mean_weight','hand','result'])
        print(entries)

    def exec(self):
        sumSynapse0 = np.dot(self.entries, weigths1)
        hiddenLayer = self.sigmoide_func(sumSynapse0)

        sumSynapse1 = np.dot(hiddenLayer, weigths2)
    
        result = self.sigmoide_func(sumSynapse1)[0][0]
        # self.save_register(self.entries[0], round(result))
        self.archive.close()
        return result
    
    def sigmoide_func(self, sum):
        return 1 / ( 1 + np.exp(-sum) )

    def save_register(self, fields, result):
        self.writer.writerow({
            "who_m_f": int(fields[0]),
            "card_table": round(fields[1], 2),
            "cards_in_hand_mean_weight": round(fields[2], 2),
            "hand": int(fields[3]),
            "result": result
        })