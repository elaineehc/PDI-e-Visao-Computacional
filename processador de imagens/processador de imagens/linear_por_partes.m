function linear_por_partes(entrada, saida, r1, s1, r2, s2)
  img = imread(entrada);

  if ndims(img) == 3
    img = rgb2gray(img);
  endif

  altura = size(img)(1);
  largura = size(img)(2);

  imglp = img;

  for i = 1:altura
    for j = 1:largura

      if img(i, j) <= r1
        imglp(i, j) = (s1/r1)*img(i, j);
      endif

      if img(i, j) > r1 && img(i, j) <= r2
        imglp(i, j) = ((s2-s1)/(r2-r1))*img(i, j);
      endif

      if img(i, j) > r2
        imglp(i, j) = ((255-s2)/(255-r2))*img(i, j);
      endif
    endfor
  endfor

  imwrite(imglp, saida);

