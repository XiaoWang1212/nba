<template>
  <div class="analysis-container">
    <div class="charts-wrapper">
      <div
        v-for="(type, index) in ['score', 'defense']"
        :key="index"
        class="chart-box"
        :class="{
          expanded: focusedChart === type,
          collapsed: focusedChart && focusedChart !== type,
          collapsing: isCollapsing,
        }"
        @click="!focusedChart && handleCardClick($event, type)"
      >
        <component
          :is="type === 'score' ? 'TeamsTotalScore' : 'TeamsTotalDefense'"
        />
      </div>
      <div v-if="focusedChart" class="overlay" @click="resetFocus"></div>
    </div>
  </div>
</template>

<script>
  import TeamsTotalScore from "@/components/TeamsTotalScore.vue";
  import TeamsTotalDefense from "@/components/TeamsTotalDefense.vue";
  export default {
    components: {
      TeamsTotalScore,
      TeamsTotalDefense,
    },
    data() {
      return {
        focusedChart: null,
        isCollapsing: false,
      };
    },
    methods: {
      handleCardClick(event, chartName) {
        if (this.focusedChart === chartName) {
          this.isCollapsing = true;
          setTimeout(() => {
            this.isCollapsing = false;
            this.focusedChart = null;
          }, 300);
        } else {
          const card = event.currentTarget;
          const rect = card.getBoundingClientRect();
          card.style.setProperty("--original-width", `${rect.width}px`);
          card.style.setProperty("--original-height", `${rect.height}px`);
          card.style.setProperty("--original-top", `${rect.top}px`);
          card.style.setProperty("--original-left", `${rect.left}px`);
          this.focusedChart = chartName;
        }
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
  .analysis-container {
    min-height: 100vh;
    padding: 20px;
    position: relative;
    overflow: hidden;
  }

  .charts-wrapper {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
    max-width: 1800px;
    margin: 0 auto;
    position: relative;
    z-index: 1;
  }

  .chart-box {
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
    cursor: pointer;
    position: relative;
    min-height: 600px;
    transform-origin: center;
    display: flex;
    flex-direction: column;
    z-index: 1;
  }

  .chart-box:not(.expanded):not(.collapsed):hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  }

  .chart-box.expanded {
    position: fixed;
    z-index: 12; 
    animation: expandFromOrigin 0.3s ease-out forwards;
    background: white;
    pointer-events: auto;
    cursor: default;
  }

  .chart-box.expanded :deep(.team-selection-form),
  .chart-box.expanded :deep(.chart-container) {
    pointer-events: auto;
    position: relative;
    z-index: 13; 
    cursor: default;
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
    pointer-events: auto;
  }

  .chart-box.collapsing {
    animation: collapseToOrigin 0.3s ease-out forwards;
  }

  .chart-box.collapsed {
    transform: scale(0.95);
    opacity: 0.6;
    pointer-events: none;
    z-index: 1;
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

  @media (max-width: 1024px) {
    .charts-wrapper {
      grid-template-columns: 1fr;
    }

    .chart-box.expanded {
      width: 95vw;
      height: 95vh;
    }
  }
</style>
