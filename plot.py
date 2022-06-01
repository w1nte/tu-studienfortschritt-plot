import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as dates
import numpy as np

df = pd.read_excel('certificateList.xlsx', skiprows=2)

df['Prüfungsdatum'] = pd.to_datetime(df['Prüfungsdatum'])
df = df.sort_values(by=['Prüfungsdatum']).reset_index()

df['ECTS open'] = 0

ects_open = 180

for index, row in df.iterrows():
    ects_open = ects_open - float(row['ECTS'])
    row['ECTS open'] = ects_open
    df.iloc[index, :] = row


fig, ax1 = plt.subplots()

plt.title('Studiendauer')

ax1.plot_date(df['Prüfungsdatum'], df['ECTS open'], 'k-*', label='Prüfungsleistungen')

x_dates = df['Prüfungsdatum']
x_num = dates.date2num(x_dates)
trend = np.polyfit(x_num, df['ECTS open'], 1)
fit = np.poly1d(trend)
x_fit = np.linspace(x_num.min(), fit.roots[0])
plt.plot(dates.num2date(x_fit), fit(x_fit), 'r--', label='Studiendauer')

ax1.plot_date([datetime.strptime('2018-10-01', '%Y-%m-%d'), datetime.strptime('2021-10-01', '%Y-%m-%d')], [180, 0], 'g--', label='Regelstudiendauer')
ax1.plot_date([datetime.strptime('2018-10-01', '%Y-%m-%d'), datetime.strptime('2022-02-28', '%Y-%m-%d')], [180, 0], 'c--', label='Regelstudiendauer + Toleranzsemester')
ax1.plot_date([datetime.strptime('2018-10-01', '%Y-%m-%d'), datetime.strptime('2023-10-01', '%Y-%m-%d')], [180, 0], 'b--', label='Median')
ax1.axhline(y = ects_open, color = 'r', linestyle = '-', label='Offenen ECTS')
ax1.axhline(y = 0, color = 'g', linestyle = '-')
plt.ylabel('ECTS')
ax1.legend()

plt.show()