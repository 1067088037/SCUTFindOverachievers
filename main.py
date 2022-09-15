import functools
import os
import re
import network
import process
import sys
import time


def get_one_student(evaluation_id):
    moral_html = network.get_moral_detail(evaluation_id)
    moral_base, moral_bonus = process.calc_moral(moral_html)
    moral_sum = moral_base + moral_bonus
    intellectual_html = network.get_intellectual_detail(evaluation_id)
    name, intellectual_exam, intellectual_bonus = process.calc_intellectual(intellectual_html)
    intellectual_sum = intellectual_exam + intellectual_bonus
    gym_html = network.get_gym_detail(evaluation_id)
    gym_base, gym_bonus = process.calc_gym(gym_html)
    gym_sum = gym_base + gym_bonus
    moral_contribution = round(moral_sum * 0.2, 3)
    intellectual_contribution = round(intellectual_sum * 0.65, 3)
    gym_contribution = round(gym_sum * 0.15, 3)
    total = round(moral_contribution + intellectual_contribution + gym_contribution, 3)
    return {'id': evaluation_id, 'name': name,
            'point': [moral_base, moral_bonus, moral_sum, moral_contribution,
                      intellectual_exam, intellectual_bonus, intellectual_sum, intellectual_contribution,
                      gym_base, gym_bonus, gym_sum, gym_contribution],
            'result': total}


def cmp(i1, i2):
    return i2.get('result') - i1.get('result')


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
    out_text = "排名\t姓名\t" \
               "德育基础分\t德育加分\t德育总分\t德育贡献\t" \
               "智育基础分\t智育加分\t智育总分\t智育贡献\t" \
               "文体基础分\t文体加分\t文体总分\t文体贡献\t" \
               "综测总分\n"
    result.sort(key=functools.cmp_to_key(cmp))
    for i, v in enumerate(result):
        out_text += f"{i + 1}\t{v.get('name')}"
        for j in v.get('point'):
            out_text += f"\t{j}"
        out_text += f"\t{v.get('result')}"
        out_text += "\n"
    print(out_text)
    out_file.write(out_text.replace("\t", ","))

    print(f"文件已经写入 {os.path.abspath(file_name)}\n请使用Excel打开")
    out_file.close()


if __name__ == '__main__':
    res_path = "./result"
    if not os.path.exists(res_path):
        os.mkdir(res_path)
    main(saved_path=res_path)
