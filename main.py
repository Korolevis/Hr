import pandas as pd
import requests
import os
if __name__ == '__main__':

    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if ('A_office_data.xml' not in os.listdir('../Data') and
        'B_office_data.xml' not in os.listdir('../Data') and
        'hr_data.xml' not in os.listdir('../Data')):
        print('A_office_data loading.')
        url = "https://www.dropbox.com/s/jpeknyzx57c4jb2/A_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/A_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('B_office_data loading.')
        url = "https://www.dropbox.com/s/hea0tbhir64u9t5/B_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/B_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('hr_data loading.')
        url = "https://www.dropbox.com/s/u6jzqqg1byajy0s/hr_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/hr_data.xml', 'wb').write(r.content)
        print('Loaded.')

        # All data in now loaded to the Data folder.

    # write your code here
a_office_df = pd.read_xml("../Data/A_office_data.xml")
b_office_df = pd.read_xml("../Data/B_office_data.xml")
hr_df = pd.read_xml("../Data/hr_data.xml")

a_index = list()
b_index = list()

for id in a_office_df['employee_office_id']:
    a_index.append(f"A{id}")

for id in b_office_df['employee_office_id']:
    b_index.append(f"B{id}")

a_office_df.set_index([a_index], inplace=True)
b_office_df.set_index([b_index], inplace=True)
hr_df.set_index('employee_id', inplace=True)

a_b_office_df = pd.concat([a_office_df, b_office_df])
final_df = pd.merge(a_b_office_df, hr_df, left_index=True, right_index=True)

final_df.drop(['employee_office_id'], axis=1, inplace=True)
final_df.sort_index(inplace=True)

df = final_df.pivot_table(index='Department', columns=['left', 'salary'], values='average_monthly_hours', aggfunc='median')
df = df.round(2)
df = df[(df[0, 'medium'] > df[0, 'high']) | (df[1, 'low'] < df[1, 'high'])]

print(df.to_dict())

pd.set_option('display.max_columns', None)

final_df = final_df[(final_df['time_spend_company'] == 2)]

dfppt = final_df.pivot_table(index=['time_spend_company'], columns=['promotion_last_5years'], values=['satisfaction_level', 'last_evaluation'], aggfunc=['max', 'mean', 'min'])
dfppt = dfppt.round(2)


print(dfppt.to_dict())


