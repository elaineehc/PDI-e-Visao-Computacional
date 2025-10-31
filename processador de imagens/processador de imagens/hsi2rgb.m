function rgb = hsi2rgb(hsi)

  H = double(hsi(:,:,1));
  S = double(hsi(:,:,2));
  I = double(hsi(:,:,3));

  H = H*2*pi;

  S = min(max(S,0),1);
  I = min(max(I,0),1);
  H = mod(H, 2*pi);

  [m,n] = size(H);
  R = zeros(m,n);
  G = zeros(m,n);
  B = zeros(m,n);

  caso1 = (H >= 0) & (H < 2*pi/3);
  caso2 = (H >= 2*pi/3) & (H < 4*pi/3);
  caso3 = (H >= 4*pi/3) & (H < 2*pi);

  if any(caso1(:))
    h1 = H(caso1);
    s1 = S(caso1);
    i1 = I(caso1);
    B(caso1) = i1.*(1 - s1);
    x = cos(pi/3 - h1) + eps; % eps eh um numero muito pequeno
    R(caso1) = i1.*(1 + ((s1.*cos(h1))./x));
    G(caso1) = 3.*i1 - (R(caso1) + B(caso1));
  endif

  if any(caso2(:))
    h2 = H(caso2) - 2*pi/3;
    s2 = S(caso2);
    i2 = I(caso2);
    R(caso2) = i2.*(1 - s2);
    x = cos(pi/3 - h2) + eps;
    G(caso2) = i2.*(1 + ((s2.*cos(h2))./x));
    B(caso2) = 3.*i2 - (R(caso2) + G(caso2));
  endif

  if any(caso3(:))
    h3 = H(caso3) - 4*pi/3;
    s3 = S(caso3);
    i3 = I(caso3);
    G(caso3) = i3 .* (1 - s3);
    x = cos(pi/3 - h3) + eps;
    B(caso3) = i3.*(1 + ((s3.*cos(h3))./x));
    R(caso3) = 3.*i3 - (G(caso3) + B(caso3));
  endif

  rgb = cat(3, R, G, B);
  rgb = min(max(rgb, 0), 1);

endfunction
