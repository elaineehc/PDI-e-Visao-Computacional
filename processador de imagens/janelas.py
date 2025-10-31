from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton, QSpinBox, QWidget,
    QCheckBox, QComboBox, QGroupBox, QButtonGroup, QGridLayout, QLineEdit 
    )
from PyQt6.QtCore import Qt, QLocale
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtGui import QPixmap

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import matplotlib.pyplot as plt
import os
import numpy as np
import funcoes

class JanelaGama(QDialog):
    def __init__(self, p, gh, parent=None, modal=False):
        super().__init__(parent)
        self.p = p
        self.gh = gh

        self.setWindowTitle("Ajuste de Gama")
        self.setWindowModality(Qt.WindowModality.NonModal)
        self.resize(300, 150)

        self.label_gama = QLabel("Gama: 1.00")
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(10, 500)
        self.slider.setValue(100)
        self.slider.setTickInterval(10)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.valueChanged.connect(self.atualizar_label_gama)

        self.botao_aplicar = QPushButton("Aplicar")
        self.botao_aplicar.clicked.connect(lambda: funcoes.aplicar_gama(self.p, self.gh, self.slider.value() / 100.0))

        h = QHBoxLayout()
        h.addWidget(self.botao_aplicar)

        layout = QVBoxLayout()
        layout.addWidget(self.label_gama)
        layout.addWidget(self.slider)
        layout.addLayout(h)
        self.setLayout(layout)

    def atualizar_label_gama(self, val):
        gama = val / 100.0
        self.label_gama.setText(f"Gama: {gama:.2f}")
        
def abrir_janela_gama(p, gh, parent=None, modal=False):
    dlg = JanelaGama(p, gh, parent=parent, modal=modal)
    # guarda referência no parent (evita que o diálogo seja coletado)
    if parent is not None:
        setattr(parent, "_janela_gama", dlg)
    dlg.show()
    return dlg


class JanelaLinearPorPartes(QDialog):
    def __init__(self, p, gh, parent=None, modal=False):
        super().__init__(parent)
        self.p = p
        self.gh = gh

        self.setWindowTitle("Linear por partes")
        self.setWindowModality(Qt.WindowModality.NonModal)
        self.resize(520, 460)

        self.r1, self.s1 = 64, 64
        self.r2, self.s2 = 192, 192

        self.label_info = QLabel(f"r1={int(self.r1)} s1={int(self.s1)}    r2={int(self.r2)} s2={int(self.s2)}")

        self.fig = Figure(figsize=(5,4), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(0, 255)
        self.ax.set_ylim(0, 255)
        self.ax.set_xlabel("r (entrada)")
        self.ax.set_ylabel("s (saída)")
        self.ax.set_title("Transformação linear por partes")

        controls = QWidget()
        hcontrols = QHBoxLayout()
        controls.setLayout(hcontrols)

        def make_spin(label_text, init):
            lbl = QLabel(label_text)
            sp = QSpinBox()
            sp.setRange(0, 255)
            sp.setValue(init)
            sp.setSingleStep(1)
            return lbl, sp

        lbl_r1, self.spin_r1 = make_spin("r1", self.r1)
        lbl_s1, self.spin_s1 = make_spin("s1", self.s1)
        lbl_r2, self.spin_r2 = make_spin("r2", self.r2)
        lbl_s2, self.spin_s2 = make_spin("s2", self.s2)

        self.spin_r1.setRange(0, 254)
        self.spin_r2.setRange(1, 255)

        if self.spin_r1.value() >= self.spin_r2.value():
            self.spin_r2.setValue(self.spin_r1.value() + 1)

        self.spin_r1.valueChanged.connect(self._on_r1_changed)
        self.spin_r2.valueChanged.connect(self._on_r2_changed)
        self.spin_s1.valueChanged.connect(self._draw_curve)
        self.spin_s2.valueChanged.connect(self._draw_curve)

        hcontrols.addWidget(lbl_r1); hcontrols.addWidget(self.spin_r1); hcontrols.addSpacing(8)
        hcontrols.addWidget(lbl_s1); hcontrols.addWidget(self.spin_s1); hcontrols.addSpacing(8)
        hcontrols.addWidget(lbl_r2); hcontrols.addWidget(self.spin_r2); hcontrols.addSpacing(8)
        hcontrols.addWidget(lbl_s2); hcontrols.addWidget(self.spin_s2)

        self.botao_aplicar = QPushButton("Aplicar")
        self.botao_cancelar = QPushButton("Fechar")
        self.botao_aplicar.clicked.connect(self.on_aplicar)
        self.botao_cancelar.clicked.connect(self.close)

        h_buttons = QHBoxLayout()
        h_buttons.addStretch(1)
        h_buttons.addWidget(self.botao_aplicar)
        h_buttons.addWidget(self.botao_cancelar)

        layout = QVBoxLayout()
        layout.addWidget(self.label_info)
        layout.addWidget(self.canvas)
        layout.addWidget(controls)
        layout.addLayout(h_buttons)
        self.setLayout(layout)

        self._draw_curve()


    def _draw_curve(self):
        self.r1 = int(self.spin_r1.value())
        self.s1 = int(self.spin_s1.value())
        self.r2 = int(self.spin_r2.value())
        self.s2 = int(self.spin_s2.value())
        
        self.ax.clear()
        self.ax.set_xlim(0, 255)
        self.ax.set_ylim(0, 255)
        self.ax.set_xlabel("r (entrada)")
        self.ax.set_ylabel("s (saída)")
        self.ax.set_title("Transformação linear por partes")

        xs = [0, self.r1, self.r2, 255]
        ys = [0, self.s1, self.s2, 255]

        self.ax.plot(xs, ys, linewidth=2, marker='o', markersize=6)
        self.ax.grid(True, linestyle=':', linewidth=0.5)
        self.canvas.draw_idle()
        self.label_info.setText(f"r1={int(self.r1)} s1={int(self.s1)}    r2={int(self.r2)} s2={int(self.s2)}")

    def _on_r1_changed(self, val):
        self.spin_r2.blockSignals(True)
        self.spin_r2.setMinimum(val)

        if self.spin_r2.value() < val:
            self.spin_r2.setValue(val)
        self.spin_r2.blockSignals(False)

        self.spin_r1.blockSignals(True)
        self.spin_r1.setMaximum(self.spin_r2.value())
        self.spin_r1.blockSignals(False)

        self._draw_curve()

    def _on_r2_changed(self, val):
        self.spin_r1.blockSignals(True)
        self.spin_r1.setMaximum(val)

        if self.spin_r1.value() > val:
            self.spin_r1.setValue(val)
        self.spin_r1.blockSignals(False)

        self.spin_r2.blockSignals(True)
        self.spin_r2.setMinimum(self.spin_r1.value())
        self.spin_r2.blockSignals(False)

        self._draw_curve()

    def on_aplicar(self):
        r1 = int(self.spin_r1.value())
        s1 = int(self.spin_s1.value())
        r2 = int(self.spin_r2.value())
        s2 = int(self.spin_s2.value())

        try:
            funcoes.aplicar_linear_por_partes(self.p, self.gh, r1, s1, r2, s2)
        except Exception as e:
            print("Erro ao aplicar linear por partes:", e)
        else:
            self.close()

def abrir_janela_linearpp(p, gh, parent=None, modal=False):
    dlg = JanelaLinearPorPartes(p, gh, parent=parent, modal=modal)
    if parent is not None:
        setattr(parent, "_janela_linear", dlg)
    dlg.show()
    return dlg

class JanelaHistograma(QDialog):
    def __init__(self, p, gh, octave, caminho_imagem, parent=None):
        super().__init__(parent)
        self.p = p
        self.gh = gh
        self.octave = octave
        self.caminho = caminho_imagem
        self.setWindowTitle("Histograma")
        self.resize(400, 300)

        v = QVBoxLayout(self)
        self.label = QLabel("Histograma")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v.addWidget(self.label)

        self.fig = Figure(figsize=(6,4), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        v.addWidget(self.canvas)

        h = QHBoxLayout()
        self.chk_r = QCheckBox("R")
        self.chk_g = QCheckBox("G")
        self.chk_b = QCheckBox("B")
        self.chk_i = QCheckBox("I")   # novo checkbox para o canal I
        self.chk_r.setChecked(True)
        self.chk_g.setChecked(True)
        self.chk_b.setChecked(True)
        self.chk_i.setChecked(True)   # por padrão mostramos I também

        h.addWidget(self.chk_r)
        h.addWidget(self.chk_g)
        h.addWidget(self.chk_b)
        h.addWidget(self.chk_i)
        h.addStretch(1)
        btn_atualizar = QPushButton("Atualizar")
        btn_equalizar = QPushButton("Equalizar")
        btn_atualizar.clicked.connect(self.atualizar_hist)
        btn_equalizar.clicked.connect(self.equalizar_hist)
        h.addWidget(btn_atualizar)
        h.addWidget(btn_equalizar)
        v.addLayout(h)

        self.chk_r.stateChanged.connect(self._update_plot)
        self.chk_g.stateChanged.connect(self._update_plot)
        self.chk_b.stateChanged.connect(self._update_plot)
        self.chk_i.stateChanged.connect(self._update_plot)  # conectar I

        self.generate_hist()

    def generate_hist(self):
        try:
            # agora pede 6 saídas: tipo, c, r, g, b, i
            tipo, c, r, g, b, i = self.octave.feval('canais', self.caminho, nout=6)
        except Exception as e:
            print("Erro ao receber valores da imagem: ", e)
            return

        tipo = str(tipo)
        self._tipo = tipo.lower().strip()
        # converter retornos para numpy arrays (eles podem ser vazios)
        self._c = (np.asarray(c)).flatten()
        self._r = (np.asarray(r)).flatten()
        self._g = (np.asarray(g)).flatten()
        self._b = (np.asarray(b)).flatten()
        self._i = (np.asarray(i)).flatten()

        if self._tipo == 'gray':
            # esconder checkboxes RGB/I
            self.chk_r.setVisible(False)
            self.chk_g.setVisible(False)
            self.chk_b.setVisible(False)
            self.chk_i.setVisible(False)
            self.label.setText("Histograma - Escala de Cinza")
        else:
            self.label.setText("Histograma - RGB + I")

        self._update_plot()

    def equalizar_hist(self):
        try:
            funcoes.equalizar_hist(self.p, self.gh)
            # após equalizar, atualizar vetores chamando generate_hist novamente
            self.generate_hist()
            self._update_plot()
        except Exception as e:
            print("Erro ao chamar funcao equalizar_hist: ", e)

    def atualizar_hist(self):
        self.generate_hist()
        self._update_plot()

    def _update_plot(self):
        self.ax.clear()

        if self._tipo == 'gray':
            if self._c.size == 0:
                self.ax.text(0.5, 0.5, "Sem dados (vetor vazio).", ha='center', va='center')
            else:
                counts, bins = np.histogram(self._c, bins=256, range=(0,255))
                centers = np.arange(256)
                self.ax.bar(centers, counts, width=1.0, align='center', color='gray')
                self.ax.set_xlabel("Nível")
                self.ax.set_ylabel("Contagem")
        elif self._tipo == 'rgb':
            bins = np.arange(256)
            plotted = False
            show_r = self.chk_r.isChecked() and self._r.size > 0
            show_g = self.chk_g.isChecked() and self._g.size > 0
            show_b = self.chk_b.isChecked() and self._b.size > 0
            show_i = self.chk_i.isChecked() and self._i.size > 0

            if not (show_r or show_g or show_b or show_i):
                self.ax.text(0.5, 0.5, "Nenhum canal selecionado.", ha='center', va='center')
            else:
                if show_r:
                    counts_r, _ = np.histogram(self._r, bins=256, range=(0,255))
                    self.ax.bar(bins, counts_r, label='R', color='red', alpha=0.7)
                    plotted = True
                if show_g:
                    counts_g, _ = np.histogram(self._g, bins=256, range=(0,255))
                    self.ax.bar(bins, counts_g, label='G', color='green', alpha=0.7)
                    plotted = True
                if show_b:
                    counts_b, _ = np.histogram(self._b, bins=256, range=(0,255))
                    self.ax.bar(bins, counts_b, label='B', color='blue', alpha=0.7)
                    plotted = True
                if show_i:
                    counts_i, _ = np.histogram(self._i, bins=256, range=(0,255))
                    # escolhi magenta para I (você pode trocar)
                    self.ax.bar(bins, counts_i, label='I', color='magenta', alpha=0.7)
                    plotted = True

                if plotted:
                    self.ax.set_xlabel("Níveis de Intensidade")
                    self.ax.set_ylabel("Quantidade de pixels")
                    self.ax.legend()
        else:
            self.ax.text(0.5, 0.5, "Tipo desconhecido.", ha='center', va='center')

        self.ax.grid(True, linestyle=':', linewidth=0.5)
        self.canvas.draw_idle()

def abrir_janela_histograma(p, gh, octave, caminho_imagem, parent=None):
    dlg = JanelaHistograma(p, gh, octave, caminho_imagem, parent=parent)
    if parent is not None:
        setattr(parent, "_janela_hist_oct", dlg)
    print(dlg)
    dlg.show()
    return dlg

class JanelaLimiar(QDialog):
    def __init__(self, p, gh, parent=None, modal=False):
        super().__init__(parent)
        self.p = p
        self.gh = gh

        self.setWindowTitle("Linear por partes")
        self.setWindowModality(Qt.WindowModality.NonModal)
        self.resize(520, 460)

        self.l = 127
        self.label_info = QLabel(f"l={int(self.l)}")

        self.fig = Figure(figsize=(5,4), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(0, 255)
        self.ax.set_ylim(0, 255)
        self.ax.set_xlabel("r (entrada)")
        self.ax.set_ylabel("s (saída)")
        self.ax.set_title("Função de Limiarização")

        controls = QWidget()
        hcontrols = QHBoxLayout()
        controls.setLayout(hcontrols)

        def make_spin(label_text, init):
            lbl = QLabel(label_text)
            sp = QSpinBox()
            sp.setRange(0, 255)
            sp.setValue(init)
            sp.setSingleStep(1)
            return lbl, sp

        label, self.spin_l = make_spin("l", self.l)
        self.spin_l.setRange(0, 255)

        self.spin_l.valueChanged.connect(self._draw_curve)

        hcontrols.setAlignment(Qt.AlignmentFlag.AlignLeft)
        hcontrols.addWidget(label)
        hcontrols.addWidget(self.spin_l)        

        self.botao_aplicar = QPushButton("Aplicar")
        self.botao_cancelar = QPushButton("Fechar")
        self.botao_aplicar.clicked.connect(self.on_aplicar)
        self.botao_cancelar.clicked.connect(self.close)

        h_buttons = QHBoxLayout()
        h_buttons.addStretch(1)
        h_buttons.addWidget(self.botao_aplicar)
        h_buttons.addWidget(self.botao_cancelar)

        layout = QVBoxLayout()
        layout.addWidget(self.label_info)
        layout.addWidget(self.canvas)
        layout.addWidget(controls)
        layout.addLayout(h_buttons)
        self.setLayout(layout)

        self._draw_curve()

    def _draw_curve(self):
        self.l = int(self.spin_l.value())
        
        self.ax.clear()
        self.ax.set_xlim(0, 255)
        self.ax.set_ylim(0, 255)
        self.ax.set_xlabel("r (entrada)")
        self.ax.set_ylabel("s (saída)")
        self.ax.set_title("Função de Limiarização")

        xs = [0, self.l, self.l, 255]
        ys = [0, 0, 255, 255]

        self.ax.plot(xs, ys, linewidth=2, marker='o', markersize=6)
        self.ax.grid(True, linestyle=':', linewidth=0.5)
        self.canvas.draw_idle()
        self.label_info.setText(f"l={int(self.l)}")

    def on_aplicar(self):
        l = int(self.spin_l.value())
        try:
            funcoes.aplicar_limiarizar(self.p, self.gh, l)
        except Exception as e:
            print("Erro ao aplicar limiarização: ", e)
        else:
            self.close()

def abrir_janela_limiar(p, gh, parent=None, modal=False):
    dlg = JanelaLimiar(p, gh, parent=parent, modal=modal)
    if parent is not None:
        setattr(parent, "_janela_limiarizar", dlg)
    dlg.show()
    return dlg

class JanelaFiltros(QDialog):
    def __init__(self, p=None, gh=None, parent=None, modal=False):
        super().__init__(parent)
        self.p = p
        self.gh = gh

        self.setWindowTitle("Filtros")
        self.setWindowModality(Qt.WindowModality.NonModal)
        self.resize(520, 460)

        main = QVBoxLayout()

        # --- Opções (check, exclusivas) ---
        options_box = QGroupBox("Tipo de filtro")
        opt_layout = QVBoxLayout()

        # Usamos QCheckBox com QButtonGroup para forçar exclusividade visual
        # (parece checkbox mas se comporta como radio — seleciona apenas 1)
        self.btn_group = QButtonGroup(self)
        self.btn_group.setExclusive(True)

        self.chk_generico = QCheckBox("Filtro Genérico")
        self.chk_media_s = QCheckBox("Suavização (Média Simples)")
        self.chk_media_p = QCheckBox("Suavização (Média Ponderada)")
        self.chk_gauss = QCheckBox("Suavização (Gaussiano)")
        self.chk_mediana = QCheckBox("Mediana")
        self.chk_laplace1 = QCheckBox("Laplaciano 1")
        self.chk_laplace2 = QCheckBox("Laplaciano 2")
        self.chk_laplace1aj = QCheckBox("Laplaciano 1 (com ajuste)")
        self.chk_laplace2aj = QCheckBox("Laplaciano 2 (com ajuste)")
        self.chk_nlaplace1 = QCheckBox("Aguçamento (Laplaciano 1)")
        self.chk_nlaplace2 = QCheckBox("Aguçamento (Laplaciano 2)")
        self.chk_highboost = QCheckBox("Aguçamento (High-Boost)")
        self.chk_sobel_x = QCheckBox("Filtro de Sobel (x)")
        self.chk_sobel_y = QCheckBox("Filtro de Sobel (y)")
        self.chk_bordas = QCheckBox("Detecção de Bordas (pelo gradiente)")

        for i, chk in enumerate((self.chk_generico, self.chk_media_s, self.chk_media_p, self.chk_gauss,
                                 self.chk_mediana, self.chk_laplace1, self.chk_laplace2, self.chk_laplace1aj,
                                 self.chk_laplace2aj, self.chk_nlaplace1, self.chk_nlaplace2, self.chk_highboost,
                                 self.chk_sobel_x, self.chk_sobel_y, self.chk_bordas)):
            chk.setCheckable(True)
            self.btn_group.addButton(chk, i)
            opt_layout.addWidget(chk)
            chk.toggled.connect(self._update_grid)

        options_box.setLayout(opt_layout)
        main.addWidget(options_box)

        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Tamanho do filtro:"))
        self.combo_size = QComboBox()
        sizes = [3, 5, 7, 9]
        for s in sizes:
            self.combo_size.addItem(f"{s} x {s}", s)
        self.combo_size.setCurrentIndex(0)
        self.combo_size.currentIndexChanged.connect(self._update_grid)
        size_layout.addWidget(self.combo_size)
        size_layout.addStretch()
        main.addLayout(size_layout)

        # --- Grid 9x9 (inicialmente oculto) ---
        self.grid_group = QGroupBox("Janela de filtro")
        self.grid_layout = QGridLayout()
        self.grid_group.setLayout(self.grid_layout)

        self.grid_edits = []  # lista de listas
        double_validator = QDoubleValidator(-1e9, 1e9, 6, self)
        double_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        double_validator.setLocale(QLocale(QLocale.Language.English))

        for r in range(9):
            row = []
            for c in range(9):
                le = QLineEdit()
                le.setFixedWidth(40)
                le.setValidator(double_validator)
                le.setAlignment(Qt.AlignmentFlag.AlignCenter)
                le.setText("0")
                le.setVisible(False)
                self.grid_layout.addWidget(le, r, c)
                row.append(le)
            self.grid_edits.append(row)

        self.grid_group.setVisible(False)
        main.addWidget(self.grid_group)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.btn_ok = QPushButton("Aplicar")
        self.btn_clear = QPushButton("Limpar Grid")
        self.btn_clear.setVisible(False)
        self.btn_ok.clicked.connect(self.aplicar)
        self.btn_clear.clicked.connect(self.clear_grid)

        btn_layout.addWidget(self.btn_ok)
        btn_layout.addWidget(self.btn_clear)
        main.addLayout(btn_layout)

        self.setLayout(main)
        self._update_grid()

    def aplicar(self):
        tam = self.combo_size.currentData()
        tipo = ""
        if self.chk_generico.isChecked() or self.chk_media_p.isChecked():
            if self.chk_generico.isChecked():
                tipo = "generico"
            else:
                tipo = "mponderada"
            f = self.get_filtro()
            funcoes.aplicar_filtro(self.p, self.gh, tipo, tam, f)
        else:
            if self.chk_media_s.isChecked():
                tipo = "msimples"
            if self.chk_media_p.isChecked():
                tipo = "mponderada"
            if self.chk_mediana.isChecked():
                tipo = "mediana"
            if self.chk_gauss.isChecked():
                tipo = "gaussiano"
            if self.chk_laplace1.isChecked():
                tipo = "laplaciano1"
            if self.chk_laplace2.isChecked():
                tipo = "laplaciano2"
            if self.chk_laplace1aj.isChecked():
                tipo = "laplaciano1aj"
            if self.chk_laplace2aj.isChecked():
                tipo = "laplaciano2aj"
            if self.chk_nlaplace1.isChecked():
                tipo = "nlaplaciano1"
            if self.chk_nlaplace2.isChecked():
                tipo = "nlaplaciano2"
            if self.chk_highboost.isChecked():
                tipo = "highboost"

            if self.chk_sobel_x.isChecked():
                tipo = "sobelx"
            if self.chk_sobel_y.isChecked():
                tipo = "sobely"
            if self.chk_bordas.isChecked():
                tipo = "bordas"

            funcoes.aplicar_filtro(self.p, self.gh, tipo, tam)
        

    def _update_grid(self):
        if (self.chk_laplace1.isChecked() or self.chk_laplace2.isChecked() or self.chk_laplace1aj.isChecked() 
            or self.chk_laplace2aj.isChecked() or self.chk_nlaplace1.isChecked() or self.chk_nlaplace2.isChecked()
            or self.chk_sobel_x.isChecked() or self.chk_sobel_y.isChecked() or self.chk_bordas.isChecked()):
            self.combo_size.setCurrentIndex(0)
            self.combo_size.setEnabled(False)
        else:
            self.combo_size.setEnabled(True)

        if self.chk_generico.isChecked() or self.chk_media_p.isChecked():
            size = self.combo_size.currentData()
            if size is None:
                size = 5
            self.grid_group.setVisible(True)
            self.btn_clear.setVisible(True)
            for r in range(9):
                for c in range(9):
                    visible = (r<size) and (c<size)
                    self.grid_edits[r][c].setVisible(visible)
        else:
            self.grid_group.setVisible(False)
            self.btn_clear.setVisible(False)
            for r in range(9):
                for c in range(9):
                    self.grid_edits[r][c].setVisible(False)
    
    def clear_grid(self):
        for row in self.grid_edits:
            for cell in row:
                cell.setText("0")

    def get_filtro(self):
        size = self.combo_size.currentData()
        filtro = [[1 for _ in range(size)] for _ in range(size)]
        for r in range(size):
            for c in range(size):
                text = self.grid_edits[r][c].text().strip()
                if text == "":
                    val = 0
                else:
                    try:
                        val = float(text)
                    except ValueError:
                        val = 0
                filtro[r][c] = val
        return filtro

def abrir_janela_filtros(p, gh, parent=None, modal=False):
    dlg = JanelaFiltros(p, gh, parent=parent, modal=modal)
    if parent is not None:
        setattr(parent, "_janela_filtros", dlg)
    dlg.show()
    return dlg


class JanelaEscala(QDialog):
    def __init__(self, p, gh, parent=None, modal=False):
        super().__init__(parent)
        self.p = p
        self.gh = gh

        self.setWindowTitle("Escala")
        self.setWindowModality(Qt.WindowModality.NonModal)
        self.resize(300, 150)

        self.label_sx = QLabel("X: 1.00")
        self.sliderX = QSlider(Qt.Orientation.Horizontal)
        self.sliderX.setRange(10, 200)
        self.sliderX.setValue(100)
        self.sliderX.setTickInterval(10)
        self.sliderX.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.sliderX.valueChanged.connect(self.atualizar_label_sx)

        self.label_sy = QLabel("Y: 1.00")
        self.sliderY = QSlider(Qt.Orientation.Horizontal)   
        self.sliderY.setRange(10, 200)
        self.sliderY.setValue(100)
        self.sliderY.setTickInterval(10)
        self.sliderY.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.sliderY.valueChanged.connect(self.atualizar_label_sy)

        self.botao_aplicar = QPushButton("Aplicar")
        self.botao_aplicar.clicked.connect(lambda: funcoes.aplicar_escala(self.p, self.gh, (self.sliderX.value()/100.0), (self.sliderY.value()/100.0)))

        h = QHBoxLayout()
        h.addWidget(self.botao_aplicar)

        layout = QVBoxLayout()
        layout.addWidget(self.label_sx)
        layout.addWidget(self.sliderX)
        layout.addWidget(self.label_sy)
        layout.addWidget(self.sliderY)
        layout.addLayout(h)
        self.setLayout(layout)

    def atualizar_label_sx(self, val):
        sx = val / 100.0
        self.label_sx.setText(f"X: {sx:.2f}")
    def atualizar_label_sy(self, val):
        sy = val / 100.0
        self.label_sy.setText(f"Y: {sy:.2f}")

def abrir_janela_escala(p, gh, parent=None, modal=False):
    dlg = JanelaEscala(p, gh, parent=parent, modal=modal)
    # guarda referência no parent (evita que o diálogo seja coletado)
    if parent is not None:
        setattr(parent, "_janela_escala", dlg)
    dlg.show()
    return dlg


class JanelaRotacao(QDialog):
    def __init__(self, p, gh, parent=None, modal=False):
        super().__init__(parent)
        self.p = p
        self.gh = gh

        self.setWindowTitle("Rotação")
        self.setWindowModality(Qt.WindowModality.NonModal)
        self.resize(300, 150)

        self.label_ang = QLabel("Ângulo (em graus): 180")
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 360)
        self.slider.setValue(180)
        self.slider.setTickInterval(1)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.valueChanged.connect(self.atualizar_label_ang)

        self.botao_aplicar = QPushButton("Aplicar")
        self.botao_aplicar.clicked.connect(lambda: funcoes.aplicar_rotacao(self.p, self.gh, self.slider.value()))

        h = QHBoxLayout()
        h.addWidget(self.botao_aplicar)

        layout = QVBoxLayout()
        layout.addWidget(self.label_ang)
        layout.addWidget(self.slider)
        layout.addLayout(h)
        self.setLayout(layout)

    def atualizar_label_ang(self, val):
        self.label_ang.setText(f"Ângulo (em graus): {val}")
        
def abrir_janela_rotacao(p, gh, parent=None, modal=False):
    dlg = JanelaRotacao(p, gh, parent=parent, modal=modal)
    if parent is not None:
        setattr(parent, "_janela_rotacao", dlg)
    dlg.show()
    return dlg


class JanelaMatizSatBri(QDialog):
    def __init__(self, p, gh, parent=None, modal=False):
        super().__init__(parent)
        self.p = p
        self.gh = gh

        self.setWindowTitle("Matiz, Saturação e Brilho")
        self.setWindowModality(Qt.WindowModality.NonModal)
        self.resize(360, 220)

        self.label_h = QLabel("Matiz: 0°")
        self.slider_h = QSlider(Qt.Orientation.Horizontal)
        self.slider_h.setRange(-180, 180)
        self.slider_h.setValue(0)
        self.slider_h.setTickInterval(30)
        self.slider_h.valueChanged.connect(self._atualizar_label_h)

        self.label_s = QLabel("Saturação: 100%")
        self.slider_s = QSlider(Qt.Orientation.Horizontal)
        self.slider_s.setRange(0, 200)   # 0% .. 200%
        self.slider_s.setValue(100)
        self.slider_s.setTickInterval(10)
        self.slider_s.valueChanged.connect(self._atualizar_label_s)

        self.label_b = QLabel("Brilho: 0%")
        self.slider_b = QSlider(Qt.Orientation.Horizontal)
        self.slider_b.setRange(-100, 100)  # -100% .. 100%
        self.slider_b.setValue(0)
        self.slider_b.setTickInterval(10)
        self.slider_b.valueChanged.connect(self._atualizar_label_b)

        # Botões
        self.botao_aplicar = QPushButton("Aplicar")
        self.botao_aplicar.clicked.connect(self.on_aplicar)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_h)
        layout.addWidget(self.slider_h)
        layout.addWidget(self.label_s)
        layout.addWidget(self.slider_s)
        layout.addWidget(self.label_b)
        layout.addWidget(self.slider_b)

        h_buttons = QHBoxLayout()
        h_buttons.addStretch(1)
        h_buttons.addWidget(self.botao_aplicar)
        layout.addLayout(h_buttons)

        self.setLayout(layout)

    def _atualizar_label_h(self, val):
        self.label_h.setText(f"Matiz: {val}°")

    def _atualizar_label_s(self, val):
        self.label_s.setText(f"Saturação: {val}%")

    def _atualizar_label_b(self, val):
        # brilho exibido como percentual (adição)
        self.label_b.setText(f"Brilho: {val}%")

    def on_aplicar(self):
        # ler valores e chamar função em funcoes.py
        hue_deg = int(self.slider_h.value())
        sat_percent = int(self.slider_s.value())
        bri_percent = int(self.slider_b.value())

        try:
            import funcoes
            funcoes.aplicar_matiz_saturacao_brilho(self.p, self.gh, hue_deg, sat_percent, bri_percent)
        except Exception as e:
            print("Erro ao aplicar Matiz/Saturação/Brilho:", e)
        else:
            self.close()

def abrir_janela_matiz(p, gh, parent=None, modal=False):
    dlg = JanelaMatizSatBri(p, gh, parent=parent, modal=modal)
    if parent is not None:
        setattr(parent, "_janela_matiz", dlg)
    dlg.show()
    return dlg


class JanelaAjusteCanais(QDialog):
    def __init__(self, p, gh, parent=None, modal=False):
        super().__init__(parent)
        self.p = p
        self.gh = gh

        self.setWindowTitle("Ajuste de Canal (C/R, M/G, Y/B)")
        self.setWindowModality(Qt.WindowModality.NonModal)
        self.resize(360, 240)

        # Labels e sliders
        self.label_c = QLabel("C/R: 0% (Ciano + / Vermelho -)")
        self.slider_c = QSlider(Qt.Orientation.Horizontal)
        self.slider_c.setRange(-100, 100)
        self.slider_c.setValue(0)
        self.slider_c.setTickInterval(10)
        self.slider_c.valueChanged.connect(self._atualizar_label_c)

        self.label_m = QLabel("M/G: 0% (Magenta + / Verde -)")
        self.slider_m = QSlider(Qt.Orientation.Horizontal)
        self.slider_m.setRange(-100, 100)
        self.slider_m.setValue(0)
        self.slider_m.setTickInterval(10)
        self.slider_m.valueChanged.connect(self._atualizar_label_m)

        self.label_y = QLabel("Y/B: 0% (Amarelo + / Azul -)")
        self.slider_y = QSlider(Qt.Orientation.Horizontal)
        self.slider_y.setRange(-100, 100)
        self.slider_y.setValue(0)
        self.slider_y.setTickInterval(10)
        self.slider_y.valueChanged.connect(self._atualizar_label_y)

        # Botões
        self.botao_aplicar = QPushButton("Aplicar")
        self.botao_fechar = QPushButton("Fechar")
        self.botao_aplicar.clicked.connect(self.on_aplicar)
        self.botao_fechar.clicked.connect(self.close)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_c)
        layout.addWidget(self.slider_c)
        layout.addWidget(self.label_m)
        layout.addWidget(self.slider_m)
        layout.addWidget(self.label_y)
        layout.addWidget(self.slider_y)

        h_buttons = QHBoxLayout()
        h_buttons.addStretch(1)
        h_buttons.addWidget(self.botao_aplicar)
        h_buttons.addWidget(self.botao_fechar)
        layout.addLayout(h_buttons)

        self.setLayout(layout)

    def _atualizar_label_c(self, val):
        # texto explicativo: positivo = mais Ciano
        self.label_c.setText(f"C/R: {val}% (Ciano {'+' if val>0 else ''}{val} / Vermelho {'+' if val<0 else ''}{-val if val<0 else 0})")

    def _atualizar_label_m(self, val):
        self.label_m.setText(f"M/G: {val}% (Magenta {'+' if val>0 else ''}{val} / Verde {'+' if val<0 else ''}{-val if val<0 else 0})")

    def _atualizar_label_y(self, val):
        self.label_y.setText(f"Y/B: {val}% (Amarelo {'+' if val>0 else ''}{val} / Azul {'+' if val<0 else ''}{-val if val<0 else 0})")

    def on_aplicar(self):
        dc = int(self.slider_c.value())
        dm = int(self.slider_m.value())
        dy = int(self.slider_y.value())

        try:
            import funcoes
            funcoes.aplicar_ajuste_canais(self.p, self.gh, dc, dm, dy)
        except Exception as e:
            print("Erro ao aplicar ajuste de canais:", e)
        else:
            self.close()

def abrir_janela_ajuste_canais(p, gh, parent=None, modal=False):
    dlg = JanelaAjusteCanais(p, gh, parent=parent, modal=modal)
    if parent is not None:
        setattr(parent, "_janela_ajuste_canais", dlg)
    dlg.show()
    return dlg

class JanelaEscalaCinza(QDialog):
    def __init__(self, p, gh, parent=None, modal=False):
        super().__init__(parent)
        self.p = p
        self.gh = gh

        self.setWindowTitle("Converter para Escala de Cinza")
        self.setWindowModality(Qt.WindowModality.NonModal)
        self.resize(320, 140)

        layout = QVBoxLayout(self)

        lbl = QLabel("Escolha o método de conversão para escala de cinza:")
        layout.addWidget(lbl)

        from PyQt6.QtWidgets import QRadioButton, QButtonGroup
        self.rb_media_simples = QRadioButton("Média simples")
        self.rb_media_ponderada = QRadioButton("Média ponderada")
        self.rb_media_ponderada.setChecked(True)  # padrão

        layout.addWidget(self.rb_media_simples)
        layout.addWidget(self.rb_media_ponderada)

        self._bg = QButtonGroup(self)
        self._bg.addButton(self.rb_media_simples, 0)
        self._bg.addButton(self.rb_media_ponderada, 1)
        self._bg.setExclusive(True)

        # botões
        h = QHBoxLayout()
        btn_aplicar = QPushButton("Aplicar")
        btn_fechar = QPushButton("Fechar")
        btn_aplicar.clicked.connect(self.on_aplicar)
        btn_fechar.clicked.connect(self.close)
        h.addStretch(1)
        h.addWidget(btn_aplicar)
        h.addWidget(btn_fechar)

        layout.addLayout(h)
        self.setLayout(layout)

    def on_aplicar(self):
        metodo = "ponderada"
        if self.rb_media_simples.isChecked():
            metodo = "simples"
        try:
            import funcoes
            funcoes.aplicar_escala_cinza(self.p, self.gh, metodo)
        except Exception as e:
            print("Erro ao aplicar escala de cinza:", e)
        else:
            self.close()

def abrir_janela_escala_cinza(p, gh, parent=None, modal=False):
    dlg = JanelaEscalaCinza(p, gh, parent=parent, modal=modal)
    if parent is not None:
        setattr(parent, "_janela_escala_cinza", dlg)
    dlg.show()
    return dlg



class JanelaDFT(QDialog):
    """
    Janela para visualizar e editar o espectro da Transformada de Fourier.
    Mostra espectro em preto e branco com contraste e brilho equilibrados.
    Pintar branco = manter (1), pintar preto = remover (0).
    """

    def __init__(self, p, gh, mag_path, spec_mat, parent=None):
        super().__init__(parent)
        self.p = p
        self.gh = gh
        self.mag_path = mag_path
        self.spec_mat = spec_mat

        self.setWindowTitle("Espectro (DFT) - Editar máscara")
        self.resize(900, 700)

        # --- carregar imagem do espectro ---
        import imageio
        try:
            mag_img = imageio.v3.imread(self.mag_path)
        except Exception:
            import matplotlib.pyplot as plt
            mag_img = plt.imread(self.mag_path)

        # garantir grayscale 2D e converter para float
        if mag_img.ndim == 3:
            mag = mag_img[:, :, 0].astype(float)
        else:
            mag = mag_img.astype(float)

                # --- ajuste de escala e contraste ---
        # usamos logaritmo para reduzir picos muito altos
        mag = np.log1p(mag)

        # Normalização usando percentis menos extremos -> reduz contraste exagerado
        # (alternar 2,98 -> 5,99 ou outro par para ajustar)
        pct_low, pct_high = 5, 99
        low, high = np.percentile(mag, (pct_low, pct_high))

        # evitar divisão por zero
        mag = (mag - low) / (high - low + 1e-9)
        mag = np.clip(mag, 0.0, 1.0)

        # diminuir contraste global: levar valores em volta de 0.5 com fator <1
        # contrast: 0..1 (1 = contraste original, <1 = contraste reduzido)
        contrast = 1.5
        # brightness: adição final em -0.2..+0.2 (negativo = escurecer)
        brightness = -0.3

        mag_adj = 0.5 + contrast * (mag -0.5) + brightness
        mag_adj = np.clip(mag_adj, 0.0, 1.0)

        # conversão final para imagem 8-bit (grayscale)
        self.mag_disp = (mag_adj * 255.0).astype(np.uint8)
        self.rows, self.cols = self.mag_disp.shape

        # máscara inicial
        self.mask = np.ones((self.rows, self.cols), dtype=np.uint8)

        # estado do pincel
        self.drawing = False
        self.draw_mode = 'white'
        self.brush_radius = 10

        # --- figure / canvas ---
        self.fig = Figure(figsize=(6, 5), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Espectro — pintar branco = manter, pintar preto = remover")
        # exibir em grayscale; menos opacidade para máscara para deixar espectro visível
        self.im_mag = self.ax.imshow(self.mag_disp, cmap='gray', origin='upper', vmin=0, vmax=255)
        self.im_mask = self.ax.imshow(self.mask, cmap='gray', origin='upper', alpha=0.35, vmin=0, vmax=1)
        self.ax.set_axis_off()
        self.canvas.draw_idle()


        # conectar eventos do matplotlib
        self.cid_press = self.canvas.mpl_connect('button_press_event', self.on_press)
        self.cid_release = self.canvas.mpl_connect('button_release_event', self.on_release)
        self.cid_move = self.canvas.mpl_connect('motion_notify_event', self.on_move)

        # --- controles UI ---
        btn_white = QPushButton("Pintar Branco (manter)")
        btn_black = QPushButton("Pintar Preto (remover)")
        btn_clear = QPushButton("Limpar Máscara")
        btn_save_mask = QPushButton("Salvar Máscara")
        btn_apply_mask = QPushButton("Aplicar (com máscara)")
        btn_apply_no_mask = QPushButton("Aplicar (sem máscara)")
        btn_close = QPushButton("Fechar")

        lbl_brush = QLabel("Tamanho pincel:")
        self.spin_brush = QSpinBox()
        self.spin_brush.setRange(1, 200)
        self.spin_brush.setValue(self.brush_radius)
        self.spin_brush.valueChanged.connect(self._on_brush_changed)

        # conectar botões
        btn_white.clicked.connect(self.set_white_mode)
        btn_black.clicked.connect(self.set_black_mode)
        btn_clear.clicked.connect(self.clear_mask)
        btn_save_mask.clicked.connect(self.save_mask)
        btn_apply_mask.clicked.connect(self.apply_with_mask)
        btn_apply_no_mask.clicked.connect(self.apply_no_mask)
        btn_close.clicked.connect(self.close)

        # layout
        h_top = QHBoxLayout()
        h_top.addWidget(btn_white)
        h_top.addWidget(btn_black)
        h_top.addWidget(btn_clear)
        h_top.addStretch(1)
        h_top.addWidget(lbl_brush)
        h_top.addWidget(self.spin_brush)
        h_top.addWidget(btn_save_mask)

        h_bottom = QHBoxLayout()
        h_bottom.addStretch(1)
        h_bottom.addWidget(btn_apply_mask)
        h_bottom.addWidget(btn_apply_no_mask)
        h_bottom.addWidget(btn_close)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addLayout(h_top)
        layout.addLayout(h_bottom)
        self.setLayout(layout)

    # ----------------- pincel -----------------
    def _on_brush_changed(self, v):
        self.brush_radius = int(v)

    def set_white_mode(self):
        self.draw_mode = 'white'

    def set_black_mode(self):
        self.draw_mode = 'black'

    def clear_mask(self):
        self.mask[:, :] = 1
        self.im_mask.set_data(self.mask)
        self.canvas.draw_idle()

    def save_mask(self):
        mask_path = f"{os.path.splitext(self.spec_mat)[0]}_mask.png"
        import imageio
        imageio.v3.imwrite(mask_path, (self.mask * 255).astype(np.uint8))
        print("Máscara salva em:", mask_path)

    def on_press(self, event):
        if event.inaxes != self.ax:
            return
        self.drawing = True
        self._draw_at(event.xdata, event.ydata)

    def on_release(self, event):
        self.drawing = False

    def on_move(self, event):
        if (not self.drawing) or (event.inaxes != self.ax):
            return
        self._draw_at(event.xdata, event.ydata)

    def _draw_at(self, x, y):
        if x is None or y is None:
            return
        cx = int(round(x))
        cy = int(round(y))
        rr, cc = self.rows, self.cols
        Y, X = np.ogrid[:rr, :cc]
        dist = (X - cx) ** 2 + (Y - cy) ** 2
        mask_area = dist <= (self.brush_radius ** 2)
        if self.draw_mode == 'white':
            self.mask[mask_area] = 1
        else:
            self.mask[mask_area] = 0
        self.im_mask.set_data(self.mask)
        self.canvas.draw_idle()

    # ----------------- aplicar IFFT -----------------
    def apply_with_mask(self):
        mask_path = f"{os.path.splitext(self.spec_mat)[0]}_mask.png"
        import imageio
        imageio.v3.imwrite(mask_path, (self.mask * 255).astype(np.uint8))
        try:
            from funcoes import aplicar_ifft_com_mascara
            aplicar_ifft_com_mascara(self.p, self.gh, self.spec_mat, mask_path)
        except Exception as e:
            print("Erro ao aplicar IFFT com máscara:", e)
        self.close()

    def apply_no_mask(self):
        try:
            from funcoes import aplicar_ifft_sem_mascara
            aplicar_ifft_sem_mascara(self.p, self.gh, self.spec_mat)
        except Exception as e:
            print("Erro ao aplicar IFFT sem máscara:", e)
        self.close()

def abrir_janela_dft(p, gh, mag_path, spec_mat, parent=None):
    dlg = JanelaDFT(p, gh, mag_path, spec_mat, parent=parent)
    if parent is not None:
        setattr(parent, "_janela_dft", dlg)
    dlg.show()
    return dlg


