from PyQt6.QtWidgets import (
    QApplication, QSlider, QLabel, QPushButton, 
    QFileDialog, QWidget, QVBoxLayout, QHBoxLayout
    )
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import sys
import os
import shutil

from historico import GerenciadorHistorico
from janelas import (
    abrir_janela_gama, abrir_janela_linearpp, abrir_janela_histograma, 
    abrir_janela_limiar, abrir_janela_filtros, abrir_janela_escala,
    abrir_janela_rotacao, abrir_janela_matiz, abrir_janela_ajuste_canais,
    abrir_janela_dft, abrir_janela_escala_cinza
    )
import funcoes

from oct2py import Oct2Py
octave = Oct2Py()

class Processador(QWidget):

    def __init__(self, gh: GerenciadorHistorico = None):
        super().__init__()

        self.setWindowTitle("Processador de Imagens")
        self.resize(400, 400)

        octave.addpath(os.getcwd())
        self.octave = octave
        self.hist_open = False

        self.historico_dir = "historico_imagens"
        self.max_historico = 10

        if gh is None:
            self.gh = GerenciadorHistorico(self.historico_dir, self.max_historico)
        else:
            self.gh = gh

        #label
        self.label = QLabel("Nenhuma imagem carregada.")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setMinimumWidth(600)
        self.label.setScaledContents(False)
        
        #QPixmap original
        self.original_pixmap = None

        #botoes
        self.botao_abrir = QPushButton("Abrir imagem")
        self.botao_salvar = QPushButton("Salvar imagem")
        self.botao_negativo = QPushButton("Aplicar negativo")
        self.botao_hist = QPushButton("Histograma")
        self.botao_gama = QPushButton("Gama")
        self.botao_linearpp = QPushButton("Linear por Partes")
        self.botao_desfazer = QPushButton("Desfazer")
        self.botao_limiarizar = QPushButton("Limiarização")
        self.botao_filtros = QPushButton("Filtros")
        self.botao_escala = QPushButton("Escala")
        self.botao_rotacao = QPushButton("Rotação")
        self.botao_matiz = QPushButton("Matiz, Saturação e Brilho")
        self.botao_ajuste_canais = QPushButton("Ajuste de Canal")
        self.botao_escala_cinza = QPushButton("Escala de cinza")
        self.botao_sepia = QPushButton("Sépia")
        self.botao_fft = QPushButton("FFT")


        # Conexões
        self.botao_abrir.clicked.connect(self.abrir_imagem)
        self.botao_salvar.clicked.connect(self.salvar_imagem)
        self.botao_negativo.clicked.connect(lambda: funcoes.aplicar_negativo(self, self.gh))
        self.botao_hist.clicked.connect(self.hist)
        self.botao_gama.clicked.connect(lambda: abrir_janela_gama(self, self.gh, parent=self))
        self.botao_linearpp.clicked.connect(lambda: abrir_janela_linearpp(self, self.gh, parent=self))
        self.botao_desfazer.clicked.connect(self.desfazer)
        self.botao_limiarizar.clicked.connect(lambda: abrir_janela_limiar(self, self.gh, parent=self))
        self.botao_filtros.clicked.connect(lambda: abrir_janela_filtros(self, self.gh, parent=self)) 
        self.botao_escala.clicked.connect(lambda: abrir_janela_escala(self, self.gh, parent=self))
        self.botao_rotacao.clicked.connect(lambda: abrir_janela_rotacao(self, self.gh, parent=self))
        self.botao_matiz.clicked.connect(lambda: abrir_janela_matiz(self, self.gh, parent=self))
        self.botao_ajuste_canais.clicked.connect(lambda: abrir_janela_ajuste_canais(self, self.gh, parent=self))
        self.botao_escala_cinza.clicked.connect(lambda: abrir_janela_escala_cinza(self, self.gh, parent=self))
        self.botao_sepia.clicked.connect(lambda: funcoes.aplicar_sepia(self, self.gh))
        self.botao_fft.clicked.connect(lambda: funcoes.calcular_dft(self, self.gh))


        botoes_layout = QVBoxLayout()
        botoes_layout.addWidget(self.botao_negativo)
        botoes_layout.addWidget(self.botao_hist)
        botoes_layout.addWidget(self.botao_gama)
        botoes_layout.addWidget(self.botao_limiarizar)
        botoes_layout.addWidget(self.botao_linearpp)
        botoes_layout.addWidget(self.botao_filtros)
        botoes_layout.addWidget(self.botao_escala)
        botoes_layout.addWidget(self.botao_rotacao)
        botoes_layout.addWidget(self.botao_matiz)
        botoes_layout.addWidget(self.botao_ajuste_canais)
        botoes_layout.addWidget(self.botao_escala_cinza)
        botoes_layout.addWidget(self.botao_sepia)
        botoes_layout.addWidget(self.botao_fft)

        self.botao_negativo.setFixedWidth(150)
        self.botao_hist.setFixedWidth(150)
        self.botao_gama.setFixedWidth(150)
        self.botao_limiarizar.setFixedWidth(150)
        self.botao_linearpp.setFixedWidth(150)
        self.botao_filtros.setFixedWidth(150)
        self.botao_escala.setFixedWidth(150)
        self.botao_rotacao.setFixedWidth(150)
        self.botao_matiz.setFixedWidth(150)
        self.botao_ajuste_canais.setFixedWidth(150)
        self.botao_sepia.setFixedWidth(150)
        self.botao_fft.setFixedWidth(150)
        self.botao_escala_cinza.setFixedWidth(150)


        botoes_top_layout = QHBoxLayout()
        botoes_top_layout.addWidget(self.botao_abrir)
        botoes_top_layout.addWidget(self.botao_salvar)
        botoes_top_layout.addWidget(self.botao_desfazer)
        self.botao_abrir.setFixedWidth(120)
        self.botao_salvar.setFixedWidth(120)
        self.botao_desfazer.setFixedWidth(120)

        imagem_layout = QVBoxLayout()
        imagem_layout.addWidget(self.label)
        imagem_layout.addLayout(botoes_top_layout)

        layout = QHBoxLayout()
        layout.addLayout(imagem_layout)
        layout.addLayout(botoes_layout)

        self.setLayout(layout)

    def hist(self):
        if hasattr(self, "imagem_atual_path"):
            self.hist_open = True
            abrir_janela_histograma(self, self.gh, self.octave, self.imagem_atual_path, parent=self)
        else:
            print("Nenhuma imagem carregada.")
            return
    
    def abrir_imagem(self):

        caminho, _ = QFileDialog.getOpenFileName(self, "Abrir imagem", "", "Imagens (*.png *.jpg *.bmp)")

        if caminho:
            self.imagem_original_path = caminho
            self.imagem_atual_path = "imagem_atual.png"
            self.img = octave.imread(caminho)
            
            print(self.img.min(), self.img.max(), self.img.dtype)
            octave.feval("normalizar", self.imagem_original_path, self.imagem_atual_path, nout=0)

            if os.path.exists(self.imagem_atual_path):
                self.original_pixmap = QPixmap(self.imagem_atual_path)
            else:
                self.original_pixmap = QPixmap(caminho)

            self._update_pixmap_scaled()
        self.gh.limpa_historico()
 
    def salvar_imagem(self):
        # Verifica se há imagem carregada
        if not hasattr(self, "imagem_atual_path") or not os.path.exists(self.imagem_atual_path):
            print("Nenhuma imagem carregada para salvar.")
            return

        # Diálogo de salvar arquivo
        destino, filtro = QFileDialog.getSaveFileName(
            self,
            "Salvar imagem",
            "",
            "PNG (*.png);;JPEG (*.jpg *.jpeg);;Bitmap (*.bmp);;All Files (*)"
        )

        if not destino:
            # usuário cancelou
            return

        # Se usuário não forneceu extensão, adicionar .png por padrão
        raiz, ext = os.path.splitext(destino)
        if ext == "":
            destino = raiz + ".png"

        try:
            # Tenta copiar o arquivo original (mais simples e preserva metadados)
            shutil.copyfile(self.imagem_atual_path, destino)
            print("Imagem salva em:", destino)
        except Exception as e:
            # se copiar falhar, tenta salvar a partir do QPixmap (fallback)
            try:
                if self.original_pixmap and not self.original_pixmap.isNull():
                    ok = self.original_pixmap.save(destino)
                    if ok:
                        print("Imagem salva (via QPixmap) em:", destino)
                        return
                print("Erro ao salvar imagem (copy fallback QPixmap falhou):", e)
            except Exception as e2:
                print("Erro ao salvar imagem:", e2)


    def atualizar_display(self, caminho):
        if os.path.exists(caminho):
            self.original_pixmap = QPixmap(caminho)
            self._update_pixmap_scaled()
            print("Filtro aplicado com sucesso!")
        else:
            print("Erro: Arquivo de saída não foi criado")

    def desfazer(self):
        if not self.gh.historico:
            print("Nada para desfazer.")
            return
        ultimo = self.gh.historico.pop()
        if not os.path.exists(ultimo):
            print("Arquivo de historico nao encontrado.")
            return
        try:
            shutil.copyfile(ultimo, self.imagem_atual_path)
        except Exception as e:
            print("Erro ao restaurar imagem do historico.")
            return
        
        try:
            if os.path.exists(ultimo):
                os.remove(ultimo)
        except Exception as e:
            print("Erro ao remover imagem do historico: ", e)
            return 
        
        self.atualizar_display(self.imagem_atual_path)

    def _update_pixmap_scaled(self, allow_upscale=False):
        if not self.original_pixmap or self.original_pixmap.isNull():
            return

        label_w = self.label.width()
        label_h = self.label.height()
        if label_w == 0 or label_h == 0:
            return

        orig_w = self.original_pixmap.width()
        orig_h = self.original_pixmap.height()
        target_w = label_w
        target_h = label_h
        if not allow_upscale:
            target_w = min(label_w, orig_w)
            target_h = min(label_h, orig_h)

        scaled = self.original_pixmap.scaled(target_w, target_h, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.label.setPixmap(scaled)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_pixmap_scaled()


app = QApplication(sys.argv)
janela = Processador()
janela.show()
sys.exit(app.exec())



