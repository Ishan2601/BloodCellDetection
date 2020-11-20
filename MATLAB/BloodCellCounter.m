%{
Author: Ishan Vatsaraj
%}

%% Read and show original Image

img = imread('bloodcell.jpg');
figure;
subplot(4,2,1);
imshow(img);

%% Convert to grayscale and show Image

gray_image = rgb2gray(img);
subplot(4,2,2);
imshow(gray_image)

%% Separate the channels (RGB) and display Red and Blue channel

red = img(:,:,1);
subplot(4,2,3);
imshow(red);

subplot(4,2,4);
blue = img(:,:,3);
imshow(blue);

%% Segment WBC Nucleas from RED channel

[w,h]=size(red);
for i=1:w
   for j=1:h
      if red(i,j)<140
          red(i,j)=255;
      end
   end
end

w_nuc = imbinarize(red);
subplot(4,2,5);
imshow(w_nuc);

%% Segment RBC from BLUE channel

[w,h]=size(blue);
for i=1:w
   for j=1:h
      if blue(i,j)>175
          blue(i,j)=255;
      end
   end
end

rbc = imbinarize(blue);
subplot(4,2,6);
imshow(rbc);

%% Add both Images and Invert the output
% Adding both images will remove the WBC nucleus from the image.
% This will improve the detection and will reduce the misidentification
rbc_clean = w_nuc + rbc;
subplot(4,2,7);
imshow(rbc_clean);

inv_rbc_clean = ~rbc_clean;
subplot(4,2,8);
imshow(inv_rbc_clean);

%% Count the circles in the image and Highlight them
figure;
imshow(img);
[centers, radii, metric] = imfindcircles(inv_rbc_clean,[7 10],'ObjectPolarity','bright','Sensitivity',0.95,'Method','twostage');
h = viscircles(centers,radii);

[m,n]=size(centers);
disp(m); %RBC COUNT