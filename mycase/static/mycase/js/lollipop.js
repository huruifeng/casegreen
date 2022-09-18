/**
 * Created by fgnad on 8/18/17. xx
 * Modified by casegreen on 08122022
 */

// ************************************************ get values ******************************************************



function draw_lollipop(recepit_num,seq,mut_sites,mut_domain) {
    // var seq = document.getElementById('statu_sequence').value,
    //     recepit_num = document.getElementById('recepit_num').value;

    //#############
    var mutsAvailable = true;

    var jsonobj_sites = mut_sites;
    if (jsonobj_sites.length <= 0) {
        mutsAvailable = false;
        var jsonobj_sites = createPseudoMUT();
    }

    var jsonobj_domains = mut_domain;
    jsonobj_domains.sort(function (a, b) {
        return a.START - b.START
    });

    var seqarray = seq.split("");

    // **************************************** define size and categories *************************************************
    var margin = {top: 0, right: 0, bottom: 30, left: 0},
        svg_width = 800,
        svg_height = 120,
        chart_width = svg_width - margin.left - margin.right,
        chart_height = svg_height - margin.top - margin.bottom,
        moveXaxis = 0,
        belowXaxis = 22;

    var xCat = "POS",
        yCat = "Num";

    var xMax = seq.length + 1,
        xMin = 0,
        yMax = 2.5,
        yMin = 0;


    // **************************************** define axes *********************************************
    var xScale = d3.scaleLinear()
        .range([0, chart_width]).nice()
        .domain([xMin, xMax]);

    var xAxis = d3.axisBottom(xScale);

    var yScale = d3.scaleLinear()
        .range([chart_height, 0]).nice()
        .domain([yMin, yMax]);


    // **************************************** define colors, tip, and zoom *********************************************
    var colorStatus = {
        "REC": "#1072f1", "FP": "#11a9fa", "ITV": "#2b04da", "RFE": "#ffe95a",
        "TRF": "#c77cff", "APV": "#1db063", "RJC": "#ff001a", "OTH": "#78787a"
    }
    statusMap = {
        "REC": "Received(R)",
        "FP": "FP_Taken(F)",
        "ITV": "Interviewed(I)",
        "RFE": "RFE(E)",
        "TRF": "Transferred(T)",
        "APV": "Approved(A)",
        "RJC": "Rejected(J)",
        "OTH": "Other(O)"
    }
    var tip = d3.tip()
        .attr("class", "d3-tip")
        .offset([-10, 0])
        .html(function (d) {
            var htmltext = "<table style='font:12px Verdana;'>" +
                "<tr><td colspan='2'><b>" + d.ID + "</b></td></tr>" +
                "<tr><td>Case status class:</td><td style='color:'#666666'>" + statusMap[d.STATUS] + "</td></tr>" +
                "<tr><td>Action date:</td><td>" + d.ACTDATE + "</td></tr>";
            htmltext = htmltext + "</table>";
            return htmltext;
        })
        .direction("n")
        .style("background-color", "#edf2f6")
        .style("color", "#666666")
        .style("leftmargin", "0")
        .style("topmargin", "0");

    var zoom = d3.zoom()
        .scaleExtent([1, 4 / 120 * seq.length]) //1,50
        .translateExtent([[0, 0], [chart_width, chart_height]])
        .on("zoom", zoomed);


    // **************************************** append SVG and objects *****************************************************
    var svg = d3.select("#case_in_receipt_order")
        .append("svg")
        .attr("id", "status_bar")
        .attr("width", svg_width)
        .attr("height", svg_height)
        .style("background-color", "white")
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var svg2 = svg.append("svg")
        .attr("width", chart_width)
        .attr("height", chart_height)
        .append("g")
        .call(zoom)
        .call(tip);

    var view = svg2.append("rect")
        .attr("width", chart_width)
        .attr("height", chart_height)
        .style("fill", "white");

    var gX = svg.append("g")
        .classed("xAxis", true)
        .attr("transform", "translate(0," + (chart_height + moveXaxis) + ")")
        .call(xAxis);

    var xAxisLabel = svg.append("text")
        .attr("class", "x label")
        .attr("text-anchor", "start")
        .attr("x", 0)
        .attr("y", chart_height + 30)
        .text("Cases in order of Receipt Number")
        .style("font-size", "13px")
        .style("font-family", "Arial")
        .attr("visibility", "hidden");

    var mutLines = svg2.append("g")
        .attr("id", "lines")
        .selectAll(".line")
        .data(jsonobj_sites)
        .enter()
        .append("line")
        .classed("line", true)
        .attr("stroke-width", 1)
        // .attr("stroke", "#666666")
        .attr("stroke", function (d) {
            return colorStatus[d.STATUS];
        })
        .attr("x1", function (d) {
            return xScale(d[xCat]);
        })
        .attr("y1", chart_height - belowXaxis)
        .attr("x2", function (d) {
            return xScale(d[xCat]);
        })
        .attr("y2", function (d) {
            return yScale(d[yCat]);
        });

    var mutsites = svg2.append("g")
        .attr("id", "circles")
        .selectAll("circle")
        .data(jsonobj_sites)
        .enter()
        .append("circle")
        .attr("id", function (d) {
            return d['ID'];
        })
        .attr("r", 4)
        .attr("cx", function (d) {
            return xScale(d[xCat]);
        })
        .attr("cy", function (d) {
            return yScale(d[yCat]);
        })
        .style("fill", function (d) {
            return colorStatus[d["STATUS"]];
        })
        .on("mouseover", function (d) {
            d3.select(this).attr("r", 8);
            tip.show(d);
        })
        .on("mouseout", function (d) {
            d3.select(this).attr("r", 4);
            tip.hide(d);
        })
        // .style("stroke","#666666").style("stroke-width","1")
        .style("stroke", function (d) {
            return colorStatus[d.STATUS];
        }).style("stroke-width", "1")
        .on("click", function (d) {
            // window.open("", '_blank');
        });

    var domains = svg2.append("g")
        .selectAll("rect")
        .data(jsonobj_domains)
        .enter()
        .append("rect")
        .attr("x", function (d) {
            return xScale(d["START"]);
        })
        .attr("y", chart_height - belowXaxis)
        .attr("width", function (d) {
            return xScale(d["END"]) - xScale(d["START"]);
        })
        .attr("height", 18)
        .style("fill", function (d, i) {
                if (i == 0) {
                    return "white"
                }
                return colorStatus[d["ID"]];
            }
        )
        .style("stroke-width", "1")
        // .style("stroke", "#666666");
        .style("stroke", function (d) {
            return colorStatus[d["ID"]];
        });


    var domainannotation = svg2.append("g")
        .selectAll("text")
        .data(jsonobj_domains)
        .enter()
        .append("a")
        .attr("target", "_blank")
        .append("text")
        .attr("y", chart_height - 10)
        .text(function (d) {
            // return d["ID"].substring(0, Math.floor(xScale(d["END"]) - xScale(d["START"]))/9);
            return "";
        })
        .attr("x", function (d, i) {
            return (xScale(d["END"]) + xScale(d["START"])) / 2;
        })
        .attr("text-anchor", "middle")
        .style("color", "#666666")
        .style("font-weight", "normal")
        .style("font-size", "12px")
        .style("font-family", "Arial")
        .style("cursor", "pointer");//"Courier New");


    var statusseq = svg2.append("g")
        .selectAll("text")
        .data(seqarray)
        .enter()
        .append("text")
        .attr("y", chart_height - 7)
        .text(function (d) {
            return d;
        })
        .attr("x", function (d, i) {
            return xScale(i + 1);
        })
        .style("font-size", "13px")
        .attr("text-anchor", "middle")
        .attr("visibility", "hidden");

    goBackCheck();


    // **************************************** add navigation compass ****************************************************

    var circleReset = svg.append("circle")
        .attr("cx", chart_width - 64)
        .attr("cy", 15)
        .attr("r", 10)
        .style("fill", "white")
        .style("stroke", "#666666").style("stroke-width", "1")
        .attr("class", "compassNav")
        .on("mouseover", function (d) {
            d3.select(this).style("fill", "#bdbdbd");
        })
        .on("mouseout", function (d) {
            d3.select(this).style("fill", "white");
        })
        .on("click", applyReset);

    svg.append("path")
        .attr("d", "M440.935 12.574l3.966 82.766C399.416 41.904 331.674 8 256 8 134.813 8 33.933 94.924 12.296 209.824 10.908 217.193 16.604 224 24.103 224h49.084c5.57 0 10.377-3.842 11.676-9.259C103.407 137.408 172.931 80 256 80c60.893 0 114.512 30.856 146.104 77.801l-101.53-4.865c-6.845-.328-12.574 5.133-12.574 11.986v47.411c0 6.627 5.373 12 12 12h200.333c6.627 0 12-5.373 12-12V12c0-6.627-5.373-12-12-12h-47.411c-6.853 0-12.315 5.729-11.987 12.574zM256 432c-60.895 0-114.517-30.858-146.109-77.805l101.868 4.871c6.845.327 12.573-5.134 12.573-11.986v-47.412c0-6.627-5.373-12-12-12H12c-6.627 0-12 5.373-12 12V500c0 6.627 5.373 12 12 12h47.385c6.863 0 12.328-5.745 11.985-12.599l-4.129-82.575C112.725 470.166 180.405 504 256 504c121.187 0 222.067-86.924 243.704-201.824 1.388-7.369-4.308-14.176-11.807-14.176h-49.084c-5.57 0-10.377 3.842-11.676 9.259C408.593 374.592 339.069 432 256 432z")
        .style("fill", "#666666")
        .style("stroke", "#666666").style("stroke-width", "1")
        .attr("class", "compassNav")
        .attr("transform", "translate(" + (chart_width - 69) + ", 10) scale(0.02)")
        .on("mouseover", function (d) {
            circleReset.style("fill", "#bdbdbd");
        })
        .on("mouseout", function (d) {
            circleReset.style("fill", "white");
        })
        .on('click', applyReset);


    var circlePanRight = svg.append("circle")
        .attr("cx", chart_width - 42)
        .attr("cy", 15)
        .attr("r", 10)
        .style("fill", "white")
        .style("stroke", "#666666").style("stroke-width", "1")
        .attr("class", "compassNav")
        .on("mouseover", function (d) {
            d3.select(this).style("fill", "#bdbdbd");
        })
        .on("mouseout", function (d) {
            d3.select(this).style("fill", "white");
        })
        .on("click", zoomINbuttonAction);

    svg.append("line")
        .attr("class", "designInButton")
        .attr("stroke-width", 2)
        .attr("stroke", "#666666")
        .attr("x1", chart_width - 46).attr("y1", 15).attr("x2", chart_width - 38).attr("y2", 15)
        .attr("class", "compassNav")
        .on("mouseover", function (d) {
            circlePanRight.style("fill", "#bdbdbd");
        })
        .on("mouseout", function (d) {
            circlePanRight.style("fill", "white");
        })
        .on("click", zoomINbuttonAction);

    svg.append("line")
        .attr("class", "designInButton")
        .attr("stroke-width", 2)
        .attr("stroke", "#666666")
        .attr("x1", chart_width - 42).attr("y1", 11).attr("x2", chart_width - 42).attr("y2", 19)
        .attr("class", "compassNav")
        .on("mouseover", function (d) {
            circlePanRight.style("fill", "#bdbdbd");
        })
        .on("mouseout", function (d) {
            circlePanRight.style("fill", "white");
        })
        .on("click", zoomINbuttonAction);

    var circlePanLeft = svg.append("circle")
        .attr("cx", chart_width - 86)
        .attr("cy", 15)
        .attr("r", 10)
        .style("fill", "white")
        .style("stroke", "#666666").style("stroke-width", "1")
        .attr("class", "compassNav")
        .on("mouseover", function (d) {
            d3.select(this).style("fill", "#bdbdbd");
        })
        .on("mouseout", function (d) {
            d3.select(this).style("fill", "white");
        })
        .on("click", zoomOUTbuttonAction)

    svg.append("line")
        .attr("class", "designInButton")
        .attr("stroke-width", 2)
        .attr("stroke", "#666666")
        .attr("x1", chart_width - 90).attr("y1", 15).attr("x2", chart_width - 82).attr("y2", 15)
        .attr("class", "compassNav")
        .on("mouseover", function (d) {
            circlePanLeft.style("fill", "#bdbdbd");
        })
        .on("mouseout", function (d) {
            circlePanLeft.style("fill", "white");
        })
        .on("click", zoomOUTbuttonAction);

    var panLeftx = chart_width - 118;
    var panLeft = svg.append("path")
        .attr("d", "M" + panLeftx + " 14 l20 -12 a100,40 0 0,0 0,24z")
        .style("fill", "white")
        .style("stroke", "#666666").style("stroke-width", "1")
        .attr("class", "compassNav")
        .on("mouseover", function (d) {
            d3.select(this).style("fill", "#bdbdbd");
        })
        .on("mouseout", function (d) {
            d3.select(this).style("fill", "white");
        })
        .on("click", panLeftbuttonAction);

    var panRightx = chart_width - 10; ///2 + 54;
    var panRight = svg.append("path")
        .attr("d", "M" + panRightx + " 14 l-20 -12 a100,40 0 0,1 0,24z")
        .style("fill", "white")
        .style("stroke", "#666666").style("stroke-width", "1")
        .attr("class", "compassNav")
        .on("mouseover", function (d) {
            d3.select(this).style("fill", "#bdbdbd");
        })
        .on("mouseout", function (d) {
            d3.select(this).style("fill", "white");
        })
        .on("click", panRightbuttonAction);

    var svgSaveButton = svg.append("path")
        .attr("d", "M216 0h80c13.3 0 24 10.7 24 24v168h87.7c17.8 0 26.7 21.5 14.1 34.1L269.7 378.3c-7.5 7.5-19.8 7.5-27.3 0L90.1 226.1c-12.6-12.6-3.7-34.1 14.1-34.1H192V24c0-13.3 10.7-24 24-24zm296 376v112c0 13.3-10.7 24-24 24H24c-13.3 0-24-10.7-24-24V376c0-13.3 10.7-24 24-24h146.7l49 49c20.1 20.1 52.5 20.1 72.6 0l49-49H488c13.3 0 24 10.7 24 24zm-124 88c0-11-9-20-20-20s-20 9-20 20 9 20 20 20 20-9 20-20zm64 0c0-11-9-20-20-20s-20 9-20 20 9 20 20 20 20-9 20-20z")
        .style("fill", "#c7cfd7")
        .style("stroke", "#369").style("stroke-width", "1")
        .style('cursor', 'pointer')
        .attr("class", "compassNav")
        .attr("transform", "translate(" + (panLeftx - 30) + ",0) scale(0.05)")
        .on('click', saveLollipop);


    // **************************************** control actions ******************************************************
    d3.selectAll("input[name='status_type_lollipop']")
        .on("change", HS_Filter);

    // **************************************** control action functions *************************************************

    function HS_Filter() {
        var status_type_selected = []
        status_type = d3.selectAll('input[name="status_type_lollipop"]:checked')
        status_type.each(function () {
            status_type_selected.push(d3.select(this).node().value)
        })

        if (d3.selectAll('input[name="status_type_lollipop"]:checked')) {
            mutsites.transition()
                .duration(750)
                .attr("visibility", function (d) {
                    if (!status_type_selected.includes(d.STATUS)) {
                        if (d.ID != recepit_num) {
                            return "hidden";
                        } else {
                            if (!status_type_selected.includes("ME")) return "hidden";
                        }
                    }

                });

            mutLines.transition()
                .duration(750)
                .attr("visibility", function (d) {
                    if (!status_type_selected.includes(d.STATUS)) {
                        if (d.ID != recepit_num) {
                            return "hidden";
                        } else {
                            if (!status_type_selected.includes("ME")) return "hidden";
                        }
                    }
                });
        }

    }

    function applyReset() {
        svg2.transition()
            .duration(2000)
            .call(zoom.transform, d3.zoomIdentity);
    }


    function goBackCheck() {

        if (d3.selectAll('input[name="status_type_lollipop"]:checked')) {
            HS_Filter();
        }
    }

    function zoomINbuttonAction() {
        svg2.transition()
            .duration(200)
            .call(zoom.scaleBy, 1.5);
        //zoom.scaleBy(svg2, 1.5);
    }

    function zoomOUTbuttonAction() {
        svg2.transition()
            .duration(200)
            .call(zoom.scaleBy, 0.66);
        //zoom.scaleBy(svg2, 0.66);
    }

    function panLeftbuttonAction() {
        svg2.transition()
            .duration(500)
            .call(zoom.translateBy, 10 * 1200 / seq.length, 0);
    }

    function panRightbuttonAction() {
        svg2.transition()
            .duration(500)
            .call(zoom.translateBy, -10 * 1200 / seq.length, 0);
        // zoom.translateBy(svg2, -10, 0);
    }


    // **************************************** general functions ******************************************************
    function zoomed() {
        svg.select(".xAxis").call(xAxis.scale(d3.event.transform.rescaleX(xScale)));
        var new_xScale = d3.event.transform.rescaleX(xScale);
        mutsites
            .attr("cx", function (d) {
                return new_xScale(d[xCat]);
            });
        mutLines
            .attr("x1", function (d) {
                return new_xScale(d[xCat]);
            })
            .attr("x2", function (d) {
                return new_xScale(d[xCat]);
            });
        domains
            .attr("x", function (d) {
                return new_xScale(d["START"]);
            })
            .attr("width", function (d) {
                return new_xScale(d["END"]) - new_xScale(d["START"]);
            });
        domainannotation
            .attr("x", function (d, i) {
                return (new_xScale(d["END"]) + new_xScale(d["START"])) / 2;
            })
            .text(function (d) {
                //return d["ID"].substring(0, Math.floor(new_xScale(d["END"]) - new_xScale(d["START"]))/9);
                return ""
            });
        statusseq
            .attr("x", function (d, i) {
                return new_xScale(i + 1);
            });
        if (new_xScale.domain()[1] - new_xScale.domain()[0] >= 60) {
            statusseq
                .attr("visibility", "hidden")
        } else {
            statusseq
                .attr("visibility", "visible")
        }
    }


    function createPseudoMUT() {
        return [{"POS": -100, "Mut": 0, "TCGA": 0, "ICGC": 0, "COSMIC": 0, "CCLE": 0, "GDSC": 0}];
    }


    function findModsInJASON(JSON) {
        var received = false,
            rfe = false,
            approved = false,
            interviewed = false,
            other = false,
            rejected = false,
            transferred = false,
            figureprinted = false;
        for (var i = 0; i < JSON.length; ++i) {
            if (JSON[i].STATUS == "REC") received = true;
            if (JSON[i].STATUS == "RFE") rfe = true;
            if (JSON[i].STATUS == "APV") approved = true;
            if (JSON[i].STATUS == "ITV") interviewed = true;
            if (JSON[i].STATUS == "RJC") rejected = true;
            if (JSON[i].STATUS == "TRF") transferred = true;
            if (JSON[i].STATUS == "OTH") other = true;
            if (JSON[i].STATUS == "FP") figureprinted = true;
        }
        return [received, figureprinted, interviewed, transferred, rfe, approved, rejected, other]
    }


    function saveLollipop() {
        d3.selectAll(".compassNav").attr("visibility", "hidden");
        saveSvgAsPng(d3.select('#status_bar').node(), recepit_num + '.png', {scale: 2});
        d3.selectAll(".compassNav").transition().duration(750).attr("visibility", "visible");
    }

    // **************************************** add legend *************************************************

    var svgLegend = d3.select("#lollipop_legend")
        .append("svg")
        .attr("width", 800)
        .attr("height", 30)
        .append("g");

    var thismods = findModsInJASON(jsonobj_sites),
        statusTotal = ["REC", "FP", "ITV", "RFE", "TRF", "APV", "RJC", "OTH"]

    var xlegend = 5, ylegend = 15;
    for (var i = 0; i < thismods.length; ++i) {
        if (thismods[i]) {
            svgLegend.append("circle").attr("r", 6).attr("cx", xlegend).attr("cy", ylegend).style("fill", colorStatus[statusTotal[i]]);
            svgLegend.append("text").attr("x", xlegend + 10).attr("y", ylegend + 5).attr("text-anchor", "start").text(statusMap[statusTotal[i]]).style("font-size", "12px").style("font-family", "Verdana");
            xlegend = xlegend + statusMap[statusTotal[i]].length * 5 + 45;
        }
    }
}