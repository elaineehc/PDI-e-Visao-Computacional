function filtro(entrada, saida, filtro)
  pkg load image;

  img = imread(entrada);
  img = double(img)/255;

  imgf = conv2(img, filtro);

  imgf = uint8(imgf*255);
  imwrite(imgf, saida);
  return;
