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


def get_base(tree, xpath):
    class_and_grade = list(tree.xpath(xpath))
    self_eva, class_eva, campus_eva = 0.0, 0.0, 0.0
    for i in range(0, len(class_and_grade)):
        if str(class_and_grade[i]).__contains__('合计'):
            self_eva = float(class_and_grade[i + 1])
            class_eva = float(class_and_grade[i + 2])
            campus_eva = float(class_and_grade[i + 3])
    if class_eva == 0.0:
        class_eva = self_eva
    if campus_eva == 0.0:
        campus_eva = class_eva
    base = self_eva * 0.1 + class_eva * 0.6 + campus_eva * 0.3
    return round(base, 2)


def get_bonus_point(tree, xpath):
    bonus_point_src = list(tree.xpath(xpath))
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
        if bonus_point_items[start + 0].strip() == '算分':
            start += 1
        one_bonus = {
            'index': int(bonus_point_items[start + 0].strip()),
            'name': bonus_point_items[start + 1].strip(),
            'type': bonus_point_items[start + 2].strip(),
            'rank': bonus_point_items[start + 3].strip(),
            'reference': bonus_point_items[start + 4].strip(),
            'point': float(bonus_point_items[start + 5].strip()),
            'status': bonus_point_items[start + 6].strip()
        }
        if one_bonus.get('status') != '算分':
            continue
        bonus_point_list.append(one_bonus)
        bonus_count += one_bonus.get('point')

    return bonus_count


def calc_moral(htmlData):
    tree = etree.HTML(htmlData)
    base = get_base(tree, '/html/body/form/table/tr[4]/td/table[2]/tr/td/text()')
    bonus = get_bonus_point(tree, '/html/body/form/table/tr[6]/td/table[2]/tr/td/text()')
    return base, bonus


def calc_gym(htmlData):
    tree = etree.HTML(htmlData)
    class_and_grade = list(tree.xpath('/html/body/form/table/tr[4]/td/table[2]/tr/td/text()'))

    for i in class_and_grade:
        if str(i).strip() == "":
            class_and_grade.remove(i)

    class_list = []
    class_name_list = []
    exam_base = 0.0
    for i in range(0, int(len(class_and_grade) / 7)):
        start = 7 * i
        class_name = class_and_grade[start + 0].strip()
        one_class = {
            'name': class_name,
            'season': class_and_grade[start + 1].strip(),
            'grade': class_and_grade[start + 2].strip(),
            'credit': class_and_grade[start + 3].strip(),
            'mode': class_and_grade[start + 4].strip(),
            'reread': class_and_grade[start + 5].strip(),
            'status': class_and_grade[start + 6].strip()
        }
        class_name_list.append(one_class.get('name'))
        class_list.append(one_class)
        exam_base += float(one_class.get('grade'))

    base = get_base(tree, '/html/body/form/table/tr[6]/td/table[2]/tr/td/text()')
    bonus = get_bonus_point(tree, '/html/body/form/table/tr[8]/td/table[2]/tr/td/text()')
    return round(exam_base / 2 * 0.55 + base, 2), bonus


def calc_intellectual(htmlData):
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

    for i in class_and_grade:
        if str(i).strip() == "":
            class_and_grade.remove(i)

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
        if not str(dict(i).get('status')).__contains__("通过"):
            continue
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

    bonus_count = get_bonus_point(tree, '/html/body/form/table/tr[6]/td/table[2]/tr/td/text()')

    return student_name, round(counter * 2, 2), bonus_count
