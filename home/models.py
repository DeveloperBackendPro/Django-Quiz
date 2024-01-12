import random
from django.db import models
from django.db.models import Count
from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from ckeditor_uploader.fields import RichTextUploadingField


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    full_name = models.CharField(max_length=255)
    group = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователь'

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студент'

class Code(models.Model):
    number = models.CharField(max_length=6, blank=True, verbose_name='Номер')
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return str(self.number)

    def save(self, *args, **kwargs):
        number_list = [x for x in range(10)]
        code_items = []
        for i in range(6):
            num = random.choice(number_list)
            code_items.append(num)
            code_string = ''.join(str(item) for item in code_items)
            self.number = code_string
        super().save(*args, **kwargs)

    @property
    def number_user(self):
        return self.user.full_name.upper()

    @property
    def user_group(self):
        return self.user.group.upper()

    class Meta:
        verbose_name = 'Номер'
        verbose_name_plural = 'Номер'

class Information(models.Model):
    STATUS = (
        ('Open', 'Открыть'),
        ('Close', 'Закрыто'),
    )
    time = models.TimeField(verbose_name='Время', blank=True, null=True)
    facebook = models.URLField(max_length=1000, blank=True, null=True, verbose_name='Фейсбук')
    instagram = models.URLField(max_length=1000, blank=True, null=True, verbose_name='Инстаграм')
    youtube = models.URLField(verbose_name='Юутубе', blank=True, null=True, )
    telegram = models.URLField(max_length=1000, blank=True, null=True, verbose_name='Телеграм')
    status = models.CharField(max_length=15, choices=STATUS, default='Open', verbose_name='Статусы')
    create_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.time} | {self.status} | {self.create_at}"

    class Meta:
        verbose_name = 'Информация'
        verbose_name_plural = 'Информация'

class Course(models.Model):
    STATUS = (
        ('Open', 'Ochiq'),
        ('Close', 'Yopiq'),
    )
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    image = models.ImageField(upload_to='images/Course', verbose_name='Изображение',
    validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])])
    status = models.CharField(max_length=15, choices=STATUS, default='Open', verbose_name='Статусы',)
    time = models.TimeField(blank=True, null=True, verbose_name='Время',)
    code = models.CharField(max_length=1000, blank=True, null=True, unique=True, verbose_name='Код')
    def __str__(self):
        return self.title.upper()

    def save(self, *args, **kwargs):
        code = self.code
        if not code:
            code = get_random_string(8).upper()
        while Course.objects.filter(code=code).exclude(pk=self.pk).exists():
            code = get_random_string(8).upper()
        self.code = code
        super(Course, self).save(*args, **kwargs)

    def count_quiz(self):
        count_question = Question.objects.filter(course=self).aggregate(count=Count('id'))
        cnt = 0
        if count_question["count"] is not None:
            cnt = int(count_question["count"])
        return cnt

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курс'

class Question(models.Model):
    Answer = (
        ('option1', 'Вариант-1'),
        ('option2', 'Вариант-2'),
        ('option3', 'Вариант-3'),
        ('option4', 'Вариант-4'),
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    question = RichTextUploadingField(verbose_name='Вопрос')
    op1 = models.CharField(max_length=200, null=True, verbose_name='Вариант-1')
    op2 = models.CharField(max_length=200, null=True, verbose_name='Вариант-2')
    op3 = models.CharField(max_length=200, null=True, verbose_name='Вариант-3')
    op4 = models.CharField(max_length=200, null=True, verbose_name='Вариант-4')
    score = models.FloatField(verbose_name='Общий счет')
    ans = models.CharField(max_length=100, choices=Answer, default='True', verbose_name='Ответ')
    create_at = models.DateField(auto_now=True, verbose_name='Созданный')

    def __str__(self):
        return self.question.upper()

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопрос'

class Answers(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Студент')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    total_score = models.FloatField(verbose_name='Общий счет')
    create_at = models.DateTimeField(auto_now=True, verbose_name='Созданный')

    def save(self, *args, **kwargs):
        self.total_score = round(self.total_score, 1)
        super().save(*args, **kwargs)

    @property
    def student_course(self):
        return self.course.title.upper()

    @property
    def student_username(self):
        return self.student.user.username

    @property
    def student_full_name(self):
        return self.student.user.full_name.upper()

    @property
    def student_group(self):
        return self.student.user.group.upper()

    class Meta:
        verbose_name = 'Ответы'
        verbose_name_plural = 'Ответы'

class Ready(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Студент')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    true_answer = models.CharField(max_length=255, verbose_name='Ответ', blank=True, null=True)
    is_true = models.BooleanField(default=False, verbose_name='Правильный ответ')
    is_none = models.BooleanField(default=False, verbose_name='Нет ответа')
    create_at = models.DateField(auto_now=True, verbose_name='Созданный')

    @property
    def course_name(self):
        return self.course.title.upper()

    @property
    def student_full_name(self):
        return self.student.user.full_name.upper()

    @property
    def student_group(self):
        return self.student.user.group.upper()

    def save(self, *args, **kwargs):
        if self.true_answer is None:
            self.true_answer = ''
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Готовый'
        verbose_name_plural = 'Готовый'
