from home.models import User, Code, Ready
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

@receiver(post_save, sender=User)
def post_save_generate_code(sender, instance, created, *args, **kwargs):
    if created:
        Code.objects.create(user=instance)



@receiver(pre_save, sender=Ready)
def checkquestion(sender, instance, *args, **kwargs):
    if instance.question.ans == instance.true_answer:
        instance.is_true = True
    else:
        instance.is_true = False