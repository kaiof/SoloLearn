// script locations are only to balance editor lag

function getInnerCoincidences(s) {
  original = s.toLowerCase().replace(/[^a-z]/g, '').split(''); // extract only [a-z]
  var sBot, sXOR;
  var coincArr = new Array();
  coincArr[0] = 0; // throw out 0 shift

  for(ofs=1; ofs<=original.length/2; ofs++) {
    sBot = original.slice(-ofs).concat(original.slice(0, -ofs));
   
    sXOR = '';
    for(i=0; i<original.length; i++) {
      sXOR += String.fromCharCode(original[i].charCodeAt(0) ^ sBot[i].charCodeAt(0));
    }
    coincArr[ofs] = sXOR.split("\0").length;
  }
  return coincArr; 
}

function standardDeviation(values) {
  var avg = average(values);
  
  var squareDiffs = values.map(function(value) {
    var diff = value - avg;
    var sqrDiff = diff * diff;
    return sqrDiff;
  });
  
  var avgSquareDiff = average(squareDiffs);

  var stdDev = Math.sqrt(avgSquareDiff);
  return stdDev;
}

function average(data){
  var sum = data.reduce(function(sum, value){
    return sum + value;
  }, 0);

  var avg = sum / data.length;
  return avg;
}

var keylen;
var offsets = new Array();

function getBestOffset(i) {
  var bestOffset = 0;
  var bestSoFar=0.0;
  var check, stopOfs, ofs;
  var t_ratios;
  stopOfs=col_ratios[i].length;
  for(ofs=0;ofs<stopOfs;ofs++){
    t_ratios = col_ratios[i].slice(ofs).concat(col_ratios[i].slice(0, ofs));
    
    check=0;
    for(j=0;j<t_ratios.length;j++){
        check+=(t_ratios[j]*std_occs[j]);
    }
    if(check > bestSoFar) { // TODO: Ties?
      bestOffset=ofs;
      bestSoFar=check;
    }
  }
  return bestOffset;
}

function guess() {
  var col;
  std_occs=getOccurs("a:z");
  getCols();
  getRatios();
  var k = "";
  for(var i=0; i<keylen; i++){
    k += String.fromCharCode(getBestOffset(i)+97);
  }
  return k;
}

function tryOut(k){
   var c, cc, st, kArr;
   var kArrNums=new Array();
   var outArr=new Array();
   st=sampleText.toLowerCase().split("");
   kArr=k.split("");
   for(i=0;i<kArr.length;i++){
     kArrNums[i]=kArr[i].charCodeAt(0)-97;  
   }
   klen=k.length; // bugfix
   ii=0; ki=0;
   for(i=0;i<st.length;i++){
     c=st[i].charCodeAt(0);
     if(c<65 || (c>90 && c<97) || c>122){
         outArr.push(String.fromCharCode(c));
         continue;
     }
     cc=((c-97)-(kArrNums[ii%klen])); // bugfix
     if(cc<0) cc+=26;
     
     outArr.push(String.fromCharCode(cc+97));
     ii +=1;
   }
  
   return outArr.join("");
}

function doChart() {
  $.jqplot.config.enablePlugins = true;
  var s1 = coincidences;
  var ticks = new Array();
  for (var i=1; i<=(s1.length/100)+2; i++) {
    ticks.push((i-1)*100);
  }

  var _hiliteB=parseFloat(_avg)-parseFloat(_stddev);

  bdat = [ [[0,_hiliteB],[s1.length-1,_hiliteB]], [[0,_hiliteT],[s1.length-1,_hiliteT]] ];
  dat = [ [0,_avg], [s1.length-1,_avg] ];
  myTheme = {
    grid: {
      drawBorder: false,
      shadow: false,
      background: 'rgba(255, 255, 255, 0.0)'
    },
    seriesDefaults: {
      shadow: false,
      showMarker: false
    },
    axes: {
      xaxis: {
        pad: 1.0,
        tickOptions: {showGridline: false}
      },
      yaxis: {pad: 1.05}
    }
  };
 
  plot1 = $.jqplot('chart1', [s1.slice(1), dat], $.extend(true, {}, myTheme, {
    animate: !$.jqplot.use_excanvas, // Only animate if we're not using excanvas (not in IE 7 or IE 8)..
    series: [{
      renderer:$.jqplot.BarRenderer,
      pointLabels: { show: false },
      showMarker: false,
    },{
      rendererOptions: {
        bandData: bdat,
        smooth: false,
        bands: { show: true },
      },
    }],
    axes: {
      xaxis: {
        renderer: $.jqplot.CategoryAxisRenderer,
        ticks: ticks, // omg slow if too many
      },
    },
    highlighter: { show: true },
    }
  ));
   
  $('#chart1').bind('jqplotDataClick', 
    function (ev, seriesIndex, pointIndex, data) {
      $('#info1').html('series: '+seriesIndex+', point: '+pointIndex+', data: '+data);
    }
  );
}