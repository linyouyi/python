from django.shortcuts import render, redirect, HttpResponseRedirect,HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from .forms import LoginForm
import paramiko
import json
from . import models
# Create your views here.
def login(request):
    if request.method == 'GET':
        #记录用户原来请求的页面存入session中,登陆成功再后跳转回原来的页面
        request.session['loginfrom'] = request.GET.get('next', '/master/index/')
        login_form = LoginForm()
        return render(request, 'login.html', {'login_form': login_form})
    else:
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                try:
                    # 此处预防未分组的用户登录user_group没有值会报错
                    group = Group.objects.get(user=request.user)
                    user_group = group.name
                except:
                    user_group = "未分组"
                request.session['group'] = user_group
                response = HttpResponseRedirect(request.session['loginfrom'])
                return response
                # return redirect('/master/index/')
            else:
                return render(request, 'login.html', {'login_form':login_form})
        else:
            return render(request, 'login.html', {'login_form': login_form})
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/master/login/')

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
@login_required
def changePass(request):
    if request.method == 'GET':
        return render(request,'changePass.html')
    elif request.method == 'POST':
        import json
        from django.contrib.auth.hashers import make_password
        result = {'status': False, 'error': None, 'data': None}
        #username = request.user
        username = request.POST.get('username')
        oldpassword = request.POST.get('oldpassword')
        print(username,oldpassword)
        try:
            user = auth.authenticate(username=username,password=oldpassword)
            if user is not None and user.is_active:
                newpassword = request.POST.get('newpassword')
                newpassword = make_password(newpassword, None, 'pbkdf2_sha256')#密码加密
                user.password = newpassword
                user.save()
                return HttpResponse('OK')    #修改成功，允许特殊符号
            else:
                return HttpResponse("修改失败!")       #旧密码错误
        except Exception as e:
            result['status'] = False
            result['data'] = "请求出错"
        return HttpResponse(json.dumps(result, ensure_ascii=False))

@login_required
def index(request):
    host_obj = models.Host.objects.all()
    hostgroup = models.HostGroup.objects.all()
    business = models.Business.objects.all()
    return render(request, 'index.html',{'host_obj': host_obj, 'hostgroup': hostgroup, 'business': business,})

@login_required
def hostList(request):
    host_obj = models.Host.objects.all()
    hostgroup = models.HostGroup.objects.all()
    business = models.Business.objects.all()
    return render(request, 'index.html', {'host_obj': host_obj, 'hostgroup': hostgroup, 'business': business,})

@permission_required('master.add_host')
@login_required
def hostAdd(request):
    if request.method == 'GET':
        #获取status_choice有哪些选项,然后传向前端,也可以在前端写成静态的
        status_obj = models.Host.status_choice
        hostgroup = models.HostGroup.objects.all()
        business = models.Business.objects.all()
        return render(request, 'hostAdd.html', {'hostgroup':hostgroup, 'business':business, 'status_obj':status_obj})
    elif request.method == 'POST':
        hostname = request.POST.get("hostname")
        public_ip = request.POST.get("public_ip")
        private_ip = request.POST.get("private_ip")
        system = request.POST.get("system")
        cpu_version = request.POST.get("cpu_version")
        cpu_thread_num = request.POST.get("cpu_thread_num")
        memory = request.POST.get("memory")
        hard_disk = request.POST.get("hard_disk")
        admin_root = request.POST.get("admin_root")
        admin_pass = request.POST.get("admin_pass")
        port = request.POST.get("port")
        host_group = request.POST.get("host_group")
        business = request.POST.get("business")
        status = request.POST.get("status")

        models.Host.objects.create(
            hostname=hostname,
            public_ip=public_ip,
            private_ip=private_ip,
            system=system,
            cpu_version=cpu_version,
            cpu_thread_num=cpu_thread_num,
            memory=memory,
            hard_disk=hard_disk,
            admin_root=admin_root,
            admin_pass=admin_pass,
            port=port,
            hostgroup_id=host_group,
            business_id=business,
            status=status,
        )
        hostgroup = models.HostGroup.objects.all()
        business = models.Business.objects.all()
        return render(request, 'hostAdd.html', {'hostgroup': hostgroup, 'business': business})

@permission_required('master.change_host')
@login_required
def hostEdit(request, id):
    if request.method == 'GET':
        host_obj = models.Host.objects.filter(id=id).first()
        hostgroup = models.HostGroup.objects.all()
        business = models.Business.objects.all()
        return render(request,'hostEdit.html',{'host_obj':host_obj,'hostgroup':hostgroup,'business':business})
    elif request.method == 'POST':
        hostname = request.POST.get("hostname")
        alias = request.POST.get("alias")
        public_ip = request.POST.get("public_ip")
        private_ip = request.POST.get("private_ip")
        system = request.POST.get("system")
        cpu_version = request.POST.get("cpu_version")
        cpu_thread_num = request.POST.get("cpu_thread_num")
        memory = request.POST.get("memory")
        hard_disk = request.POST.get("hard_disk")
        admin_root = request.POST.get("admin_root")
        admin_pass = request.POST.get("admin_pass")
        port = request.POST.get("port")
        host_group = request.POST.get("host_group")
        business = request.POST.get("business")
        status = request.POST.get("status")

        models.Host.objects.filter(id=id).update(
            hostname=hostname,
            alias=alias,
            public_ip=public_ip,
            private_ip=private_ip,
            system=system,
            cpu_version=cpu_version,
            cpu_thread_num=cpu_thread_num,
            memory=memory,
            hard_disk=hard_disk,
            admin_root=admin_root,
            admin_pass=admin_pass,
            port=port,
            hostgroup_id=host_group,
            business_id=business,
            status=status,
        )
        return redirect('/master/index/')

@permission_required('master.delete_host')
@login_required
def hostDelete(request, id):
    models.Host.objects.filter(id=id).delete()
    return redirect('/master/index/')

@permission_required('master.add_hostgroup')
@login_required
def hostGroup(request):
    if request.method == 'GET':
        try:
            # 此处预防位分组的用户登录user_group没有值会报错
            user_group = Group.objects.get(user=request.user)
        except:
            user_group = "未分组"
        host_group = models.HostGroup.objects.all()
        return render(request,'hostGroup.html',{'host_group':host_group,'user_group':user_group})
    elif request.method == 'POST':
        #host_group = request.POST.get('name')
        pass

@permission_required('master.add_hostgroup')
@login_required
def hostGroupAdd(request):
    import json
    ret = {'status':False,'error':None,'data':None}
    try:
        name = request.GET.get('hostgroupname')
        models.HostGroup.objects.create(name=name)
        return HttpResponse('OK')
    except Exception as e:
        ret['status'] = False
        ret['data'] = "请求出错"
    return HttpResponse(json.dumps(ret,ensure_ascii=False))

@permission_required('master.change_hostgroup')
@login_required
def hostGroupEdit(request):
    if request.method == 'GET':
        host_group = models.HostGroup.objects.all()
        return render(request,'hostGroup.html',{'host_group':host_group})
    elif request.method == 'POST':
        import json
        ret = {'status':False,'error':None,'data':None}
        try:
            id = request.POST.get('gid')
            name = request.POST.get('hostgroupname')
            print(name)
            models.HostGroup.objects.filter(id=id).update(name=name)
            return HttpResponse('OK')
        except Exception as e:
            ret['status'] = False
            ret['error'] = "修改失败"
        return HttpResponse(json.dump(ret,ensure_ascii=False))

@permission_required('master.delete_hostgroup')
@login_required
def hostGroupDel(request, id):
    models.HostGroup.objects.filter(id=id).delete()
    return redirect('/master/host/group/')

@permission_required('master.add_host')
@csrf_exempt
@login_required
def hostExecute(request):
    if request.method == 'GET':
        return render(request, 'execute.html')
    elif request.method == 'POST':
        excuteuser = request.user
        ip = request.POST.get('ipaddress')
        user = request.POST.get('remoteuser')
        pwd = request.POST.get('remotepwd')
        command = request.POST.get('command')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, 22, username=user, password=pwd, allow_agent=False, look_for_keys=False, timeout=5)
        stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
        stdout.flush()
        outmsg = stdout.read()
        outmsg = str(outmsg.decode()).replace("\\r\\n","<br>")
        ssh.close()
        #记录操作日志
        excuteip = get_client_ip(request)
        print(excuteip)
        models.ExecuteLog.objects.create(
            hostip=ip,
            hostuser=user,
            hostpass=pwd,
            hostcmd=command,
            excuteuser=excuteuser,
            excuteip=excuteip,
        )
        return HttpResponse(outmsg)

@permission_required('master.add_host')
@login_required
@csrf_exempt
def hostPi(request):
    if request.method == 'GET':
        hostinfo = models.Host.objects.all()
        return render(request, 'hostPi.html',{'hostinfo':hostinfo})
    elif request.method == 'POST':
        excuteuser = request.user
        ip = request.POST.get('ipaddress')
        user = request.POST.get('remoteuser')
        pwd = request.POST.get('remotepwd')
        command = request.POST.get('command')
        x = ip.strip(',').split(',')
        y = user.strip(',').split(',')
        z = pwd.strip(',').split(',')
        res = zip(x,y,z)
        exc_result = ""
        for (ip,user,pwd) in res:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(ip, 22, username=user, password=pwd, allow_agent=False, look_for_keys=False, timeout=5)
                ssh.exec_command(command, get_pty=True)
                stdin, stdout, stderr = ssh.exec_command('echo $?', get_pty=True)
                stdout.flush()
                outmsg = stdout.read()
                print(outmsg)
                #outmsg = str(outmsg.decode()).replace("\\r\\n","")
                print(type(outmsg))
                if (outmsg==b'0\r\n'):
                    exc_result += "主机" + ip + "命令执行成功!</br>"
                    print(exc_result)
                else:
                    exc_result += "主机" + ip + "命令执行失败!</br>"
                    print(exc_result)
                ssh.close()
                #记录操作日志
                excuteip = get_client_ip(request)
                print(excuteip)
                models.ExecuteLog.objects.create(
                    hostip=ip,
                    hostuser=user,
                    hostpass=pwd,
                    hostcmd=command,
                    excuteuser=excuteuser,
                    excuteip=excuteip,
                )
            except:
                exc_result += "主机" + ip + "无法连接!</br>"
                print(exc_result)
                pass
        return HttpResponse(exc_result)

@permission_required('master.add_host')
@csrf_exempt
@login_required
def hostUpload(request):
    if request.method == 'GET':
        return render(request, 'execute.html')
    elif request.method == 'POST':
        excuteuser = request.user
        ip = request.POST.get('ipaddress')
        user = request.POST.get('remoteuser')
        pwd = request.POST.get('remotepwd')
        file = request.FILES.get('fileinput')
        import os
        shell_path = os.path.join('shell',file.name)
        if (os.path.exists(shell_path)):
            result = "文件已经存在,请重新命名文件再上传!"
        else:
            with open (shell_path,'wb') as f:
                for item in file.chunks():	#chunks()分块,一点一点取数据(生成器,迭代器)
                    f.write(item)
            ssh = paramiko.Transport(ip, 22)
            ssh.connect(username=user, password=pwd)
            sftp = paramiko.SFTPClient.from_transport(ssh)
            localfile = shell_path
            remotefile = file.name
            try:
                sftp.put(localfile, remotefile)
                print("上传成功")
                result = "success!"
            except Exception:
                print("[-]put Error:User name or password error or uploaded file does not exist")
                result = "fail!"
            ssh.close()
            # 记录操作日志
            excuteip = get_client_ip(request)
            models.ExecuteLog.objects.create(
                hostip=ip,
                hostuser=user,
                hostpass=pwd,
                excuteuser=excuteuser,
                filepath=shell_path,
                excuteip=excuteip,
            )
        return HttpResponse(result)

# @login_required
# def hostMonitor(request):
#     if request.method == 'GET':
#         status_obj = models.Host.status_choice
#         hostinfo = models.Host.objects.all()
#         hostgroup = models.HostGroup.objects.all()
        # ssh = paramiko.SSHClient()
        # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # ssh.connect('121.196.192.5', 22, 'lin', 'Ningdeshidai-2018')
        # commands = ['top -bn1 | grep Cpu | awk -F\' \' \'{print $2}\'',
        #             'free -h | grep Mem | awk -F\' \' \'{print $7}\' | awk -F\'G\' \'{print $1}\'',
        #             'df -hl | grep /dev/vda1 | awk -F\' \' \'{print $5}\' | awk -F\'%\' \'{print $1}\'',
        #             ]
        # result = []
        # redic = {}
        # for cmd in commands:
        #     stdin, stdout, stderr = ssh.exec_command(cmd)
        #     outmsg = stdout.read().decode()
        #     outmsg = outmsg.replace('\n','')
        #     result.append(outmsg)
        # print(result)
        # for i in range(len(result)):
        #     redic['num'+str(i)] = result[i]
        #return render(request,'monitor.html',{'hostinfo':hostinfo,'hostgroup':hostgroup,'status_obj':status_obj,'cpu_use':redic['num0'],'mem_use':redic['num1'],'disk_use':redic['num2']})
        #return render(request,'monitor.html',{'hostinfo':hostinfo,'hostgroup':hostgroup,'status_obj':status_obj,})

@permission_required('master.add_host')
@csrf_exempt
@login_required
def hostMonitor(request):
    if request.method == 'GET':
        status_obj = models.Host.status_choice
        hostinfo = models.Host.objects.all()
        hostgroup = models.HostGroup.objects.all()
        return render(request,'monitor.html',{'hostinfo':hostinfo,'hostgroup':hostgroup,'status_obj':status_obj})
    elif request.method == 'POST':
        hn = request.POST.get('hostname')
        hg = request.POST.get('hostgroup')
        st = request.POST.get('status')
        data = []
        redata = {}
        if (hn != ''):
            host = models.Host.objects.filter(id=hn)
        if (hg != ''):
            host = models.Host.objects.filter(hostgroup=hg)
        if (st != ''):
            host = models.Host.objects.filter(status=st)
        for rhost in host:
            hname = rhost.alias
            hip = rhost.public_ip
            hroot = rhost.admin_root
            hpass = rhost.admin_pass
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hip, 22, hroot, hpass)
            commands = ['top -bn1 | grep Cpu | awk -F\' \' \'{print $2}\'',
                        'free -h | grep Mem | awk -F\' \' \'{print $7}\' | awk -F\'G\' \'{print $1}\'',
                        'df -hl | grep /dev/vda1 | awk -F\' \' \'{print $5}\' | awk -F\'%\' \'{print $1}\'',
                        ]
            result = []
            redic = {}
            for cmd in commands:
                stdin, stdout, stderr = ssh.exec_command(cmd)
                outmsg = stdout.read().decode()
                outmsg = outmsg.replace('\n', '')
                result.append(outmsg)
            #print(hip,result)
            for i in range(len(result)):
                redic['num' + str(i)] = result[i]
            data.append(redic)
            for i in range(len(data)):
                redata[hname] = data[i]
        #redata={'beida': {'num0': '0.1', 'num2': '19', 'num1': '3.2'}, 'zhongyiyuan': {'num0': '0.2', 'num2': '19', 'num1': '3.3'}}
        print(redata)
        return HttpResponse(json.dumps(redata), content_type='application/json')

def hostSearch(request):
    hostgroup = models.HostGroup.objects.all()
    hostbusiness = models.Business.objects.all()
    line_status = request.POST.get('linestatus')
    group_host = request.POST.get('grouphost')
    business = request.POST.get('business')
    public_ip = request.POST.get('publicip')
    print(public_ip)
    private_ip = request.POST.get('privateip')
    hostname = request.POST.get('hostname')
    if (line_status != ''):
        host = models.Host.objects.filter(status=line_status)
    if (group_host != ''):
        host = models.Host.objects.filter(hostgroup_id=group_host)
    if (business != ''):
        host = models.Host.objects.filter(business_id=business)
    if (public_ip != ''):
        host = models.Host.objects.filter(public_ip=public_ip)
    if (private_ip != ''):
        host = models.Host.objects.filter(private_ip=private_ip)
    if (hostname != ''):
        host = models.Host.objects.filter(hostname=hostname)
    return render(request,'search.html',{'host_obj':host, 'hostgroup': hostgroup, 'business': hostbusiness,})

def get_client_ip(request):
    '''nginx和fastcgi配置要加入如下,不然有可能获取不到HTTP_XFORWARED_FORREMOTE_ADDR'''
    '''fastcgi_param REMOTE_ADDR $remote_addr;'''
    try:
        real_ip = request.META['HTTP_XFORWARED_FOR']
        reip = real_ip.split(",")[0]
    except:
        try:
            reip = request.META['REMOTE_ADDR']
        except:
            reip = ""
    return reip
