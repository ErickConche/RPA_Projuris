import warnings
from mainapp import initThreads
##from mainapp import initApp
from server import initServer
warnings.filterwarnings('ignore')
from threading import Thread

def main():
    list_queues = ["app-adm-legalone","app-jud-legalone"]
    t = Thread(target=initServer,args=(list_queues,))
    t.start()
    initThreads(list_queues)

if __name__ == '__main__':
    main()