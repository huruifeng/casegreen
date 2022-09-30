function linechart(data_ls,label_ls) {
	 let chartStatus = Chart.getChart("line_chart"); // <canvas> id
	   if (chartStatus != undefined) {
		  chartStatus.destroy();
	   }

	const data = {
	  labels: label_ls,
	  datasets: [
		{
		  label: 'New',
		  data: data_ls[0],
		  borderColor: "rgba(16,114,241,0.7)",
		  backgroundColor: "#1072f1",
			borderWidth: 2,
			pointRadius: 1,
		},{
		  label: 'FP_Taken',
		  data: data_ls[1],
		  borderColor: "rgba(17,169,250,0.7)",
		  backgroundColor: "#11a9fa",
			borderWidth: 1,
			pointRadius: 1,
		},{
		  label: 'Interviewed',
		  data: data_ls[2],
		  borderColor: "rgba(43,4,218,0.7)",
		  backgroundColor: "#2b04da",
			borderWidth: 1,
			pointRadius: 1,
		},{
		  label: 'RFE',
		  data: data_ls[3],
		  borderColor: "rgba(244,184,36,0.7)",
		  backgroundColor: "#f4b824",
			borderWidth: 1,
			pointRadius: 1,
		},{
		  label: 'Transferred',
		  data: data_ls[4],
		  borderColor:  "rgba(199,124,255,0.7)",
		  backgroundColor: "#c77cff",
			borderWidth: 1,
			pointRadius: 1,
		},{
		  label: 'Approved',
		  data: data_ls[5],
		  borderColor:  "rgba(29,176,99,0.7)",
		  backgroundColor: "#1db063",
			borderWidth: 2,
			pointRadius: 1,
		},{
		  label: 'Rejected',
		  data: data_ls[6],
		  borderColor:  "rgba(255,0,26,0.7)",
		  backgroundColor: "#ff001a",
			borderWidth: 1,
			pointRadius: 1,
		},{
		  label: 'Other',
		  data: data_ls[7],
		  borderColor: "rgba(120,120,122,0.7)",
		  backgroundColor: "#78787a",
			borderWidth: 1,
			pointRadius: 1,
		},{
		  label: 'Pending',
		  data: data_ls[8],
		  borderColor: "rgba(161,241,16,0.7)",
		  backgroundColor: "#a6f110",
			borderWidth: 2,
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
