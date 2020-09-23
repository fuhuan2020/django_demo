from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import json, time, requests, datetime
from assets import forms
import functools, os
from requests_toolbelt import MultipartEncoder
import traceback, heapq, datetime
from django.contrib.auth.models import User
from django.contrib import auth
from demo.settings import BASE_DIR
from common.logs import request_log
from common.utils import mkdirs,open_write_json,open_read_json

CODE_000 = "000"
CODE_001 = "001"
CODE_111 = "111"
DESC = {"000": "请求成功", "001": "请求失败", "111": "登录失败"}


def login_out(request, login_out=False, action="dashboard", *args, **kwargs):
    '''
    :param request: 判断是否登录 如未登录直接返回登录页面
    :param login_out:
    :return:
    '''
    if not login_out and request.session.get('is_login', None):
        return False
    else:
        if request.method == "POST":
            result = CODE_111
            desc = "请重新登录"
            js = {'result': result, 'desc': desc}
            text = json.dumps(js)
            return HttpResponse(text, content_type="application/json")
        else:
            login_form = forms.UserForm()
            req = render(request, 'assets/login.html', locals())
            req.set_cookie("action", action, 120)
            return req

    pass


def is_login(request):
    if request.session.get('is_login', None):
        return True
    return False


def check_login(action="dashboard"):
    '''
    检查是否登录
    :param action:
    :return:
    '''

    def decorator(func):
        @functools.wraps(func)
        def dd(*args, **kwargs):
            flag = login_out(action=action, *args, **kwargs)
            if flag:
                return flag
            return func(*args, **kwargs)

        return dd

    return decorator

def login(request):
    def action_post(request):
        result = "001"
        desc = "请求成功"
        action = request.POST.get("action")
        # print(request.POST)
        if is_login(request) and action == "login_out":
            # print(request.session.get("is_login"))
            if request.session.get("is_login"):
                request.session["is_login"] = False
                request.session.flush()
                result = CODE_000
            else:
                result = CODE_001
                desc = "退出失败"
            pass
        js = {'result': result, 'desc': desc}
        text = json.dumps(js)
        return HttpResponse(text, content_type="application/json")
        pass

    login_status = login_out(request)

    if request.method == 'POST':
        action = request.POST.get("action")
        if action:
            return action_post(request)
        else:
            login_form = forms.UserForm(request.POST)
            message = '请检查填写的内容！'
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = auth.authenticate(username=username, password=password)
                # print(user)
                if user is not None:
                    # auth_login(request,user)
                    # 这个用户存在数据库中
                    request.session['is_login'] = True
                    request.session.set_expiry(60 * 60 * 12 * 7)
                    ac = request.COOKIES.get("action")
                    u = User.objects.get(username=username)
                    u.last_login = datetime.datetime.now()
                    u.save()
                    if ac:
                        return redirect('/assets/%s/' % ac)
                    return redirect('/assets/dashboard/')
                    pass
                else:
                    # 用户名或者密码错误
                    return render(request, 'assets/login.html', locals())
                    pass
    # 判断是否登录，登录直接进入
    if not login_status:
        if request.session.get("action"):
            action = request.session["action"]
        else:
            action = "dashboard"
        return redirect('/assets/%s/' % action)
    login_form = forms.UserForm()
    return render(request, 'assets/login.html', locals())


# @check_login("register")
def register(request):
    if request.method == 'POST':
        login_form = forms.UserRegForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            password2 = login_form.cleaned_data.get('password2')
            reg_code = login_form.cleaned_data.get('reg_code')
            user = auth.authenticate(username=username)
            if user == None and password == password2 and reg_code == "66666":
                kwargs = dict(username=username, password=password)
                User.objects.create_user(**kwargs)
                message = '注册成功'
                return render(request, 'assets/login.html', locals())
            else:
                message = '注册失败'
        return render(request, 'assets/register.html', locals())
    else:
        login_form = forms.UserRegForm()
        return render(request, 'assets/register.html', locals())
    pass


@check_login("index")
def index(request):
    """
    资产总表视图
    :param request:
    :return:
    """
    # return render(request, 'assets/index.html', locals())
    # return render(request, 'assets/login.html', locals())
    ip = "192.168.88.125"
    type = "icmp"
    area = "广州"
    ip = "192.168.88.125"
    ip = "192.168.88.125"
    domain = "www.baidu"
    interval = "2"
    create_time = "2012"
    update_time = "2011"
    record_id = "001"
    remove = 1
    if remove == 1:
        remove = "运行中"
    return render(request, 'assets/pingdetail.html', locals())

@request_log
@check_login("kvm")
def kvm(request):
    class HostData(object):
        # http://192.168.88.87/vnc_lite.html?host=192.168.9.140&port=8007&path=websockify/?token=34
        host = None
        hostname = None
        selected = False
        vnc_lite_host = None
        vnc_host = None
        vnc_port = None

        def __init__(self, host=None, hostname=None, selected=False, vnc_host=None, vnc_lite_host=None, vnc_port=None):
            self.host = host
            self.hostname = hostname
            self.selected = selected
            self.vnc_lite_host = vnc_lite_host
            self.vnc_host = vnc_host
            self.vnc_port = vnc_port

        pass

    class KvmBean(object):
        id = None
        name = None
        status = None
        uuid = None
        memory = None
        cpu = None
        source_path = None
        port = None
        macs = None
        power_on = False
        create_time = None
        create_time_str = None
        tag = None
        desc = None
        eth0_ip = None,
        eth0_net = None,
        os_version = None,

        def __init__(self, id=None,
                     name=None,
                     create_time=None,
                     desc=None,
                     tag=None,
                     status=None,
                     uuid=None,
                     memory=None,
                     cpu=None,
                     source_path=None,
                     eth0_ip=None,
                     eth0_net=None,
                     eth1_ip=None,
                     eth1_net=None,
                     os_version=None,
                     port=None,
                     macs=None, *args, **kwargs):
            self.id = int(id) + 1
            self.name = name
            if status == 0:
                self.status = "stop"
            elif status == 1:
                self.status = "running"
                self.power_on = True
            else:
                self.status = "None"
            self.uuid = uuid
            self.memory = str(int(float(memory) / 1.024 / 1000))
            self.cpu = cpu
            self.source_path = source_path
            self.port = port
            self.macs = macs
            self.tag = tag
            self.create_time = create_time
            self.desc = desc
            self.eth0_ip = eth0_ip
            self.eth0_net = eth0_net
            self.os_version = os_version
            if kwargs.get("ips"):
                ips=kwargs["ips"]
                self.eth0_ip=ips
            if create_time:
                self.create_time_str = datetime.datetime.fromtimestamp(create_time)

    def __get_kvm_host(host=None):
        evn = BASE_DIR + "/conf/kvm_host.json"
        data_list=open_read_json(evn)
        if not data_list:
            mkdirs(evn)
            data1 = dict(host="192.168.88.86:8001", hostname="192.168.88.86",vnc_lite_host="192.168.88.86",
                         vnc_host="192.168.88.86", vnc_port="8007")
            data2 = dict(host="192.168.88.87:8008", hostname="192.168.88.87", vnc_lite_host="192.168.88.87",
                         vnc_host="192.168.88.87", vnc_port="8007")

            data_list = [data1, data2]

        open_write_json(evn,data_list)
        hos_datas_list = []
        local_bean = None
        for item in data_list:
            h = None
            if host and item["host"] == host:
                item["selected"] = True
                h = HostData(**item)
                local_bean = h
            else:
                h = HostData(**item)

            hos_datas_list.append(h)

        return hos_datas_list, local_bean

    def __get_kvm_info_json_file(diqu):
        evn = BASE_DIR + "/media/kvm/"
        mkdirs(evn)
        kvm_info_dict = {}
        kvm_json_file = evn + "kvm_%s.json" % str(diqu).replace(".", "_").replace(":", "_")
        try:
            with open(kvm_json_file, "r") as kvm_info:
                kvm_info_dict = json.load(kvm_info)
        except Exception as e:
            traceback.print_exc()
            pass

        return kvm_info_dict
        pass

    def __save_kvm_info_json_file(diqu, data_dict):
        evn = BASE_DIR + "/media/kvm/"
        kvm_json_file = evn + "kvm_%s.json" % str(diqu).replace(".", "_").replace(":", "_")
        if not os.path.exists(evn):
            os.mkdir(evn)
        try:
            with open(kvm_json_file, "w") as kvm_info:
                json.dump(data_dict, kvm_info, indent=4, ensure_ascii=False)
        except Exception as e:
            traceback.print_exc()
            pass
        pass

    def post_request(diqu, data_dict):
        '''
        通用方法
        :param data_dict:
        :return:
        '''
        result_dict = None
        da = data_dict
        url = "http://%s/kvm" % diqu
        result = requests.post(url, data=da)
        if result and result.status_code == 200:
            try:
                result_dict = json.loads(result.content)
            except Exception as e:
                print("解析错误")
                print(result.content)
                raise ValueError(str(e))
            pass
        elif result:
            print(result.status_code)
        else:
            print("未知错误")
        return result_dict

    def kvm_host(request_dict):
        diqu = request_dict["diqu"]
        bean_list = []
        da = dict(js="kvm_info", )
        result_dict = post_request(diqu, da)
        kvm_info_dict = __get_kvm_info_json_file(diqu)
        if result_dict and result_dict.get("result"):
            if result_dict["result"] == "000":
                data_list = result_dict.get("data")
                print(data_list)
                bean_list = []
                for da in data_list:
                    if kvm_info_dict.get(da["name"]):
                        old = kvm_info_dict.get(da["name"])
                        old.update(da)
                        kvm_info_dict[da["name"]] = old
                    else:
                        da["create_time"] = time.time()
                        kvm_info_dict[da["name"]] = da
                        old = da
                    b = KvmBean(**old)
                    bean_list.append(b)

        __save_kvm_info_json_file(diqu, kvm_info_dict)
        bean_list = heapq.nsmallest(len(bean_list), bean_list, key=lambda x: str(x.create_time))
        bean_list.reverse()
        for i, item in enumerate(bean_list):
            item.id = i + 1
        kvm_datas = bean_list
        return kvm_datas
        pass

    def os_install(data_dir):
        result = False
        req_dict = {}
        re_tag = data_dir["tag"]
        desc = data_dir["desc"]
        host = data_dir["diqu"]
        eth0_ip = data_dir.get("eth0_ip")
        if eth0_ip:
            if len(str(eth0_ip).split(".")) == 4:
                req_dict["eth0_ip"] = eth0_ip
            else:
                raise ValueError("raise", "eth0_ip error")
        eth0_netmask = data_dir.get("eth0_net")

        if eth0_netmask:
            if len(str(eth0_netmask).split(".")) == 4:
                req_dict["eth0_net"] = eth0_netmask
            else:
                raise ValueError("raise", "eth0_netmask error")

        req_dict["js"] = "create"
        req_dict["os_version"] = data_dir["system"]
        req_dict["cpu_num"] = data_dir["he"]
        req_dict["memory_num"] = data_dir["memory"]
        req_dict["disk_size"] = data_dir["disk"]
        result_dict = post_request(host, req_dict)
        if result_dict and result_dict.get("result"):
            if result_dict["result"] == "000":
                if result_dict.get("data"):
                    data_dict = result_dict["data"]
                    tag = data_dict.get("tag")  # kvm常见机子的名字
                    data_info = dict(tag=re_tag, desc=desc, create_time=time.time(), eth0_ip=eth0_ip,
                                     eth0_net=eth0_netmask, os_version=data_dir["system"])
                    kvm_dict = __get_kvm_info_json_file(host)
                    kvm_dict[tag] = data_info
                    __save_kvm_info_json_file(host, kvm_dict)
        return result_dict

        pass

    def js_post(request, request_dict):
        result = "001"
        desc = "请求失败"
        data = ""
        error_message = None
        try:
            action = request_dict["js"]
            if action == "stop" or action == "start" or action == "reboot" or action == "destroy" or action == "kuaiz" or action=="eth1:" or action=="make_mirror":  # 关机
                uuid = request_dict["uuid"]
                diqu = request_dict["diqu"]
                version_num=str(time.time()).split(".")[0]
                req_dict = dict(uuid=uuid, js=action,version_num=version_num)
                result_dir = post_request(diqu, req_dict)
                result = result_dir["result"]
                desc = result_dir["desc"]
                data = result_dir["data"]
            elif action == "re_install":
                uuid = request_dict["uuid"]
                diqu = request_dict["diqu"]
                name = request_dict["name"]
                req_dict = dict(uuid=uuid, js=action, s_uuid=uuid)
                all_info_dict = __get_kvm_info_json_file(diqu)
                info_dict = all_info_dict.get(name)
                if info_dict:
                    eth0_ip = info_dict["eth0_ip"]
                    eth0_net = info_dict["eth0_net"]
                    os_version = info_dict["os_version"]
                    if eth0_ip and eth0_net:
                        req_dict["eth0_ip"] = eth0_ip
                        req_dict["eth0_netmask"] = eth0_net
                        req_dict["os_version"] = os_version
                result_dir = post_request(diqu, req_dict)
                result = result_dir["result"]
                desc = result_dir["desc"]
                data = result_dir["data"]
        except Exception as e:
            traceback.print_exc()
            desc = str(e)
        return json.dumps({'result': result, 'desc': desc, 'data': data})

    def form_post(request, request_dict):
        error_message = None
        try:
            host_data_list, local_bean = __get_kvm_host(request_dict["diqu"])
            action = request_dict["form"]
            if action == "kvm_host":  # 获取该地区kvm列表
                diqu = request_dict["diqu"]
                kvm_datas = kvm_host(request_dict)

            elif action == "kvm_images":
                host = request_dict["diqu"]
                error_message = "请选择系统参数："
                neihes = ["1", "2", "3", "4"]
                memorys = ["1024", "2048", "3072","4096"]
                yingpans = ["20", "30", "40", "50","70","80","100","200","300"]
                result = post_request(host, dict(js="all_images"))
                kvm_images = result["data"]
            elif action == "os_install":
                error_message = os_install(request_dict)
            elif action == "xiugai":
                xiugai = True
                uuid = request_dict["uuid"]
                diqu = request_dict["diqu"]
                name = request_dict["name"]
                kvm_info_dict = __get_kvm_info_json_file(diqu)
                info = kvm_info_dict.get(name)
                if info:
                    info_bean = KvmBean(**info)
            elif action == "xiugai_":
                diqu = request_dict["diqu"]
                tag = request_dict["tag"]
                desc = request_dict["desc"]
                name = request_dict["name"]
                info_dict = __get_kvm_info_json_file(diqu)
                data_dict = info_dict[name]
                data_dict["desc"] = desc
                data_dict["tag"] = tag
                __save_kvm_info_json_file(diqu, info_dict)
                error_message = "修改成功，请重新刷新列表！"
                pass

            pass
        except Exception as e:
            error_message = str(e)
            traceback.print_exc()

        return render(request, 'assets/kvm.html', locals())

    def get(request):
        error_message = "哈哈"
        try:
            host_data_list, local_bean = __get_kvm_host()
        except Exception as e:
            traceback.print_exc()
        return render(request, 'assets/kvm.html', locals())

    # 接口入口
    if request.method == 'POST':
        request_dir = request.POST
        form = request_dir.get("form")
        js = request_dir.get("js")
        if form:
            return form_post(request, request_dir)
        elif js:
            return HttpResponse(js_post(request, request_dir), content_type="application/json")
    else:
        return get(request)

    return render(request, 'assets/kvm.html', locals())


@request_log
@check_login("dashboard")
def dashboard(request):
    return render(request, 'assets/dashboard.html', locals())
