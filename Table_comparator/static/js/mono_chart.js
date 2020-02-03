var label = d3.select(".label");
var yMaxLabelWidth= yMaxRange.toString(10).length;

// Set the dimensions of the canvas / graph
var screenWidth = window.screen.availWidth;
var screenHeight = window.screen.availHeight;
var margin = {top: 30, right: 20, bottom: 30, left: 50 + yMaxLabelWidth*7 };
var width = Math.min(600 + (numberOfRecords/4) - margin.left - margin.right, screenWidth - margin.left - margin.right - 250);
var height = Math.min(270 + (yMaxRange/2) - margin.top - margin.bottom, (3/5)*screenHeight - margin.top - margin.bottom );

// Set the ranges
var x = d3.scale.linear().range([0, width]);
var y = d3.scale.linear().range([height, 0]);

// Define the axes
var xAxis = d3.svg.axis().scale(x).orient("bottom").ticks(5);

var yAxis = d3.svg.axis().scale(y).orient("left").ticks(5);

// Define the line
var   valueline = d3.svg.line()
.x(function(d) { return x(d._x); })
.y(function(d) { return y(d._y); });
      
// Adds the svg canvas
var   svg = d3.select("body")
.append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Get the data
data.forEach(function(d) {
      d._x = +d._x;
      d._y = +d._y;

// Scale the range of the data
x.domain(d3.extent(data, function(d) { return d._x; }));
y.domain(d3.extent(data, function(d) { return d._y; }));

// Add the valueline path.
svg.append("path")           
      .attr("class", "line")
      .attr("d", valueline(data));
      
// Add the valueline path.
svg.data(data)
      .enter()
      .append("path")
      .attr("r", 10)
      .attr("cx", function(d) {return x(d._x)})
      .attr("cy", function(d) {return y(d._y)})
      .on("mouseover", function(d,i) {

label.style("transform", "translate("+ x(d._x) +"px," + (y(d._y)) +"px)")
label.text(d._y)

});
      

// Add the X Axis
svg.append("g")               
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

// Add the Y Axis
svg.append("g")               
      .attr("class", "y axis")
      .call(yAxis);
      
// Add title
svg.append("text")
      .attr("x", (width / 2))             
      .attr("y", 0 - (margin.top / 2))
      .attr("text-anchor", "middle")  
      .style("font-size", "16px") 
      .style("text-decoration", "underline")  
      .text(title);

});
