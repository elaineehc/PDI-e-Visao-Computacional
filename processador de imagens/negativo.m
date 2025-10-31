function negativo(caminho_entrada, caminho_saida)

  img = imread(caminho_entrada);
  
  imgn = 255 - img;

  imwrite(imgn, caminho_saida);

endfunction