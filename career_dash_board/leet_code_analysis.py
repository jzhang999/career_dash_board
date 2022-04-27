import matplotlib.pyplot as plt

def get_leetcode_data(dataFrame, company_name):

    count_dict = {}
    for idx in dataFrame.index:
        company = dataFrame['Company'][idx]
        if company != company_name:
            continue
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

    print("\nThe top5 questions in " + company_name + " are:")
    i = 1
    for question in question_list:
        new_question_string = question.replace("\n", ' ')
        print(str(i) + ". " + new_question_string , end = "\n")
        i += 1
    ax = plt.axes()
    plt.bar(range(len(count_list)), count_list, tick_label=question_list)
    plt.show()
