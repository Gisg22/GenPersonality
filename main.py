import datetime
import requests
import random
import json
from googletrans import Translator
from person import person
from bs4 import BeautifulSoup
from index_upper import get_index_upper

headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}


def get_name(gender):
    translator = Translator()
    req_name_mans = requests.get(url='http://analiz-imeni.ru/men/vse-muzhskie-imena.htm', headers=headers)
    req_name_woman = requests.get(url='http://analiz-imeni.ru/women/vse-zhenskie-imena.htm', headers=headers)
    soup_name_male = BeautifulSoup(req_name_mans.text, 'lxml')
    soup_name_woman = BeautifulSoup(req_name_woman.text, 'lxml')
    if gender == 'man':
        table_list = soup_name_male.find('div', class_='tablobertka').find_all('p')
        man_names = []
        for m in table_list:
            man_names.append(m.text.strip('	 '))
        random_index = random.randint(0, len(man_names) - 1)
        return translator.translate(man_names[random_index]).text

    elif gender == 'woman':
        table_list = soup_name_woman.find('div', class_='tablobertka').find_all('p')
        woman_names = []
        for w in table_list:
            woman_names.append(translator.translate(w.text.strip('	 ')).text)
        random_index = random.randint(0, len(woman_names) - 1)
        return woman_names[random_index]


def get_surname():
    req_surname_rus = requests.get(url='https://ru.wikipedia.org/wiki/Список_общерусских_фамилий', headers=headers)
    req_surname_ukr = requests.get(
        url='https://ru.wiktionary.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A3%D0%BA%D1%80%D0%B0%D0%B8%D0%BD%D1%81%D0%BA%D0%B8%D0%B5_%D1%84%D0%B0%D0%BC%D0%B8%D0%BB%D0%B8%D0%B8/ru',
        headers=headers)
    req_surname_euro = requests.get(
        url='https://englishlib.org/%D0%B8%D0%BD%D0%BE%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%BD%D1%8B%D0%B5-%D1%84%D0%B0%D0%BC%D0%B8%D0%BB%D0%B8%D0%B8-%D0%BF%D0%BE-%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%B8.html',
        headers=headers)
    soup_surname_rus = BeautifulSoup(req_surname_rus.text, 'lxml')
    soup_surname_ukr = BeautifulSoup(req_surname_ukr.text, 'lxml')
    soup_surname_euro = BeautifulSoup(req_surname_euro.text, 'lxml')
    columns_rus = soup_surname_rus.find('div', class_='columns').find_all('li')
    groups_ukr = soup_surname_ukr.find('div', class_='mw-category mw-category-columns').find_all('li')
    table_class_euro = soup_surname_euro.find('table', class_='tourist-table table-50x50').find_all('tr')
    rus_surnames = []
    ukr_surnames = []
    euro_surnames = []
    for r in columns_rus:
        rus_surnames.append(r.text)
    for u in groups_ukr:
        ukr_surnames.append(u.text)
    for e in table_class_euro:
        euro_surnames.append(e.find_next('td').text)
    all_surnames = rus_surnames + ukr_surnames + euro_surnames
    random_index = random.randint(0, len(all_surnames) - 1)
    return all_surnames[random_index]


def get_date_birthday():
    return datetime.date(random.randint(1, 29), random.randint(1, 12), random.randint(1930, 2010))


def get_country_and_city():
    county_and_cities = []
    with open('jsonfiles/countries.json') as file:
        contry_json = json.load(file)
    for c in contry_json:
        rand_country = random.choice(list(contry_json))
        for cc in contry_json[c]:
           rand_city = random.choice(list(contry_json[rand_country]))
    county_and_cities.append(rand_country)
    county_and_cities.append(rand_city)

    return county_and_cities

def get_bad_habits():
    bad_habits_1 = []
    bad_habits_2 = []
    request_bad_habits = requests.get(url='https://pavlok.com/blog/list-of-bad-habits/',
                                      headers=headers)
    soup_bad_habits = BeautifulSoup(request_bad_habits.text, 'lxml')
    ul_list_bad_habits = soup_bad_habits.find('div', class_='et_pb_text_inner').find('ol').find_all('li')
    for u in ul_list_bad_habits:
        if u == 'Learn how to take control of your habits. Click Here.':
            ul_list_bad_habits.remove('Learn how to take control of your habits. Click Here.')
    for i in range(0, random.randint(2, 10)):
        random_index = random.randint(0, len(ul_list_bad_habits) - 1)
        bad_habits_1.append(ul_list_bad_habits[random_index].text)
    for i in bad_habits_1:
        if i not in bad_habits_2:
            bad_habits_2.append(i)
    return bad_habits_2


def get_hobby():
    hobby_1 = []
    hobby_2 = []
    with open('jsonfiles/hobbies.json') as file:
        hobby_json = json.load(file)
    for i in range(len(hobby_json)):
        hobby_1.append(hobby_json[i]['title'])
    for i in range(random.randint(1, 6)):
        random_index = random.randint(0, len(hobby_1) - 1)
        hobby_2.append(hobby_1[random_index])
    return hobby_2


def get_speciality(age):
    speciality_1 = []
    speciality_2 = []
    if age <= 6:
        speciality_1.append('Preschooler')
        return speciality_1
    if age <= 18:
        speciality_1.append('Schoolkid')
        return speciality_1
    if age <= 22:
        speciality_1.append('Student')
        return speciality_1
    speciality_requests = requests.get('https://www.careerprofiles.info/top-100-careers.html', headers=headers)
    speciality_soup = BeautifulSoup(speciality_requests.text, 'lxml')
    table_speciality = speciality_soup.find('table').find_all('a')
    style_speciality = speciality_soup.find('table').find_all('td', style='text-align: left; padding-left: 2%;')
    speciality_1 = table_speciality + style_speciality
    for i in range(random.randint(0, 3)):
        random_index = random.randint(0, len(speciality_1) - 1)
        speciality_2.append(speciality_1[random_index].text)
    return speciality_2


def get_person():
    gender = ['woman', 'man']
    random_index = random.randint(0, len(gender) - 1)
    return_gender = gender[random_index]
    return person(name=get_name(return_gender), surname=get_surname(),
                  bat_habits=get_bad_habits(), contry=get_country_and_city(),
                  gender=return_gender, date_birthday=get_date_birthday(),
                  hobby=get_hobby(),
                  speciality=get_speciality(random.randint(6, 90)))


def main():
    personality = get_person()
    print(personality)


if __name__ == '__main__':
    main()
