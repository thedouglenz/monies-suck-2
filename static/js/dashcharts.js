$(document).ready(function() {
  // Handle dash charts
  var ctx = document.getElementById("dash-chart").getContext("2d");

  var resetCanvas = function()  {
    $("#dash-chart").remove();
    $("#chart-legend").remove();
    $("#charts-container").append('<canvas id="dash-chart" width="600" height="400"><canvas>"');
    ctx = document.getElementById("dash-chart").getContext("2d");
  }

  function displayRadialChart() {
    resetCanvas();
    $.getJSON("../api/v1/charts/radial/totals/month", function(data){
      var dashChart = new Chart(ctx).PolarArea(data);
    });
  }

  function displayBarChart() {
    resetCanvas();
    var options = {
      legendTemplate : '<ul id="chart-legend" style="list-style-type:none;">'
      +'<% for (var i=0; i<datasets.length; i++) { %>'
      +'<li>'
      +'<span style="color:<%=datasets[i].fillColor%>;"> <i class="fa fa-square-o" style="padding: 5px; font-weight:bold;"> </i></span>'
      +'<% if (datasets[i].label) { %><%= datasets[i].label %><% } %>'
      +'</li>'
      +'<% } %>'
      +'</ul>'
    };
    $.getJSON("../api/v1/charts/bar/totals/month", function(data){
      var dashChart = new Chart(ctx).Bar(data, options);
      var legend = dashChart.generateLegend();
      $('#charts-container').append(legend);
    });
  } displayBarChart();

  $("#radial-chart-btn").click(displayRadialChart);
  $("#bar-chart-btn").click(displayBarChart);
});
