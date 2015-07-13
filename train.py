from __future__ import print_function, division
from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
from pybrain.tools.customxml.networkreader import NetworkReader
from pybrain.tools.customxml.networkwriter import NetworkWriter
import os
import data

train_type = "symbol"
hidden_units = 10

xmldir = "xml/"
networkname = train_type + "-" + str(hidden_units) + ".xml"

training_set, test_set = data.get_datasets("pics/resized/", dstype = train_type)
training_set._convertToOneOfMany()
test_set._convertToOneOfMany()

print("Test type: '{}'".format(train_type))
print("Number of training patterns:", len(training_set))
print("Number of test patterns:", len(test_set))
print("Input and output dimensions:", training_set.indim, training_set.outdim)
print("Number of hidden units:", hidden_units)
print()
print("First sample (input, target, class):")
print(training_set['input'][0], training_set['target'][0], training_set['class'][0])
print()

network = buildNetwork(training_set.indim, hidden_units, training_set.outdim, outclass=SoftmaxLayer)
trainer = BackpropTrainer(network, dataset = training_set)

for i in range(1000):
    error = trainer.train()
    training_result = percentError(trainer.testOnClassData(dataset = training_set), training_set['class']) / 100
    test_result     = percentError(trainer.testOnClassData(dataset = test_set),     test_set['class']) / 100

    print("epoch: {0:4d}   trnerr: {1:10.8f}   tsterr: {2:10.8f}   err: {3:10.8f}"
        .format(trainer.totalepochs, training_result, test_result, error))

    # save network after every 10 epochs
    if (i+1) % 10 == 0:
        print()
        for c in range(test_set.nClasses):
            (class_, _) = test_set.splitByClass(c)
            sensitivity = (100 - percentError(trainer.testOnClassData(dataset = class_), class_['class']) / 100) if len(class_) > 0 else 0
            print("Class {0:2d}: {1:4d} items. Correctly classified: {2:10.8f}".format(c, len(class_), sensitivity))
            
        NetworkWriter.writeToFile(network, xmldir + networkname)
        print("Network saved as", networkname)
        print()
