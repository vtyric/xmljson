import itertools
import datetime
from urllib.request import urlopen
from json import loads

(gradski_wiki_url, gradski_page_id, gradski_filename) = (
    'https://ru.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&rvlimit=500&titles=%D0' \
    '%93%D1%80%D0%B0%D0%B4%D1%81%D0%BA%D0%B8%D0%B9,' \
    '_%D0%90%D0%BB%D0%B5%D0%BA%D1%81%D0%B0%D0%BD%D0%B4%D1%80_%D0%91%D0%BE%D1%80%D0%B8%D1%81%D0%BE%D0' \
    '%B2%D0%B8%D1%87', '183903', 'gradski.txt')

(belmondo_wiki_url, belmondo_page_id, belmondo_filename) = (
    'https://ru.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&rvlimit=500&titles' \
    '=%D0%91%D0%B5%D0%BB%D1%8C%D0%BC%D0%BE%D0%BD%D0%B4%D0%BE,' \
    '_%D0%96%D0%B0%D0%BD-%D0%9F%D0%BE%D0%BB%D1%8C', '192203', 'belmondo.txt')


def get_statistics(url, page_id):
    data = loads(urlopen(url).read().decode('utf8'))
    return list(map(lambda x: (x[0], len(list(x[1]))),
                    itertools.groupby(data['query']['pages'][page_id]['revisions'], get_date_from_data)))


def get_date_from_data(data):
    return datetime.datetime.strptime(data['timestamp'], '%Y-%m-%dT%H:%M:%SZ').date()


def print_statistics(filename, statistics):
    with open(filename, 'w', encoding='utf8') as file:
        for date, revision_count in statistics:
            print(date, revision_count, file=file)


def print_date_of_death(expected_date, statistics, name):
    date_of_death = max(statistics, key=lambda statistic: statistic[1])[0]
    print(f"предполагаемая дата смерти({name}): {date_of_death}")
    print("дата смерти совпадает с ожидаемой"
          if str(date_of_death) == expected_date
          else "дата смерти не совпадает с ожидаемой")


def print_all_infos(url, page_id, filename, name, date_of_death):
    stats = get_statistics(url, page_id)
    print_statistics(filename, stats)
    print(f"статистика({name}) записана в {filename}")
    print_date_of_death(date_of_death, stats, name)


if __name__ == "__main__":
    print_all_infos(gradski_wiki_url, gradski_page_id, gradski_filename, "Александр Борисович Градский", "2021-11-28")
    print()
    print_all_infos(belmondo_wiki_url, belmondo_page_id, belmondo_filename, "Жан-Поль Бельмондо", "2021-09-06")
