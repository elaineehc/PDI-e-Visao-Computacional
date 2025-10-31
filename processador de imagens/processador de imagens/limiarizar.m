function limiarizar(entrada, saida, x)

  img = imread(entrada);

  altura = size(img)(1);
  largura = size(img)(2);

  imglim = uint8(zeros(altura, largura));

  for i = 1:altura
    for j = 1:largura
      if img(i, j) < x
        imglim(i, j) = 0;
      else
        imglim(i, j) = 255;
      endif
    endfor
  endfor

  imwrite(imglim, saida);