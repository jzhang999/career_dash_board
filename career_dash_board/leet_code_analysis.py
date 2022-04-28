import matplotlib.pyplot as plt
import pandas as pd
"""
Python script to analyze Leetcode data
@author: Shu Wu
"""

def get_leetcode_data(dataFrame, company_name):
    count_dict = {}
    dataFrame1 = pd.read_csv('./data_source/download_questions.csv')
    
    #this is the data from leetcode API
    for idx in dataFrame.index:
        company = dataFrame['Company'][idx]
        if company != company_name:
            continue
        question = dataFrame["Question"][idx].replace(" ", '\n')

        if question in count_dict.keys():
            count_dict[question] += 1
        else:
            count_dict[question] = 1

    #this is the data I download
    for idx in dataFrame1.index:
        company = dataFrame1['Company'][idx]
        if company != company_name:
            continue
        question = dataFrame1["Question"][idx].replace(" ", '\n')

        if question in count_dict.keys():
            count_dict[question] += 1
        else:
            count_dict[question] = 1

    # dataFrame['question'] = ['\n'.join(wrap(x, 12)) for x in dataFrame['question']]
    sorted_dict = dict(sorted(count_dict.items(),
                              key=lambda item: item[1],
                              reverse=True))
    # print(sorted_dict)

    question_list = list(sorted_dict.keys())[:5]
    count_list = list(sorted_dict.values())[:5]

    print("\nThe top5 questions in " + company_name + " are:")
    i = 1
    for question in question_list:
        new_question_string = question.replace("\n", ' ')
        print(str(i) + ". " + new_question_string , end = "\n")
        i += 1
    ax = plt.axes()
    plt.bar(range(len(count_list)), count_list, tick_label=question_list)
    plt.show()
