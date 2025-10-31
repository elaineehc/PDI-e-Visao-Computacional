function fft2d_save(entrada, mag_saida, spec_mat)
  img = imread(entrada);

  % converter para grayscale se necessário (luminosidade)
  if ndims(img) >= 3 && size(img,3) >= 3
    R = double(img(:,:,1));
    G = double(img(:,:,2));
    B = double(img(:,:,3));
    img_gray = 0.2989 .* R + 0.5870 .* G + 0.1140 .* B;
  else
    img_gray = double(img);
  endif

  % guardar info original
  rows = size(img_gray,1);
  cols = size(img_gray,2);
  orig_min = min(img_gray(:));
  orig_max = max(img_gray(:));

  % calcular fft2 e deslocar
  F = fft2(img_gray);
  Fshift = fftshift(F);

  % magnitude log-scaled para visualização
  mag = log(1 + abs(Fshift));

  mn = min(mag(:));
  mx = max(mag(:));
  if mx > mn
    mag_norm = (mag - mn) / (mx - mn);
  else
    mag_norm = zeros(size(mag));
  endif

  mag_uint8 = uint8(round(mag_norm * 255));
  imwrite(mag_uint8, mag_saida);

  % salvar espectro e metadados em .mat (complexo OK)
  save(spec_mat, 'Fshift', 'rows', 'cols', 'orig_min', 'orig_max');
endfunction
