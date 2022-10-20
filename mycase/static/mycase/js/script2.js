function form_bar_plot(form_status_count) {
	var form_count = {}
	for(let form_i in form_status_count){
		var n = 0;
		for(let status_i in form_status_count[form_i]){
			n += form_status_count[form_i][status_i]
		}
		form_count[form_i] = n
	}

	var chartDom = document.getElementById('form_bar');
	var myChart = echarts.init(chartDom);
	var option;

	option = {
		title: {
			text: 'Form types'
		},
		tooltip: {
			trigger: 'axis',
			axisPointer: {
				type: 'shadow'
			}
		},
		legend: {},
		grid: {
			left: '3%',
			right: '4%',
			bottom: '3%',
			containLabel: true
		},
		xAxis: {
			type: 'value',
			boundaryGap: [0, 0.01]
		},
		yAxis: {
			type: 'category',
			data: Object.keys(form_count)
		},
		series: [
			{
				name: '',
				type: 'bar',
				data: Object.values(form_count),
				showBackground: true,
				label: {
					position: 'right',
					show: true
				},

			}
		]
	};

	option && myChart.setOption(option);

	form_pie_plot(form_status_count[Object.keys(form_count)[0]])

	myChart.on('click', function (params) {
		form_pie_plot(form_status_count[params.name])
	});

}


function form_pie_plot(data) {
	var data_ls = [];
	for(let status_i in data){
		data_ls.push({"name":status_i,"value":data[status_i]})
	}
	var chartDom = document.getElementById('form_pie');
	var myChart = echarts.init(chartDom);
	var option;

	option = {
		tooltip: {
			trigger: 'item'
		},
		series: [
			{
				name: 'Status',
				type: 'pie',
				radius: '85%',
				data: data_ls,
				label: {
				  formatter: '{b}: {c} ({d}%)'
				},
				emphasis: {
					itemStyle: {
						shadowBlur: 10,
						shadowOffsetX: 0,
						shadowColor: 'rgba(0, 0, 0, 0.5)'
					}
				}
			}
		]
	};

	option && myChart.setOption(option);
}