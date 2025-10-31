function ajustar_cmy(entrada, saida, delta_c, delta_m, delta_y)

  img = imread(entrada);

  if ndims(img) == 2 || size(img,3) == 1
    img = cat(3, img, img, img);
  endif

  img_n = double(img) / 255;

  R = img_n(:,:,1);
  G = img_n(:,:,2);
  B = img_n(:,:,3);

  C = 1 - R;
  M = 1 - G;
  Y = 1 - B;

  C = min(max(C + delta_c, 0), 1);
  M = min(max(M + delta_m, 0), 1);
  Y = min(max(Y + delta_y, 0), 1);

  R2 = 1 - C;
  G2 = 1 - M;
  B2 = 1 - Y;

  rgb_out = cat(3, R2, G2, B2);
  rgb_out = min(max(rgb_out, 0), 1);

  imwrite(uint8(round(rgb_out * 255)), saida);
endfunction
