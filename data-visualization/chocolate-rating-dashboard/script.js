const C = {
  blue:"#0077BB", cyan:"#33BBEE", teal:"#009988",
  orange:"#EE7733", magenta:"#CC3311", yellow:"#DDCC77",
  grey:"#BBBBBB", textDark:"#1a0f0a", textMid:"#4a3020", textSoft:"#8a7060"
};

const wordColors=[C.blue,C.teal,C.cyan,C.orange,C.magenta];
const CHART_ASPECT=0.62;
const BAR_CHART_ASPECT=0.82;

// Ingredient lookup
const ingredientLookup={
  'B':'Beans','S':'Sugar','S*':'Sweetener',
  'C':'Cocoa Butter','V':'Vanilla','L':'Lecithin','Sa':'Salt'
};

function getFullNames(initials){
  return initials.split(',').map(i=>ingredientLookup[i.trim()]||i.trim()).join(', ');
}

// Tooltip
const tooltip=d3.select("body").append("div").attr("class","tooltip");
function showTip(e,html){tooltip.style("opacity",1).html(html).style("left",(e.clientX+14)+"px").style("top",(e.clientY-44)+"px");}
function hideTip(){tooltip.style("opacity",0);}

// Axis labels
function axisLabel(svg,type,text,W,H,m){
  const fs="14px";
  if(type==="x"){
    svg.append("text").attr("x",(m.left+W-m.right)/2).attr("y",H-8)
      .attr("text-anchor","middle").style("font-size",fs).style("font-weight","600")
      .style("fill",C.textMid).text(text);
  } else {
    svg.append("text").attr("transform","rotate(-90)")
      .attr("x",-(m.top+(H-m.top-m.bottom)/2)).attr("y",20)
      .attr("text-anchor","middle").style("font-size",fs).style("font-weight","600")
      .style("fill",C.textMid).text(text);
  }
}

// Responsive sizing
function getChartSize(id,aspect=CHART_ASPECT){
  const el=document.getElementById(id);
  const W=el?el.clientWidth:640;
  return {W,H:W*aspect};
}

function makeSVG(id,W,H){
  d3.select(`#${id}`).html("");
  return d3.select(`#${id}`).append("svg")
    .attr("width","100%").attr("viewBox",`0 0 ${W} ${H}`)
    .attr("preserveAspectRatio","xMidYMid meet");
}

// Data
let fullData=[],fullExplodedData=[],filteredData=[],filteredExplodedData=[];

Promise.all([
  d3.csv("cleaned_ratings.csv"),
  d3.csv("exploded_ratings.csv")
]).then(([data,exploded])=>{
  data.forEach(d=>{
    d.Rating=+d.Rating; d.CocoaPercent=+d.CocoaPercent;
    d.IngredientCount=+d.IngredientCount; d.Year=+d.Year;
  });
  fullData=data; fullExplodedData=exploded;
  filteredData=data; filteredExplodedData=exploded;
  d3.selectAll(".card-loading").remove();
  setupFilter(); updateAllCharts();

  let t;
  window.addEventListener("resize",()=>{
    clearTimeout(t);
    t=setTimeout(updateAllCharts,200);
  });
});

// Filter
function setupFilter(){
  const order=["Africa","South America","Asia","North America","Europe","Oceania","Other"];
  const continents=order.filter(c=>fullData.some(d=>d.Continent===c));
  const sel=d3.select("#countryFilter");
  sel.selectAll("option:not([value='All'])").remove();
  continents.forEach(c=>sel.append("option").attr("value",c).text(c));
  sel.on("change",function(){
    const v=this.value;
    filteredData=v==="All"?fullData:fullData.filter(d=>d.Continent===v);
    filteredExplodedData=v==="All"?fullExplodedData:fullExplodedData.filter(d=>d.Continent===v);
    updateAllCharts();
  });
}

// Helper: Get best combo name
function getBestComboName(data){
  const comboRollup = d3.rollup(
    data.filter(d=>d.IngredientInitials),
    v => d3.mean(v, d=>d.Rating),
    d=>d.IngredientInitials.trim()
  );
  const best = Array.from(comboRollup).filter(d=>d[1]).sort((a,b)=>b[1]-a[1])[0];
  if(!best) return "-";
  return best[0].split(',').map(i=>ingredientLookup[i.trim()]||i).slice(0,3).join(', ');
}

function updateKPIs(data){
  // 1. Bars
  d3.select("#kpiCount").text(data.length.toLocaleString());

  // 2. Rating
  const avgRating = d3.mean(data, d=>d.Rating);
  d3.select("#kpiRating").text(avgRating ? avgRating.toFixed(2) : "-");

  // 3. Top Bean Origin
  const originRollup = d3.rollup(
    data.filter(d=>d.BeanOrigin && d.Rating),
    v => ({
      rating: d3.mean(v, d=>d.Rating),
      count: v.length
    }),
    d=>d.BeanOrigin
  );
  
  const originArray = Array.from(originRollup, ([origin, val]) => ({
    origin: origin,
    rating: val.rating,
    count: val.count
  }))
  .filter(d=>d.count >= 5)
  .sort((a,b)=>b.rating - a.rating);
  
  const topOrigin = originArray[0];
  
  let originDisplay = "-";
  if (topOrigin) {
    const originLower = topOrigin.origin.toLowerCase().trim();
    if (originLower.includes("blend")) {
      originDisplay = "Mixed Origins";
    } else {
      originDisplay = topOrigin.origin;
    }
  }
  
  d3.select("#kpiOrigin").text(originDisplay);

  // 4. Premium %
  const premiumBars = data.filter(d=>d.Rating > 3.5).length;
  const premiumPercent = (premiumBars / data.length) * 100;
  d3.select("#kpiPremium").text(data.length > 0 ? `${premiumPercent.toFixed(1)}%` : "-");
}


function updateAllCharts(){
  updateKPIs(filteredData);
  drawLineChart(filteredData);
  drawWordCloud(filteredExplodedData);
  drawHeatmap(filteredData);
  drawComboChart(filteredData);
}

function drawLineChart(data){
  const {W,H}=getChartSize("linechart");
  const m={top:54, right:30, bottom:72, left:62};
  const svg=makeSVG("linechart", W, H);

  const avg=Array.from(
    d3.rollup(data,v=>d3.mean(v,d=>d.Rating),d=>d.Year),
    ([Year,Rating])=>({Year,Rating})
  ).sort((a,b)=>a.Year-b.Year);

  if(!avg.length)return;

  const x=d3.scaleLinear().domain(d3.extent(avg,d=>d.Year)).range([m.left, W-m.right]);
  const y=d3.scaleLinear().domain([2.5, 4.1]).range([H-m.bottom, m.top]);

  const defs=svg.append("defs");
  const grad=defs.append("linearGradient").attr("id","lineAreaGrad").attr("x1","0").attr("x2","0").attr("y1","0").attr("y2","1");
  grad.append("stop").attr("offset","0%").attr("stop-color",C.cyan).attr("stop-opacity",0.3);
  grad.append("stop").attr("offset","100%").attr("stop-color",C.cyan).attr("stop-opacity",0);

  svg.append("path").datum(avg)
    .attr("fill","url(#lineAreaGrad)")
    .attr("d",d3.area().x(d=>x(d.Year)).y0(y(2.5)).y1(d=>y(d.Rating)).curve(d3.curveMonotoneX));

  svg.append("path").datum(avg)
    .attr("fill","none").attr("stroke",C.blue).attr("stroke-width",3)
    .attr("d",d3.line().x(d=>x(d.Year)).y(d=>y(d.Rating)).curve(d3.curveMonotoneX));

  svg.selectAll("circle").data(avg).enter().append("circle")
    .attr("cx",d=>x(d.Year)).attr("cy",d=>y(d.Rating)).attr("r",4)
    .attr("fill","#fff").attr("stroke",C.blue).attr("stroke-width",2.5)
    .on("mouseover",(e,d)=>{
      d3.select(e.currentTarget).attr("r",7).attr("fill",C.orange).attr("stroke",C.orange);
      showTip(e,`<strong>${d.Year}</strong><br>Avg Rating: ${d.Rating.toFixed(2)}`);
    })
    .on("mouseout",e=>{
      d3.select(e.currentTarget).attr("r",4).attr("fill","#fff").attr("stroke",C.blue);
      hideTip();
    });

  svg.append("g").attr("transform",`translate(0,${H-m.bottom})`)
    .call(d3.axisBottom(x).tickFormat(d3.format("d")).tickSize(0))
    .call(g=>g.select(".domain").remove())
    .selectAll("text").style("fill",C.textSoft).style("font-size","13px");

  svg.append("g").attr("transform",`translate(${m.left},0)`)
    .call(d3.axisLeft(y).ticks(5).tickSize(0))
    .call(g=>g.select(".domain").remove())
    .selectAll("text").style("fill",C.textSoft).style("font-size","13px");

  axisLabel(svg,"x","Year",W,H,m);
  axisLabel(svg,"y","Average Rating",W,H,m);

  svg.append("text").attr("x",W/2).attr("y",28).attr("text-anchor","middle")
    .style("font-size","16px").style("font-weight","700").style("fill",C.textDark)
    .text("Average Rating Over Years");
}

// Word cloud
function drawWordCloud(data){
  d3.select("#rightchart").html("");
  const {W,H}=getChartSize("rightchart");
  const svg=d3.select("#rightchart").append("svg")
    .attr("width","100%").attr("viewBox",`0 0 ${W} ${H}`)
    .attr("preserveAspectRatio","xMidYMid meet");

  svg.append("text").attr("x",W/2).attr("y",28).attr("text-anchor","middle")
    .style("font-size","16px").style("font-weight","700").style("fill",C.textDark)
    .text("Most Common Chocolate Characteristics");

  const g=svg.append("g").attr("transform",`translate(${W/2},${H/2})`);

  const words=d3.rollups(data,v=>v.length,d=>d.Characteristic)
    .map(([text,size])=>({text,size}))
    .sort((a,b)=>b.size-a.size).slice(0,42);

  if(!words.length)return;

  const scale=d3.scaleLinear().domain([0,d3.max(words,d=>d.size)]).range([12,34]);

  d3.layout.cloud()
    .size([W*0.9,H*0.7])
    .words(words.map((d,i)=>({...d,colorIdx:i})))
    .padding(5).rotate(()=>0)
    .font("DM Sans").fontSize(d=>scale(d.size))
    .on("end",arr=>{
      g.selectAll("text").data(arr).enter().append("text")
        .attr("text-anchor","middle")
        .attr("transform",d=>`translate(${d.x},${d.y})`)
        .style("font-size",d=>`${d.size}px`)
        .style("fill",d=>wordColors[d.colorIdx%wordColors.length])
        .style("font-weight",d=>d.size>24?"600":"400")
        .text(d=>d.text)
        .on("mouseover",(e,d)=>{
          d3.select(e.currentTarget).style("fill",C.yellow).style("font-weight","700");
          showTip(e,`<strong>${d.text}</strong><br>Count: ${d.size}`);
        })
        .on("mouseout",(e,d)=>{
          d3.select(e.currentTarget)
            .style("fill",wordColors[d.colorIdx%wordColors.length])
            .style("font-weight",d.size>24?"600":"400");
          hideTip();
        });
    })
    .start();
}

// Heatmap
function drawHeatmap(data){
  const {W,H}=getChartSize("heatmap");
  const m={top:70,right:52,bottom:62,left:66};
  const svg=makeSVG("heatmap",W,H);

  const cocoaOrder=['50-60%','60-70%','70-80%','80-90%','90-100%'];
  const ingOrder=[2,3,4,5,6];

  const heatData=Array.from(
    d3.rollup(data,v=>d3.mean(v,d=>d.Rating),d=>d.CocoaBin,d=>d.IngredientCount),
    ([CocoaBin,inner])=>Array.from(inner,([IngredientCount,Rating])=>({CocoaBin,IngredientCount,Rating}))
  ).flat().filter(d=>cocoaOrder.includes(d.CocoaBin)&&ingOrder.includes(+d.IngredientCount));

  const x=d3.scaleBand().domain(cocoaOrder).range([m.left,W-m.right]).padding(0.1);
  const y=d3.scaleBand().domain(ingOrder).range([H-m.bottom,m.top]).padding(0.1);

  const color=d3.scaleSequential().domain([2.5,4.0])
    .interpolator(t=>{
      if(t<0.5)return d3.interpolateRgb("#c8eaf8",C.blue)(t*2);
      return d3.interpolateRgb(C.blue,C.teal)((t-0.5)*2);
    });

  svg.selectAll("rect.cell").data(heatData).enter().append("rect")
    .attr("class","cell")
    .attr("x",d=>x(d.CocoaBin)).attr("y",d=>y(d.IngredientCount))
    .attr("width",x.bandwidth()).attr("height",y.bandwidth())
    .attr("rx",8).attr("fill",d=>color(d.Rating)).attr("opacity",0.92)
    .on("mouseover",(e,d)=>{
      d3.select(e.currentTarget).attr("stroke",C.orange).attr("stroke-width",2.5).attr("opacity",1);
      showTip(e,`Cocoa: <strong>${d.CocoaBin}</strong><br>Ingredients: <strong>${d.IngredientCount}</strong><br>Avg Rating: <strong>${d.Rating.toFixed(2)}</strong>`);
    })
    .on("mouseout",e=>{
      d3.select(e.currentTarget).attr("stroke",null).attr("opacity",0.92);
      hideTip();
    });

  svg.selectAll("text.cell-label").data(heatData).enter().append("text")
    .attr("class","cell-label")
    .attr("x",d=>x(d.CocoaBin)+x.bandwidth()/2)
    .attr("y",d=>y(d.IngredientCount)+y.bandwidth()/2)
    .attr("text-anchor","middle")
    .style("font-size","13px").style("font-weight","500")
    .style("fill",d=>d.Rating>3.1?"#fff":C.textDark)
    .style("pointer-events","none")
    .text(d=>d.Rating.toFixed(2));

  svg.append("g").attr("transform",`translate(0,${H-m.bottom})`)
    .call(d3.axisBottom(x).tickSize(0))
    .call(g=>g.select(".domain").remove())
    .selectAll("text").style("fill",C.textSoft).style("font-size","13px");

  svg.append("g").attr("transform",`translate(${m.left},0)`)
    .call(d3.axisLeft(y).tickSize(0))
    .call(g=>g.select(".domain").remove())
    .selectAll("text").style("fill",C.textSoft).style("font-size","13px");

  axisLabel(svg,"x","Cocoa Percentage",W,H,m);
  axisLabel(svg,"y","No. of Ingredients",W,H,m);

  svg.append("text").attr("x",W/2).attr("y",24).attr("text-anchor","middle")
    .style("font-size","16px").style("font-weight","700").style("fill",C.textDark)
    .text("Cocoa % vs Ingredient Count");

  svg.append("text")
    .attr("x", W/2)
    .attr("y", 46)
    .attr("text-anchor", "middle")
    .style("font-size", "13px")
    .style("fill", C.textMid)
    .style("font-style", "italic")
    .text("Each square shows the average rating for that cocoa % and ingredient count combination");

  const legendX = W - 48;
  const legendY = m.top + 8;
  
  svg.append("text")
    .attr("x", legendX + 8)
    .attr("y", legendY - 6)
    .attr("text-anchor", "middle")
    .style("font-size", "11px")
    .style("font-weight", "600")
    .style("fill", C.textMid)
    .text("Rating");
  
  const legendGrad = svg.append("defs")
    .append("linearGradient")
    .attr("id", "legendGrad")
    .attr("x1", "0").attr("x2", "0")
    .attr("y1", "0").attr("y2", "1");
  
  legendGrad.append("stop").attr("offset", "0%").attr("stop-color", C.teal);
  legendGrad.append("stop").attr("offset", "50%").attr("stop-color", C.blue);
  legendGrad.append("stop").attr("offset", "100%").attr("stop-color", "#c8eaf8");
  
  svg.append("rect")
    .attr("x", legendX)
    .attr("y", legendY)
    .attr("width", 16)
    .attr("height", 75)
    .attr("rx", 4)
    .attr("fill", "url(#legendGrad)");
  
  svg.append("text")
    .attr("x", legendX + 20)
    .attr("y", legendY + 12)
    .style("font-size", "11px")
    .style("font-weight", "500")
    .style("fill", C.textMid)
    .text("High");
  
  svg.append("text")
    .attr("x", legendX + 20)
    .attr("y", legendY + 68)
    .style("font-size", "11px")
    .style("font-weight", "500")
    .style("fill", C.textMid)
    .text("Low");
}

// Bar chart
function drawComboChart(data){
  const {W,H}=getChartSize("barchart", BAR_CHART_ASPECT);
  const m={top:54, right:40, bottom:62, left:85};
  const svg=makeSVG("barchart", W, H);

  const comboData=Array.from(
    d3.rollup(
      data.filter(d=>d.IngredientInitials&&d.IngredientInitials.trim()!==""),
      v=>({rating:d3.mean(v,d=>d.Rating),count:v.length}),
      d=>d.IngredientInitials.trim()
    ),
    ([combo,{rating,count}])=>({combo,rating,count})
  )
  .filter(d=>d.count>=3)
  .sort((a,b)=>b.rating-a.rating)
  .slice(0,7);

  if(!comboData.length){
    svg.append("text").attr("x",W/2).attr("y",H/2)
      .attr("text-anchor","middle").text("No data");
    return;
  }

  const x=d3.scaleLinear()
    .domain([2.5, d3.max(comboData, d=>d.rating) + 0.15])
    .range([m.left, W - m.right]);


  const y=d3.scaleBand()
    .domain(comboData.map(d=>d.combo))
    .range([m.top, H - m.bottom])
    .padding(0.5); 

  svg.selectAll("rect.combo-bar").data(comboData).enter().append("rect")
    .attr("class","combo-bar")
    .attr("x", m.left)
    .attr("y", d=>y(d.combo))
    .attr("width", d=>Math.max(0, x(d.rating) - m.left))
    .attr("height", y.bandwidth())
    .attr("rx", 4)
    .attr("fill", C.teal)
    .attr("opacity", 0.9)
    .on("mouseover", (e,d)=>{
      d3.select(e.currentTarget).attr("opacity", 1).attr("fill", C.blue);
      showTip(e,`<strong>${getFullNames(d.combo)}</strong><br>Avg Rating: ${d.rating.toFixed(2)}<br>Count: ${d.count}`);
    })
    .on("mouseout", (e,d)=>{
      d3.select(e.currentTarget).attr("opacity", 0.9).attr("fill", C.teal);
      hideTip();
    });

  svg.selectAll("text.combo-label").data(comboData).enter().append("text")
    .attr("class","combo-label")
    .attr("x", m.left - 12)
    .attr("y", d=>y(d.combo) + y.bandwidth()/2 + 4)
    .attr("text-anchor", "end")
    .style("font-size", "13px")
    .style("font-weight", "600")
    .style("fill", C.textMid)
    .text(d=>d.combo);

  svg.append("g")
    .attr("transform", `translate(0,${H - m.bottom})`)
    .call(d3.axisBottom(x).ticks(5).tickSize(0))
    .call(g => g.select(".domain").remove())
    .selectAll("text")
    .style("font-size", "13px")
    .style("fill", C.textSoft);

  svg.append("text")
    .attr("x", (W - m.right + m.left) / 2)
    .attr("y", 28)
    .attr("text-anchor", "middle")
    .style("font-size", "16px")
    .style("font-weight", "700")
    .style("fill", C.textDark)
    .text("Top Ingredient Combinations");

  axisLabel(svg, "x", "Average Rating", W, H, m);
}