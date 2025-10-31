function normalizar(caminho_entrada, caminho_saida)
  fprintf("Normalizando imagem: %s\n", caminho_entrada);

  img = imread(caminho_entrada);
  fprintf("Antes: class=%s, min=%.2f, max=%.2f\n", class(img), double(min(img(:))), double(max(img(:))));

  % Converte para double (temporariamente) para normalização
  img = double(img);

  % Normaliza de acordo com o máximo detectado
  max_val = max(img(:));

  if max_val <= 1
    % Imagem entre [0, 1]
    img = uint8(img * 255);
  elseif max_val <= 255
    % Já está no intervalo certo
    img = uint8(img);
  elseif max_val <= 65535
    % Imagem de 16 bits
    img = uint8(img / 65535 * 255);
  else
    % Caso extremo
    img = uint8((img - min(img(:))) / (max(img(:)) - min(img(:))) * 255);
  endif

  fprintf("Depois: class=%s, min=%d, max=%d\n", class(img), min(img(:)), max(img(:)));

  imwrite(img, caminho_saida);
  fprintf("Imagem normalizada salva em %s\n", caminho_saida);
endfunction
