function imghsi = rgb2hsi(img)

  if isa(img, 'uint8')
    img = double(img)/255;
  endif

  R = img(:,:,1);
  G = img(:,:,2);
  B = img(:,:,3);

  u1 = 0.5.*((R-G) + (R-B));
  u2 = sqrt((R-G).^2 + (R-B).*(G-B));

  u2 = u2 + eps; %eps eh um valor muito pequeno

  cos = u1./u2;
  cos = max(min(cos, 1), -1);
  ang = acos(cos);

  H = ang;
  h = (B > G);
  H(h) = 2*pi - ang(h);

  H = mod(H, 2*pi)/(2*pi);

  soma = R+G+B;
  I = soma/3;

  rgb_min = min(cat(3, R, G, B), [], 3);
  S = zeros(size(I));
  s = (soma > 0);
  S(s) = 1 - ((3.*rgb_min(s))./soma(s));
  S = min(max(S, 0), 1);

  H = min(max(H, 0), 1);
  I = min(max(I, 0), 1);

  imghsi = cat(3, H, S, I);
endfunction
