import functools
import os
import re
import network
import process
import sys
import time


def get_one_student(evaluation_id):
    html_content = network.get_detail(evaluation_id)
    name, exam, bonus = process.calc(html_content)
    return {'id': evaluation_id, 'name': name, 'exam': exam, 'bonus': bonus}


def cmp(i1, i2):
    return i2.get('exam') + i2.get('bonus') - (i1.get('exam') + i1.get('bonus'))


def main(saved_path):
    id_html_content = network.get_list()
    id_list = re.findall(r"(evaluationId=[0-9]+)", id_html_content)
    if len(id_list) <= 0:
        print("连接失败")
        return
    else:
        print("连接成功，请稍后...")

    result = []
    for i in id_list:
        evaluation_id = int(i.replace('evaluationId=', ''))
        result.append(get_one_student(evaluation_id))
        print(len(result) % 10, end="")
        if len(result) % 10 == 0:
            print(" ", end="")
        sys.stdout.flush()
    print("\n")

    form_time = time.strftime("%Y-%m-%d %H%M%S", time.localtime())
    file_name = str(f"{saved_path}/{form_time}.csv")
    out_file = open(file=file_name, mode="w")
    out_text = "排名\t姓名\t考试折分\t加分\t智育总分\n"
    result.sort(key=functools.cmp_to_key(cmp))
    for i, v in enumerate(result):
        exam = v.get('exam')
        bonus = v.get('bonus')
        sum_point = round(exam + bonus, 2)
        out_text += f"{i + 1}\t{v.get('name')}\t{exam}\t{bonus}\t{sum_point}\n"
    print(out_text)
    out_file.write(out_text.replace("\t", ","))

    print(f"文件已经写入 {os.path.abspath(file_name)}\n请使用Excel打开")
    out_file.close()


if __name__ == '__main__':
    res_path = "./result"
    if not os.path.exists(res_path):
        os.mkdir(res_path)
    main(saved_path=res_path)
