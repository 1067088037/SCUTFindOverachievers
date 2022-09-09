import functools
import re
import network
import process


def get_one_student(evaluation_id):
    html_content = network.get_detail(evaluation_id)
    name, count = process.calc(html_content)
    return {'id': evaluation_id, 'name': name, 'count': count}


def cmp(i1, i2):
    return i2.get('count') - i1.get('count')


def main():
    id_html_content = network.get_list()
    id_list = re.findall(r"(evaluationId=[0-9]+)", id_html_content)
    if len(id_list) <= 0:
        print("连接失败")
        return
    else:
        print("连接成功，请稍后...\n")

    result = []
    for i in id_list:
        evaluation_id = int(i.replace('evaluationId=', ''))
        result.append(get_one_student(evaluation_id))
        print(len(result) % 10, end="")
        if len(result) % 10 == 0:
            print(" ", end="")
    print("\n排名\t姓名\t加权成绩")
    result.sort(key=functools.cmp_to_key(cmp))
    for i, v in enumerate(result):
        print(f"{i + 1}\t{v.get('name')}\t{v.get('count')}")


if __name__ == '__main__':
    main()
