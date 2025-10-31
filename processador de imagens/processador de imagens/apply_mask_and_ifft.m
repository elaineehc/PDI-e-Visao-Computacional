function apply_mask_and_ifft(spec_mat, mask_path, saida)
  % carregar espectro salvo
  s = load(spec_mat);
  if ~isfield(s, 'Fshift')
    error('Arquivo .mat não contém Fshift.');
  endif
  Fshift = s.Fshift;
  rows = s.rows;
  cols = s.cols;

  % carregar máscara
  mask_img = imread(mask_path);
  % converter para grayscale se necessário
  if ndims(mask_img) >= 3 && size(mask_img,3) >= 3
    mask_gray = double(mask_img(:,:,1)); % basta um canal
  else
    mask_gray = double(mask_img);
  endif

  % ajustar tamanho da máscara se necessário (nearest neighbor)
  [mr, mc] = size(mask_gray);
  if mr ~= rows || mc ~= cols
    % redimensionar (usa imresize se disponível); fallback simples: replicar/recortar
    try
      mask_resized = imresize(mask_gray, [rows, cols], 'nearest');
    catch
      % fallback: crop/zero-pad
      mask_resized = zeros(rows, cols);
      rr = min(rows, mr);
      cc = min(cols, mc);
      mask_resized(1:rr, 1:cc) = mask_gray(1:rr, 1:cc);
    end_try_catch
  else
    mask_resized = mask_gray;
  endif

  % gerar máscara binária: pixels > 0 -> 1, else 0
  mask_bin = double(mask_resized > 0);

  % aplicar máscara no espectro deslocado
  Fshift_masked = Fshift .* mask_bin;

  % voltar para posição original e reconstruir
  F = ifftshift(Fshift_masked);
  img_rec = real(ifft2(F));

  % normalizar / ajustar escala: arredondar e truncar para 0..255
  img_rec = round(img_rec);
  img_rec = min(max(img_rec, 0), 255);
  img_out = uint8(img_rec);

  imwrite(img_out, saida);
endfunction
