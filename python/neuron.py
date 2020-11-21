import numpy as np

weigths1 = np.array([[-12.61855908, -5.68237376],
                    [ 24.05617412, 5.44164911],
                    [ 17.99825565, 9.50152],
                    [  2.39572936, 0.69976315]])

weigths2 = np.array([[ 13.67363944],
                    [-14.27666008]])
class Neuron:
    def __init__(self, entries: list):
        self.entries = np.array(entries)
        print(self.entries)

    def exec(self):
        sumSynapse0 = np.dot(self.entries, weigths1)
        hiddenLayer = self.sigmoide_func(sumSynapse0)

        sumSynapse1 = np.dot(hiddenLayer, weigths2)
        return self.sigmoide_func(sumSynapse1)
    
    def sigmoide_func(self, sum):
        return 1 / ( 1 + np.exp(-sum) )
