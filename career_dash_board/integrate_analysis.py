# From the university's perspective, where did Tartans go?
import iso3166
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
import numpy as np


# help to get the CMU Alumnus in Major Tech Firms
def get_CMU_alumnus_firms(merged_df):
    # prepare color
    salary = merged_df['salary']
    normalizer = Normalize(vmin=min(salary), vmax=max(salary))
    normalized_salary = normalizer(salary)
    color_brewer = cm.get_cmap('summer')

    # plot main bar
    fig, ax = plt.subplots(figsize=(18, 4))
    color = color_brewer(normalized_salary)
    bar = plt.barh(merged_df['company'], merged_df['alumni_count'], color = color)

    # plot color bar
    sm = ScalarMappable(cmap=color_brewer, norm=normalizer)
    sm.set_array([])
    cbar = plt.colorbar(sm)
    cbar.set_label('Annual Salary, SDE I', rotation = 90, labelpad = 20, fontsize=12)

    # plot number of alumnus annotation
    for index, count in enumerate(merged_df['alumni_count']):
        plt.text(count, index, str(count), fontstyle = 'italic', fontweight='semibold', va='center', ha='right')

    # plot title and axis labels
    plt.yticks(fontsize=12)
    plt.xticks(fontsize=12)
    plt.xlabel('Number of Alumnus', fontsize=15)
    plt.title('CMU Alumnus in Major Tech Firms', fontsize=15)

    plt.show()


# From the company's perspective, the CMU factor?
def get_CMU_influence_firms(alumni_df):
    # filter schools from a combination of both schools and regions
    countries = set([c.name for c in iso3166.countries])
    company_df = pd.read_csv('./data_source/linkedin_companies.csv')
    company_alumni_df = company_df[np.logical_and(
        ['Area' not in geo for geo in company_df['university/region']]
        , [all([geo not in country for country in countries]) for geo in company_df['university/region']])]
    company_alumni_df = company_alumni_df[[geo not in {'London, United Kingdom',
                                                       'INSEAD',
                                                       'Trailhead by Salesforce',
                                                       'Sydney, Australia'
                                                       }  # manual
                                           for geo in company_alumni_df['university/region']]]

    # add school alumni ranking for school for each company as a new column
    company_alumni_df['rank'] = company_alumni_df \
        .sort_values(['company', 'alumni_count'], ascending=False) \
        .groupby('company')["alumni_count"] \
        .rank(method="first", ascending=False)

    # augment company_alumni_df with additional CMU alumni data
    alumni_df['university/region'] = 'Carnegie Mellon University'
    cmu_alumni_df = pd.merge(alumni_df,
                             company_alumni_df,
                             on=('university/region', 'company'),
                             how='left')
    cmu_alumni_df.drop('alumni_count_y', axis=1, inplace=True)
    cmu_alumni_df.rename(columns={'alumni_count_x': 'alumni_count'}, inplace=True)
    cmu_alumni_df.fillna(16, inplace=True)  # use 16 as a placeholder if CMU's rank is lower than top 15

    # merge the augmented alumni CMU data to the company_alumni_df
    for _, row in cmu_alumni_df.iterrows():
        company = row['company']
        rank_info = company_alumni_df.loc[(company_alumni_df['company'] == company) &
                                          (company_alumni_df['university/region'] == 'Carnegie Mellon University')]
        if not len(rank_info):
            company_alumni_df.loc[len(company_alumni_df.index)] = row

    # filter the top 5 schools for each company, plus CMU
    company_alumni_df = company_alumni_df[(company_alumni_df['rank'] <= 5)
                                          | (company_alumni_df['university/region'] == 'Carnegie Mellon University')]

    # retrieve CMU's ranking for each company (caveat: data only have top 15)
    target_ranking = {}
    companies = set(company_alumni_df['company'])
    for company in companies:
        rank_info = company_alumni_df.loc[(company_alumni_df['company'] == company) &
                                          (company_alumni_df['university/region'] == 'Carnegie Mellon University')]
        rank = int(rank_info['rank'])
        target_ranking[company] = rank

    # sort companies (x-axis) by CMU's ranking
    sorted_companies = sorted(companies,
                              key=lambda company: (-target_ranking[company],
                                                   int(cmu_alumni_df[cmu_alumni_df.company == company]['alumni_count']))
                              )
    # break the dataframe into bar plot components
    school_bars = {}
    schools = list(set(company_alumni_df['university/region']))
    schools.remove('Carnegie Mellon University')
    schools.insert(0, 'Carnegie Mellon University')
    for school in schools:
        alumni_list = []
        # each school has its own alumni list bar for all companies
        for company in sorted_companies:
            alumni_info = company_alumni_df.loc[(company_alumni_df['university/region'] == school) &
                                                (company_alumni_df['company'] == company)]
            alumni_count = 0  # ignore a school's presence if it's 1) not in top 5 and 2) not CMU
            if len(alumni_info):
                alumni_count = int(alumni_info['alumni_count'])
            alumni_list.append(alumni_count)
        school_bars[school] = alumni_list

    # plot main bar
    # all bars except CMU has 0.5 alpha value
    fig, ax = plt.subplots(figsize=(24, 5))

    # brewing colors
    cmap = plt.cm.get_cmap('hsv', len(schools))

    # iteratively draw stacked bars
    starts = np.zeros(len(companies))
    for i, school in enumerate(schools):
        alpha = 0.15 if school != 'Carnegie Mellon University' else 1
        color = list(cmap(i)[:3]) + [alpha]
        alumni_list = school_bars[school]
        ax.barh(sorted_companies, alumni_list, left=starts, label=school, color=color)
        starts += alumni_list

    # plot title and axis labels
    plt.yticks(fontsize=12)
    plt.xticks(fontsize=12)
    plt.title("CMU's influence in Major Tech Firms", fontsize=15)

    # plot legend
    legend = plt.legend(loc='center',
                        frameon=False,
                        bbox_to_anchor=(0., 1.4, 1., 0),
                        mode='expand',
                        ncol=3,
                        borderaxespad=-1,
                        prop={'size': 12})

    plt.show()


def get_cmu_and_other_school(alumni_df):
    # filter schools from a combination of both schools and regions
    countries = set([c.name for c in iso3166.countries])
    company_df = pd.read_csv('./data_source/linkedin_companies.csv')
    company_alumni_df = company_df[np.logical_and(
        ['Area' not in geo for geo in company_df['university/region']]
        , [all([geo not in country for country in countries]) for geo in company_df['university/region']])]
    company_alumni_df = company_alumni_df[[geo not in {'London, United Kingdom',
                                                       'INSEAD',
                                                       'Trailhead by Salesforce',
                                                       'Sydney, Australia'
                                                       }  # manual
                                           for geo in company_alumni_df['university/region']]]

    # add school alumni ranking for school for each company as a new column
    company_alumni_df['rank'] = company_alumni_df \
        .sort_values(['company', 'alumni_count'], ascending=False) \
        .groupby('company')["alumni_count"] \
        .rank(method="first", ascending=False)

    # augment company_alumni_df with additional CMU alumni data
    alumni_df['university/region'] = 'Carnegie Mellon University'
    cmu_alumni_df = pd.merge(alumni_df,
                             company_alumni_df,
                             on=('university/region', 'company'),
                             how='left')
    cmu_alumni_df.drop('alumni_count_y', axis=1, inplace=True)
    cmu_alumni_df.rename(columns={'alumni_count_x': 'alumni_count'}, inplace=True)
    cmu_alumni_df.fillna(16, inplace=True)  # use 16 as a placeholder if CMU's rank is lower than top 15

    # merge the augmented alumni CMU data to the company_alumni_df
    for _, row in cmu_alumni_df.iterrows():
        company = row['company']
        rank_info = company_alumni_df.loc[(company_alumni_df['company'] == company) &
                                          (company_alumni_df['university/region'] == 'Carnegie Mellon University')]
        if not len(rank_info):
            company_alumni_df.loc[len(company_alumni_df.index)] = row

    # filter the top 5 schools for each company, plus CMU
    company_alumni_df = company_alumni_df[(company_alumni_df['rank'] <= 5)
                                          | (company_alumni_df['university/region'] == 'Carnegie Mellon University')]

    # retrieve CMU's ranking for each company (caveat: data only have top 15)
    target_ranking = {}
    companies = set(company_alumni_df['company'])
    for company in companies:
        rank_info = company_alumni_df.loc[(company_alumni_df['company'] == company) &
                                          (company_alumni_df['university/region'] == 'Carnegie Mellon University')]
        rank = int(rank_info['rank'])
        target_ranking[company] = rank

    # sort companies (x-axis) by CMU's ranking
    sorted_companies = sorted(companies,
                              key=lambda company: (-target_ranking[company],
                                                   int(cmu_alumni_df[cmu_alumni_df.company == company]['alumni_count']))
                              )
    # break the dataframe into bar plot components
    school_bars = {}
    schools = list(set(company_alumni_df['university/region']))
    schools.remove('Carnegie Mellon University')
    schools.insert(0, 'Carnegie Mellon University')
    for school in schools:
        alumni_list = []
        # each school has its own alumni list bar for all companies
        for company in sorted_companies:
            alumni_info = company_alumni_df.loc[(company_alumni_df['university/region'] == school) &
                                                (company_alumni_df['company'] == company)]
            alumni_count = 0  # ignore a school's presence if it's 1) not in top 5 and 2) not CMU
            if len(alumni_info):
                alumni_count = int(alumni_info['alumni_count'])
            alumni_list.append(alumni_count)
        school_bars[school] = alumni_list

    # plot main bar
    fig, ax = plt.subplots(figsize=(24, 5))

    # brewing colors
    cmap = plt.cm.get_cmap('hsv', len(schools))

    # iteratively draw stacked bars
    starts = np.zeros(len(companies))
    for i, school in enumerate(schools):
        alpha = 1
        color = list(cmap(i)[:3]) + [alpha]
        alumni_list = school_bars[school]
        ax.barh(sorted_companies, alumni_list, left=starts, label=school, color=color)
        starts += alumni_list

    # plot title and axis labels
    plt.yticks(fontsize=12)
    plt.xticks(fontsize=12)
    plt.title("CMU's influence in Major Tech Firms", fontsize=15)

    # plot legend
    legend = plt.legend(loc='center',
                        frameon=False,
                        bbox_to_anchor=(0., 1.4, 1., 0),
                        mode='expand',
                        ncol=3,
                        borderaxespad=-1,
                        prop={'size': 12})

    plt.show()

# company_alumni_df[company_alumni_df.company == 'Meta']

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
    print(sorted_dict)

    question_list = list(sorted_dict.keys())[:5]
    count_list = list(sorted_dict.values())[:5]

    ax = plt.axes()
    plt.bar(range(len(count_list)), count_list, tick_label=question_list)
    plt.show()