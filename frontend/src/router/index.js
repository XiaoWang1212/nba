import { createRouter, createWebHistory } from 'vue-router'
import NbaStatsGraph from '@/components/NbaStatsGraph.vue'
import TeamsTotalScore from '@/components/TeamsTotalScore.vue'
import TeamsTotalDefense from '@/components/TeamsTotalDefense.vue'
import TeamsTotalStats from '@/components/TeamsTotalStats.vue'
import TeamsAnalysisView from '@/views/TeamsAnalysisView.vue'
import HomePage from '@/views/HomePage.vue'
import SelectTeam from '@/views/SelectTeam.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomePage,
  },
  {
    path: '/select-team',
    name: 'select-team',
    component: SelectTeam,
  },
  {
    path: '/stats/:team?',
    name: 'stats',
    component: NbaStatsGraph,
    props: true,
  },
  {
    path: '/score',
    name: 'score',
    component: TeamsTotalScore,
    props: (route) => ({ 
      teams: route.query.teams ? route.query.teams.split(',') : [] 
    })
  },
  {
    path: '/defense',
    name: 'defense',
    component: TeamsTotalDefense, 
    props: (route) => ({ 
      teams: route.query.teams ? route.query.teams.split(',') : [] 
    })
  },
  {
    path: '/team-stats',
    name: 'team-stats',
    component: TeamsTotalStats,
  },
  {
    path: '/teams-analysis',
    name: 'teams-analysis',
    component: TeamsAnalysisView,
    props: (route) => ({ 
      teams: route.query.teams ? route.query.teams.split(',') : [] 
    })
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
