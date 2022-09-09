import urllib3
import config

detail_url = 'http://xsgl.7i5q.cas.scut.edu.cn/sms2/student/module/evaluation/studentIntellectualDetail.jsp'
list_url = 'http://xsgl.7i5q.cas.scut.edu.cn/sms2/student/evaluation/intellectualList.jsp'

cookies = {'Cookie': config.cookies.strip()}
http = urllib3.PoolManager()


def get_detail(evaluationId: int):
    res = http.request(
        method='GET',
        url=detail_url + '?evaluationId=' + evaluationId.__str__() + '&classYearId=' + str(
            config.classYearId),
        headers=cookies)
    return res.data.decode('UTF-8')


def get_list():
    res = http.request(method='POST',
                       url=list_url,
                       headers=cookies)
    return res.data.decode('UTF-8')
