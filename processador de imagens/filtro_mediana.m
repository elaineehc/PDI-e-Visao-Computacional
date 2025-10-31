function filtro_mediana(entrada, saida, tam)
  pkg load image;

  img = imread(entrada);
  img = double(img)/255;

  [altura, largura, cor] = size(img);

  imgf = zeros(altura, largura, cor);

  a = (tam-1)/2;
  b = (tam-1)/2;

  img2 = padarray(img, [a, b]);

  for c = 1:cor
   for x = 1:altura

    xarr = x : x+tam-1;

    for y = 1:largura

      yarr = y : y+tam-1;

      janela = img2(xarr, yarr,c);
      vals = sort(janela(:));
      imgf(x, y, c) = vals(((tam*tam)+1)/2);

    endfor
   endfor
  endfor

  imgf = uint8(imgf*255);
  imwrite(imgf, saida);
  return;
