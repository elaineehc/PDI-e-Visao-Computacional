function bordas(entrada, saida)

  img = imread(entrada);
  img = double(img)/255;

  if ndims(img)==3
    img = rgb2gray(img);
  end

  [h, w] = size(img);

  Gx = [-1 0 1; -2 0 2; -1 0 1];
  Gy = Gx';

  gx = conv2(img, Gx, 'same');
  gy = conv2(img, Gy, 'same');

  imgb = sqrt(gx.^2 + gy.^2);

  imgb = uint8(imgb*255);
  imwrite(imgb, saida);

