function rotacao_intb(entrada, saida, a)

  img = imread(entrada);

  a = pi*a/180;

  sina = sin(-a);
  cosa = cos(-a);

  [altura, largura, canais] = size(img);

  p1x = largura*cos(a);
  p1y = largura*sin(a);

  p2x = largura*cos(a) - altura*sin(a);
  p2y = largura*sin(a) + altura*cos(a);

  p3x = - altura*sin(a);
  p3y = altura*cos(a);

  vx = [0 p1x p2x p3x];
  vy = [0 p1y p2y p3y];

  largf = max(vx) - min(vx);
  altf = max(vy) - min(vy);

  dx = min(vx);
  dy = min(vy);

  img = double(img)/255;
  imgr = zeros(round(altf), round(largf), canais);

  for y = 1:round(altf)
    for x = 1:round(largf)

      xo = ((x+dx)*cosa - (y+dy)*sina);
      yo = ((x+dx)*sina + (y+dy)*cosa);

      if xo < 1 || xo > largura || yo < 1 || yo > altura
        imgr(y, x,:) = 0;
      else
        x1 = floor(xo);
        y1 = floor(yo);

        x1 = max(1, x1);
        y1 = max(1, y1);
        x1 = max(1, min(x1, largura-1));
        y1 = max(1, min(y1, altura-1));

        x2 = x1 + 1;
        y2 = y1 + 1;

        pfx = xo - x1;
        pfy = yo - y1;

        for c = 1:canais
          i1 = img(y1, x1, c);
          i2 = img(y1, x2, c);
          i3 = img(y2, x1, c);
          i4 = img(y2, x2, c);
          u1 = (1-pfx)*i1 + pfx*i2;
          u2 = (1-pfx)*i3 + pfx*i4;
          u = (1-pfy)*u1 + pfy*u2;
          imgr(y, x, c) = u;
        endfor


      endif
    endfor
  endfor

  imgr = uint8(imgr*255);
  imwrite(imgr, saida);

end

