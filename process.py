from lxml import etree
import re


def find_class_in_list(class_list, name):
    for i in class_list:
        if dict(i).get('name') == name:
            return i
    return None


def calc(htmlData):
    tree = etree.HTML(htmlData)
    name_str = tree.xpath('/html/body/form/table/tr[2]/td/table/tr/td/text()')
    student_name = re.findall(r"(学生：.*\S)", str(name_str[0]))[0].replace("学生：", "")

    class_and_grade = list(tree.xpath('/html/body/form/table/tr[4]/td/table[2]/tr/td/text()'))
    class_and_grade.extend(tree.xpath('/html/body/form/table/tr[4]/td/table[5]/tr/td/text()'))

    class_list = []
    class_name_list = []
    for i in range(0, int(len(class_and_grade) / 7)):
        start = 7 * i
        class_name = class_and_grade[start + 0].strip()
        grade = float(re.findall(r"[0-9]+", class_and_grade[start + 1].strip())[0])
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

    counter = 0
    for i in class_list:
        if dict(i).get('mode') == '必修课和专业必修课（或限定选修课）':
            counter += float(dict(i).get('grade')) / 100 * float(dict(i).get('credit'))

    return student_name, round(counter * 2, 2)
