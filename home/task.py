from datetime import datetime
from home.models import Course, Ready, Information

def close_status():
    current_time = datetime.now().strftime("%H:%M:%S")
    course = Course.objects.all()
    for item in course.values('id','title','status','time','code'):
        item_id = item['id']
        item_title = item['title']
        item_status = item['status']
        item_time = item['time'].strftime("%H:%M:%S")
        item_code = item['code']
        if item_status == 'Open' and item_time == current_time:
            for start in course.filter(id=item_id, title=item_title, status=item_status, time=item_time, code=item_code):
                start.status = 'Close'
                start.save()
            return 'ok'
def Taskone():
    return close_status()

def ready_to_test():
    ready = Ready.objects.all()
    for item in ready.values('id', 'course', 'student', 'question', 'question__ans', 'true_answer', 'is_true', 'is_none'):
        item_id = item['id']
        item_course = item['course']
        item_student = item['student']
        item_is_true = item['is_true']
        item_none = item['is_none']
        item_question = item['question']
        item_question_ans = item['question__ans']
        item_true_answer = item['true_answer']
        if item_question_ans == item_true_answer and item_is_true == False and item_none == False:
            for start in ready.filter(id=item_id, course=item_course, question=item_question, student=item_student, is_true=item_is_true):
                start.is_true = True
                start.save()
            return 'ok'
def Tasktwo():
    return ready_to_test()

def none_test():
    ready = Ready.objects.all()
    for item in ready.values('id', 'course', 'student', 'question', 'true_answer', 'is_true', 'is_none'):
        item_id = item['id']
        item_course = item['course']
        item_student = item['student']
        item_is_true = item['is_true']
        item_is_none = item['is_none']
        item_question = item['question']
        item_true_answer = item['true_answer']
        if item_true_answer == '' and item_is_none == False:
            for start in ready.filter(id=item_id, course=item_course, question=item_question, student=item_student, is_true=item_is_true):
                start.is_none = True
                start.save()
            return 'ok'
def Taskthree():
    return none_test()

def taskfour():
    current_time = datetime.now().strftime("%H:%M:%S")
    info = Information.objects.all()
    for item in info.values('id', 'time',):
        item_id = item['id']
        item_time = item['time'].strftime("%H:%M:%S")
        if item_time == current_time:
            for start in info.filter(id=item_id,):
                start.status = 'Open'
                start.save()
            return 'ok'

def Taskfour():
    return taskfour()