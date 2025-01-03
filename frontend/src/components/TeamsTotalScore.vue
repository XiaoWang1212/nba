<template>
  <div class="teams-total-score">
    <div v-if="error" class="error-message">{{ error }}</div>
    <LoadingSpinner v-else-if="isLoading" />
    <div v-else>
      <div id="score-chart" class="chart-container"></div>
    </div>
  </div>
</template>

<script>
  import Plotly from "plotly.js-dist";
  import apiService from "@/services/api";
  import LoadingSpinner from "./common/LoadingSpinner.vue";

  export default {
    name: "TeamsTotalScore",
    components: {
      LoadingSpinner,
    },
    props: {
      teams: {
        type: Array,
        required: true,
      },
    },
    data() {
      return {
        chartData: [],
        isLoading: false,
        error: null,
      };
    },
    async mounted() {
      await this.fetchTeams();
    },
    watch: {
      teams: {
        handler: "fetchTeams",
        immediate: true,
      },
    },
    methods: {
      async fetchTeams() {
        if (!this.teams.length) {
          this.error = "未選擇球隊";
          return;
        }

        this.isLoading = true;
        this.error = null;

        try {
          const teamMapping = await apiService.teams.getTeamMapping();
          const teamIds = this.teams
            .map((teamName) => teamMapping[teamName])
            .filter((id) => id);

          if (teamIds.length === 0) {
            this.error = "無效的球隊名稱";
            return;
          }

          const response = await apiService.teams.getTeamStats(
            teamIds.join(",")
          );
          if (response.status === "success" && response.data.length > 0) {
            this.chartData = response.data;
            this.$nextTick(() => {
              if (document.getElementById("score-chart")) {
                this.renderChart();
              }
            });
          } else {
            this.error = "無法取得球隊數據";
          }
        } catch (error) {
          console.error("Error:", error);
          this.error = "載入數據時發生錯誤";
        } finally {
          this.isLoading = false;
        }
      },

      renderChart() {
        const teamNames = [...new Set(this.chartData.map((d) => d.team))];
        const traces = teamNames.map((teamName) => {
          const teamYears = this.chartData.filter((d) => d.team === teamName);
          return {
            mode: "lines+markers",
            type: "scatter",
            x: teamYears.map((d) => d.season),
            y: teamYears.map((d) => d.total_points),
            name: teamName,
            marker: { size: 8 },
          };
        });

        const layout = {
          title: {
            text: "NBA 球隊總得分比較 (2018-2024)",
            font: { size: 24 },
          },
          xaxis: {
            title: "賽季年份",
            gridcolor: "#eee",
          },
          yaxis: {
            title: "總得分",
            dtick: 100,
            gridcolor: "#eee",
          },
          paper_bgcolor: "white",
          plot_bgcolor: "white",
          showlegend: true,
          autosize: true,
          margin: { t: 50, l: 50, r: 80, b: 50, pad: 4 },
        };

        Plotly.newPlot("score-chart", traces, layout, {
          responsive: true,
          displayModeBar: false,
          useResizeHandler: true,
        });
      },
    },
  };
</script>

<style scoped>
  .teams-total-score {
    padding: 10px;
    width: 100%;
    height: 100%;
  }

  .chart-container {
    width: 100%;
    height: 100%;
    min-height: 450px;
    border: 1px solid #eee;
    border-radius: 4px;
    padding: 10px;
  }

  .error-message {
    color: #ff4d4f;
    margin-bottom: 16px;
    text-align: center;
  }
</style>
