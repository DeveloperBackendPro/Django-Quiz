import csv
from django.contrib import admin
from django.http import HttpResponse
from django.utils.encoding import smart_str
from home.models import User, Student, Course, Question, Answers, Ready, Information, Code

class AnswersAdmin(admin.ModelAdmin):
    list_display = ['student_full_name','student_group','student_course','total_score','create_at']
    actions = ['download_csv']

    def download_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="answers.csv"'
        writer = csv.writer(response, delimiter=',')
        writer.writerow(['F.I.SH', 'GRUPPA', 'FAN', 'UMUMIY BALL', 'SANA'])
        for obj in queryset:
            writer.writerow([
                smart_str(obj.student_full_name),
                smart_str(obj.student_group),
                smart_str(obj.student_course),
                smart_str(obj.total_score),
                smart_str(obj.create_at),
            ])
        return response
    download_csv.short_description = 'Download selected objects as CSV'

class CourseAdmin(admin.ModelAdmin):
    exclude = ('title','code',)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question','score',]
    exclude = ('question','op1','op2','op3','op4',)


class ReadyAdmin(admin.ModelAdmin):
    list_display = ['student_full_name', 'course_name', 'student_group','is_true', 'create_at']


class CodeAdmin(admin.ModelAdmin):
    list_display = ['number_user','user_group','number']


admin.site.register(User)
admin.site.register(Student)
admin.site.register(Information)
admin.site.register(Code, CodeAdmin)
admin.site.register(Ready, ReadyAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Answers, AnswersAdmin)
admin.site.register(Question, QuestionAdmin)






