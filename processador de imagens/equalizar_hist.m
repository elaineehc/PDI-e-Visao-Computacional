function equalizar_hist(entrada, saida)

  img = imread(entrada);

  if ndims(img) == 2 || size(img)(3) == 1
    altura = size(img)(1);
    largura = size(img)(2);

    imgeq = zeros(altura, largura);

    mn = largura * altura;
    nk = zeros(1, 256);
    pdf = zeros(1, 256);
    map = zeros(1, 256);

    nk(1) = sum(img(:) == 0) / mn;
    pdf(1) = nk(1);
    map(1) = round(pdf(1) * 255);
    for x = 2:256
      nk(x) = sum(img(:) == x-1) / mn;
      pdf(x) = pdf(x-1) + nk(x);
      map(x) = round(pdf(x) * 255);
      if map(x) > 255
        map(x) = 255;
      endif
    endfor

    for x = 1:altura
      for y = 1:largura
        p = img(x, y);
        imgeq(x, y) = map(p + 1);
      endfor
    endfor

    imgeq = uint8(imgeq);
    imwrite(imgeq, saida);
    return;
  endif


  img = double(img) / 255;
  imgh = rgb2hsi(img);
  H = imgh(:,:,1);
  S = imgh(:,:,2);
  I = imgh(:,:,3);

  I = uint8(round(I * 255));
  altura = size(I, 1);
  largura = size(I, 2);
  mn = largura * altura;

  nk = zeros(1, 256);
  pdf = zeros(1, 256);
  map = zeros(1, 256);

  nk(1) = sum(I(:) == 0) / mn;
  pdf(1) = nk(1);
  map(1) = round(pdf(1) * 255);
  for x = 2:256
    nk(x) = sum(I(:) == x-1) / mn;
    pdf(x) = pdf(x-1) + nk(x);
    map(x) = round(pdf(x) * 255);
    if map(x) > 255
      map(x) = 255;
    endif
  endfor

  I_eq = uint8(map(double(I) + 1));

  I_eq = double(I_eq) / 255;
  imgh_eq = cat(3, H, S, I_eq);

  imgr_eq = hsi2rgb(imgh_eq);
  imgr_eq = uint8(round(min(max(imgr_eq, 0), 1) * 255));

  imwrite(imgr_eq, saida);

endfunction
