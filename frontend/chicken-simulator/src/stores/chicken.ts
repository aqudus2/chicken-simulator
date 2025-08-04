//src/stores/chicken.ts
import axios from 'axios'
import { defineStore } from 'pinia'

// Interfaces based on your models and schemas
interface Chicken {
  chicken_id: number
  coop: string
  breed: string
  age: number
  health_status: string
  last_checked_time: string
}

interface ChickenCreate {
  coop: string
  breed: string
  age: number
  health_status: string
  
}

interface ChickenUpdate {
  coop?: string
  breed?: string
  age?: number
  health_status?: string

}

interface EggProduction {
  production_id: number
  chicken_id: number
  egg_count: number
  production_date: string
}

interface EggProductionCreate {
  chicken_id: number
  egg_count: number
  production_date?: string
}

interface CoopSummary {
  coop_name: string
  total_chickens: number
  total_eggs_produced: number
  chickens: Array<{
    chicken_id: number
    breed: string
    health_status: string
    total_eggs: number
  }>
}

interface ChickenDetails {
  chicken: Chicken
  production_history: Array<{
    production_id: number
    egg_count: number
    production_date: string
  }>
  total_productions: number
  total_eggs_produced: number
}

export const useChickenStore = defineStore('chicken', {
  state: () => ({
    // Chickens
    chickens: [] as Chicken[],
    chickenLoaded: null as Chicken | null,
    chickenDetails: null as ChickenDetails | null,
    
    // Egg Production
    eggProductions: [] as EggProduction[],
    chickenEggProductions: [] as EggProduction[],
    
    // Analytics    
    coopSummary: null as CoopSummary | null,
    
    // Loading states
    loading: false,
    addChickenLoading: false,
    updateChickenLoading: false,
    deleteChickenLoading: false,
    eggProductionLoading: false,
    analyticsLoading: false,
    
    // Error states
    error: '',
    addChickenError: '',
    updateChickenError: '',
    deleteChickenError: '',
    eggProductionError: '',
    analyticsError: '',

    // Initialization state
    isInitialized: false, // Add this new state property
  }),

  getters: {
    chickensCount: (state): number => state.chickens.length,
    healthyChickensCount: (state): number => 
      state.chickens.filter(chicken => chicken.health_status === 'Good').length,
    sickChickensCount: (state): number => 
      state.chickens.filter(chicken => chicken.health_status === 'Sick').length,
    totalEggsProduced: (state): number => 
      state.coopSummary ? state.coopSummary.total_eggs_produced : 0,
    chickensByBreed: (state) => {
      const breeds: Record<string, number> = {}
      state.chickens.forEach(chicken => {
        breeds[chicken.breed] = (breeds[chicken.breed] || 0) + 1
      })
      return breeds
    },
    chickensByCoop: (state) => {
      const coops: Record<string, number> = {}
      state.chickens.forEach(chicken => {
        coops[chicken.coop] = (coops[chicken.coop] || 0) + 1
      })
      return coops
    },
    isDataEmpty: (state): boolean => {
      return state.chickens.length === 0 && state.eggProductions.length === 0
    }
  },

  actions: {
    async populateChickens() {
      this.loading = true
      this.error = ''

      try {
        const response = await axios.post('http://localhost:8000/chickens/populate')
        this.chickens = response.data
        
        // After populating chickens, seed egg production data
        await this.seedEggProductionData()
        
        // Refresh all data
        await this.initializeData()
        return response.data
      } catch (error: any) {
        this.error = error.response?.data?.detail || 'Failed to populate chickens'
        console.error('Error populating chickens:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchChickens() {
      this.loading = true
      this.error = ''

      try {
        const response = await axios.get('http://localhost:8000/chickens/')
        this.chickens = response.data
      } catch (error: any) {
        this.error = 'Failed to fetch chickens'
        console.error('Error fetching chickens:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchChickenById(chickenId: number) {
      this.loading = true
      this.error = ''

      try {
        const response = await axios.get(`http://localhost:8000/chickens/${chickenId}`)
        this.chickenLoaded = response.data
        return response.data
      } catch (error: any) {
        this.error = 'Failed to fetch chicken'
        throw error
      } finally {
        this.loading = false
      }
    },

    async addChicken(chickenData: ChickenCreate) {
      this.addChickenLoading = true
      this.addChickenError = ''

      try {
        const response = await axios.post('http://localhost:8000/chickens/', chickenData)
        this.chickens.push(response.data)
        return response.data
      } catch (error: any) {
        this.addChickenError = error.response?.data?.detail || 'Failed to add chicken'
        console.error('Error adding chicken:', error)
        throw error
      } finally {
        this.addChickenLoading = false
      }
    },

    async updateChicken(chickenId: number, chickenData: ChickenUpdate) {
      this.updateChickenLoading = true
      this.updateChickenError = ''

      try {
        const response = await axios.put(`http://localhost:8000/chickens/${chickenId}`, chickenData)
        const index = this.chickens.findIndex(chicken => chicken.chicken_id === chickenId)
        if (index !== -1) {
          this.chickens[index] = response.data
        }
        return response.data
      } catch (error: any) {
        this.updateChickenError = error.response?.data?.detail || 'Failed to update chicken'
        console.error('Error updating chicken:', error)
        throw error
      } finally {
        this.updateChickenLoading = false
      }
    },

    async deleteChicken(chickenId: number) {
      this.deleteChickenLoading = true
      this.deleteChickenError = ''

      try {
        await axios.delete(`http://localhost:8000/chickens/${chickenId}`)
        this.chickens = this.chickens.filter(chicken => chicken.chicken_id !== chickenId)
      } catch (error: any) {
        this.deleteChickenError = error.response?.data?.detail || 'Failed to delete chicken'
        console.error('Error deleting chicken:', error)
        throw error
      } finally {
        this.deleteChickenLoading = false
      }
    },

    async seedEggProductionData() {
      this.eggProductionLoading = true
      this.eggProductionError = ''

      try {
        const response = await axios.post('http://localhost:8000/egg-production/seed')
        return response.data
      } catch (error: any) {
        this.eggProductionError = error.response?.data?.detail || 'Failed to seed egg production data'
        console.error('Error seeding egg production data:', error)
        throw error
      } finally {
        this.eggProductionLoading = false
      }
    },

    async fetchEggProductions() {
      this.eggProductionLoading = true
      this.eggProductionError = ''

      try {
        const response = await axios.get('http://localhost:8000/egg-production/')
        this.eggProductions = response.data
      } catch (error: any) {
        this.eggProductionError = 'Failed to fetch egg productions'
        console.error('Error fetching egg productions:', error)
      } finally {
        this.eggProductionLoading = false
      }
    },

    async fetchChickenEggProductions(chickenId: number) {
      this.eggProductionLoading = true
      this.eggProductionError = ''

      try {
        const response = await axios.get(`http://localhost:8000/chickens/${chickenId}/egg-production`)
        this.chickenEggProductions = response.data
        return response.data
      } catch (error: any) {
        this.eggProductionError = 'Failed to fetch chicken egg productions'
        console.error('Error fetching chicken egg productions:', error)
        throw error
      } finally {
        this.eggProductionLoading = false
      }
    },

    async addEggProduction(eggData: EggProductionCreate) {
      this.eggProductionLoading = true
      this.eggProductionError = ''

      try {
        const response = await axios.post('http://localhost:8000/egg-production/', eggData)
        this.eggProductions.push(response.data)
        return response.data
      } catch (error: any) {
        this.eggProductionError = error.response?.data?.detail || 'Failed to add egg production'
        console.error('Error adding egg production:', error)
        throw error
      } finally {
        this.eggProductionLoading = false
      }
    },

    async fetchCoopSummary(coopName: string) {
      this.analyticsLoading = true
      this.analyticsError = ''

      try {
        const response = await axios.get(`http://localhost:8000/analytics/coop/${coopName}`)
        this.coopSummary = response.data
        return response.data
      } catch (error: any) {
        this.analyticsError = error.response?.data?.detail || 'Failed to fetch coop summary'
        console.error('Error fetching coop summary:', error)
        throw error
      } finally {
        this.analyticsLoading = false
      }
    },

    async fetchChickenDetails(chickenId: number) {
      this.loading = true
      this.error = ''

      try {
        const response = await axios.get(`http://localhost:8000/chickens/${chickenId}/details`)
        this.chickenDetails = response.data
        return response.data
      } catch (error: any) {
        this.error = error.response?.data?.detail || 'Failed to fetch chicken details'
        console.error('Error fetching chicken details:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    clearErrors() {
      this.error = ''
      this.addChickenError = ''
      this.updateChickenError = ''
      this.deleteChickenError = ''
      this.eggProductionError = ''
      this.analyticsError = ''
    },

    async initializeData() {
      if (this.isInitialized) {
        return
      }

      this.loading = true
      this.error = ''

      try {
        await Promise.all([
          this.fetchChickens(),
          this.fetchEggProductions(),
        ])
        this.isInitialized = true
      } catch (error: any) {
        this.error = 'Failed to initialize data'
        console.error('Error initializing data:', error)
      } finally {
        this.loading = false
      }
    },

    // Add a new reset action
    resetStore() {
      this.chickens = []
      this.chickenLoaded = null
      this.chickenDetails = null
      this.eggProductions = []
      this.chickenEggProductions = []
      this.coopSummary = null
      this.isInitialized = false
      this.clearErrors()
    }
  },
})