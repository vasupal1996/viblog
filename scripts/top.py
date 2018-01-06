import os, sys

from unipath import Path
import django
#proj_path = "/path/to/my/project/"
PROJECT_DIR = Path(os.path.abspath(__file__)).parent.parent
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "viblog.settings")
sys.path.append(PROJECT_DIR)

# This is so my local_settings.py gets loaded.
#os.chdir(proj_path)

# This is so models get loaded.


django.setup()
from twisted.internet import task
from twisted.internet import reactor


ONE_MINUTES = 1 * 30
THIRTY_MINUTES = 30 * 60

# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()




# def fun1():
#     print ("Running Script")


# def main():
#     l1 = (
#         (fun1(), ONE_MINUTES),
#     )

#     for l in l1:
#         task.LoopingCall(l[0]).start(l[1])

#     reactor.run()

# if __name__ == '__main__':
#     main()

from twisted.internet import task
from twisted.internet import reactor

def runEverySecond():
    print ("a second has passed")

l = task.LoopingCall(runEverySecond)
l.start(10.0) # call every second

# l.stop() will stop the looping calls
reactor.run()
