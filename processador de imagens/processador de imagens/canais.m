function [tipo, c, r, g, b, i] = canais(entrada)

  img = imread(entrada);

  tipo = '';
  c = [];
  r = [];
  g = [];
  b = [];
  i = [];

  if ndims(img) == 2
    tipo = 'gray';
    c = img(:);
    return;
  endif

  if ndims(img) >= 3 && size(img,3) >= 3
    tipo = 'rgb';
    r = img(:,:,1)(:);
    g = img(:,:,2)(:);
    b = img(:,:,3)(:);

    img = double(img) / 255;
    imgh = rgb2hsi(img);
    I = imgh(:,:,3);
    I = round(I * 255);
    i = double(I(:));
    return;
  endif

  error('Formato de imagem não suportado.');
endfunction
