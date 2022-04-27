import pandas as pd
import integrate_analysis as ia


# help to merge all the data sources together into one single data frame
def merge_data():
    # join the two df
    merged_df = pd.merge(alumni_df, salary_df, on="company", how="left")

    return merged_df


if __name__ == '__main__':
    # preprocess the alumni data to sort it by alumni count
    alumni_df = pd.read_csv('./data_source/alumni.csv')
    alumni_df = alumni_df.sort_values(by=['alumni_count'])

    # preprocess the salary data for entry-level SDE salary
    salary_df = pd.read_csv('./data_source/company_salary_info.csv')
    salary_df['salary'] = [int(salary_df.replace('$', '').replace(',', '')) for salary_df in salary_df['salary']]
    salary_df = salary_df.loc[(salary_df['job_title'] == 'Software Engineer') & (salary_df['salary'] > 1.1e5)]

    merged_data = merge_data()
    ia.get_CMU_alumnus_firms(merged_data)
    ia.get_CMU_influence_firms(alumni_df)  # focus on CMU
    ia.get_cmu_and_other_school(alumni_df)
    



