<template>
  <div class="teams-defense">
    <form @submit.prevent="updateChart" class="team-selection-form">
      <div v-for="n in 3" :key="n" class="team-select">
        <select v-model="selectedTeams[n - 1]">
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
    <div id="defense-chart" class="chart-container" v-show="!isLoading"></div>
  </div>
</template>

<script>
  import Plotly from "plotly.js-dist";
  import apiService from "@/services/api";

  export default {
    name: "TeamsTotalDefense",
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
      async updateChart() {
        this.error = null;
        this.isLoading = true;
        try {
          const teamIds = this.selectedTeams.filter((id) => id);
          const response = await apiService.teams.getTeamStats(
            teamIds.join(",")
          );

          if (response.status === "success" && response.data.length > 0) {
            this.chartData = response.data;
            this.renderDefenseChart();
          } else {
            this.error = "無法取得球隊數據";
          }
        } catch (error) {
          this.error = "載入數據時發生錯誤";
          console.error("Error:", error);
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
          width: 1600,
          height: 800,
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
    padding: 20px;
    max-width: 1600px;
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

  .error-message {
    color: #ff4d4f;
    margin-bottom: 16px;
  }

  .chart-container {
    width: 100%;
    height: 800px;
    border: 1px solid #eee;
    border-radius: 4px;
    padding: 16px;
  }

  .team-selection-form {
    pointer-events: auto;
  }
</style>
