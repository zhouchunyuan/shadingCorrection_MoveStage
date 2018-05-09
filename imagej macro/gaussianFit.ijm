/*****************************
* reads the "shadingSample.txt"
* and fits it to gaussian
******************************/
str = getDataString();
size = countLine(str);
X = newArray(size);
Y = newArray(size);
Z = newArray(size);
pxy = newArray(size);//calculated parameter

/******** to get arrays **************/
start=0;end=0;
for(i=0;i<size;i++){
	end = indexOf(str,"\n",start);
	line = substring(str,start,end-1);
	start = end+1;
	
	firstComma = indexOf(line,",");
	secondComma = indexOf(line,",",firstComma+1);
	X[i]= parseFloat(substring(line,0,firstComma));
	Y[i]= parseFloat(substring(line,firstComma+1,secondComma));
	Z[i]= parseFloat(substring(line,secondComma+1,lengthOf(line)));
}

/******** to calculate center **************/
centerx=0;centery=0;
for(i=0;i<size;i++){
	centerx +=X[i]*Z[i];
	centery +=Y[i]*Z[i];
	sum +=Z[i];
}
centerx = centerx/sum;
centery = centery/sum;

/******** to calculate params **************/
for(i=0;i<size;i++){
	pxy[i]=sqrt((X[i]-centerx)*(X[i]-centerx)+(Y[i]-centery)*(Y[i]-centery));
}

equation = "y = a*exp(-x*x/(2*b*b))";
Fit.doFit(equation,pxy,Z);
Fit.plot;

amp = Fit.p(0);
sigma = Fit.p(1);

picSize = 512;
newImage("Untitled", "8-bit black", picSize , picSize , 1);

for(j=0.0;j<picSize ;j++){
	for(i=0.0;i<picSize ;i++){
	x = i/picSize - centerx;
	y = j/picSize - centery;
	pixelValue = amp*exp(-(x*x+y*y)/(2*sigma*sigma));
	putPixel(i,j,pixelValue);
	
	}
}



/**********functions******************/ 
/****************************/
function getDataString(){
	unistr = File.openAsRawString("");
	str="";
	for(i=0;i<lengthOf(unistr);i++){
		code = charCodeAt(unistr,i);
		if(code!=0)str+=fromCharCode(code);
	}
	return str;
}

/***************************/
function countLine(str){
	number = 0;
	start = 0;
	end =0;
	
	do{
		end = indexOf(str,"\n",start);
		start = end+1;
		number++;
	}while(start < lengthOf(str))
	if(end==-1)number--;
	return number;
}
