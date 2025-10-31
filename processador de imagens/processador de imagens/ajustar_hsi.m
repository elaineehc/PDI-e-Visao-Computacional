function ajustar_hsi(entrada, saida, delta_h, scale_s, delta_i)

  img = imread(entrada);

  if ndims(img) == 2 || size(img,3) == 1
    img = cat(3, img, img, img);
  endif

  img_norm = double(img) / 255;
  hsi = rgb2hsi(img_norm);  

  H = hsi(:,:,1);
  S = hsi(:,:,2);
  I = hsi(:,:,3);

  H = mod(H + delta_h, 1);                
  S = min(max(S .* scale_s, 0), 1);       
  I = min(max(I + delta_i, 0), 1);        

  hsi_adj = cat(3, H, S, I);
  rgb_adj = hsi2rgb(hsi_adj);            
  rgb_out = uint8(round(min(max(rgb_adj, 0), 1) * 255));

  imwrite(rgb_out, saida);
endfunction
