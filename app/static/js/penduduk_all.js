async function fetchData() {
    const response = await fetch("/penduduk/all");
    const data = await response.json();
    return data;
}

function renderPieChart(data) {
    const width = 450;
    const height = 450;
    const margin = 40;

    const radius = Math.min(width, height) / 2 - margin;

    const svg = d3.select("#pie-chart")
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", `translate(${width / 2}, ${height / 2})`);

    const color = d3.scaleOrdinal()
        .domain(data.map(d => d.label))
        .range(['steelblue', 'pink']);

    const pie = d3.pie()
        .value(d => d.value);

    const data_ready = pie(data);

    svg.selectAll('slices')
        .data(data_ready)
        .enter()
        .append('path')
        .attr('d', d3.arc()
            .innerRadius(0)
            .outerRadius(radius)
        )
        .attr('fill', d => color(d.data.label))
        .attr("stroke", "black")
        .style("stroke-width", "2px")
        .style("opacity", 0.9);

    svg.selectAll('slices')
        .data(data_ready)
        .enter()
        .append('text')
        .text(d => `${d.data.value.toLocaleString()}`)
        .attr("transform", d => `translate(${d3.arc()
            .innerRadius(0)
            .outerRadius(radius)
            .centroid(d)})`)
        .style("text-anchor", "middle")
        .style("font-size", 15);

    // Add legend in a separate div
    const legend = d3.select("#pie-chart-legend")
        .append("svg")
        .attr("width", width)
        .attr("height", 50 * data.length)  // Adjust height based on number of legend items
        .selectAll(".legend")
        .data(data)
        .enter().append("g")
        .attr("class", "legend")
        .attr("transform", (d, i) => `translate(0, ${i * 20})`);  // Adjust vertical spacing

    legend.append("rect")
        .attr("x", 0)
        .attr("width", 18)
        .attr("height", 18)
        .style("fill", d => color(d.label));

    legend.append("text")
        .attr("x", 24)
        .attr("y", 9)
        .attr("dy", ".35em")
        .style("text-anchor", "start")
        .text(d => d.label);
}

fetchData().then(apiData => {
    const data = [
        { label: "Laki-laki", value: apiData.total_laki_laki },
        { label: "Perempuan", value: apiData.total_perempuan }
    ];
    renderPieChart(data);
});
