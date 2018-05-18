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



picSize = 512;
newImage("Untitled", "16-bit black", picSize , picSize , 1);
brghtness = 0;
for(j=0.0;j<picSize ;j++){
	for(i=0.0;i<picSize ;i++){
		x =i/picSize;y=j/picSize;
		d2min = 2.0;//max distance is sqrt(2)
		
		for(k=0;k<lengthOf(Z);k++){
			d2 = (x-X[k])*(x-X[k])+(y-Y[k])*(y-Y[k]);
			if( d2 < d2min ){
				d2min=d2;
				brightness = Z[k];	
			}
			
		}

		putPixel(i,j,brightness );
	
	}
showProgress(j, picSize );
run("Enhance Contrast", "saturated=0.35");
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
