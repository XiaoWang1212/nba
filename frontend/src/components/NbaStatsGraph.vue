<template>
  <div>
    <LoadingSpinner v-if="isLoading" />
    <div v-else-if="error">{{ error }}</div>
    <div v-else class="chart-container">
        <div id="row"></div>
    </div>
  </div>
</template>

<script>
  import Plotly from "plotly.js-dist";
  import apiService from "@/services/api.js";
  import LoadingSpinner from "./common/LoadingSpinner.vue";

  export default {
    name: "NbaStatsGraph",
    components: {
      LoadingSpinner,
    },
    props: {
      team: {
        type: String,
        required: true,
      },
    },
    data() {
      return {
        exchangeData: [],
        isLoading: false,
        error: null,
      };
    },
    async mounted() {
      await this.fetchData();
    },
    watch: {
      exchangeData: {
        handler(newData) {
          if (newData.length > 0) {
            console.log("Data received:", newData);
            this.$nextTick(() => {
              this.createCharts();
            });
          }
        },
        immediate: true,
      },
    },
    methods: {
      async fetchData() {
        this.isLoading = true;
        this.error = null;
        try {
          const response = await apiService.nba.getStats();
          if (response.status === "success") {
            this.exchangeData = response.data.filter(
              (d) => d.team === this.team
            );
            this.createCharts();
          }
        } catch (error) {
          console.error("Error fetching NBA stats:", error);
          this.error = "數據載入失敗";
        } finally {
          this.isLoading = false;
        }
      },
      createCharts() {
        // 清除現有圖表
        const container = document.getElementById("row");
        if (!container) {
            console.error("Container element not found");
            return;
        }
        container.innerHTML = "";

        if (this.exchangeData.length === 0) {
          this.error = "找不到該球隊數據";
          return;
        }

        // Find the global maximum Y value
        const globalMaxY =
          Math.ceil(
            Math.max(
              ...this.exchangeData.map((d) =>
                Math.max(d.total_points, d.three_points)
              )
            ) / 1000
          ) * 1000;

        let trace1 = {
          type: "scatter",
          mode: "lines+markers",
          name: "Total Points",
          x: this.exchangeData.map((d) => d.season),
          y: this.exchangeData.map((d) => d.total_points),
        };

        let trace2 = {
          type: "bar",
          name: "Three-Point Scores",
          x: this.exchangeData.map((d) => d.season),
          y: this.exchangeData.map((d) => d.three_points),
          marker: {
            color: "orange",
            line: {
              color: "black",
              width: 0,
            },
          },
        };

        let layout = {
          title: `${this.team} Performance by Season`,
          xaxis: {
            title: "Season",
            showline: true,
          },
          yaxis: {
            title: "Scores",
            showline: true,
            range: [0, globalMaxY],
            tickformat: ",",
            tickvals: Array.from(
              { length: globalMaxY / 1000 + 1 },
              (_, i) => i * 1000
            ),
          },
          barmode: "overlay",
          bargap: 0,
        };

        let teamDiv = document.createElement("div");
        teamDiv.style.width = "100%";
        teamDiv.style.height = "600px";
        teamDiv.id = `chart-${this.team.replace(/\s/g, "-")}`;
        container.appendChild(teamDiv);

        Plotly.newPlot(teamDiv.id, [trace1, trace2], layout);
      },
    },
  };
</script>

<style scoped>
.chart-container {
    padding: 20px;
    min-height: 600px;
}
</style>
