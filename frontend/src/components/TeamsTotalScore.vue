<template>
  <div class="teams-total-score">
    <form @submit.prevent="fetchTeamData" class="team-selection-form">
      <div v-for="n in 3" :key="n" class="team-select">
        <select v-model="selectedTeams[n - 1]" required>
          <option value="">選擇球隊 {{ n }}</option>
          <option v-for="team in teams" :key="team.id" :value="team.id">
            {{ team.full_name }}
          </option>
        </select>
      </div>
      <button type="submit" :disabled="isLoading">
        {{ isLoading ? "載入中..." : "比較球隊" }}
      </button>
    </form>

    <div v-if="error" class="error-message">{{ error }}</div>
    <div
      id="team-stats-chart"
      class="chart-container"
      v-show="!isLoading"
    ></div>
  </div>
</template>

<script>
  import Plotly from "plotly.js-dist";
  import apiService from "@/services/api";

  export default {
    name: "TeamsTotalScore",
    data() {
      return {
        teams: [],
        selectedTeams: ["", "", ""],
        chartData: [],
        isLoading: false,
        error: null,
      };
    },
    async mounted() {
      await this.fetchTeams();
    },
    methods: {
      async fetchTeams() {
        try {
          const response = await apiService.teams.getTeams();
          if (response.status === "success") {
            this.teams = response.data;
          }
        } catch (error) {
          this.error = "無法載入球隊列表";
          console.error("Error fetching teams:", error);
        }
      },
      async fetchTeamData() {
        this.error = null;
        this.isLoading = true;
        try {
          const teamIds = this.selectedTeams.filter((id) => id);
          const response = await apiService.teams.getTeamStats(
            teamIds.join(",")
          );

          if (response.status === "success" && response.data.length > 0) {
            this.chartData = response.data;
            this.$nextTick(() => {
              this.renderChart();
            });
          } else {
            this.error = "無法取得球隊數據";
          }
        } catch (error) {
          this.error = "載入數據時發生錯誤";
          console.error("Error fetching team data:", error);
        } finally {
          this.isLoading = false;
        }
      },
      renderChart() {
        const teamContainer = document.getElementById("team-stats-chart");
        teamContainer.style.display = "block";

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

        const maxY = Math.max(...this.chartData.map((d) => d.total_points));
        const minY = Math.min(...this.chartData.map((d) => d.total_points));

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
            range: [minY - 100, maxY + 100],
            dtick: 100,
            gridcolor: "#eee",
          },
          paper_bgcolor: "white",
          plot_bgcolor: "white",
          showlegend: true,
          legend: {
            x: 1,
            xanchor: "right",
            y: 1,
          },
          autosize: true,
          margin: { t: 50, l: 50, r: 80, b: 50, pad: 4 },
        };

        Plotly.newPlot("team-stats-chart", traces, layout, {
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
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
  }

  .team-selection-form {
    display: flex;
    gap: 20px;
    margin-bottom: 20px;
    flex-wrap: wrap;
  }

  .team-select select {
    padding: 8px 12px;
    min-width: 250px;
    border-radius: 4px;
    border: 1px solid #ddd;
  }

  .chart-container {
    width: 100%;
    height: 600px;
    border: 1px solid #eee;
    border-radius: 4px;
    padding: 16px;
  }
</style>
