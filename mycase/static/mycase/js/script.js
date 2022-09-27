

function linechart() {

	const labels = months({count: 20});
	const data = {
	  labels: labels,
	  datasets: [
		{
		  label: 'Dataset 1',
		  data: [1,3,4,8,9,3,4,2,3,1,2,3,1,5,6,2,3,2,6,4,2,7],
		  borderColor: CHART_COLORS.red,
		  backgroundColor: "#FF0000",
			borderWidth: 1,
			pointRadius: 1,
		},
		{
		  label: 'Dataset 2',
		  data: [6,2,3,0,8,4,7,1,3,4,8,9,3,4,5,3,4,6,7],
		  borderColor: CHART_COLORS.blue,
		  backgroundColor: "#0000FF",
			borderWidth: 1,
			pointRadius: 1,
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

/////////////////////////////////////////////////////
 function generateDataset(shift, label, color) {
      var data = [];
      var x = 0;

      while (x < 30) {
        data.push({ x: x, y: Math.sin(shift + x / 3) });
        x += Math.random();
      }

      var dataset = {
        backgroundColor: color,
        borderColor: color,
        showLine: true,
        fill: false,
        pointRadius: 2,
        label: label,
        data: data,
        lineTension: 0,
        interpolate: true
      };
      return dataset;
    }

function plotlines() {

	///////////////////
	const scaleOpts = {
	  grid: {
		borderColor:"#999999",
		color: 'rgba( 0, 0, 0, 0.1)',
	  },
	  title: {
		display: true,
		text: (ctx) => ctx.scale.axis + ' axis',
	  }
	};
	const scales = {
	  x: {
		type: 'linear',
	  },
	  y: {
		type: 'linear'
	  },
	};
	Object.keys(scales).forEach(scale => Object.assign(scales[scale], scaleOpts));


    var chart1 = new Chart(document.getElementById("line_chart").getContext("2d"), {
      type: "scatter",
      options: {
		  responsive: true,
        plugins: {
          crosshair: {
            sync: {
              enabled: false
            },
          },

		  legend: {
			position: 'top',
		  },
		  title: {
			display: true,
			text: 'Chart.js Line Chart'
		  },
          tooltip: {
            animation: false,
            mode: "interpolate",
            intersect: false,
            callbacks: {
              title: function(a, d) {
                return a[0].element.x.toFixed(2);
              },
              label: function(d) {
                return (
                  d.chart.data.datasets[d.datasetIndex].label + ": " + d.element.y.toFixed(2)
                );
              }
            }
          }
        },
        scales: scales,
      },
      data: {
        datasets: [
          generateDataset(0, "A", "red"),
          generateDataset(1, "B", "green"),
          generateDataset(2, "C", "blue")
        ]
      }
    });
}
