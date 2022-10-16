function linechart(data_ls,label_ls) {
	 let chartStatus = Chart.getChart("line_chart"); // <canvas> id
	   if (chartStatus != undefined) {
		  chartStatus.destroy();
	   }

	const data = {
	  labels: label_ls,
	  datasets: [
		  {label: 'New',data: data_ls[0], borderColor: "rgba(16,114,241,0.7)", backgroundColor: "#1072f1", borderWidth: 2, pointRadius: 1,},
		  {label: 'FP_Taken', data: data_ls[1],borderColor: "rgba(17,169,250,0.7)", backgroundColor: "#11a9fa", borderWidth: 1, pointRadius: 1,},
		  {label: 'Interviewed', data: data_ls[2], borderColor: "rgba(43,4,218,0.7)", backgroundColor: "#2b04da", borderWidth: 1, pointRadius: 1,},
		  {label: 'RFE', data: data_ls[3], borderColor: "rgba(244,184,36,0.7)", backgroundColor: "#f4b824", borderWidth: 1, pointRadius: 1,},
		  {label: 'Transferred', data: data_ls[4], borderColor:  "rgba(199,124,255,0.7)", backgroundColor: "#c77cff", borderWidth: 1, pointRadius: 1,},
		  {label: 'Approved', data: data_ls[5], borderColor:  "rgba(29,176,99,0.7)", backgroundColor: "#1db063", borderWidth: 2, pointRadius: 1,},
		  {label: 'Rejected', data: data_ls[6], borderColor:  "rgba(255,0,26,0.7)", backgroundColor: "#ff001a", borderWidth: 1, pointRadius: 1,},
		  {label: 'Other', data: data_ls[7], borderColor: "rgba(120,120,122,0.7)", backgroundColor: "#78787a", borderWidth: 1, pointRadius: 1,},
		  {label: 'Pending', data: data_ls[8], borderColor: "rgba(161,241,16,0.7)", backgroundColor: "#a6f110", borderWidth: 2, pointRadius: 1,
		}
	  ]
	};

	///////////////////
	const scales = {
	  x: {type: 'category'},
	  y: { position: 'right',
		ticks: { callback: (val, index, ticks) => index === 0 || index === ticks.length - 1 ? null : val,},
		grid: {borderColor:"#870aec", color: 'rgba( 0, 0, 0, 0.1)',	},
		title: {display: true,text: 'Counts',}
	  },
	};

	const config = {
	  type: 'line',
	  data: data,
	  options: {
		  scales: scales,
		responsive: true,
		plugins: {
		  legend: {	position: 'top'},
		  title: {display: false, text: ''},
		  zoom: {
			pan: { enabled: true,mode: 'x', modifierKey: 'ctrl',},
			zoom: { wheel: {enabled: true}, drag: {enabled: true}, pinch: {enabled: true}, mode: 'x',},
		  },
			tooltip: {
            animation: true,
            mode: "interpolate",
            intersect: false,
          }
		}
	  },
	};

	const ctx = document.getElementById('line_chart').getContext('2d');
	var myChart = new Chart(ctx, config);
}

const getDaysInMonth = (year, month) => new Date(year, month, 0).getDate()
const addMonths = (input, months) => {
  const date = new Date(input)
  date.setDate(1)
  date.setMonth(date.getMonth() + months)
  date.setDate(Math.min(input.getDate(), getDaysInMonth(date.getFullYear(), date.getMonth()+1)))
  return date
}
// console.log(addMonths(new Date('2020-01-31T00:00:00'), -6))
// // "2019-07-31T06:00:00.000Z"
//
// console.log(addMonths(new Date('2020-01-31T00:00:00'), 1))
// // "2020-02-29T06:00:00.000Z"
//
// console.log(addMonths(new Date('2020-05-31T00:00:00'), -6))
// // "2019-11-30T06:00:00.000Z"
//
// console.log(addMonths(new Date('2020-02-29T00:00:00'), -12))
// // "2019-02-28T06:00:00.000Z"

function dailylinechart(value_ls,date_ls) {
	const legend_ls =  ["New",'FP_Taken','Interviewed','RFE','Transferred','Approved','Rejected','Other','Pending'];
	var themeRiver_data = [];
	for (let i = 0; i < value_ls.length; i++) {
	  for (let j = 0; j < value_ls[i].length; j++) {
		themeRiver_data.push([date_ls[j], value_ls[i][j], legend_ls[i]]);
	  }
	}

	var chartDom = document.getElementById('line_chart');
	var myChart = echarts.init(chartDom);
	var option;
	option = {
	  tooltip: {trigger: 'axis'},
	  legend: {data: legend_ls},
	  toolbox: {
		feature: {dataZoom: {yAxisIndex: 'none'}, restore: {},}
	  },
	  grid: [
		  {left: 60, right: '1%',bottom: 70,}],
	  dataZoom: [
		{show: true, realtime: true, startValue:addMonths(new Date(),-6), xAxisIndex: [0, 1]},
		{type: 'inside', realtime: true, startValue: addMonths(new Date(),-6), xAxisIndex: [0, 1]}
	  ],
	  xAxis: [
		  {gridIndex:0,type: 'category', boundaryGap: false, axisLine: { lineStyle: { color: '#8392A5' } }, data: date_ls,},
	  ],
	  yAxis: [
		  {gridIndex:0,type: 'value', name:'Counts', nameLocation:'center', nameGap:45, axisLine: { lineStyle: { color: '#1c8007' } },},
	  ],
	  series: [
		{name: 'New', type: 'line', data: value_ls[0], lineStyle: {color: color_ls[0]}, itemStyle: {color: color_ls[0],}},
		{name: 'FP_Taken',type: 'line',data: value_ls[1],lineStyle: {color: color_ls[1]},itemStyle: {color: color_ls[1]}},
		{name: 'Interviewed',type: 'line',data: value_ls[2],lineStyle: {color: color_ls[2]},itemStyle: {color: color_ls[2]}},
		{name: 'RFE',type: 'line',data: value_ls[3],lineStyle: {color: color_ls[3]},itemStyle: {color: color_ls[3]}},
		{name: 'Transferred',type: 'line',data: value_ls[4],lineStyle: {color: color_ls[4]},itemStyle: {color: color_ls[4]}},
		{name: 'Approved',type: 'line',data: value_ls[5],lineStyle: {color: color_ls[5]},itemStyle: {color: color_ls[5]}},
		{name: 'Rejected',type: 'line',data:value_ls[6],lineStyle: {color: color_ls[6]},itemStyle: {color: color_ls[6]}},
		{name: 'Other',type: 'line',data: value_ls[7],lineStyle: {color: color_ls[7]},itemStyle: {color: color_ls[7]}},
		{name: 'Pending',type: 'line',data: value_ls[8],lineStyle: {color: color_ls[8]},itemStyle: {color: color_ls[8]}},
	  ]
	};

	option && myChart.setOption(option);

}


 function plot_sankey(sankey_data){
	google.charts.load('current', {'packages':['sankey']});
	google.charts.setOnLoadCallback(drawChart);
	function drawChart() {
		var data = new google.visualization.DataTable();
		data.addColumn('string', 'From');
		data.addColumn('string', 'To');
		data.addColumn('number', 'Count');
		data.addRows(sankey_data);

		var height = 100;
		if(sankey_data.length *20 > height) height = sankey_data.length*5;

		// Sets chart options.
		var options = {
			width: 1200,
			height: height,
			tooltip: {
				textStyle:{fontSize: 10, bold:false, italic: false },
				showColorCode: true
			},
			sankey: {
				link: { colorMode: 'gradient'}
			  }
		};

		// Instantiates and draws our chart, passing in some options.
		var chart = new google.visualization.Sankey(document.getElementById('status_sankey'));
		chart.draw(data, options);
	}
}

function status_sankey(sankey_data) {
	var chartDom = document.getElementById('status_sankey_div');
	var myChart = echarts.init(chartDom);

	var height = 400;
	if(sankey_data.nodes.length > 20) height = sankey_data.nodes.length*10
	$("#status_sankey_div").css({'height': height+'px'});
	myChart.resize({ width: 1200, height: height});

	var option;
	myChart.setOption(
	   (option = {
		  tooltip: {trigger: 'item', triggerOn: 'mousemove', textStyle: {fontSize:12}},
		  grid:{left: 0, right: 0, bottom: 0, top:0, containLabel: true},
		  series: [
			{
			  type: 'sankey',
			  emphasis: {focus: 'adjacency'},
			  nodeAlign: 'left',
			  data: sankey_data.nodes,
			  links: sankey_data.links,
			  lineStyle: { color: 'gradient', curveness: 0.5},
			  label: {color: 'rgba(0,0,0,0.7)', fontFamily: 'Arial', fontSize: 10}
			}
		  ]
	   })
	);
	option && myChart.setOption(option);
}
