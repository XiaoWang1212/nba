<template>
  <div class="member-stats">
    <LoadingSpinner v-if="isLoading" />
    <div v-if="error" class="error-message">{{ error }}</div>
    <div v-else class="charts-container">
      <div :id="chartId"></div>
    </div>
  </div>
</template>

<script>
  import Plotly from "plotly.js-dist";
  import apiService from "@/services/api";
  import LoadingSpinner from "./common/LoadingSpinner.vue";

  export default {
    name: "MemberStats",
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
        chartData: [],
        isLoading: false,
        error: null,
        chartId: `member-chart-${Date.now()}`,
      };
    },
    async mounted() {
      this.fetchData();
    },
    beforeUnmount() {
      const element = document.getElementById("member-chart");
      if (element) {
        element.innerHTML = "";
      }
    },
    watch: {
      team: {
        immediate: true,
        handler() {
          this.fetchData();
        },
      },
    },
    methods: {
      async fetchData() {
        this.isLoading = true;
        this.error = null;
        try {
          const response = await apiService.nba.getMemberStats();
          if (response.status === "success") {
            this.chartData = response.data.filter((d) => d.team === this.team);
            if (this.chartData.length === 0) {
              this.error = "找不到該球隊數據";
              return;
            }
            this.$nextTick(() => {
              this.renderCharts();
            });
          }
        } catch (error) {
          console.error("Error fetching member stats:", error);
          this.error = "數據載入失敗";
        } finally {
          this.isLoading = false;
        }
      },

      renderCharts() {
        if (!this.chartData || this.chartData.length === 0) {
          console.error("No data available for rendering");
          return;
        }

        const container = document.getElementById(this.chartId);
        if (!container) {
          console.error("Container element not found");
          return;
        }

        container.innerHTML = "";

        const playerNames = this.chartData.map((d) => d.full_name);
        const points = this.chartData.map((d) => d.points);
        const rebounds = this.chartData.map((d) => d.rebounds);
        const assists = this.chartData.map((d) => d.assists);

        const maxRange = Math.max(...[...points, ...rebounds, ...assists]) + 10;

        const data = [
          {
            type: "scatterpolar",
            r: points,
            theta: playerNames,
            fill: "toself",
            name: "得分",
            marker: { color: "rgba(255, 99, 71, 0.8)" },
          },
          {
            type: "scatterpolar",
            r: rebounds,
            theta: playerNames,
            fill: "toself",
            name: "籃板",
            marker: { color: "rgba(54, 162, 235, 0.8)" },
          },
          {
            type: "scatterpolar",
            r: assists,
            theta: playerNames,
            fill: "toself",
            name: "助攻",
            marker: { color: "rgba(75, 192, 192, 0.8)" },
          },
        ];

        const layout = {
          title: {
            text: `${this.team} 球員數據雷達圖`,
            font: { size: 24 },
          },
          polar: {
            radialaxis: {
              visible: true,
              range: [0, maxRange],
              tickfont: { size: 14 },
            },
            angularaxis: {
              tickfont: { size: 14 },
            },
          },
          margin: { l: 100, r: 100, t: 50, b: 50 },
          showlegend: true,
          legend: { font: { size: 16 } },
          width: this.isExpanded ? 1000 : 400,
          height: this.isExpanded ? 800 : 600,
          autosize: true,
        };

        const teamDiv = document.createElement("div");
        teamDiv.style.width = "400px";
        teamDiv.style.height = "600px";
        teamDiv.id = `chart-${this.team.replace(/\s/g, "-")}`;
        container.appendChild(teamDiv);

        Plotly.newPlot(this.chartId, data, layout);
      },
    },
  };
</script>

<style scoped>
  .member-stats {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .charts-container {
    width: 100%;
    height: 100%;
    min-height: 600px;
  }

  .error-message {
    color: #ff4d4f;
    text-align: center;
    margin: 20px 0;
  }
</style>
