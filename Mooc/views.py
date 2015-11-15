# -*- coding:utf-8 -*-
from django.template import RequestContext
from django.http import FileResponse
from django.shortcuts import render_to_response, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from Mooc.models import *
from Mooc.forms import *
import urllib2
import StringIO
import random
import datetime
from os import environ
#from sae.ext.storage import monkey
from django.http import JsonResponse
from django.template import Context,loader
from django.http import HttpResponse
import os
# Create your views here.
STUDY_TIME_INF = 2999


def ren2res(template, request, dic={}):
    if request.user.is_authenticated():
        dic.update({'user': {'id': request.user.id, 'name': request.user.get_username()}})
        userinfo = request.user.info
        dic.update({'userinfo': userinfo})
    else:
        dic.update({'user': False})
    if request:
        return render_to_response(template, dic, context_instance=RequestContext(request))
    else:
        return render_to_response(template, dic)


def home(request):
    courses = list(Course.objects.all().order_by('id')[0:6])
    if Course.objects.all().count() > len(courses):
        Flag = True
    else:
        Flag = False
    courseclass = 'all'
    number=2
    courses_num=[]
    for i in range(0,len(courses)):
        if((i+1)%3 == 1):
            courses_num.append([courses[i],0])
            print(courses[i].img)
        elif ((i+1)%3 == 2):
            courses_num.append([courses[i],-1])
            print(courses[i].img)
        else:
            courses_num.append([courses[i],1])
            print(courses[i].img)
    #推荐课程
    str = ['first','second','third']
    course_like = list(Course.objects.all().order_by('-likeCounter')[0:3])
    courses_like = []
    for i in range(0,3):
        courses_like.append([course_like[i],str[i]])
    return ren2res('index.html', request, {'courses_num': courses_num,'courseclass':courseclass,'number':number,'Flag':Flag,'courses_like':courses_like,})


def login(request):
    print('login')
    # 第一次请求到get方法，返回页面
    if request.method == 'GET':
        # 匿名用户说明未登陆
        if request.user.is_anonymous():
            # 后继访问请求
            request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
            loginform = LoginForm()
            return ren2res('./user/login.html', request, {'loginform': loginform})
        else:
            # 已登录用户，登陆无效
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    # post方法，包含了name pw
    elif request.method == 'POST':
        # 验证身份
        loginform = LoginForm(request.POST)
        # 用于判断登录的表单的数据是否合法
        if loginform.is_valid():
            username = loginform.cleaned_data['username']
            password = loginform.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)

            print(request.META.get('HTTP_REFERER'))
            str_list = request.META.get('HTTP_REFERER').split('/')
            str_http = ''
            k=0
            for i in range(0,len(str_list)):
                if str_list[i] == '?next=':
                    k=1
                elif k:
                    str_http += '/'+str_list[i]
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect(str_http)
            else:
                # 按说不会到这一步，如果到了就是写错了
                #这一步应该是用户名，密码不匹配才执行吧
                return ren2res('./user/login.html', request, {'loginform': loginform})
        else:
            return ren2res('./user/login.html', request, {'loginform': loginform})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def register(request):
    if request.method == 'GET':
        registerform = RegisterForm()
        return ren2res('./user/register.html', request, {'registerform': registerform})
    elif request.method == 'POST':
        print(request.POST)
        registerform = RegisterForm(request.POST)
        if registerform.is_valid():
            username = registerform.cleaned_data['username']
            password1 = registerform.cleaned_data['password1']
            password2 = registerform.cleaned_data['password2']
            nickname = registerform.cleaned_data['nickname']
            # 先不保存下列信息，改到个人主页再填写
            # school = registerform.cleaned_data['school']
            # birthday = registerform.cleaned_data['birthday']
            # sex = registerform.cleaned_data['sex']
            # userform = {'username': username, 'password1': password1, 'pass2': password2,
            # 'nickname': nickname, 'school': school, 'birthday': birthday, 'sex': sex}
            # 用于存储用户信息
            newuser = User()
            newuser.username = username
            newuser.set_password(password1)
            newuser.save()
            newuserinfo = UserInfo(user=newuser, nickname=nickname)
            newuserinfo.save()
            user = auth.authenticate(username=username, password=password1)
            auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            print('error')
            registerform.password1 = ''
            registerform.password2 = ''
            try:
                username_error = str(registerform.errors['username'])[26:-10]
            except:
                username_error=None;

            try:
                password1_error = str(registerform.errors['password1'])[26:-10]
            except:
                password1_error=None;

            try:
                password2_error = str(registerform.errors['password2'])[26:-10]
            except:
                password2_error=None;
            registerform.errors.clear()
            return ren2res('./user/register.html', request, {'registerform': registerform,'username_error':username_error,
                                                                'password1_error':password1_error,'password2_error':password2_error})

@login_required
def change_pass(request):
    old = str(request.POST.get('old'))
    new1 = str(request.POST.get('new1'))
    new2 = str(request.POST.get('new2'))
    #print(old+new1+new2)
    username = request.user.username
    #print('username='+str(username))
    user = auth.authenticate(username=username, password=old)
    #print(request.user)
    if user is None:
        print('error1')
        message = u'原密码错误'
        return JsonResponse({'message':message})
    elif new1 != new2:
        message = u'两次密码不一致'
        return JsonResponse({'message':message})
    else:
        user.set_password(new1)
        user.save()
        message = u'保存成功'
        auth.login(request, user)
        return JsonResponse({'message':message})

@login_required
def change_info(request):
    sex = request.POST.get('sex')
    birthday = request.POST.get('birthday')
    school = request.POST.get('school')
    userinfo = request.user.info
    if sex is not None:
        userinfo.sex = sex
    if birthday != '':
        userinfo.birthday = birthday
    if school is not None:
        userinfo.school = school
    try:
        content = request.FILES["file1"]
        online = environ.get("APP_NAME", "")
        if len(content) != 0 and online:
            import sae.const
            access_key = sae.const.ACCESS_KEY
            secret_key = sae.const.SECRET_KEY
            appname = sae.const.APP_NAME
            domain_name = "mooc"
            import sae.storage
            s = sae.storage.Client()
            ob = sae.storage.Object(content.read())
            dir = 'img/user/'+str(request.user.id)
            url = s.put(domain_name, dir, ob)
            userinfo.img = url
    except Exception:
        print(1)
    userinfo.save()
    return JsonResponse({'message': u'个人信息修改成功！', 'user_img': userinfo.img})

@login_required
def course_summary(request, cid):
    #try:
    if True:
        servertime = datetime.date.today()
        course = Course.objects.get(id=cid)
        units = course.units.all().order_by('counter')
        unit_sum = len(units)
        begintime = course.cur_time.begin_time  # .replace(tzinfo=None)
        time_list = course.times.all().order_by('begin_time')
        # total_hour是一门课总共需要的小时数
        total_days = 0
        for unit in units:
            total_days += unit.gap_days
        # delta_hour是距今为止这门课经历的小时数
        delta_days = int((servertime - begintime).days)
        if ((delta_days >= 0) and (delta_days > total_days)) or int(course.cur_time.begin_time.year) == STUDY_TIME_INF:
            old_time = course.cur_time
            old_time.cur_course = None
            old_time.save()
            for t in time_list:
                delta = int((servertime - t.begin_time).days)
                if delta <= total_days:
                    t.cur_course = course
                    t.save()
                    break
        if int(course.cur_time.begin_time.year) == STUDY_TIME_INF:
            # 排除bug，当没有一个time可以作为选课时间的时候
            click = False
            message = u'暂无课程安排'
            return ren2res('./course/course_index.html', request,
                           {'click': click, 'course': course, 'units': units, 'message': message, 'unit_sum': unit_sum})
    # except Exception:
    #     raise Http404
    if course is not None:
        result = StudyStatus.objects.filter(course=course, user=request.user)
        course_begintime = course.cur_time.begin_time
        times = []
        # 加上当前的开课日期
        times.append(course.cur_time)
        for time in time_list:
            begin_time = time.begin_time
            if int((servertime-begin_time).days) <= int((course.units.all()[0]).gap_days) and int(begin_time.year) != STUDY_TIME_INF:
                times.append(time)
        if len(result) == 0:
            if len(times) != 0:
                click = True
                message = u'报名选课'
                return ren2res('./course/course_index.html', request,
                               {'click': click, 'time_list': time_list, 'course': course, 'units': units,
                                'message': message, 'times': times, 'unit_sum': unit_sum})
            else:
                click = False
                message = u'暂无选课安排'
                return ren2res('./course/course_index.html', request,
                                {'click': click, 'time_list': time_list, 'course': course, 'units': units,
                                'message': message, 'times': times, 'unit_sum': unit_sum})
        else:
            # 选了这门课了
            studystatus = result[0]
            if studystatus.course_time.begin_time < course_begintime:
                # 询问用户是否重新选课
                if len(times) == 0:
                    click = False
                    message = u'暂无选课安排'
                    return ren2res('./course/course_index.html', request,
                               {'click': click, 'time_list': time_list, 'course': course, 'units': units,
                                'message': message, 'times': times, 'unit_sum': unit_sum})
                else:
                    click = True
                    message = u'重新选课'
                    warning_mess = u'重新选课后，关于这门课的所有学习记录都将被清除，请谨慎选择！'
                    return ren2res('./course/course_index.html', request,
                                   {'click': click, 'time_list': time_list, 'course': course, 'units': units,
                                    'message': message, 'times': times, 'warning_mess': warning_mess,
                                    'unit_sum': unit_sum})
            else:
                # 目前正在学习
                if course_begintime > servertime or course_begintime < studystatus.course_time.begin_time:
                    # 还未开课
                    click = False
                    message = u'等待开课'
                    return ren2res('./course/course_index.html', request,
                                    {'click': click, 'course': course, 'units': units, 'message': message,
                                    'studystatus': studystatus, 'unit_sum': unit_sum})
                else:
                    # 可以学习
                    click = True
                    message = u'开始学习'
                    return ren2res('./course/course_index.html', request,
                                     {'click': click, 'course': course, 'units': units, 'message': message,
                                    'studystatus': studystatus, 'unit_sum': unit_sum})
    else:
        raise Http404


@login_required
def study(request):
    course_id = request.GET.get('cid')
    if course_id is None:
        print('wtf?!')
        return HttpResponseRedirect('/')
    course_id = int(course_id)
    course = Course.objects.get(id=course_id)
    # 排除Url漏洞
    result = StudyStatus.objects.filter(course=course, user=request.user)
    if len(result) == 0:
        print('error0')
        return HttpResponseRedirect('/')
    # 获取服务器时间，课程开始时间
    servertime = datetime.date.today()
    course_begin_time = course.cur_time.begin_time
    # 判断课程是否开始
    if servertime < course_begin_time:
        # 课程未开始
        return HttpResponseRedirect('/course/' + str(course_id))
    else:
        print('coursestart')
        # 课程已开始执行else
        #获取将要学习的unit
        units = course.units.order_by('counter')
        delta_days = int((servertime - course_begin_time).days)
        gap_days = 0
        cnt = -1
        for unit in units:
            cnt += 1
            gap_days += unit.gap_days
            if gap_days >= delta_days:
                obj_unit = units[cnt]
                break
        print(obj_unit.counter)
        unit_cnt = request.GET.get('unit_cnt')
        if unit_cnt is None:
            # 直接给出当前unit的第一个section
            sections = obj_unit.sections.all().order_by('counter')
            section = sections[0]
            video = str(section.video)
            pdf = str(section.pdf)[5:]
            # 返回前更新一下section的访问信息
            section_cnt = 1
            unit_cnt = obj_unit.counter
            #------------------获取用户笔记--------------------------
            try:
                usernote = UserNote.objects.get(user_id=request.user.id,course=course,unit_counter=unit_cnt)
            except Exception:
                usernote=None
            #--------------------------------------------------------
            studystatus = StudyStatus.objects.get(course=course, user=request.user)
            result = studystatus.quizstore.filter(unit_counter=unit_cnt, section_counter=section_cnt)
            if len(result) == 0:
                quizstore = QuizStore(unit_counter=unit_cnt, section_counter=section_cnt, studystatus=studystatus)
            else:
                quizstore = result[0]
            quizstore.visit = True
            quizstore.save()
            # 更新last_section
            studystatus.last_section = max(int(studystatus.last_section), int(section.total_counter))
            studystatus.save()
            return ren2res('./course/study.html', request, {'section': section, 'video': video, 'pdf': pdf,
                                                            'course': course, 'units': units, 'obj_unit': obj_unit,
                                                            'usernote':usernote,'course_id':course_id,'unit_cnt':unit_cnt,})
        unit_cnt = int(unit_cnt)
        section_cnt = request.GET.get('section_cnt')
        if section_cnt is None:
            return HttpResponseRedirect('/course/' + str(course_id))
        section_cnt = int(section_cnt)

        # 得到目标section
        try:
            section = course.units.all().get(counter=unit_cnt).sections.all().get(counter=section_cnt)
        except Exception:
            print('erroeqqq')
            raise Http404
        if section.unit.counter > obj_unit.counter:
            tmp_section = obj_unit.sections.all().order_by('-counter')[0]
            return HttpResponseRedirect(
                '/study/?cid=' + str(course_id) + '&unit_cnt=' + str(obj_unit.counter) + '&section_cnt=' + str(
                    tmp_section.counter))

        #------------------获取用户笔记--------------------------
        try:
            usernote = UserNote.objects.get(user_id=request.user.id,course=course,unit_counter=unit_cnt)
        except Exception:
            usernote=None
        #--------------------------------------------------------
        # 正常返回
        video = str(section.video)
        pdf = str(section.pdf)[5:]
        # 返回前更新一下section的访问信息
        studystatus = StudyStatus.objects.get(course=course, user=request.user)
        result = studystatus.quizstore.filter(unit_counter=unit_cnt, section_counter=section_cnt)
        if len(result) == 0:
            quizstore = QuizStore()
            quizstore.unit_counter = unit_cnt
            quizstore.section_counter = section_cnt
            quizstore.studystatus = studystatus
        else:
            quizstore = result[0]
        quizstore.visit = True
        quizstore.save()
        # 更新last_section
        studystatus.last_section = max(int(studystatus.last_section), int(section.total_counter))
        studystatus.save()
        return ren2res('./course/study.html', request, {'section': section, 'video': video, 'pdf': pdf,
                                                        'course': course, 'units': units, 'obj_unit': obj_unit,
                                                         'usernote':usernote,'course_id':course_id,'unit_cnt':unit_cnt})


def study_index(request, cid):
    course = Course.objects.get(id=cid)
    units = course.units.all().order_by('counter')
    user = request.user
    studystatus = StudyStatus.objects.get(course=course, user=user)
    if studystatus.course_time.begin_time == course.cur_time.begin_time:
        finished = False
    else:
        finished = True
    unit = []
    for i in range(1, len(units) + 1):
        # print(len(studystatus.teststore.filter(unit_counter=i)))
        unit.append([course.units.get(counter=i), studystatus.teststore.filter(unit_counter=i)])
    last_section_cnt = int(studystatus.last_section)
    # 未开始学习
    if last_section_cnt == 0:
        last_section_cnt = 1
        next_section_cnt = 1
        last_section = course.sections.all().get(total_counter=last_section_cnt)
        next_section = course.sections.all().get(total_counter=next_section_cnt)
        return ren2res('./course/study_index.html', request,
                   {'course': course, 'units': unit, 'studystatus': studystatus, 'last_section': last_section,
                    'next_section': next_section, 'finished': finished})
    last_section = course.sections.all().get(total_counter=last_section_cnt)
    next_section_cnt = last_section_cnt + 1
    if next_section_cnt > len(course.sections.all()):
        next_section_cnt = len(course.sections.all())
    next_section = course.sections.all().get(total_counter=next_section_cnt)
    return ren2res('./course/study_index.html', request,
                   {'course': course, 'units': unit, 'studystatus': studystatus, 'last_section': last_section,
                    'next_section': next_section, 'finished': finished})


@login_required
def take_course(request):
    try:
        course_id = request.GET.get('cid')
        course = Course.objects.get(id=course_id)
        time_id = request.GET.get('tid')
        time = CourseTime.objects.get(id=time_id)
        user = request.user
        result = StudyStatus.objects.filter(course=course, user=user)
        if len(result) >= 1:
            # 此处询问用户是否删除记录重新选课
            result[0].delete()
            print('chongxinxuanke')
            # 此处不重定向，直接继续进行下方的Studystatus的新建过程。
            # return HttpResponseRedirect('/course/' + str(course_id), request)
    except:
        raise Http404
    if len(StudyStatus.objects.filter(course=course, user=user)) == 0:
        studystatus = StudyStatus()
        studystatus.course = course
        studystatus.user = user
        studystatus.course_time = time
        studystatus.save()
    else:
        raise Http404
    return HttpResponseRedirect('/course/' + str(course_id), request)


@login_required
def take_quiz(request, course_id, unit_cnt, section_cnt):
    try:
        course = Course.objects.get(id=course_id)
        user = request.user
        quiz = course.units.all().get(counter=unit_cnt).sections.all().get(counter=section_cnt).quiz
        result = StudyStatus.objects.filter(course=course, user=user)
        if len(result) == 0:
            return HttpResponseRedirect('/')
        studystatus = result[0]
    except Exception:
        print('error1')
        raise Http404
    question = quiz.questions.all()
    questions = []
    for item in question:
        questions.append(item)
    if request.method == 'GET':
        try:
            quizstore = studystatus.quizstore.all().filter(unit_counter=unit_cnt, section_counter=section_cnt)
            if len(quizstore) == 1:
                # 用户之前做过这个quiz，要提取出答案传回html
                quizstore = quizstore[0]
                Answer = list(quizstore.Answer)
                for num in range(0, len(Answer)):
                    questions[num].user_answer = Answer[num]
                    # ......
            else:
                # 不存在quizstore
                # 为用户创建quizstore
                quizstore = QuizStore(studystatus=studystatus, unit_counter=unit_cnt, section_counter=section_cnt)
                quizstore.save()
                Answer = []
            # 按照之前的写就可以了
            # ....
            return ren2res('./course/quiz.html', request,
                           {'Question': question, 'Answer': Answer, 'course_id': course_id, 'unit_cnt': unit_cnt,
                            'section_cnt': section_cnt})
        except Exception:
            print('error2')
            raise Http404
    elif request.method == 'POST':
        try:
            # 得到用户上传的并进行处理，记得把原来的删除，新修改的save
            if ''.join(request.POST.get('DoQuiz').split()) == 'Redo':
                Answer = []
            else:
                studystatus = result[0]
                quizstores = studystatus.quizstore.all().filter(unit_counter=unit_cnt, section_counter=section_cnt)
                quizstore = quizstores[0]
                judge = question.filter(question_type='0')  # 获取quiz中的判断题
                option = question.filter(question_type='1')  # 获quiz中的取选择题
                Answer = []
                # 以下两个for循环用于获取用户答案
                #将选择题答案存入Answer
                for num in range(0, len(option)):
                    if request.POST.get('option' + str(num)) == None:
                        Answer.append(' ')
                        questions[num].user_answer = ''
                    else:
                        Answer.append(request.POST.get('option' + str(num)))
                        questions[num].user_answer = Answer[num]
                #将判断题答案存入Answer
                print(Answer)
                offset = len(option)
                for num in range(0, len(judge)):
                    if request.POST.get('judge' + str(num + offset)) == None:
                        Answer.append(' ')
                        questions[num + offset].user_answer = ''
                    else:
                        Answer.append(request.POST.get('judge' + str(num + offset)))
                        questions[num + offset].user_answer = Answer[num + offset]
                quizstore.Answer = ''.join(Answer)
                quizstore.save()
            return ren2res('./course/quiz.html', request,
                           {'Question': questions, 'Answer': Answer, 'course_id': course_id, 'unit_cnt': unit_cnt,
                            'section_cnt': section_cnt})
        except Exception:
            raise Http404
    else:
        return HttpResponseRedirect('/')

@csrf_exempt
@login_required
def take_test(request, course_id, unit_cnt, test_counter):
    # 当test_counter=0时，自动分配合适的test_counter
    print('test' + str(test_counter))
    if True:
        # try:
        course = Course.objects.get(id=course_id)
        user = request.user
        unit = course.units.get(counter=unit_cnt)
        unit_test = unit.test
        # -----------------------------------------------2
        max_submit_times = unit_test.max_submit_times
        last_time = unit_test.last_time
        # -----------------------------------------------2
        result = StudyStatus.objects.filter(user=user, course=course)
        studystatus = result[0]
    # except Exception:
    # raise Http404
    question = unit_test.test_content.questions.all()
    questions = []
    testscore = 0
    answer = []
    if int(test_counter) == 0:
        result = studystatus.teststore.all()
        test_counter = len(result) + 1
    print('test' + str(test_counter))
    # -----------------------------------------------3
    if int(test_counter) > int(max_submit_times):
        return HttpResponseRedirect('/')
    #-----------------------------------------------3
    if request.method == 'GET':
        try:
            teststore = studystatus.teststore.filter(unit_counter=unit_cnt, test_counter=test_counter)
            if len(teststore) == 1:  #用户做过该test,查看该test
                teststore = teststore[0]
                questions_id = (teststore.question_id).split(',')[:len(teststore.question_id) / 2]
                print(questions_id)
                for i in questions_id:
                    if i != '':  #根据题目数目不同，question_id最后一个值可能为'',需要除去
                        questions.append(question.get(counter=int(i)))
                questions.sort(key=lambda x: x.question_type)
                answer = list(teststore.Answer)
                for j in range(0, len(answer)):
                    questions[j].user_answer = answer[j]
                testscore = teststore.score
            else:  #teststore不存在，用户第一次做test
                #用于保存题目的编号
                print('not exist')
                questions_id = ''
                while ( len(questions) < ( len(question) * 2 / 3 ) ):  #随机抽取数量2/3的题目
                    a = random.randint(1, len(question))
                    if question.get(counter=a) in questions:
                        continue
                    else:
                        questions.append(question.get(counter=a))
                        questions_id += (str(a) + ',')
                #建立一个teststore存储题目
                teststore = TestStore(unit_counter=unit_cnt, test_counter=test_counter, studystatus=studystatus,
                                      question_id=questions_id, score=0, submit_time=datetime.date.today())
                teststore.save()
                #调整题目顺序,判断在前，选择在后
                questions.sort(key=lambda x: x.question_type)
            return ren2res('./course/test.html', request,
                           {'Questions': questions, 'Answer': answer, 'TestScore': testscore, 'course_id': course_id,
                            'unit_cnt': unit_cnt, 'test_counter': test_counter})
        except Exception:
            raise Http404
    elif request.method == 'POST':
        #用户提交答案
        try:
            #必定有teststore存在
            teststore = studystatus.teststore.get(unit_counter=unit_cnt, test_counter=test_counter)
            questions_id = (teststore.question_id).split(',')[:len(teststore.question_id) / 2]
            for i in questions_id:
                if i != '':
                    questions.append(question.get(counter=int(i)))
            questions.sort(key=lambda x: x.question_type)
            judge = []
            option = []
            #获取不同类型题目的数量
            for item in questions:
                if item.question_type == '0':
                    judge.append(item)
                elif item.question_type == '1':
                    option.append(item)
            #以下两个for循环用于获取用户答案
            #将选择题答案存入Answer
            for num in range(0, len(judge)):
                if request.POST.get('judge' + str(num)) == None:
                    answer.append(' ')
                    questions[num].user_answer = ''
                else:
                    answer.append(request.POST.get('judge' + str(num)))
                    questions[num].user_answer = answer[num]
            #将判断题答案存入Answer
            offset = len(judge)
            for num in range(0, len(option)):
                if request.POST.get('option' + str(num + offset)) == None:
                    answer.append(' ')
                    questions[num + offset].user_answer = ''
                else:
                    answer.append(request.POST.get('option' + str(num + offset)))
                    questions[num + offset].user_answer = answer[num + offset]
            #------------------------------------------------------------------------
            if datetime.date.today() <= last_time:
                #计算得分
                #在提交时间内保存题目分数，逾期不保存
                for i in range(0, len(answer)):
                    if answer[i] == questions[i].answer:
                        testscore += questions[i].question_score
                teststore.Answer = ''.join(answer)
                teststore.score = testscore
                teststore.save()
            else:
                #逾期不保存任何信息
                teststore.delete()
            return ren2res('./course/test.html', request,
                           {'Questions': questions, 'Answer': answer, 'TestScore': testscore, 'course_id': course_id,
                            'unit_cnt': unit_cnt, 'test_counter': test_counter})
        except:
            raise Http404
    else:
        return HttpResponseRedirect('/')


@login_required
def member(request):
    if request.method == 'GET':
        user = request.user
        result = StudyStatus.objects.filter(user=user)
        course_in = []
        course_out = []
        for studystatus in result:
            course = studystatus.course
            if studystatus.course_time.begin_time == course.cur_time.begin_time:
                units = course.units.all()
                deltadays = int((datetime.date.today() - course.cur_time.begin_time).days)
                for unit in units:
                    deltadays = deltadays - int(unit.gap_days)
                    if deltadays <= 0:
                        process_num = int(float(unit.counter)/float(len(units))*100)
                        print(process_num)
                        course_in.append([course, process_num])
                        break
            else:
                course_out.append([course, studystatus.course_time.begin_time])
        return ren2res('./user/personal.html', request, {'course_in': course_in, 'course_out': course_out})


def get_file(request):
    url = str(request.GET.get('url'))
    f = urllib2.urlopen(url)
    data = f.read()
    response = FileResponse(data)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="test.pdf"'
    return response


def download(request):
    url = str(request.GET.get('url'))
    name = request.GET.get('name')
    f = urllib2.urlopen(url)
    data = f.read()
    response = FileResponse(data)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="'+name+'.pdf"'
    print(name)
    return response



@login_required
def ttt(request):
    if not request.user.has_perm('Mooc.can_change_user'):
        raise Http404
    STORAGE_URL='http://moockitchen-mooc.stor.sinaapp.com/'
    if request.method == 'GET':
        return ren2res('ttt.html', request, {})
    else:
        content = request.FILES['file1']
        online = environ.get("APP_NAME", "")
        if online:
            import sae.const
            access_key = sae.const.ACCESS_KEY
            secret_key = sae.const.SECRET_KEY
            appname = sae.const.APP_NAME
            domain_name = "mooc"
            import sae.storage

            s = sae.storage.Client()
            ob = sae.storage.Object(content.read())
            type = str(request.POST.get('type'))
            subtype = str(request.POST.get('subtype'))
            if type == 'section':
                course_id = request.POST.get('course_id')
                course = Course.objects.get(id=course_id)
                unit_id = request.POST.get('unit_id')
                unit = course.units.all().get(counter=unit_id)
                section_id = request.POST.get('section_id')
                section = unit.sections.all().get(counter=section_id)
                dir = str(subtype)+'/'+str(course_id)+'_'+str(unit_id)+'_'+str(section_id)
                if subtype == 'pdf':
                    section.pdf = STORAGE_URL+dir
                elif subtype == 'video':
                    section.video = STORAGE_URL+dir
                else:
                    raise Http404
                section.save()
            elif type == 'img':
                if subtype == 'course':
                    course_id = request.POST.get('course_id')
                    course = Course.objects.get(id=course_id)
                    dir = str(type)+'/'+str(subtype)+'/'+str(course_id)
                    course.img = STORAGE_URL+dir
                    course.save()
                elif subtype == 'user':
                    user_id = request.POST.get('user_id')
                    user = User.objects.get(id=user_id)
                    userinfo = user.info
                    dir = str(type)+'/'+str(subtype)+'/'+str(user_id)
                    userinfo.img = STORAGE_URL+dir
                    userinfo.save()
                elif subtype == 'problem':
                    problem_id = request.POST.get('problem_id')
                    problem = QuizQuestion.objects.get(id=problem_id)
                    dir = str(type)+'/'+str(subtype)+'/'+str(problem_id)+'/summary'
                    problem.image = STORAGE_URL+dir
                    problem.save()
                elif subtype == 'option':
                    problem_id = request.POST.get('problem_id')
                    problem = QuizQuestion.objects.get(id=problem_id)
                    option_id = str(request.POST.get('option_id'))
                    dir = str(type)+'/'+'problem'+'/'+str(problem_id)+'/'+str(option_id)
                    if option_id == 'a':
                        problem.image_a = STORAGE_URL+dir
                    elif option_id == 'b':
                        problem.image_b = STORAGE_URL+dir
                    elif option_id == 'c':
                        problem.image_c = STORAGE_URL+dir
                    elif option_id == 'd':
                        problem.image_d = STORAGE_URL+dir
                    else:
                        raise Http404
                    problem.save()
                else:
                    raise Http404
            elif type == 'serverfile':
                dir = str(request.POST.get('dir'))
            else:
                raise Http404
            url = s.put(domain_name, dir, ob)
            return ren2res('ttt.html', request, {'value': url})
        else:
            return ren2res('ttt.html', request, {'value': 'save failed'})

@login_required
def create_message(request):
    servertime = datetime.date.today()
    user = request.user
    course_id = request.POST.get('course_id')
    course = Course.objects.get(id=course_id)
    content = request.POST.get('content')
    reference_id = request.POST.get('reference_id')
    if reference_id is None:
        reference_id = -1
    floor_counter = int(len(Message.objects.all().filter(course=course)))+1
    message = Message(user=user, course=course, reference=reference_id, content=content, floor=floor_counter,
                      publishTime=servertime)
    message.save()
    return JsonResponse({'message': u'上传成功'})

@login_required
def keepnote(request):
    print('innote')
    if request.is_ajax():
        t = loader.get_template('./course/note.html')
    course_id = request.POST.get('course_id')
    course = Course.objects.get(id=course_id)
    unit_cnt = request.POST.get('unit_cnt')
    note_content = request.POST.get('content')
    try:
        note = UserNote.objects.get(user_id=request.user.id,course=course,unit_counter=unit_cnt)
        note.content=note_content
    except Exception:
        note = UserNote(course=course,unit_counter=unit_cnt,user_id=request.user.id,content=note_content)
    note.save()
    content_html = t.render(Context({'usernote': note}))
    return HttpResponse(content_html)

@login_required
def get_messages(request):
    if request.is_ajax():
        t = loader.get_template('./course/message.html')
    course_id = request.GET.get('course_id')
    course = Course.objects.get(id=course_id)
    messages = course.messages.all().order_by('floor')
    content_html = t.render(Context({'messages': messages}))
    return HttpResponse(content_html)

@login_required
def set_likes(request):
    course_id = request.GET.get('course_id')
    course = Course.objects.get(id=course_id)
    user = request.user
    query_result = LikeUserCourse.objects.filter(user=user, course=course)
    if len(query_result) == 0:
        new = LikeUserCourse(user=user, course=course)
        new.save()
        course.likeCounter += 1
        html_data = '+1'
    else:
        old = query_result[0]
        old.delete()
        course.likeCounter -= 1
        html_data = '-1'
    course.save()
    return JsonResponse({'likeCounter': course.likeCounter, 'html_data': html_data})

def getCourseClass(request):
    #根据courseclass获取课程的类别
    #根据number判断加载课程的数量
    #根据Flag判断是否需要加载更多的按钮
    if request.is_ajax():
        t = loader.get_template('courseclass.html')
    courseclass = request.GET.get('content_class')
    search_text = request.GET.get('content_text')
    number = request.GET.get('number')
    if number is None:
        number=1
    else:
        number=int(number)
    if search_text=="" or search_text is None:
        if courseclass=='all':
            courses = list(Course.objects.all()[0:6*number])
            if Course.objects.all().count() > len(courses):
                Flag = True
            else:
                Flag = False
        else:
            courses = list(Course.objects.filter(courseClass=courseclass)[0:6*number])
            if Course.objects.filter(courseClass=courseclass).count() > len(courses):
                Flag = True
            else:
                Flag = False
    elif courseclass=="":
            courses = list(Course.objects.filter(name__icontains=search_text)[0:6*number])
            if Course.objects.filter(name__icontains=search_text).count() > len(courses):
                Flag = True
            else:
                Flag = False
    courses_num=[]
    for i in range(0,len(courses)):
        if((i+1)%3 == 1):
            courses_num.append([courses[i],0])
        elif ((i+1)%3 == 2):
            courses_num.append([courses[i],-1])
        else:
            courses_num.append([courses[i],1])
    number=number+1
    if search_text=="" or  search_text is None:
        content_html = t.render(Context({'courses_num':courses_num,'courseclass':courseclass,'number':number,'Flag':Flag}))
    elif courseclass=="":
        content_html = t.render(Context({'courses_num':courses_num,'search_text':search_text,'number':number,'Flag':Flag}))
    return HttpResponse(content_html)

def search(request):
    # if request.is_ajax():
    #     t = loader.get_template('./course/search.html')
    data = request.GET.get('search_text')
    courses = list(Course.objects.filter(name__icontains=data)[0:6])
    if Course.objects.filter(name__icontains=data).count() > len(courses):
        Flag = True
    else:
        Flag = False
    search_text = data
    print(search_text)
    number=2
    courses_num=[]
    for i in range(0,len(courses)):
        if((i+1)%3 == 1):
            courses_num.append([courses[i],0])
        elif ((i+1)%3 == 2):
            courses_num.append([courses[i],-1])
        else:
            courses_num.append([courses[i],1])
    # content_html = t.render(Context({{'courses_num': courses_num,'courseclass':courseclass,
    #                                                  'number':number,'Flag':Flag,}}))
    print("Hello++++++++++++++")
    # return HttpResponse(content_html)
    return ren2res('./course/search.html', request, {'courses_num': courses_num,'search_text':search_text,
                                                     'number':number,'Flag':Flag,})
