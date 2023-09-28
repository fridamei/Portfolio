toGcode();

function toGcode()

%{
The start and end parts of the template must be saved in path folder and
called header.gcode and footer.gcode respectively
%}

boxXlength = 10;
boxYlength = 10;
boxZheight = 10;
fillPercent = 0.7;
fileName = 'sylinder.gcode';

% 0.3 seems like an appropriate value based on testing 
layerHeight = 0.3;

voxDim = layerHeight/fillPercent;

eRate = 0.033; % extrusion per mm 

% Calculate number of layers needed to get given height (layer height is
% defined by printer, not number of voxels in vG)
heightRatio = round(voxDim/layerHeight);
adjustedHeight = boxZheight*heightRatio;

% MAKE VOXEL BODY USING GENLIB
%vG = voxBox(boxXlength, boxYlength, adjustedHeight, 'voxSize', voxDim);
vG = voxRod(boxXlength/2, adjustedHeight, 'voxSize', voxDim);
%vG = voxSphere(adjustedHeight, 'voxSize', voxDim);
%vG = voxCone(boxXlength, boxYlength, adjustedHeight, 'voxSize', voxDim);

%{
% For visualizing the figure
fig1; 
plotVg(vG, 'dark');
plotVgBoundingBox(vG, 'txt', 'dark');
%}

% Create file and write the given header to it
fid = fopen(fileName, 'w', 'n','UTF-8');
fwrite(fid, fileread('header.gcode'));

% Start coordinates(center of plate is center of figure, these are in lower
% left corner of model)
startX = 117.5 - (size(vG, 1)/2)*voxDim;
startY = 117.5 - (size(vG, 2)/2)*voxDim;
startZ = layerHeight;

x = startX;
y = startY;
z = startZ;

% Extrusion Value
eTotal = 0; % Cumulated extruted filament

% Defines direction of single line along x-/y-axis
lineDirection = 1; % Defines if the line is printed from left to right/bottom to top or vice versa

g0_start = ['G0 F6000 X' num2str(startX) ' Y' num2str(startY) ' Z' num2str(startZ)];
fprintf(fid, '%s\n', g0_start);

% For every layer (third dimension of vG matrix):
nLayers = size(vG, 3);
for i = 1:nLayers
   
    % Change layer direction (want to print in alternating directions for
    % strength):
    horizontalLayer = mod(i, 2); % 1 gives a horizontal layer
    verticalLayer = 1 - horizontalLayer; % 1 gives a vertical layer
    
    % Reset x and y for every layer
    y = startY;
    x = startX;
   
    % Move nozzle to start y and new z for every new layer
    g0_layer = [';LAYER:' num2str(i) newline ';TYPE:SKIN' newline 'G0 F6000 X' num2str(x) ' Y' num2str(y) ' Z' num2str(z)];
    fprintf(fid, '%s\n', g0_layer);    
    
    % Find number of lines to print for current layer (depends on
    % dimensions and if it should be printed horizontally or vertically)
    nLines = size(vG, 2) * horizontalLayer + size(vG, 1) * verticalLayer;
    
    % For every line
    for j = 1:nLines

        if horizontalLayer
            [xFirst, ~]  = find(vG(:,j,i), 1);
            [xLast, ~]  = find(vG(:,j,i), 1, 'last');
            
            if isempty(xFirst) || isempty(xLast)
                continue
            end 
            
            % Number of voxels times their length
            xDist = (xLast - xFirst) * voxDim;
            yDist = 0;

            x = startX +((xLast-1) * voxDim *(lineDirection==-1)) + ((xFirst-1) * voxDim * (lineDirection==1));
            g0_toFirst = ['G0 F6000 X' num2str(x)];
        end 
        
        if verticalLayer
            [~, yFirst]  = find(vG(j,:,i), 1);
            [~, yLast]  = find(vG(j,:,i), 1, 'last');
            
            if isempty(yFirst) || isempty(yLast)
                continue
            end 
            yDist = (yLast - yFirst) * voxDim;
            xDist = 0;
            
            y = startY +((yLast-1)* voxDim *(lineDirection==-1)) + ((yFirst-1) * voxDim * (lineDirection==1));
            g0_toFirst = ['G0 F6000 Y' num2str(y)];
        end
        
        % Update E-value
        eTotal = eTotal + (eRate * xDist * horizontalLayer) + (eRate * yDist * verticalLayer);
        
        % G1 command string
        x = x + (xDist * lineDirection);
        y = y + (yDist * lineDirection);
        g1_out = ['G1 F600 X' num2str(x) ' Y' num2str(y) ' E' num2str(eTotal)];
        
        % G0 command string
        x = x + (voxDim * verticalLayer);
        y = y + (voxDim * horizontalLayer);
        g0_out = ['G0 F6000 X' num2str(x) ' Y' num2str(y)];
        
        % Add commands to file
        fprintf(fid, '%s\n',g0_toFirst, g1_out, g0_out); 
        
        % Change line direction
        lineDirection = lineDirection*-1; 
    end
    
    % Increment z to make next layer
    z = z + layerHeight;
    
end % End for layer

% Update footer script with correct E-value
changeFooter(eTotal);

% Add the footer to the current file and close it 
fwrite(fid, fileread('footer.gcode'));
fclose(fid);
end

function changeFooter(last_e)
%{
Change the footer file to include correct pull back length of filament
%}

pullBackLength = 5; % in mm, the given template uses 5
e = last_e - pullBackLength;

if e < 0
    e = 0;
end

eStr = ['E' num2str(e)];

% Regex to change the original value to new value. 
lines = readlines('footer.gcode');
lines{5} = regexprep(lines{5}, 'E\d+\.\d+', eStr); % Change current E-value from footer to new E-value

% Open new file
[fid, msg] = fopen('footer.gcode', 'w');

if fid < 1; 
    error('could not write output file because "%s"', msg);
end

fwrite(fid, strjoin(lines, '\n'));

fclose(fid);
end