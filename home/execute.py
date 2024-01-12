from apscheduler.schedulers.background import BackgroundScheduler
from home.task import Taskone, Tasktwo, Taskthree, Taskfour

scheduler = BackgroundScheduler()
scheduler.add_job(Taskone, 'interval', seconds=1)
scheduler.add_job(Taskthree, 'interval', seconds=1)
scheduler.add_job(Taskfour, 'interval', seconds=1)
scheduler.start()
