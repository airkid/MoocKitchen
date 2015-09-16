# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserInfo(models.Model):
    user = models.OneToOneField(User, primary_key=True, related_name='info')
    nickname = models.CharField(unique=True, max_length=20)
    school = models.CharField(max_length=20, blank=True)
    birthday = models.DateField(blank=True, null=True)
    sex = models.CharField(choices=(('M', u'男'), ('F', u'女')), max_length=1, blank=True)
    img = models.CharField(max_length=200, blank=True, default='http://moockitchen-mooc.stor.sinaapp.com/img/user/default')

    def __unicode__(self):
        return self.nickname


class Course(models.Model):
    # 课程名称
    name = models.CharField(max_length=30)
    subTitle = models.CharField(max_length=30, default="")
    # 课程简介
    summary = models.CharField(max_length=200)
    announcement = models.CharField(max_length=200, blank=True, default=u'暂无公告')
    img = models.CharField(max_length=200, blank=True, default='http://moockitchen-mooc.stor.sinaapp.com/img/course/default')
    teacher = models.CharField(max_length=20, default='NoTeacher')
    likeCounter = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name


class CourseTime(models.Model):
    course = models.ForeignKey(Course, related_name='times')
    begin_time = models.DateField()
    cur_course = models.OneToOneField(Course, related_name='cur_time', blank=True, null=True)

    def __unicode__(self):
        return str(self.begin_time)


class StudyStatus(models.Model):
    user = models.ForeignKey(User, related_name='status')
    course = models.ForeignKey(Course, related_name='status')
    course_time = models.ForeignKey(CourseTime, related_name='status')
    last_section = models.IntegerField(default=0, blank=True)

    def __unicode__(self):
        return str(self.id)
        #return (str(self.user.info.nickname)+str(self.course.name))


class Quiz(models.Model):
    id = models.AutoField(primary_key=True)

    def __unicode__(self):
        return 'Quiz'+str(self.id)

class UnitTest(models.Model):
    title = models.CharField(max_length=30)
    summary = models.CharField(max_length=200)
    test_content = models.OneToOneField(Quiz, related_name='unit_test', blank=True)
    # 单元测试截止时间
    last_time = models.DateField(blank=True, null=True)
    #单元测试最大提交次数
    max_submit_times = models.IntegerField(default=3, blank=True)

    def __unicode__(self):
        return self.title


class Unit(models.Model):
    course = models.ForeignKey(Course, related_name='units')
    title = models.CharField(max_length=30)
    gap_days = models.IntegerField(default=1)
    counter = models.IntegerField()
    test = models.OneToOneField(UnitTest, related_name='unit', blank=True, null=True)

    def __unicode__(self):
        return self.title

    class META:
        ordering = ['counter']


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions')
    title = models.CharField(max_length=100, blank=True)
    option_a = models.CharField(max_length=10, default='A')
    image_a = models.CharField(blank=True, max_length=100, null=True)
    option_b = models.CharField(max_length=10, default='B')
    image_b = models.CharField(blank=True, max_length=100, null=True)
    option_c = models.CharField(max_length=10, default='C')
    image_c = models.CharField(blank=True, max_length=100, null=True)
    option_d = models.CharField(max_length=10, default='D')
    image_d = models.CharField(blank=True, max_length=100, null=True)
    answer = models.CharField(max_length=30)
    counter = models.IntegerField()
    image = models.CharField(blank=True, max_length=100, null=True)
    # 用于临时存储答案
    user_answer = models.CharField(max_length=10, blank=True)
    question_score = models.IntegerField(default=5, blank=True)
    #判断 2 表示题型为简答题，1 表示题型为选择题,0表示判断
    question_type = models.CharField(choices=(('0', u'判断题'), ('1', u'选择题'), ('2', u'简答题')), max_length=10)

    class META:
        # 题目根据choose_type类型排序：顺序为:判断，选择，简答
        ordering = ['question_type']

    def __unicode__(self):
        return str(self.id)+self.title


class Section(models.Model):
    course = models.ForeignKey(Course, related_name='sections')
    unit = models.ForeignKey(Unit, related_name='sections')
    title = models.CharField(max_length=30)
    video = models.CharField(blank=True, max_length=100, null=True)
    pdf = models.CharField(blank=True, max_length=100, null=True)
    quiz = models.OneToOneField(Quiz, related_name='section', blank=True, null=True)
    counter = models.IntegerField()
    total_counter = models.IntegerField(default=0)
    # begin为该章节是否上传的标志
    begin = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

    class META:
        ordering = ['total_counter', 'counter']


class QuizStore(models.Model):
    # 通过course,unit_counter,section_counter来取得对应的答案
    studystatus = models.ForeignKey(StudyStatus, related_name='quizstore')
    unit_counter = models.IntegerField()
    section_counter = models.IntegerField()
    # 用于存储答案，将用户的答案列表转化字符串后存入
    Answer = models.CharField(default='', max_length=50)
    score = models.IntegerField(default=0, blank=True)
    # 记录用户是否访问过这个section
    visit = models.BooleanField(default=False)


class TestStore(models.Model):
    studystatus = models.ForeignKey(StudyStatus, related_name='teststore')
    test_counter = models.IntegerField()
    unit_counter = models.IntegerField()
    submit_time = models.DateField(null=True, blank=True)
    # 用于保存题目的Id
    question_id = models.CharField(default='', max_length=30, blank=True)
    Answer = models.CharField(default='', max_length=30, blank=True)
    score = models.IntegerField(blank=True)

    class META:
        ordering = ['unit_counter']


class Message(models.Model):
    course = models.ForeignKey(Course, related_name='messages')
    user = models.ForeignKey(User, related_name='messages')
    reference = models.IntegerField(default='-1', null=True)
    floor = models.IntegerField(default='1')
    content = models.CharField(max_length=120, default='', null=True)
    publishTime = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return 'Message '+str(self.id)+' :'+str(self.content)

    class META:
        ordering = ['floor']

    def get_reference(self):
        if self.reference is None:
            return None
        elif int(self.reference) == -1:
            return None
        else:
            message = Message.objects.get(id=self.reference)
            return message


class UserNote(models.Model):
    #根据用户，课程，单元保存笔记
    user = models.ForeignKey(User, related_name='notes')
    course = models.ForeignKey(Course,related_name='notes')
    unit_counter = models.IntegerField(blank=True)
    #笔记内容
    content = models.CharField(max_length=200, blank=True)


class LikeUserCourse(models.Model):
    user = models.ForeignKey(User, related_name='likes')
    course = models.ForeignKey(Course, related_name='likes')

    def __unicode__(self):
        return str(self.user.info.nickname).decode('utf8')+str(self.course).decode('utf8')