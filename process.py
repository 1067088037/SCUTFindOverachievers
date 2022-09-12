import functools

from lxml import etree
import re
import config


def cmp_optional(c1, c2):
    return float(dict(c2).get('credit')) - float(dict(c1).get('credit'))


def find_class_in_list(class_list, name):
    for i in class_list:
        if dict(i).get('name') == name:
            return i
    return None


def calc(htmlData):
    tree = etree.HTML(htmlData)
    name_str = tree.xpath('/html/body/form/table/tr[2]/td/table/tr/td/text()')

    try:
        find_name = re.findall(r"(学生：.*\S)", str(name_str[0]))
    finally:
        pass
    try:
        student_name = find_name[0].replace("学生：", "")
    except IndexError:
        student_name = "Unknown"

    class_and_grade = list(tree.xpath('/html/body/form/table/tr[4]/td/table[2]/tr/td/text()'))
    class_and_grade.extend(tree.xpath('/html/body/form/table/tr[4]/td/table[5]/tr/td/text()'))

    class_list = []
    class_name_list = []
    for i in range(0, int(len(class_and_grade) / 7)):
        start = 7 * i
        class_name = class_and_grade[start + 0].strip()
        try:
            grade = float(re.findall(r"[0-9]+", class_and_grade[start + 1].strip())[0])
        except IndexError:
            grade = 0.0
        if class_name in class_name_list:
            old_class = find_class_in_list(class_list, class_name)
            if grade > old_class.get('grade'):
                class_list.remove(old_class)
            else:
                continue
        one_class = {
            'name': class_name,
            'grade': grade,
            'credit': class_and_grade[start + 2].strip(),
            'mode': class_and_grade[start + 3].strip(),
            'reread': class_and_grade[start + 4].strip(),
            'gpa': class_and_grade[start + 5].strip(),
            'status': class_and_grade[start + 6].strip()
        }
        class_name_list.append(one_class.get('name'))
        class_list.append(one_class)

    counter = 0.0
    optional_list = []
    for i in class_list:
        if dict(i).get('name') in config.offsetClass:
            optional_list.append(i)
            continue
        if dict(i).get('mode') == '必修课和专业必修课（或限定选修课）':
            counter += float(dict(i).get('grade')) / 100 * float(dict(i).get('credit'))
        elif dict(i).get('mode') == '专业选修课':
            optional_list.append(i)

    optional_list.sort(key=functools.cmp_to_key(cmp_optional))
    optional_counter = 0.0
    optional_num_count = 0
    optional_credit_count = 0.0

    for i in optional_list:
        optional_counter += float(dict(i).get('grade')) / 100 * float(dict(i).get('credit'))
        optional_num_count += 1
        optional_credit_count += float(dict(i).get('credit'))
        if optional_num_count >= config.optionalCountLimit \
                or optional_credit_count >= config.optionalCreditLimit:
            break
    if optional_credit_count > config.optionalCreditLimit:
        optional_counter = optional_counter / optional_credit_count * config.optionalCreditLimit
    counter += optional_counter

    bonus_point_src = list(tree.xpath('/html/body/form/table/tr[6]/td/table[2]/tr/td/text()'))
    bonus_point_items = []
    for i in bonus_point_src:
        item = str(i).strip()
        if item == "" or item.find("通过") != -1:
            continue
        else:
            bonus_point_items.append(item)

    bonus_count = 0.0
    bonus_point_list = []
    for i in range(0, int(len(bonus_point_items) / 7)):
        start = 7 * i
        one_bonus = {
            'index': int(bonus_point_items[start + 0].strip()),
            'name': bonus_point_items[start + 1].strip(),
            'type': bonus_point_items[start + 2].strip(),
            'rank': bonus_point_items[start + 3].strip(),
            'reference': bonus_point_items[start + 4].strip(),
            'point': float(bonus_point_items[start + 5].strip()),
            'status': bonus_point_items[start + 6].strip()
        }
        bonus_point_list.append(one_bonus)
        bonus_count += one_bonus.get('point')

    return student_name, round(counter * 2, 2), bonus_count
