<template>
    <div>
        <div id="row" class="chart-container"></div>
    </div>
</template>

<script>
import Plotly from 'plotly.js-dist'
import apiService from '@/services/api.js'

export default {
    name: 'NbaStatsGraph',
    data() {
        return {
            exchangeData: []
        }
    },
    async mounted() {
        await this.fetchData();
    },
    watch: {
        exchangeData: {
            handler(newData) {
                if (newData.length > 0) {
                    console.log('Data received:', newData);
                    this.$nextTick(() => {
                        this.createCharts();
                    });
                }
            },
            immediate: true
        }
    },
    methods: {
        async fetchData() {
            try {
                const response = await apiService.nba.getStats();
                console.log('API Response:', response);
                if (response.status === 'success') {
                    this.exchangeData = response.data;
                }
            } catch (error) {
                console.error('Error fetching NBA stats:', error);
            }
        },
        createCharts() {
            // 清除現有圖表
            const container = document.getElementById("row");
            container.innerHTML = '';

            // 其餘的 createCharts 邏輯保持不變
            const teams = [...new Set(this.exchangeData.map(d => d.team))];
            console.log('Teams found:', teams);

            // Find the global maximum Y value
            const globalMaxY = Math.ceil(Math.max(
                ...this.exchangeData.map(d => Math.max(d.total_points, d.three_points))
            ) / 1000) * 1000;

            teams.forEach(team => {
                const teamData = this.exchangeData.filter(d => d.team === team);

                let trace1 = {
                    type: "scatter",
                    mode: "lines+markers",
                    name: "Total Points",
                    x: teamData.map(d => d.season),
                    y: teamData.map(d => d.total_points),
                };

                let trace2 = {
                    type: "bar",
                    name: "Three-Point Scores",
                    x: teamData.map(d => d.season),
                    y: teamData.map(d => d.three_points),
                    marker: {
                        color: 'orange',
                        line: {
                            color: 'black',
                            width: 0
                        }
                    }
                };

                let layout = {
                    title: `${team} Performance by Season`,
                    xaxis: {
                        title: "Season",
                        showline: true
                    },
                    yaxis: {
                        title: "Scores",
                        showline: true,
                        range: [0, globalMaxY],
                        tickformat: ",",
                        tickvals: Array.from({ length: globalMaxY / 1000 + 1 }, (_, i) => i * 1000),
                    },
                    barmode: 'overlay',
                    bargap: 0,
                };

                let teamDiv = document.createElement("div");
                teamDiv.style.width = "600px";
                teamDiv.style.height = "400px";
                teamDiv.id = `chart-${team.replace(/\s/g, '-')}`;
                document.getElementById("row").appendChild(teamDiv);

                Plotly.newPlot(teamDiv.id, [trace1, trace2], layout);
            });
        }
    }
}
</script>

<style scoped>
.chart-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    padding: 20px;
    min-height: 400px;
}
</style>