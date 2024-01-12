from modeltranslation.translator import register, TranslationOptions
from home.models import Course, Question

@register(Course)
class CourseTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Question)
class CourseTranslationOptions(TranslationOptions):
    fields = ('question','op1','op2','op3','op4',)