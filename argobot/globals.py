from database import GlobalData


global_data: GlobalData
def init():
    global global_data, CONSTANTES

    global_data = GlobalData()
    CONSTANTES = global_data.CST
