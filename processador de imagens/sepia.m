% sepia.m
% sepia(entrada, saida)
% Aplica filtro sépia clássico (matriz) e salva

function sepia(entrada, saida)
  img = imread(entrada);

  % garantir 3 canais
  if ndims(img) == 2 || size(img,3) == 1
    img = cat(3, img, img, img);
  endif

  img_n = double(img) / 255;

  % matriz clássica de sépia aplicada em RGB normalizado
  T = [0.393, 0.769, 0.189;
       0.349, 0.686, 0.168;
       0.272, 0.534, 0.131];

  R = img_n(:,:,1);
  G = img_n(:,:,2);
  B = img_n(:,:,3);

  R2 = T(1,1).*R + T(1,2).*G + T(1,3).*B;
  G2 = T(2,1).*R + T(2,2).*G + T(2,3).*B;
  B2 = T(3,1).*R + T(3,2).*G + T(3,3).*B;

  out = cat(3, R2, G2, B2);
  out = min(max(out, 0), 1);

  imwrite(uint8(round(out * 255)), saida);
endfunction
