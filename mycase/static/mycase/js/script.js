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

function formatDate(date_x) {
    var d = new Date(date_x),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2)
        month = '0' + month;
    if (day.length < 2)
        day = '0' + day;

    return [year, month, day].join('-');
}


function dailylinechart(value_ls,date_ls) {
	const legend_ls = ["New", 'FP_Taken', 'Interviewed', 'RFE', 'Transferred', 'Approved', 'Rejected', 'Other', 'Pending'];
	var themeRiver_data = [];
	for (let i = 0; i < value_ls.length; i++) {
		for (let j = 0; j < value_ls[i].length; j++) {
			themeRiver_data.push([formatDate(date_ls[j]), value_ls[i][j], legend_ls[i]]);
		}
	}

	var chartDom = document.getElementById('line_chart');
	var myChart = echarts.init(chartDom);
	var option;
	option = {
		tooltip: {trigger: 'axis'},
		legend: {data: legend_ls},
		toolbox: {feature: {dataZoom: {yAxisIndex: 'none'}, restore: {},}},
		grid: [	{left: 60, right: '1%'},],
		dataZoom: [
			{show: true, realtime: true, startValue: addMonths(new Date(), -3), endValue: new Date(), xAxisIndex: [0, 1]},
			{type: "inside", realtime: true, startValue: addMonths(new Date(), -3), endValue: new Date(), xAxisIndex: [0, 1]},
		],
		xAxis: [
			{gridIndex: 0, type: 'category', boundaryGap: false, axisLine: {lineStyle: {color: '#8392A5'}}, data: date_ls,},
		],
		yAxis: [
			{gridIndex: 0, type: 'value', name: 'Counts', nameLocation: 'center', nameGap: 45, axisLine: {lineStyle: {color: '#1c8007'}},},
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
	river_chart(value_ls,date_ls,start=option.dataZoom[0].startValue,end=option.dataZoom[0].endValue);

	myChart.on('dataZoom', function (evt) {
		var option_x = myChart.getOption();
		var startIdx = option_x.dataZoom[0].startValue;
		var endIdx=option_x.dataZoom[0].endValue;

		var axis_x = myChart.getModel().option.xAxis[0];
		var starttime = axis_x.data[startIdx];
		var endtime = axis_x.data[endIdx];

		river_chart(value_ls,date_ls,start=starttime,end=endtime);
	});

	myChart.on('restore', function (evt) {
		river_chart(value_ls,date_ls, addMonths(new Date(), -3), new Date());
	});
}
function river_chart(value_ls,date_ls,start,end) {
	const legend_ls = ["New", 'FP_Taken', 'Interviewed', 'RFE', 'Transferred', 'Approved', 'Rejected', 'Other', 'Pending'];
	var starttime = new Date(start);
	var endtime = new Date(end);
	var themeRiver_data = [];
	for (let i = 0; i < value_ls.length; i++) {
		for (let j = 0; j < value_ls[i].length; j++) {
			var date_j = new Date(date_ls[j]);
			if (date_j >= starttime && date_j <= endtime) {
				themeRiver_data.push([formatDate(date_ls[j]), value_ls[i][j], legend_ls[i]]);
			}
		}
	}
	/////////////////
	var option2;
	var chartDom2 = document.getElementById('river_chart');
	var myChart2 = echarts.init(chartDom2);
	option2 = {
		tooltip: {
			trigger: 'axis',
			axisPointer: {type: 'line', lineStyle: {color: 'rgba(0,0,0,0.2)', width: 1, type: 'solid'}}
		},
		color: color_ls,
		legend: {data: legend_ls, show: false},
		singleAxis: {
			top: 5, bottom: 20, left: 60, right: "1%",
			type: 'time',
			splitLine: {show: true, lineStyle: {type: 'dashed', opacity: 0.2}}
		},
		series: [
			{
				type: 'themeRiver',
				emphasis: {
					itemStyle: {shadowBlur: 5, shadowColor: 'rgba(0, 0, 0, 0.3)'}
				},
				data: themeRiver_data
			}
		]
	};
	option2 && myChart2.setOption(option2);
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
			left:0,right:0,
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


function plot_heatmap(dataset,range_ls,date_ls, status,color_x) {
	if(status=="New"){var scale_max=200}
	else{var scale_max=10}

	var chartDom = document.getElementById('range_heatmap_chart');
	var myChart = echarts.init(chartDom);
	var option;

	var height = 400;
	var rnrange_n = range_ls.length;
	height = rnrange_n * 30
	$("#range_heatmap_chart").css({'height': height+'px'});
	myChart.resize({ width: 1200, height: height});

	var data = [];
	for(let range_i in dataset){
		for(let date_i in dataset[range_i]){
			// if(dataset[range_i][date_i]==0)
			// 	dataset[range_i][date_i] = "-";
			data.push([date_i,range_i,dataset[range_i][date_i]])
		}
	}
	option = {
		tooltip: {
			position: 'top'
		},
		grid: {
			top: 10,
			left: 10,
			right: 70,
			bottom:10,
			containLabel: true
		},
		xAxis: {
			type: 'category',
			data: date_ls,
			splitArea: {
				show: true
			},
			axisLabel: {
				interval: 0,
				rotate: 90 //If the label names are too long you can manage this by rotating the label.
			}
		},
		yAxis: {
			type: 'category',
			data: range_ls,
			splitArea: {
				show: false
			}
		},
		visualMap: {
			min: 0,
			max: scale_max,
			calculable: true,
			orient: 'vertical',
			top: 10,
			right: 0,
			color:[color_x, '#fcfbf5']
		},
		series: [
			{
				name: status,
				type: 'heatmap',
				data: data,
				label: {
					show: true,
					fontSize: 10
				},
				emphasis: {
					label: {
						show: true
					},
					itemStyle: {
						borderColor: "#333",
						borderWidth: 1,
					},
				}
			}
		]
	};

	option && myChart.setOption(option);

}
