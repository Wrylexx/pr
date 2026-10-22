import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Завантаження та очищення
df = pd.read_csv('КІПЗс-25-1_оцінки_готові.csv')
df = df.dropna(subset=['Студент'])

dates = [col for col in df.columns if col not in ['№', 'Студент']]

for col in dates:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 2. Розрахунок статистики
matrix = df[dates].to_numpy()
averages = np.nanmean(matrix, axis=1)

low_grades = np.nansum((matrix >= 1) & (matrix <= 3), axis=1)

results = pd.DataFrame({
    'Студент': df['Студент'],
    'Середній бал': np.round(averages, 2),
    'Оцінок 1–3': low_grades.astype(int),
    'Статус': np.where(averages < 7, 'Потребує уваги', 'Добре')
})

# 3. Графіки
plt.figure(figsize=(12, 6))
colors = ['crimson' if avg < 7 else 'skyblue' for avg in results['Середній бал']]
plt.bar(results['Студент'], results['Середній бал'], color=colors)
plt.axhline(7, color='red', linestyle='--')
plt.xticks(rotation=90, fontsize=8)
plt.tight_layout()
plt.savefig('average_grades.png')
plt.close()

date_avg = df[dates].mean()
plt.figure(figsize=(10, 5))
plt.plot(dates, date_avg, marker='o')
plt.grid(True)
plt.tight_layout()
plt.savefig('performance_trend.png')
plt.close()

all_grades = matrix[~np.isnan(matrix)]
plt.figure(figsize=(8, 4))
plt.hist(all_grades, bins=range(1, 14), align='left', rwidth=0.8)
plt.tight_layout()
plt.savefig('grades_distribution.png')
plt.close()

# 4. Сортування та пошук
students = list(zip(results['Студент'], results['Середній бал']))

def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            if arr[j][1] < arr[min_idx][1]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

sorted_students = selection_sort(students)

def linear_search(df_res, name):
    for idx, row in df_res.iterrows():
        if row['Студент'] == name:
            return row
    return None

# 5. Збереження
results.to_csv('results.csv', index=False)