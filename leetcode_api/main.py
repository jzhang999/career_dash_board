from leetmodel import *
import matplotlib.pyplot as plt
import pandas as pd

username = 'xxxx'
password = 'xxxx'
model = Graphql_API(username, password)

submitData = model.getRecentSubs(username)
question_set = set()
for record in submitData:
  question_set.add(record['title'])

#
# for question in question_set:
#   print(question)

dataFrame = pd.DataFrame(question_set, columns=['question'])
dataFrame['Company'] = pd.Series(["Facebook" for i in range(len(dataFrame.index))])
dataFrame.to_csv("result.csv", sep='\t')
count_dict = {}

dataFrame.loc[len(dataFrame.index)] = ['Expression Add Operators', "Facebook"]

for idx in dataFrame.index:
  company = dataFrame['Company'][idx]
  question = dataFrame["question"][idx].replace(" ", '\n')

  if question in count_dict.keys():
    count_dict[question] += 1
  else:
    count_dict[question] = 1

# dataFrame['question'] = ['\n'.join(wrap(x, 12)) for x in dataFrame['question']]
sorted_dict = dict(sorted(count_dict.items(),
                           key=lambda item: item[1],
                           reverse=True))
print(sorted_dict)



question_list = list(sorted_dict.keys())[:5]
count_list = list(sorted_dict.values())[:5]
# name_list = ['Monday','Tuesday','Friday','Sunday']
# num_list = [1.5,0.6,7.8,6]


ax = plt.axes()
plt.bar(range(len(count_list)), count_list , tick_label=question_list)
plt.show()