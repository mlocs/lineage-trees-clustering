% This file is part of the Lineage Tree Clustering. 
% Copyright (C) 2014 
% Author: Michael Schwarzfischer
% 
% Lineage Tree Clustering is free software: you can redistribute it and/or modify
% it under the terms of the GNU General Public License as published by
% the Free Software Foundation, either version 3 of the License, or
% (at your option) any later version.
%
% Lineage Tree Clustering is distributed in the hope that it will be useful,
% but WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
% GNU General Public License for more details.
%
% You should have received a copy of the GNU General Public License
% along with the Lineage Tree Clustering project files.  If not, see <http://www.gnu.org/licenses/>.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clear all
distance = importdata('distance.m4.out');

classes=importdata('assignments.m4.k2.out');
centroids=importdata('centroids.m4.k2.out')+1;

% classes=importdata('assignments.m1.k1.out');
% centroids=importdata('centroids.m1.k1.out')+1;
figure;
imagesc(distance)


%% pca

[pc, score, latent] = princomp((distance));
% [pc, score, latent] = pcacov((distance));

% cumsum(latent)./sum(latent)
uniclasses = unique(classes);

figure;
hold all
plot(score(classes == uniclasses(1),1),score(classes == uniclasses(1),2),'.r')
% plot(score(classes == uniclasses(2),1),score(classes == uniclasses(2),2),'.b')
plot(score(centroids(1),1),score(centroids(1),2),'or')
% plot(score(centroids(2),1),score(centroids(2),2),'ob')
% plot3(score(:,1),score(:,2),range1,'.')
% plot3(score(range2,1),score(range2,2),range2,'.r')
% legend('WT','PuGata')
xlabel('PC1')
ylabel('PC2')
%% mds
uniclasses = unique(classes);

Y=mdscale(distance,2,'criterion','sstress');
figure
hold on
plot(Y(classes == uniclasses(1),1),Y(classes == uniclasses(1),2),'.r')
plot(Y(classes == uniclasses(2),1),Y(classes == uniclasses(2),2),'.b')
plot(Y(centroids(1),1),Y(centroids(1),2),'or')
plot(Y(centroids(2),1),Y(centroids(2),2),'ob')

%% isomap
uniclasses = unique(classes);


figure;
hold on
plot3(Y.coords{1}(1,classes == uniclasses(1)),Y.coords{1}(2,classes == uniclasses(1)),find(classes == uniclasses(1)),'.r')
plot3(Y.coords{1}(1,classes == uniclasses(2)),Y.coords{1}(2,classes == uniclasses(2)),find(classes == uniclasses(2)),'.b')
plot(Y.coords{1}(1,centroids(1)),Y.coords{1}(2,centroids(1)),'or')
plot(Y.coords{1}(1,centroids(2)),Y.coords{1}(2,centroids(2)),'ob')

mop=99;
plot(Y.coords{1}(1,mop),Y.coords{1}(2,mop),'xk','markersize',20)
