import math
import os

# PATHS
current_path = os.path.dirname(os.path.abspath(__file__))
# trained data path
global train_features_file_path 
train_features_file_path = os.path.join(current_path,'train-features.txt')
global train_labels_file_path
train_labels_file_path = os.path.join(current_path,'train-labels.txt')
# test data path
global test_features_file_path
test_features_file_path = os.path.join(current_path,'test-features.txt')
global test_labels_file_path
test_labels_file_path = os.path.join(current_path,'test-labels.txt')
# result data path
global result_labels_file_path
result_labels_file_path = os.path.join(current_path,'result-labels.txt')

# Data
global train_labels_list
train_labels_list = []
global allWordsAndCounts
allWordsAndCounts = dict()

# get count of training labels
def getTrainedLabelsData():
    global train_labels_list
    file = open(train_labels_file_path,'r')
    count = 0
    ham_count = 0
    spam_count = 0
    while True:
        label = file.readline()
        if not label:
            break
        train_labels_list.append(int(label))
        count += 1
        if int(label) == 0:
            ham_count += 1
        else:
            spam_count += 1
    return count , ham_count , spam_count

# gets data from training_features and returns number of all words
def getTrainedFeatures():
    global allWordsAndCounts
    file = open(train_features_file_path,'r')
    first_class_count = 0
    sec_class_count = 0
    while True:
        feature = file.readline().split()
        if not feature:
            break
        a = int(feature[2])
        b = 0
        c = 0
        if train_labels_list[int(feature[0])-1] == 0:
            first_class_count += a
            b = a
        elif train_labels_list[int(feature[0])-1] == 1:
            sec_class_count += a
            c = a
        if feature[1] in allWordsAndCounts:
            x = allWordsAndCounts[feature[1]][0] + a
            y = allWordsAndCounts[feature[1]][1] + b
            z = allWordsAndCounts[feature[1]][2] + c
            allWordsAndCounts[feature[1]] = [x,y,z]
        else:
            allWordsAndCounts[feature[1]] = [a,b,c]

    return len(allWordsAndCounts) , first_class_count , sec_class_count

# P(c[ham]) and P(c[spam])
def getTrainedClassesProbability(all_classes , ham_classes, spam_classes):
    ham_probability = ham_classes/all_classes
    spam_probability = spam_classes/all_classes
    return ham_probability , spam_probability

# gets list of all words proability
def createWordProbabilityList(vocab_size,ham_class_size,spam_class_size):
    wordsProbabilityList = dict()
    for word in allWordsAndCounts:
        ham_probability = (allWordsAndCounts[word][1] + 1)/(ham_class_size + vocab_size)
        spam_probability = (allWordsAndCounts[word][2] + 1)/(spam_class_size + vocab_size)
        wordsProbabilityList[word] = [ham_probability,spam_probability]
    return wordsProbabilityList

# Returns float of results accuracy percentage
def compaireResults():
    # open files for reading
    file_test_labels = open(test_labels_file_path, 'r')
    file_result_labels = open(result_labels_file_path, 'r')
    # number of test_labels
    all_count = 1
    # number of currect result_labels
    pass_count = 0
    while True:
        result_line = file_result_labels.readline()
        test_line = file_test_labels.readline()
        if not result_line:
            break
        if result_line == test_line:
            pass_count += 1
        all_count += 1
    return (pass_count*100)/all_count

# clculate probability of each test class an put it on result class
def calcProbability(p_list,ham_class_probability,spam_class_probability):
    file = open(test_features_file_path)
    result_file = open(result_labels_file_path, 'w')
    ham_probability = math.log(ham_class_probability) # we used logaritem to reduce floating number problem
    spam_probability = math.log(spam_class_probability)
    current_text = '1'
    while True:
        feature = file.readline().split()
        if not feature:
            break
        if not feature[0] == current_text:
            if ham_probability > spam_probability:
                result = 0
            else:
                result = 1
            result_file.write(str(result)+'\n')
            ham_probability = math.log(ham_class_probability)
            spam_probability = math.log(spam_class_probability)
            current_text = feature[0]
        if feature[1] in p_list:
            ham_probability += math.log(math.pow(p_list[feature[1]][0],int(feature[2])))
            spam_probability += math.log(math.pow(p_list[feature[1]][1],int(feature[2])))
    result_file.close()
    print('result file Created!')

if __name__ == "__main__":
    # number of classes based on train_lables # of all ,# of 0's, # of 1's
    all_classes , ham_classes, spam_classes = getTrainedLabelsData()
    # number of uniqe words # of ham_labed_features & # of spam_labeld_features
    allVocab , ham_accurence , spam_accurence = getTrainedFeatures()
    # gets probability of ham and spam classes
    ham_class_probability , spam_class_probability = getTrainedClassesProbability(all_classes,ham_classes,spam_classes)
    # gets list of all words proability
    wordsProbabilityList = createWordProbabilityList(allVocab,ham_accurence,spam_accurence)
    # clculate probability of each test class an put it on result class
    calcProbability(wordsProbabilityList,ham_class_probability,spam_class_probability)
    # get result accuracy
    print('result Accuracy: '+str(compaireResults()))