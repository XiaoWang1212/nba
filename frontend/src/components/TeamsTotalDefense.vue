<template>
  <div class="teams-defense">
    <div v-if="error" class="error-message">{{ error }}</div>
    <LoadingSpinner v-else-if="isLoading" />
    <div v-else>
      <div id="defense-chart" class="chart-container"></div>
    </div>
  </div>
</template>

<script>
  import Plotly from "plotly.js-dist";
  import apiService from "@/services/api";
  import LoadingSpinner from "./common/LoadingSpinner.vue";

  export default {
    name: "TeamsTotalDefense",
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
          // 先取得球隊映射
          const teamMapping = await apiService.teams.getTeamMapping();
          // 將球隊名稱轉換為ID
          const teamIds = this.teams
            .map((teamName) => teamMapping[teamName])
            .filter((id) => id); // 過濾掉無效的ID

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
              if (document.getElementById("defense-chart")) {
                this.renderDefenseChart();
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
      renderDefenseChart() {
        const teamNames = [...new Set(this.chartData.map((d) => d.team))];
        const traces = [
          {
            x: teamNames,
            y: teamNames.map((team) =>
              this.chartData
                .filter((d) => d.team === team)
                .reduce((sum, d) => sum + d.blocks, 0)
            ),
            type: "bar",
            name: "蓋帽次數",
            marker: { color: "lightblue" },
          },
          {
            x: teamNames,
            y: teamNames.map((team) =>
              this.chartData
                .filter((d) => d.team === team)
                .reduce((sum, d) => sum + d.steals, 0)
            ),
            type: "bar",
            name: "抄球次數",
            marker: { color: "green" },
          },
          {
            x: teamNames,
            y: teamNames.map((team) =>
              this.chartData
                .filter((d) => d.team === team)
                .reduce((sum, d) => sum + d.defensive_rebounds, 0)
            ),
            type: "bar",
            name: "籃板次數",
            marker: { color: "orange" },
          },
        ];

        const layout = {
          barmode: "stack",
          title: {
            text: "NBA 球隊防守統計數據比較",
            font: { size: 30 },
          },
          xaxis: {
            title: {
              text: "球隊名稱",
              font: { size: 25 },
            },
            tickangle: -45,
            automargin: true,
          },
          yaxis: {
            title: {
              text: "防守次數",
              font: { size: 25 },
            },
            tickformat: ",d",
            dtick: 1000,
          },
          paper_bgcolor: "white",
          plot_bgcolor: "white",
          showlegend: true,
          autosize: true,
          margin: { t: 50, l: 50, r: 80, b: 50, pad: 4 },
        };

        Plotly.newPlot("defense-chart", traces, layout, {
          responsive: true,
          displayModeBar: false,
          useResizeHandler: true,
        });
      },
    },
  };
</script>

<style scoped>
  .teams-defense {
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
  }
</style>
