<template>
  <div class="teams-total-stats">
    <form @submit.prevent="updateChart" class="team-selection-form">
      <!-- 球隊選擇 -->
      <div class="team-select">
        <select v-model="selectedTeam">
          <option value="">選擇球隊</option>
          <option v-for="(fullName, id) in teamNames" :key="id" :value="id">
            {{ fullName }}
          </option>
        </select>
      </div>
      <!-- 年份選擇 -->
      <div class="year-select">
        <select v-model="selectedYear">
          <option value="">選擇年份</option>
          <option v-for="year in years" :key="year" :value="year">
            {{ year }}
          </option>
        </select>
      </div>
      <button type="submit" :disabled="isLoading">
        {{ isLoading ? "載入中..." : "比較球隊" }}
      </button>
    </form>

    <div v-if="error" class="error-message">{{ error }}</div>
    <div class="charts-container" v-show="!isLoading">
      <div id="shot-structure" class="chart"></div>
      <div id="make-structure" class="chart"></div>
    </div>
  </div>
</template>

<script>
  import Plotly from "plotly.js-dist";
  import nbaData from "@/assets/data/nba.json";

  export default {
    name: "TeamsTotalStats",
    data() {
      return {
        selectedTeam: "",
        selectedYear: "",
        isLoading: false,
        error: null,
        nbaData: nbaData,
        teamNames: {
          "atlanta-hawks": "Atlanta Hawks",
          "boston-celtics": "Boston Celtics",
          "brooklyn-nets": "Brooklyn Nets",
          "charlotte-hornets": "Charlotte Hornets",
          "chicago-bulls": "Chicago Bulls",
          "cleveland-cavaliers": "Cleveland Cavaliers",
          "dallas-mavericks": "Dallas Mavericks",
          "denver-nuggets": "Denver Nuggets",
          "detroit-pistons": "Detroit Pistons",
          "golden-state-warriors": "Golden State Warriors",
          "houston-rockets": "Houston Rockets",
          "indiana-pacers": "Indiana Pacers",
          "la-clippers": "LA Clippers",
          "los-angeles-lakers": "Los Angeles Lakers",
          "memphis-grizzlies": "Memphis Grizzlies",
          "miami-heat": "Miami Heat",
          "milwaukee-bucks": "Milwaukee Bucks",
          "minnesota-timberwolves": "Minnesota Timberwolves",
          "new-orleans-pelicans": "New Orleans Pelicans",
          "new-york-knicks": "New York Knicks",
          "oklahoma-city-thunder": "Oklahoma City Thunder",
          "orlando-magic": "Orlando Magic",
          "philadelphia-76ers": "Philadelphia 76ers",
          "phoenix-suns": "Phoenix Suns",
          "portland-trail-blazers": "Portland Trail Blazers",
          "sacramento-kings": "Sacramento Kings",
          "san-antonio-spurs": "San Antonio Spurs",
          "toronto-raptors": "Toronto Raptors",
          "utah-jazz": "Utah Jazz",
          "washington-wizards": "Washington Wizards",
        },
        years: [
          "2018-19",
          "2019-20",
          "2020-21",
          "2021-22",
          "2022-23",
          "2023-24",
        ],
      };
    },
    methods: {
      updateChart() {
        if (!this.selectedTeam || !this.selectedYear) {
          this.error = "請選擇球隊和年份";
          return;
        }

        const teamData = this.nbaData.find(
          (item) =>
            item.YEAR === this.selectedYear &&
            item.TEAM === this.teamNames[this.selectedTeam]
        );

        if (!teamData) {
          this.error = "找不到對應的數據";
          return;
        }

        // 計算各種投籃數據
        const FG2A = teamData.FGA - teamData.FG3A;
        const FG3A = teamData.FG3A;
        const FTA = teamData.FTA;

        const FG2M = teamData.FGM - teamData.FG3M;
        const FG3M = teamData.FG3M;
        const FTM = teamData.FTM;

        // 繪製出手結構圖
        const trace1 = {
          type: "pie",
          labels: ["兩分球", "三分球", "罰球"],
          values: [FG2A, FG3A, FTA],
          textinfo: "label+value+percent",
          marker: {
            colors: ["#FF6347", "#FFD700", "#40E0D0"],
            line: { color: "black", width: 3 },
          },
        };

        // 繪製命中結構圖
        const trace2 = {
          type: "pie",
          labels: ["兩分球", "三分球", "罰球"],
          values: [FG2M, FG3M, FTM],
          textinfo: "label+value+percent",
          marker: {
            colors: ["#FF6347", "#FFD700", "#40E0D0"],
            line: { color: "black", width: 3 },
          },
        };

        const layout1 = {
          title: "球隊出手結構",
          margin: { t: 30, l: 0 },
          font: { size: 15 },
        };

        const layout2 = {
          title: "球隊命中結構",
          margin: { t: 30, l: 0 },
          font: { size: 15 },
        };

        Plotly.newPlot("shot-structure", [trace1], layout1);
        Plotly.newPlot("make-structure", [trace2], layout2);
      },
    },
  };
</script>

<style scoped>
  .teams-total-stats {
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
  }

  .team-selection-form {
    display: flex;
    gap: 20px;
    margin-bottom: 20px;
    align-items: center;
  }

  .team-select select,
  .year-select select {
    padding: 8px 12px;
    min-width: 200px;
    border-radius: 4px;
    border: 1px solid #ddd;
  }

  .charts-container {
    display: flex;
    gap: 20px;
    justify-content: space-between;
  }

  .chart {
    width: 48%;
    height: 400px;
    border: 1px solid #eee;
    border-radius: 4px;
    padding: 16px;
  }

  .error-message {
    color: #ff4d4f;
    margin-bottom: 16px;
  }
</style>
