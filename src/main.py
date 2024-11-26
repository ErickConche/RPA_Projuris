import warnings
from mainapp import initThreads
from server import initServer
from threading import Thread
warnings.filterwarnings('ignore')


def main():
    list_queues = [
        "app-adm-legalone",
        "app-adm-autojur",
        "app-adm-tarefa-autojur",
        "app-jud-legalone",
        "app-jud-autojur",
        "app-exp-jud-autojur",
        "app-identificar-cadastro-autojur",
        # "app-civeis-espaider",
        # "app-trabalhista-espaider",
        # "app-autos-espaider",
        # "app-expediente-espaider",
        # "app-cadastro-espaider"
    ]
    t = Thread(target=initServer, args=(list_queues,))
    t.start()
    initThreads(list_queues)


if __name__ == '__main__':
    main()
