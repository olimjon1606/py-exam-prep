# import requests
#
# url = "https://timeapi.io/api/Time/current/zone"
# params = {
#     "timeZone": "Europe/Warsaw"
# }
#
# response = requests.get(url, params=params)
# data = response.json()
#
# if response.status_code == 200:
#     current_time = data["time"]
#     print("Current time in Warsaw:", current_time)
# else:
#     print("Error:", data["error_message"])

# task_2

# import requests
# from bs4 import BeautifulSoup
# from collections import Counter
# import re
#
# url = "https://iso.uni.lodz.pl/"
# response = requests.get(url)
# html_content = response.text
#
# soup = BeautifulSoup(html_content, "html.parser")
#
# text = soup.get_text()
#
# text = re.sub(r"\s+", " ", text)
# text = text.lower()
#
# words = re.findall(r"\b\w+\b", text)
#
# word_frequency = Counter(words)
#
# most_frequent_word = word_frequency.most_common(1)[0][0]
# frequency_count = word_frequency[most_frequent_word]
#
# print("The most frequent word on the webpage is:", most_frequent_word)
# print("It occurs", frequency_count, "times.")

# task_3

# import pandas as pd
#
# df = pd.read_csv('StudentsPerformance.csv')
#
# math_median = df['math score'].median()
# reading_median = df['reading score'].median()
# writing_median = df['writing score'].median()
#
# largest_median = max(math_median, reading_median, writing_median)
#
# print("The largest median score among 'math score', 'reading score', and 'writing score' is:", largest_median)
#

# task 4

# import pandas as pd
# import matplotlib.pyplot as plt
#
# df = pd.read_csv('StudentsPerformance.csv')
#
# writing_score = df['writing score']
# math_score = df['math score']
#
# plt.scatter(math_score, writing_score)
#
# plt.xlabel('Math Score')
# plt.ylabel('Writing Score')
#
# plt.show()