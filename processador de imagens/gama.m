function gama(caminho_entrada, caminho_saida, gama)

  img = imread(caminho_entrada);

  img = double(img)/255;
  imgg = img.^gama;

  imgg = uint8(round(imgg.*255));

  imwrite(imgg, caminho_saida);