# -*- coding: utf-8 -*-
"""
Python script to drive the whole project

@author: Jing Zhang
"""
import pandas as pd
import integrate_analysis as ia
import leet_code_analysis as lca
import get_interview_question as iq


# help to merge all the data sources together into one single data frame
def merge_data():
    # join the two df
    merged_df = pd.merge(alumni_df, salary_df, on="company", how="left")

    return merged_df


def visual_interaction():
    # interact with the user
    print("Welcome to the career dash!!!!")
    print("Please first see the job seeking info we have provided :)\n")
    print("The first visualization info we provide is the "
          "number of CMU Alumnus in Major Tech Firms with salary for SDE attached")
    user_in = input("Please enter the word 'show' to see the visualization info, enter 'skip' to skip: ")
    if user_in == 'show':
        ia.get_CMU_alumnus_firms(merged_data)
    else:
        pass
    print("\n\nThe second visualization info we provide is the "
          "number of CMU Alumnus in Major Tech Firms compared with other universities")
    user_in = input("Please enter the word 'show' to see the visualization info, enter 'skip' to skip: ")
    if user_in == 'show':
        ia.get_CMU_influence_firms(alumni_df)  # focus on CMU
        ia.get_cmu_and_other_school(alumni_df)
    else:
        pass


def console_ui():
    global company, year
    print("\n\nPlease choose a company you are most interested in to see alumini numbers")
    company = input(
        "Please enter either of following {'Amazon', 'Meta', 'Microsoft', 'Salesforce', 'Google', 'Adobe', 'Apple'}: ")
    ia.get_company_alumni(company)

    print("\n\nPlease enter the Company Name you interested in to get the online assessment questions")
    company_name = input("Please enter either of following {'Google', 'Facebook', 'Microsoft', 'Amazon', 'Apple', 'Bloomberg', 'DoorDash'}: ")
    company_set = {"Google", "Facebook", "Microsoft", "Amazon", "Apple", "Bloomberg", "DoorDash"}
    if company_name not in company_set:
        print("Sorry, we don't have the questions of " + company_name)
    else:
        lca.get_leetcode_data(leetcode_df, company_name)

    print("\n\nPlease choose a company you are most interested in to get interview questions")
    company = input("Please enter either of following {'amazon', 'meta', 'microsoft', 'google'}: ")
    year = input("Please enter the year you want to see: ")
    iq.get_interview_question(company, year)


if __name__ == '__main__':
    # preprocess the alumni data to sort it by alumni count
    alumni_df = pd.read_csv('./data_source/alumni.csv')
    alumni_df = alumni_df.sort_values(by=['alumni_count'])
    leetcode_df = pd.read_csv('./data_source/leetcode_data.csv')

    # preprocess the salary data for entry-level SDE salary
    salary_df = pd.read_csv('./data_source/company_salary_info.csv')
    salary_df['salary'] = [int(salary_df.replace('$', '').replace(',', '')) for salary_df in salary_df['salary']]
    salary_df = salary_df.loc[(salary_df['job_title'] == 'Software Engineer') & (salary_df['salary'] > 1.1e5)]

    merged_data = merge_data()

    # interact with the user for visualizations
    visual_interaction()

    # interaction for console log info
    console_ui()
