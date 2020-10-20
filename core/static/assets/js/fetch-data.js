window.addEventListener("load", function() {
    load_report();
    load_trends();
    load_world_map();
    load_cases_table();
    load_realtime_growth_chart();
    load_daily_growth_chart();
});



function load_report() {
    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var data = JSON.parse(this.response);

            document.getElementById("daily_confirmed_label").innerText = addCommas(data.num_confirmed);
            document.getElementById("daily_recovered_label").innerText = addCommas(data.num_recovered);
            document.getElementById("daily_deaths_label").innerText = addCommas(data.num_deaths);
            document.getElementById("daily_death_rate_label").innerText = data.death_rate;
        }
    };

    xhttp.open("GET", "report");
    xhttp.send();
}



function load_trends() {
    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var data = JSON.parse(this.response);

            trend_confirmed_label = document.getElementById("trend_confirmed_label");
            trend_recovered_label =  document.getElementById("trend_recovered_label");
            trend_deaths_label = document.getElementById("trend_deaths_label");
            trend_death_rate_label = document.getElementById("trend_death_rate_label");

            if (data.confirmed_trend > 0) {
                trend_confirmed_label.innerHTML = "<i class='fa fa-angle-up'></i>";
                trend_confirmed_label.classList.add("text-danger");
            }
            else {
                trend_confirmed_label.innerHTML = "<i class='fa fa-angle-down'></i>";
                trend_confirmed_label.classList.add("text-success");
            }

            if (data.recovered_trend > 0) {
                trend_recovered_label.innerHTML = "<i class='fa fa-angle-up'></i>";
                trend_recovered_label.classList.add("text-success");
            }
            else {
                trend_recovered_label.innerHTML = "<i class='fa fa-angle-down'></i>",
                trend_recovered_label.classList.add("text-danger");
            }

            if (data.deaths_trend > 0) {
                trend_deaths_label.innerHTML = "<i class='fa fa-angle-up'></i>";
                trend_deaths_label.classList.add("text-danger");
            }
            else {
                trend_deaths_label.innerHTML = "<i class='fa fa-angle-down'></i>";
                trend_deaths_label.classList.add("text-success");
            }

            if (data.death_rate_trend > 0) {
                trend_death_rate_label.innerHTML = "<i class='fa fa-angle-up'></i>";
                trend_death_rate_label.classList.add("text-danger");
            }
            else {
                trend_death_rate_label.innerHTML = "<i class='fa fa-angle-down'></i>";
                trend_death_rate_label.classList.add("text-success");
            }

            trend_confirmed_label.innerHTML += " " + data.confirmed_trend + "%";
            trend_recovered_label.innerHTML += " " + data.recovered_trend + "%";
            trend_deaths_label.innerHTML += " " + data.deaths_trend + "%";
            trend_death_rate_label.innerHTML += " " + data.death_rate_trend;
        }
    };

    xhttp.open("GET", "trends");
    xhttp.send();
}



function load_world_map() {
    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var data = JSON.parse(this.response);
            hoverinfo = function() {
                result = [];

                for (let index = 0; index < Object.values(data["Combined_Key"]).length; index++) {
                    result.push(
                        "<b>" + Object.values(data["Combined_Key"])[index] + "</b><br>" +
                        "Confirmed: " + Object.values(data["Confirmed"])[index] + "<br>" + 
                        "Lat: " + Object.values(data["Lat"])[index] + "<br>" +
                        "Long: " + Object.values(data["Long_"])[index]
                    );
                }

                return result;
            }();

            var plot_data = [{
                type: "scattermapbox",
                lat: Object.values(data["Lat"]),
                lon: Object.values(data["Long_"]),
                hovertext: hoverinfo,
                hoverinfo: "text",
                marker: {
                    color: Object.values(data["Confirmed"]),
                    colorbar: {
                        outlinewidth: 0,
                        title: {
                            text: "Confirmed"
                        }
                    },
                    colorscale: [[0, "hsl(255, 95%, 26%)"], [0.5, "hsl(330, 60%, 50%)"], [1, "hsl(60, 100%, 60%)"]],
                    showscale: true,
                    size: Object.values(data["Confirmed"]),
                    sizemin: 0,
                    sizeref: 2000,
                    sizemode: "area"
                }
            }];

            var plot_layout = {
                margin: {t:0, l:0, r:0, b:0},
                paper_bgcolor:'rgba(0,0,0,0)',
                mapbox: {
                    style: "carto-positron",
                    center: {lat: 20, lon: -20},
                    zoom: 1
                }
            };

            var plot_config = {responsive: true, displayModeBar: false}

            Plotly.newPlot(document.getElementById("world_map"), plot_data, plot_layout, plot_config);
        }
    };

    xhttp.open("GET", "daily_report");
    xhttp.send();
}



function load_cases_table() {
    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var data = JSON.parse(this.response);
            var cases_table = document.getElementById("cases_table");
            var cases_table_body = document.getElementById("cases_table_body");

            for (let row of data) {
                if (row["Country"].length >= 15) {
                    row["Country"] = row["Country"].substring(0, 15) + "…";
                }

                let new_row = "<tr>";

                new_row += "<td class='font-weight-bold'>" + row["Country"] + "</td>";
                new_row += "<td>" + addCommas(row["Confirmed"]) + "</td>";
                new_row += "<td>" + addCommas(row["Recovered"]) + "</td>";
                new_row += "<td>" + addCommas(row["Deaths"]) + "</td>";
                new_row += "<td>" + (row["Death Rate"]) + "</td>";
                new_row += "</tr>";

                cases_table_body.innerHTML += new_row;
            }

            sorttable.makeSortable(cases_table);
            cases_table.classList.add("sortable");
        }
    };

    xhttp.open("GET", "cases");
    xhttp.send();
}



function load_realtime_growth_chart() {
    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var data = JSON.parse(this.response);

            var dates = Object.keys(data["Confirmed"]) 

            var confirmed_trace = {
                x: dates,
                y: Object.values(data["Confirmed"]),
                name: "Confirmed",
                line: {color: "#8965E0", width: 4}
            };

            var recovered_trace = {
                x: dates,
                y: Object.values(data["Recovered"]),
                name: "Recovered",
                line: {color: "#2DCE89", width: 4}
            };

            var deaths_trace = {
                x: dates,
                y: Object.values(data["Deaths"]),
                name: "Deaths",
                line: {
                    color: "#F9345E",
                    width: 4
                }
            };

            var plot_data = [confirmed_trace, recovered_trace, deaths_trace];

            var plot_layout = {
                paper_bgcolor:'rgba(0,0,0,0)',
                plot_bgcolor:'rgba(0,0,0,0)',
                yaxis: {automargin: true, type: "log", gridcolor: "#32325d"},
                xaxis: {automargin: true, showgrid: false},
                showlegend: false,
                font: {color: '#ced4da'},
                margin: {t:0, l:0, r:0, b:0},
                hovermode: "closest",
                updatemenus: [
                    {
                        visible: true,
                        type: "dropdown",
                        buttons: [
                            {method: "relayout", label: "Logarithmic", args: [{"yaxis.type": "log"}]},
                            {method: "relayout", label: "Linear", args: [{"yaxis.type": "linear"}]}
                        ],
                        x: 0.05,
                        xanchor: "auto",
                        bgcolor: "#6236FF",
                        bordercolor: "rgba(0,0,0,0)"
                    }
                ]
            };

            var plot_config = {responsive: true, displayModeBar: false};

            Plotly.newPlot(document.getElementById("realtime_growth_chart"), plot_data, plot_layout, plot_config);
        }
    };

    xhttp.open("GET", "realtime_growth");
    xhttp.send();
}



function load_daily_growth_chart() {
    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var data = JSON.parse(this.response);

            var dates = Object.keys(data["confirmed"]["World"]);
            var confirmed = Object.values(data["confirmed"]["World"]);
            var deaths = Object.values(data["deaths"]["World"]);

            var plot_data = [
                {
                    x: dates,
                    y: confirmed,
                    name: "Confirmed",
                    type: "bar",
                    visible: "legendonly",
                    marker: {color: "#6236FF", line: {color: "#fff", width: 1}}
                },
                {
                    x: dates,
                    y: deaths,
                    name: "Deaths",
                    type: "bar",
                    marker: {color: "#F9345E", line: {color: "#FFF", width: 1}}
                }
            ];

            var selectorOptions = {
                buttons: [
                    {count: 7, label: "W", step: "day", stepmode: "backward"},
                    {count: 1, label: "M", step: "month", stepmode: "backward"},
                    {count: 3, label: "3M", step: "month", stepmode: "backward"},
                    {label: "T", step: "all"}
                ]
            };

            var plot_layout = {
                barmode: "stack",
                paper_bgcolor:'rgba(0,0,0,0)',
                plot_bgcolor:'rgba(0,0,0,0)',
                margin: {t:0, l:0, r:0, b:0},
                hovermode: "closest",
                bargap: 0,
                yaxis: {automargin: true, showgrid: true, zerolinecolor: "#FFFFFF", gridcolor: "#e9ecef"},
                xaxis: {automargin: true, showgrid: false, rangeselector: selectorOptions},
                legend: {x: 0.025, y: 1}
            };

            var plot_config = {responsive: true, displayModeBar: false};

            Plotly.newPlot(document.getElementById("daily_growth_chart"), plot_data, plot_layout, plot_config);
        }
    };

    xhttp.open("GET", "daily_growth");
    xhttp.send();
}



function addCommas(input) {
    var number_string = input.toString();
    var result = "";

    for (let i = 0; i < number_string.length; i++) {
        result = number_string[number_string.length -1 - i] + result;

        if ((i + 1) % 3 == 0 && i != number_string.length - 1) {
            result = "," + result;
        } 
    }

    return result;
}
