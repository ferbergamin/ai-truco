class Neuron:
    def __init__(self, entries: list, weights: list):
        if len(entries) != len(weights):
            raise ValueError('Entries and weights must have same length')
        self.entries = entries
        self.weights = weights

    def sum_func(self):
        sum = 0
        for i in range(self.entries):
            sum += self.entries[i]*self.weights[i]
        
        return sum


    def decider_step_func(self):
        if self.sum_func() > 1:
            return True
        return False
