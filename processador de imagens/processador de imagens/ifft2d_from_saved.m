function ifft2d_from_saved(spec_mat, saida)
  s = load(spec_mat);
  if ~isfield(s, 'Fshift')
    error('Arquivo .mat não contém Fshift.');
  endif
  Fshift = s.Fshift;
  F = ifftshift(Fshift);
  img_rec = real(ifft2(F));
  img_rec = round(img_rec);
  img_rec = min(max(img_rec, 0), 255);
  img_out = uint8(img_rec);
  imwrite(img_out, saida);
endfunction
