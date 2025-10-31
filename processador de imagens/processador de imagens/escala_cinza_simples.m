function escala_cinza_simples(caminho_entrada, caminho_saida)

  img = imread(caminho_entrada);

  if ndims(img) == 3
    r = double(img(:,:,1));
    g = double(img(:,:,2));
    b = double(img(:,:,3));
    gray = (r + g + b) / 3.0;
  else
    gray = double(img);
  end

  if max(gray(:)) <= 1
    gray = gray * 255;
  end

  gray = uint8(round(gray));

  imwrite(gray, caminho_saida);

endfunction
