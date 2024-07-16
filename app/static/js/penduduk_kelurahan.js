const token = 'xYEq9m2f8C8X4F9fZvp2QbndsPfESunN';

async function getKecamatan() {
    const response = await fetch('/penduduk/kecamatan_list', {
        headers: { 'token': token }
    });
    if (!response.ok) {
        throw new Error("Network response was not ok.");
    }
    const data = await response.json();
    const kecamatanSelect = document.getElementById('kecamatan');
    data.kecamatan.forEach(kecamatan => {
        const option = document.createElement('option');
        option.value = kecamatan;
        option.text = kecamatan;
        kecamatanSelect.add(option);
    });

    // Set default kecamatan
    kecamatanSelect.value = 'KAWALU';
    await getKelurahan('KAWALU');  // Load kelurahan for default kecamatan
}

async function getKelurahan(kecamatan) {
    try {
        const response = await fetch(`/penduduk/kelurahan_list?kecamatan=${kecamatan}`, {
            headers: { 'token': token }
        });
        if (!response.ok) {
            throw new Error("Network response was not ok.");
        }
        const data = await response.json();
        const kelurahanSelect = document.getElementById('kelurahan');
        kelurahanSelect.innerHTML = '';
        data.kelurahan.forEach(kelurahan => {
            const option = document.createElement('option');
            option.value = kelurahan;
            option.text = kelurahan;
            kelurahanSelect.add(option);
        });

        // Set default kelurahan
        kelurahanSelect.value = 'LEUWILIANG';
        if (data.kelurahan.includes('LEUWILIANG')) {
            updateChart('LEUWILIANG');  // Load chart for default kelurahan
        } else {
            console.error('Kelurahan default tidak tersedia.');
        }
    } catch (error) {
        console.error("Error fetching kelurahan list:", error);
    }
}

async function updateChart(kelurahan) {
    console.log('Kelurahan selected:', kelurahan);
    console.log('Fetching data for kelurahan:', kelurahan);
    try {
        const response = await fetch(`/penduduk/kelurahan?nama_kelurahan=${encodeURIComponent(kelurahan)}`, {
            headers: { 'token': token }
        });
        if (!response.ok) {
            console.error('HTTP error!', response.status, await response.text());  // Tambahkan response.text() untuk detail error
        } else {
            const data = await response.json();
            console.log('Fetched data:', data);
            if (data.data && data.data[kelurahan]) {
                renderChart(data.data[kelurahan]);
            } else {
                console.error('Data for kelurahan not found or is in unexpected format');
            }
        }
    } catch (error) {
        console.error("Error fetching kelurahan data:", error);
    }
}

function renderChart(data) {
    console.log('Rendering chart with data:', data);
    if (!data || data.laki_laki === undefined || data.perempuan === undefined) {
        console.error('Invalid data format:', data);
        return;
    }

    const chartDiv = document.getElementById('chart');
    chartDiv.innerHTML = '';

    const margin = { top: 20, right: 30, bottom: 70, left: 50 };
    const width = 500 - margin.left - margin.right;
    const height = 300 - margin.top - margin.bottom;

    const svg = d3.select(chartDiv)
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    const x = d3.scaleBand()
        .domain(['Laki-laki', 'Perempuan'])
        .range([0, width])
        .padding(0.2);

    const y = d3.scaleLinear()
        .domain([0, d3.max([data.laki_laki, data.perempuan])])
        .nice()
        .range([height, 0]);

    const barData = [
        { gender: 'Laki-laki', value: data.laki_laki },
        { gender: 'Perempuan', value: data.perempuan }
    ];
    console.log('Bar data:', barData);

    svg.append('g')
        .selectAll('.bar')
        .data(barData)
        .enter().append('rect')
        .attr('class', 'bar')
        .attr('x', d => x(d.gender))
        .attr('y', d => y(d.value))
        .attr('width', x.bandwidth())
        .attr('height', d => height - y(d.value))
        .attr('fill', d => {
            if (d.gender === 'Laki-laki') {
                return 'steelblue';
            } else if (d.gender === 'Perempuan') {
                return 'pink';
            } else {
                return 'gray';
            }
        });

    svg.append('g')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(x))
        .selectAll("text")
        .attr("transform", "translate(0,10)rotate(-45)")
        .style("text-anchor", "end")
        .style("font-size", "12px")
        .style("fill", "#333");

    svg.append('g')
        .call(d3.axisLeft(y));

    svg.append('text')
        .attr('transform', `translate(${width / 2},${height + margin.bottom - 10})`)
        .style('text-anchor', 'middle');

    svg.append('text')
        .attr('transform', 'rotate(-90)')
        .attr('y', -margin.left + 10)
        .attr('x', -(height / 2))
        .style('text-anchor', 'middle');
}

document.getElementById('kecamatan').addEventListener('change', async function() {
    const kecamatan = this.value;
    await getKelurahan(kecamatan);
});

document.getElementById('kelurahan').addEventListener('change', function() {
    const kelurahan = this.value;
    console.log('Kelurahan selected:', kelurahan);
    updateChart(kelurahan);
});

getKecamatan();
