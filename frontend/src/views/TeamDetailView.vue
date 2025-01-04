<template>
  <div class="detail-container">
    <div class="charts-wrapper">
      <div
        v-for="(type, index) in ['stats', 'member', 'graph']"
        :key="index"
        class="chart-box"
        :class="{
          expanded: focusedChart === type,
          collapsed: focusedChart && focusedChart !== type,
          collapsing: isCollapsing,
        }"
        @click="!focusedChart && handleCardClick($event, type)"
      >
        <div class="chart-content">
          <component
            :is="getComponent(type)"
            :team="team"
            :season="season"
            :isExpanded="focusedChart === type"
          />
        </div>
      </div>
      <div v-if="focusedChart" class="overlay" @click="resetFocus"></div>
    </div>
  </div>
</template>

<script>
  import TeamsTotalStats from "@/components/TeamsTotalStats.vue";
  import MemberStats from "@/components/MemberStats.vue";
  import NbaStatsGraph from "@/components/NbaStatsGraph.vue";

  export default {
    name: "TeamDetailView",
    components: {
      TeamsTotalStats,
      MemberStats,
      NbaStatsGraph,
    },
    props: {
      team: {
        type: String,
        required: true,
      },
      season: {
        type: String,
        required: true,
      },
    },
    data() {
      return {
        focusedChart: null,
        isCollapsing: false,
      };
    },
    mounted() {
      if (!this.team || !this.season) {
        this.$router.push({ name: "select-team" });
        return;
      }
    },
    watch: {
      team: {
        immediate: true,
        handler(newTeam) {
          if (!newTeam) {
            this.$router.push({ name: "select-team" });
          }
        },
      },
    },
    methods: {
      getComponent(type) {
        const components = {
          stats: "TeamsTotalStats",
          member: "MemberStats",
          graph: "NbaStatsGraph",
        };
        return components[type];
      },
      async handleCardClick(event, chartName) {
        if (this.focusedChart) {
          this.resetFocus();
          return;
        }

        const card = event.currentTarget;
        const rect = card.getBoundingClientRect();
        card.style.setProperty("--original-width", `${rect.width}px`);
        card.style.setProperty("--original-height", `${rect.height}px`);
        card.style.setProperty("--original-top", `${rect.top}px`);
        card.style.setProperty("--original-left", `${rect.left}px`);
        this.focusedChart = chartName;
      },
      resetFocus() {
        if (this.focusedChart) {
          this.isCollapsing = true;
          setTimeout(() => {
            this.isCollapsing = false;
            this.focusedChart = null;
          }, 300);
        }
      },
    },
  };
</script>

<style scoped>
  .detail-container {
    min-height: 100vh;
    padding: 20px;
    position: relative;
    overflow: hidden;
  }

  .charts-wrapper {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    padding: 20px;
    max-width: 100%;
    margin: 0 auto;
    position: relative;
    z-index: 1;
    height: calc(100vh - 40px);
  }

  .chart-box {
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    cursor: pointer;
    position: relative;
    min-height: 600px;
    max-height: 800px;
    transform-origin: center;
    display: flex;
    flex-direction: column;
    z-index: 1;
    overflow: auto;
  }

  .chart-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    min-height: 600px;
    position: relative;
  }

  .chart-box.expanded {
    position: fixed;
    display: flex;
    justify-content: center;
    z-index: 12;
    animation: expandFromOrigin 0.3s ease-out forwards;
    background: white;
    pointer-events: auto;
    cursor: default;
  }

  .chart-box.collapsing {
    animation: collapseToOrigin 0.3s ease-out forwards;
  }

  @keyframes expandFromOrigin {
    0% {
      transform: translate(0, 0) scale(1);
      width: var(--original-width);
      height: var(--original-height);
      top: var(--original-top);
      left: var(--original-left);
    }
    100% {
      transform: translate(-50%, -50%) scale(1);
      width: 90vw;
      height: 90vh;
      top: 50%;
      left: 50%;
    }
  }

  @keyframes collapseToOrigin {
    0% {
      transform: translate(-50%, -50%) scale(1);
      width: 90vw;
      height: 90vh;
      top: 50%;
      left: 50%;
    }
    100% {
      transform: translate(0, 0) scale(1);
      width: var(--original-width);
      height: var(--original-height);
      top: var(--original-top);
      left: var(--original-left);
    }
  }

  .chart-box:not(.expanded):not(.collapsed):hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  }

  .chart-box.expanded {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 90vw;
    height: 90vh;
    z-index: 12;
    cursor: default;
    overflow: auto;
  }

  .overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.5);
    z-index: 11;
    cursor: pointer;
  }

  .chart-box.collapsed {
    transform: scale(0.95);
    opacity: 0.6;
    pointer-events: none;
  }

  @media (max-width: 1200px) {
    .charts-wrapper {
      grid-template-columns: 1fr;
    }
  }
</style>
