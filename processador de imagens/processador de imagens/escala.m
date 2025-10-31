function escala(entrada, saida, sx, sy)

  img = imread(entrada);

  [altura, largura, canais] = size(img);

  img = double(img)/255;
  imgs = zeros(round(altura*sy), round(largura*sx), canais);

  for y = 1:altura*sy
    for x = 1:largura*sx

      divx = x/sx;
      divy = y/sy;
      x1 = floor(divx);
      y1 = floor(divy);

      x1 = max(1, x1);
      y1 = max(1, y1);
      x1 = max(1, min(x1, largura-1));
      y1 = max(1, min(y1, altura-1));

      x2 = x1 + 1;
      y2 = y1 + 1;

      px = divx - x1;
      py = divy - y1;

      i1 = img(y1, x1,:);
      i2 = img(y1, x2,:);
      i3 = img(y2, x1,:);
      i4 = img(y2, x2,:);

      w1 = (1-px)*(1-py);
      w2 = px*(1-py);
      w3 = (1-px)*py;
      w4 = px*py;

      u = w1.*i1 + w2.*i2 + w3.*i3 + w4.*i4;
      imgs(y, x,:) = u;


    endfor
  endfor

  imgs = uint8(imgs*255);
  imwrite(imgs, saida);
