document.addEventListener("DOMContentLoaded", function() {
    const token = "xYEq9m2f8C8X4F9fZvp2QbndsPfESunN";  // Token yang valid

    async function fetchDataKecamatan(nama_kecamatan) {
        const url = new URL("/penduduk/kecamatan", window.location.origin);
        if (nama_kecamatan && nama_kecamatan !== "All") {
            url.searchParams.append("nama_kecamatan", nama_kecamatan);
        }
        console.log("Fetching data for kecamatan with URL:", url.toString());
        const response = await fetch(url, {
            headers: { "token": token }
        });
        if (!response.ok) {
            throw new Error("Network response was not ok.");
        }
        const data = await response.json();
        console.log("Fetched data:", data);
        return data.data;  // Data penduduk untuk kecamatan
    }

    function renderBarChartKecamatan(data) {
        console.log("Rendering bar chart with data:", data);
        const margin = { top: 20, right: 30, bottom: 40, left: 60 };  // Menambah margin kiri untuk label sumbu Y
        const width = 800 - margin.left - margin.right;
        const height = 500 - margin.top - margin.bottom;
    
        const svg = d3.select("#kecamatan-bar-chart")
            .html("")  // Clear existing chart
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", `translate(${margin.left},${margin.top})`);
    
        const x = d3.scaleBand()
            .domain(Object.keys(data))
            .range([0, width])
            .padding(0.2);  // Menambah padding
    
        console.log("X domain:", x.domain());
    
        // Log nilai maksimum untuk Y
        const maxYValue = d3.max(Object.values(data), d => Math.max(d.laki_laki, d.perempuan));
        console.log("Max Y Value:", maxYValue);
    
        // Set Y domain dengan nilai maksimum
        const y = d3.scaleLinear()
            .domain([0, maxYValue])  // Domain mulai dari 0 hingga maxYValue
            .nice()
            .range([height, 0]);
    
        console.log("Y domain:", y.domain());
    
        svg.append("g")
            .selectAll(".bar-laki-laki")
            .data(Object.entries(data))
            .enter()
            .append("rect")
            .attr("class", "bar-laki-laki")
            .attr("x", d => x(d[0]))
            .attr("y", d => y(d[1].laki_laki))
            .attr("width", x.bandwidth() / 2)
            .attr("height", d => {
                const heightValue = height - y(d[1].laki_laki);
                console.log(`Height for laki-laki in ${d[0]}: ${heightValue} (Value: ${d[1].laki_laki})`);
                return heightValue;
            })
            .attr("fill", "steelblue");
    
        svg.append("g")
            .selectAll(".bar-perempuan")
            .data(Object.entries(data))
            .enter()
            .append("rect")
            .attr("class", "bar-perempuan")
            .attr("x", d => x(d[0]) + x.bandwidth() / 2)  // Letakkan di samping bar laki-laki
            .attr("y", d => y(d[1].perempuan))
            .attr("width", x.bandwidth() / 2)
            .attr("height", d => {
                const heightValue = height - y(d[1].perempuan);
                console.log(`Height for perempuan in ${d[0]}: ${heightValue} (Value: ${d[1].perempuan})`);
                return heightValue;
            })
            .attr("fill", "pink");
    
        svg.append("g")
            .attr("transform", `translate(0,${height})`)
            .call(d3.axisBottom(x))
            .selectAll("text")
            .attr("transform", "translate(-10,0)rotate(-45)")
            .style("text-anchor", "end");
    
        svg.append("g")
            .call(d3.axisLeft(y));
    }
    

    async function fetchKecamatanList() {
        try {
            const response = await fetch("/penduduk/kecamatan_list", {
                headers: { "token": token }
            });
            if (!response.ok) {
                throw new Error("Network response was not ok.");
            }
            const data = await response.json();
            console.log("Fetched kecamatan list:", data.kecamatan);  // Log the kecamatan list
            return data.kecamatan;  // Daftar kecamatan
        } catch (error) {
            console.error("Error fetching kecamatan list:", error);
        }
    }

    function populateKecamatanDropdown(kecamatanList) {
        const kecamatanSelect = document.getElementById("nama_kecamatan");
        kecamatanSelect.innerHTML = "";  // Clear existing options
        const allOption = document.createElement("option");
        allOption.value = "All";
        allOption.text = "All";
        kecamatanSelect.add(allOption);
        kecamatanList.forEach(kecamatan => {
            const option = document.createElement("option");
            option.value = kecamatan;
            option.text = kecamatan;
            kecamatanSelect.add(option);
        });
        console.log("Dropdown populated with kecamatan:", kecamatanList);  // Log the populated dropdown
    }

    async function init() {
        const kecamatanList = await fetchKecamatanList();
        if (kecamatanList) {
            populateKecamatanDropdown(kecamatanList);
            // Muat data "All" secara default
            try {
                const data = await fetchDataKecamatan("All");
                renderBarChartKecamatan(data);
            } catch (error) {
                console.error("Error fetching default data for 'All':", error);
            }
        }
    }

    document.getElementById("nama_kecamatan").addEventListener("change", async function() {
        const nama_kecamatan = this.value;
        console.log("Selected kecamatan:", nama_kecamatan);
        try {
            const data = await fetchDataKecamatan(nama_kecamatan);
            console.log("Fetched data:", data);
            renderBarChartKecamatan(data);
        } catch (error) {
            console.error("Error fetching data for kecamatan:", error);
        }
    });

    init();
});
