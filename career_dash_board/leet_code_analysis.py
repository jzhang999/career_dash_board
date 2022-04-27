import matplotlib.pyplot as plt

def get_leetcode_data(dataFrame):

    count_dict = {}
    for idx in dataFrame.index:
        company = dataFrame['Company'][idx]
        question = dataFrame["Question"][idx].replace(" ", '\n')

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

    ax = plt.axes()
    plt.bar(range(len(count_list)), count_list, tick_label=question_list)
    plt.show()