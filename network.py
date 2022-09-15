import urllib3
import config

list_url = 'http://xsgl.7i5q.cas.scut.edu.cn/sms2/student/evaluation/intellectualList.jsp'
moral_url = 'http://xsgl.7i5q.cas.scut.edu.cn/sms2/student/module/evaluation/studentMoralDetail.jsp'
intellectual_url = 'http://xsgl.7i5q.cas.scut.edu.cn/sms2/student/module/evaluation/studentIntellectualDetail.jsp'
gym_url = 'http://xsgl.7i5q.cas.scut.edu.cn/sms2/student/module/evaluation/studentGymDetail.jsp'

cookies = {'Cookie': config.cookies.strip()}
http = urllib3.PoolManager()


def http_request(url: str, evaId: int):
    res = http.request(
        method='GET',
        url=url + '?evaluationId=' + evaId.__str__() + '&classYearId=' + str(config.classYearId),
        headers=cookies)
    return res.data.decode('UTF-8')


def get_moral_detail(evaluationId: int):
    return http_request(moral_url, evaluationId)


def get_intellectual_detail(evaluationId: int):
    return http_request(intellectual_url, evaluationId)


def get_gym_detail(evaluationId: int):
    return http_request(gym_url, evaluationId)


def get_list():
    res = http.request(method='POST',
                       url=list_url,
                       headers=cookies)
    return res.data.decode('UTF-8')
