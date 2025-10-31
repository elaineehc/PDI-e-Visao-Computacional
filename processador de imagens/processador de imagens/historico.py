import os
import uuid
import shutil

class GerenciadorHistorico:
    def __init__(self, historico_dir="historico_imagens", max_historico=10):
        self.historico_dir = historico_dir
        self.max_historico = max_historico
        self.historico = []
    
    def carrega_historico(self, imagem_atual_path: str):

        if not imagem_atual_path:
            return
        if not os.path.exists(imagem_atual_path):
            return
        
        os.makedirs(self.historico_dir, exist_ok=True)

        nome = f"hist_{uuid.uuid4().hex}.png"
        destino = os.path.join(self.historico_dir, nome)
        try:
            shutil.copyfile(imagem_atual_path, destino)
        except Exception as e:
            print("Erro ao salvar resultado no historico: ", e)
            return
        self.historico.append(destino)

    def limpa_historico(self):
        try:
            if os.path.exists(self.historico_dir):
                for arquivo in os.listdir(self.historico_dir):
                    p = os.path.join(self.historico_dir, arquivo)
                    try:
                        if os.path.exists(p):
                            os.remove(p)
                    except Exception as e:
                        print("Erro ao remover arquivo: ", e)
                        return
                self.historico = []
        except Exception as e:
            print("Erro ao limpar historico: ", e)
            return
    
