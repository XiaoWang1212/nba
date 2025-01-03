// src/services/api.js
const API_BASE_URL =
  process.env.VUE_APP_API_BASE_URL || "http://localhost:5000";

const apiService = {
  async get(endpoint) {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error("API request failed:", error);
      throw error;
    }
  },

  nba: {
    getStats: () => apiService.get("/api/nba-stats"),
  },

  teams: {
    getTeams: () => apiService.get('/api/teams'),
    getTeamStats: (teamIds) => apiService.get(`/api/team-stats?team_ids=${teamIds}`),
    getNbaTeams: () => apiService.get('/api/nba-teams'),
  },
  
};

export default apiService;