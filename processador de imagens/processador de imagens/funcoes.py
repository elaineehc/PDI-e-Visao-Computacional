import os
import math
import numpy as np
from oct2py import Oct2Py
octave = Oct2Py()


def aplicar_negativo(p, gh):
        if not hasattr(p, "imagem_atual_path"):
            print("Nenhuma imagem carregada.")
            return
            
        entrada = p.imagem_atual_path
        saida = p.imagem_atual_path
        
        try:
            gh.carrega_historico(entrada)
            p.octave.feval("negativo", entrada, saida, nout=0)
            p.atualizar_display(saida)
        except Exception as e:
            print("Erro ao aplicar negativo:", e)

def aplicar_gama(p, gh, gama: float = None):
        if not hasattr(p, "imagem_atual_path"):
            print("Nenhuma imagem carregada.")
            return

        entrada = p.imagem_atual_path
        saida = p.imagem_atual_path

        if gama is None:
             gama = 1.00

        try:
            gh.carrega_historico(entrada)
            p.octave.feval("gama", entrada, saida, float(gama), nout=0)
            p.atualizar_display(saida)
        except Exception as e:
            print("Erro ao aplicar correção de gama:", e)

def aplicar_linear_por_partes(p, gh, r1: int, s1: int, r2: int, s2: int):
    if not hasattr(p, "imagem_atual_path"):
        print("Nenhuma imagem carregada.")
        return

    entrada = p.imagem_atual_path
    saida = p.imagem_atual_path

    try:
        gh.carrega_historico(entrada)
        p.octave.feval("linear_por_partes", entrada, saida, float(r1), float(s1), float(r2), float(s2), nout=0)
        p.atualizar_display(saida)
    except Exception as e:
        print("Erro ao aplicar linear por partes:", e)

def aplicar_limiarizar(p, gh, x: int):
    if not hasattr(p, "imagem_atual_path"):
        print("Nenhuma imagem carregada.")
        return

    entrada = p.imagem_atual_path
    saida = p.imagem_atual_path

    try:
        gh.carrega_historico(entrada)
        p.octave.feval("limiarizar", entrada, saida, x, nout=0)
        p.atualizar_display(saida)
    except Exception as e:
        print("Erro ao aplicar limiarizacao: ", e)

def equalizar_hist(p, gh):
    if not hasattr(p, "imagem_atual_path"):
        print("Nenhuma imagem carregada.")
        return

    entrada = p.imagem_atual_path
    saida = p.imagem_atual_path

    try:
        gh.carrega_historico(entrada)
        p.octave.feval("equalizar_hist", entrada, saida, nout=0)
        p.atualizar_display(saida)
    except Exception as e:
        print("Erro ao equalizar histograma:", e)

def aplicar_filtro(p, gh, tipo, tam, filtro_generico=None):
    if not hasattr(p, "imagem_atual_path"):
        print("Nenhuma imagem carregada.")
        return
            
    entrada = p.imagem_atual_path
    saida = p.imagem_atual_path

    try:
        gh.carrega_historico(entrada)
        if tipo=="mediana":
            p.octave.feval("filtro_mediana", entrada, saida, tam, nout=0)
        elif tipo=="generico":
            print("Filtro aplicado: ", filtro_generico)
            p.octave.feval("filtro", entrada, saida, filtro_generico, nout=0)
        elif tipo=="laplaciano1aj" or tipo=="laplaciano2aj":
            tipo = tipo.replace("aj", "")
            f = define_filtro(tipo, tam)
            print("Filtro aplicado: ", f)
            p.octave.feval("laplaciano_com_ajuste", entrada, saida, f, nout=0)
        elif tipo=="nlaplaciano1" or tipo=="nlaplaciano2":
            tipo = tipo.replace("n", "", 1)
            f = define_filtro(tipo, tam)
            print("Filtro aplicado: ", f)
            p.octave.feval("nitidez_laplaciano", entrada, saida, f, nout=0)
        elif tipo=="mponderada":
            soma = sum(sum(linha) for linha in filtro_generico)
            filtro_generico = [[elem/soma for elem in row] for row in filtro_generico]
            print("Filtro aplicado: ", filtro_generico)
            p.octave.feval("filtro", entrada, saida, filtro_generico, nout=0)
        elif tipo=="highboost":
            filtro_hb = define_filtro("gaussiano", tam)
            print("Filtro aplicado: ", filtro_hb)
            p.octave.feval("high_boost", entrada, saida, filtro_hb, nout=0)
        elif tipo=="bordas":
            p.octave.feval("bordas", entrada, saida, nout=0)
        else:
            f = define_filtro(tipo, tam)
            print("Filtro aplicado: ", f)
            p.octave.feval("filtro", entrada, saida, f, nout=0)
        p.atualizar_display(saida)
    except Exception as e:
        print("Erro ao aplicar filtro:", e)
    
def define_filtro(tipo, tam):
    if tipo=="msimples":
        f = [[1 for _ in range(tam)] for _ in range(tam)]
        f = [[elem/(tam*tam) for elem in row] for row in f]

    if tipo=="gaussiano":
        t = math.floor(tam/2)
        f = [[0 for _ in range(tam)] for _ in range(tam)]
        s = 0
        for i in range(tam):
            e1 = i
            if i>t:
                e1 = (tam-1)-i
            for j in range(tam):
                e2 = j
                if j>t:
                    e2 = (tam-1)-j
                f[i][j] = pow(2, e1+e2)
                s += int(f[i][j])
        f = [[int(elem) for elem in row] for row in f]
        f = [[elem/s for elem in row] for row in f]

    if tipo=="laplaciano1":
        f = [[0, 1, 0],
            [1, -4, 1],
            [0, 1, 0]]
    if tipo=="laplaciano2":
        f = [[1, 1, 1],
            [1, -8, 1],
            [1, 1, 1]]
    
    if tipo=="sobelx":
        f = [[-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1]]
    if tipo=="sobely":
        f = [[-1, -2, -1],
            [0, 0, 0],
            [1, 2, 1]]


    return f

def aplicar_escala(p, gh, sx: float = None, sy: float = None):
        if not hasattr(p, "imagem_atual_path"):
            print("Nenhuma imagem carregada.")
            return

        entrada = p.imagem_atual_path
        saida = p.imagem_atual_path

        if sx is None:
            sx = 1.00
        if sy is None:
            sy = 1.00

        try:
            gh.carrega_historico(entrada)
            p.octave.feval("escala", entrada, saida, float(sx), float(sy), nout=0)
            p.atualizar_display(saida)
        except Exception as e:
            print("Erro ao aplicar escala:", e)

def aplicar_rotacao(p, gh, ang: int = None):
        if not hasattr(p, "imagem_atual_path"):
            print("Nenhuma imagem carregada.")
            return

        entrada = p.imagem_atual_path
        saida = p.imagem_atual_path

        if ang is None:
             ang = 180

        try:
            gh.carrega_historico(entrada)
            p.octave.feval("rotacao_intb", entrada, saida, int(ang), nout=0)
            p.atualizar_display(saida)
        except Exception as e:
            print("Erro ao aplicar rotacao:", e)

def aplicar_matiz_saturacao_brilho(p, gh, hue_deg: float = 0.0, sat_percent: float = 100.0, bri_percent: float = 0.0):
    if not hasattr(p, "imagem_atual_path"):
        print("Nenhuma imagem carregada.")
        return

    entrada = p.imagem_atual_path
    saida = p.imagem_atual_path

    delta_h = float(hue_deg) / 360.0          
    scale_s = float(sat_percent) / 100.0      
    delta_i = float(bri_percent) / 100.0      

    try:
        gh.carrega_historico(entrada)
        p.octave.feval("ajustar_hsi", entrada, saida, float(delta_h), float(scale_s), float(delta_i), nout=0)
        p.atualizar_display(saida)
    except Exception as e:
        print("Erro ao aplicar ajuste H/S/B:", e)

def aplicar_ajuste_canais(p, gh, delta_c_percent: float = 0.0, delta_m_percent: float = 0.0, delta_y_percent: float = 0.0):
    """
    Ajuste de canais C/R, M/G, Y/B.
    delta_*_percent: -100 .. 100  (percentual, 0 = sem alteração)
    """
    if not hasattr(p, "imagem_atual_path"):
        print("Nenhuma imagem carregada.")
        return

    entrada = p.imagem_atual_path
    saida = p.imagem_atual_path

    # mapear para deltas em fração (-1.0 .. 1.0)
    delta_c = float(delta_c_percent) / 100.0
    delta_m = float(delta_m_percent) / 100.0
    delta_y = float(delta_y_percent) / 100.0

    try:
        gh.carrega_historico(entrada)
        p.octave.feval("ajustar_cmy", entrada, saida, float(delta_c), float(delta_m), float(delta_y), nout=0)
        p.atualizar_display(saida)
    except Exception as e:
        print("Erro ao aplicar ajuste de canais:", e)

def aplicar_sepia(p, gh):
    """
    Aplica filtro sépia clássico.
    """
    if not hasattr(p, "imagem_atual_path"):
        print("Nenhuma imagem carregada.")
        return

    entrada = p.imagem_atual_path
    saida = p.imagem_atual_path

    try:
        gh.carrega_historico(entrada)
        p.octave.feval("sepia", entrada, saida, nout=0)
        p.atualizar_display(saida)
    except Exception as e:
        print("Erro ao aplicar sépia:", e)

def aplicar_escala_cinza(p, gh, metodo: str = "ponderada"):

    if not hasattr(p, "imagem_atual_path"):
        print("Nenhuma imagem carregada.")
        return

    entrada = p.imagem_atual_path
    saida = p.imagem_atual_path

    try:
        gh.carrega_historico(entrada)

        if metodo == "simples":
            p.octave.feval("escala_cinza_simples", entrada, saida, nout=0)
        else:
            p.octave.feval("escala_cinza_ponderada", entrada, saida, nout=0)

        p.atualizar_display(saida)
    except Exception as e:
        print("Erro ao aplicar escala de cinza:", e)

def calcular_dft(p, gh):
    """
    Calcula DFT da imagem atual, salva espectro (imagem) e arquivo .mat com o espectro deslocado.
    Em seguida abre a janela de edição do espectro.
    """
    if not hasattr(p, "imagem_atual_path"):
        print("Nenhuma imagem carregada.")
        return

    entrada = p.imagem_atual_path
    base = os.path.splitext(os.path.basename(entrada))[0]
    mag_saida = f"{base}_spectrum.png"
    spec_mat = f"{base}_spectrum.mat"

    try:
        # chama fft2d_save(entrada, mag_saida, spec_mat)
        p.octave.feval("fft2d_save", entrada, mag_saida, spec_mat, nout=0)
        # abrir janela de edição do espectro (import aqui para evitar import circular)
        from janelas import abrir_janela_dft
        abrir_janela_dft(p, gh, mag_saida, spec_mat, parent=p)
    except Exception as e:
        print("Erro ao calcular DFT:", e)

def aplicar_ifft_com_mascara(p, gh, spec_mat, mask_path):
    """
    Aplica máscara (imagem) no espectro salvo e reconstrói a imagem.
    """
    if not hasattr(p, "imagem_atual_path"):
        print("Nenhuma imagem carregada.")
        return

    entrada = p.imagem_atual_path
    saida = p.imagem_atual_path

    try:
        gh.carrega_historico(entrada)
        p.octave.feval("apply_mask_and_ifft", spec_mat, mask_path, saida, nout=0)
        p.atualizar_display(saida)
    except Exception as e:
        print("Erro ao aplicar IFFT com máscara:", e)

def aplicar_ifft_sem_mascara(p, gh, spec_mat):
    """
    Reconstrói a imagem a partir do espectro salvo sem aplicar máscara.
    """
    if not hasattr(p, "imagem_atual_path"):
        print("Nenhuma imagem carregada.")
        return

    entrada = p.imagem_atual_path
    saida = p.imagem_atual_path

    try:
        gh.carrega_historico(entrada)
        p.octave.feval("ifft2d_from_saved", spec_mat, saida, nout=0)
        p.atualizar_display(saida)
    except Exception as e:
        print("Erro ao aplicar IFFT sem máscara:", e)

