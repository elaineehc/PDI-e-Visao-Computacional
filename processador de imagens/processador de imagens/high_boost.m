function high_boost(entrada, saida, filtro)
  pkg load image;

  img = imread(entrada);
  img = double(img)/255;

  [altura, largura, cor] = size(img);

  imgb = zeros(altura, largura, cor);

  [m, n] = size(filtro);

  a = (m-1)/2;
  b = (n-1)/2;

  img2 = padarray(img, [a, b]);

  for c = 1:cor
   for x = 1:altura

    xarr = x : x+m-1;

    for y = 1:largura

      yarr = y : y+n-1;

      janela = img2(xarr, yarr,c);
      imgb(x, y, c) = sum(sum(janela.*filtro));

    endfor
   endfor
  endfor

  mask = img - imgb;
  imgh = img + mask;

  imgh = uint8(imgh*255);
  imwrite(imgh, saida);
  return;
