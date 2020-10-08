import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix as CM
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import recall_score


dataframe = pd.read_csv('/Users/Galaxy/Desktop/smartedge/test2.csv')
dataframe = pd.DataFrame(dataframe)
dataframe.reset_index(drop=True)
dataframe = dataframe.drop_duplicates()
print(dataframe.loc[:, 'label'].value_counts())
# dataframe.to_csv('/Users/Galaxy/Desktop/smartedge/test2.csv', header=True, index=True)
dataframe.loc[dataframe['label'] == 38, 'label'] = 50
dataframe.loc[dataframe['label'] == 39, 'label'] = 50
dataframe.loc[dataframe['label'] == 40, 'label'] = 50
dataframe.loc[dataframe['label'] == 41, 'label'] = 50
dataframe.loc[dataframe['label'] == 42, 'label'] = 50
dataframe.loc[dataframe['label'] == 43, 'label'] = 50
dataframe.loc[dataframe['label'] == 44, 'label'] = 50
dataframe.loc[dataframe['label'] == 45, 'label'] = 50
dataframe.loc[dataframe['label'] == 46, 'label'] = 50
dataframe.loc[dataframe['label'] == 47, 'label'] = 50
dataframe.loc[dataframe['label'] == 48, 'label'] = 50
dataframe.loc[dataframe['label'] == 49, 'label'] = 50
print(dataframe.loc[:, 'label'].value_counts())
x = dataframe.drop('label', axis=1)
y = dataframe.label
print('x.head = ', x.head())
#
le = LabelEncoder().fit(y)
result = le.transform(y)
# print(result)
df = dataframe
print(df.head(3))
print(df.info())
df.to_csv('/Users/Galaxy/Desktop/smartedge/dataset.csv', header=True, index=True)
print(df.loc[:, 'label'].value_counts())
# print(x[:5])
# print(y[:5])
#
# print("names", x.head(0))
names = x.head(0)
Xtrain, Xtest, ytrain, ytest = train_test_split(x, result, test_size=0.3, random_state=0)

rfc = RandomForestClassifier(n_estimators=100)
rfc = rfc.fit(Xtrain, ytrain)
ypred = rfc.predict(Xtest)
score = rfc.score(Xtest, ytest)
r = recall_score(ytest, ypred, average='micro')
r_a = recall_score(ytest, ypred, average='macro')


print("score :", score)
print("recall_score micro", r)
print("recall_score macro", r_a)
print(recall_score)
cmd = CM(ytest, ypred)
print(cmd)
print(cmd[32:45, ...])
# feature_importance = rfc.feature_importances_
# print(feature_importance)
# print(sorted(zip(map(lambda x: round(x, 4), rfc.feature_importances_), names)))
# # # # # # rfc_c = cross_val_score(rfc, x, y, cv=10)
# # # # # # plt.plot(range(1, 11), rfc_c, label = "RandomForest")
# # # # # # plt.show()

labels = list(range(1, 33))
labels.append(50)


def plot_confusion_matrix(cm, title='Confusion Matrix', cmap=plt.cm.binary):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    xlocations = np.array(range(len(labels)))
    plt.xticks(xlocations, labels, rotation=90)
    plt.yticks(xlocations, labels)
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    cm = CM(ytest, ypred)
    np.set_printoptions(precision=2)


cm_normalized = cmd.astype('float') / cmd.sum(axis=1)[:, np.newaxis]
print(cm_normalized)
plt.figure(figsize=(12, 8), dpi=120)


ind_array = np.arange(len(labels))
x, y = np.meshgrid(ind_array, ind_array)

for x_val, y_val in zip(x.flatten(), y.flatten()):
  c = cm_normalized[y_val][x_val]
  if c > 0.01:
    plt.text(x_val, y_val, "%0.2f" % (c,), color='red', fontsize=7, va='center', ha='center')

# offset the tick
plt.gca().set_xticks(labels, minor=True)
plt.gca().set_yticks(labels, minor=True)
plt.gca().xaxis.set_ticks_position('none')
plt.gca().yaxis.set_ticks_position('none')
plt.grid(True, which='minor', linestyle='-')
plt.gcf().subplots_adjust(bottom=0.15)

plot_confusion_matrix(cm_normalized, title='Normalized confusion matrix')
# show confusion matrix
# plt.savefig('../Data/confusion_matrix.png', format='png')
plt.show()
