<template>
  <div>
    <div id="plot" style="width: 100%; height: 100vh"></div>
  </div>
</template>

<script>
  import Plotly from "plotly.js-dist";
  import apiService from "@/services/api.js";

  export default {
    name: "SelectTeam",
    data() {
      return {
        teamLogos: {
          "Atlanta Hawks": require("../assets/photos/logos/hawks.svg"),
          "Boston Celtics": require("../assets/photos/logos/celtics.svg"),
          "Brooklyn Nets": require("../assets/photos/logos/nets.svg"),
          "Charlotte Hornets": require("../assets/photos/logos/hornets.svg"),
          "Chicago Bulls": require("../assets/photos/logos/bulls.svg"),
          "Cleveland Cavaliers": require("../assets/photos/logos/cavaliers.svg"),
          "Dallas Mavericks": require("../assets/photos/logos/mavericks.svg"),
          "Denver Nuggets": require("../assets/photos/logos/nuggets.svg"),
          "Detroit Pistons": require("../assets/photos/logos/pistons.svg"),
          "Golden State Warriors": require("../assets/photos/logos/warriors.svg"),
          "Houston Rockets": require("../assets/photos/logos/rockets.svg"),
          "Indiana Pacers": require("../assets/photos/logos/pacers.svg"),
          "LA Clippers": require("../assets/photos/logos/clippers.svg"),
          "Los Angeles Lakers": require("../assets/photos/logos/lakers.svg"),
          "Memphis Grizzlies": require("../assets/photos/logos/grizzlies.svg"),
          "Miami Heat": require("../assets/photos/logos/heat.svg"),
          "Milwaukee Bucks": require("../assets/photos/logos/bucks.svg"),
          "Minnesota Timberwolves": require("../assets/photos/logos/timberwolves.svg"),
          "New Orleans Pelicans": require("../assets/photos/logos/pelicans.svg"),
          "New York Knicks": require("../assets/photos/logos/knicks.svg"),
          "Oklahoma City Thunder": require("../assets/photos/logos/thunder.svg"),
          "Orlando Magic": require("../assets/photos/logos/magic.svg"),
          "Philadelphia 76ers": require("../assets/photos/logos/76ers.svg"),
          "Phoenix Suns": require("../assets/photos/logos/suns.svg"),
          "Portland Trail Blazers": require("../assets/photos/logos/blazers.svg"),
          "Sacramento Kings": require("../assets/photos/logos/kings.svg"),
          "San Antonio Spurs": require("../assets/photos/logos/spurs.svg"),
          "Toronto Raptors": require("../assets/photos/logos/raptors.svg"),
          "Utah Jazz": require("../assets/photos/logos/jazz.svg"),
          "Washington Wizards": require("../assets/photos/logos/wizards.svg"),
        },
      };
    },
    async mounted() {
      try {
        const response = await apiService.teams.getNbaTeams();
        console.log('API Response:', response); // 檢查API響應
        
        if (response.status === 'success' && Array.isArray(response.data)) {
          this.initPlot(response.data);
        } else {
          console.error('Invalid data format:', response);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    methods: {
      initPlot(data) {
        if (!Array.isArray(data) || data.length === 0) {
          console.error('Invalid or empty data:', data);
          return;
        }

        const lookup = this.processData(data);
        const teams = Object.keys(lookup);
        const seasons = this.getUniqueSortedSeasons(data);
        const traces = this.createTraces(teams, lookup);
        const layout = this.createLayout(teams, traces, seasons);

        Plotly.newPlot("plot", traces, layout).then(() => {
          this.setupFrames(teams, seasons, lookup);
        });
      },
      processData(data) {
        if (!Array.isArray(data)) {
          console.error('Data is not an array:', data);
          return {};
        }

        const lookup = {};
        data.forEach((d) => {
          if (d && d.team) {  // 確保數據物件存在且有team屬性
            if (!lookup[d.team]) {
              lookup[d.team] = {
                x: [],
                y: [],
                text: [],
                seasons: [],
              };
            }
            lookup[d.team].x.push(d.total_defense || 0);
            lookup[d.team].y.push(d.total_offense || 0);
            lookup[d.team].text.push(d.season || '');
            lookup[d.team].seasons.push(d.season || '');
          }
        });
        return lookup;
      },

      createTraces(teams, lookup) {
        return teams.map((team) => ({
          name: team,
          x: lookup[team].x,
          y: lookup[team].y,
          text: lookup[team].seasons,
          mode: "markers",
          type: "scatter",
          marker: {
            size: 60,
            opacity: 0,
          },
          customdata: Array(lookup[team].x.length).fill(this.teamLogos[team]),
        }));
      },

      createLayout(teams, traces, seasons) {
        return {
          title: "NBA Teams Performance",
          xaxis: {
            title: "Defense",
            zeroline: true,
            zerolinewidth: 2,
            zerolinecolor: "#969696",
            showline: true,
            showgrid: true,
            gridcolor: "#bdbdbd",
            gridwidth: 1,
            linecolor: "#636363",
            linewidth: 2,
            mirror: true,
          },
          yaxis: {
            title: "Offense",
            zeroline: true,
            zerolinewidth: 2,
            zerolinecolor: "#969696",
            showline: true,
            showgrid: true,
            gridcolor: "#bdbdbd",
            gridwidth: 1,
            linecolor: "#636363",
            linewidth: 2,
            mirror: true,
          },
          hovermode: "closest",
          updatemenus: [
            {
              x: 0,
              y: 0,
              yanchor: "top",
              xanchor: "left",
              showactive: false,
              direction: "left",
              type: "buttons",
              pad: { t: 87, r: 10 },
              buttons: [
                {
                  method: "animate",
                  args: [
                    null,
                    {
                      mode: "immediate",
                      fromcurrent: true,
                      transition: { duration: 300 },
                      frame: { duration: 300, redraw: true },
                    },
                  ],
                  label: "Play",
                },
                {
                  method: "animate",
                  args: [
                    [null],
                    {
                      mode: "immediate",
                      transition: { duration: 0 },
                      frame: { duration: 0, redraw: true },
                    },
                  ],
                  label: "Pause",
                },
              ],
            },
          ],
          sliders: [
            {
              currentvalue: {
                visible: true,
                prefix: "Season:",
                xanchor: "right",
                font: { size: 20, color: "#666" },
              },
              pad: { l: 130, t: 30 },
              steps: seasons.map((season) => ({
                label: season,
                method: "animate",
                args: [
                  [season],
                  {
                    mode: "immediate",
                    transition: { duration: 300 },
                    frame: { duration: 300, redraw: true },
                  },
                ],
              })),
            },
          ],
          images: teams.map((team, i) => ({
            source: this.teamLogos[team],
            x: traces[i].x[0],
            y: traces[i].y[0],
            xref: "x",
            yref: "y",
            sizex: 1000,
            sizey: 1000,
            xanchor: "center",
            yanchor: "middle",
            sizing: "contain",
            layer: "above",
          })),
        };
      },

      setupFrames(teams, seasons, lookup) {
        const frames = seasons.map((season) => ({
          name: season,
          data: teams.map((team) => ({
            x: [lookup[team].x[lookup[team].seasons.indexOf(season)]],
            y: [lookup[team].y[lookup[team].seasons.indexOf(season)]],
          })),
        }));

        Plotly.addFrames("plot", frames);

        document.getElementById("plot").on("plotly_animatingframe", (e) => {
          this.updateImagePositions(e.frame, teams);
        });
      },

      updateImagePositions(frameData, teams) {
        const gd = document.getElementById("plot");
        const images = frameData.data.map((d, i) => ({
          source: this.teamLogos[teams[i]],
          x: d.x[0],
          y: d.y[0],
          xref: "x",
          yref: "y",
          sizex: 1000,
          sizey: 1000,
          xanchor: "center",
          yanchor: "middle",
          sizing: "contain",
          layer: "above",
        }));
        Plotly.relayout(gd, { images: images });
      },

      getUniqueSortedSeasons(data) {
        return Array.from(new Set(data.map((d) => d.season))).sort(
          (a, b) => parseInt(a.split("-")[0]) - parseInt(b.split("-")[0])
        );
      },
    },
  };
</script>

<style scoped>
  #plot {
    background-color: white;
  }
</style>
