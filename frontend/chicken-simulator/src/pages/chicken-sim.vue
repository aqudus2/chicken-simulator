<template>
    <v-container>
        <!-- Title -->
        <v-row>
            <v-col cols="12">
                <v-card color="blue lighten-2" dark class="text-center">
                    <v-card-title class="headline justify-center">
                        <v-icon left>mdi-egg</v-icon>
                        Chicken Simulator 
                    </v-card-title>
                </v-card>
            </v-col>
        </v-row>

        <!-- Production Overview -->
        <v-row class="mt-4">
            <!-- Productivity Trend Section -->
            <v-col cols="12" md="6">
                <v-card 
                    color="blue lighten-3" 
                    class="pa-4 text-center"
                    height="400"
                >
                    <v-card-title class="justify-center">
                        <v-icon left>mdi-chart-line</v-icon>
                        Production Overview
                    </v-card-title>
                    <v-divider class="mb-3"></v-divider>
                    <v-card-text class="fill-height">
                        <EggProductionSparkline />
                    </v-card-text>
                </v-card>
            </v-col>

            <!-- Daily Production -->
            <v-col cols="12" md="6">
                <v-card 
                    color="blue lighten-3" 
                    class="pa-4 text-center"
                    height="400"
                >
                    <v-card-title class="justify-center">
                        <v-icon left>mdi-chart-pie</v-icon>
                        Daily Coop Production
                    </v-card-title>
                    <v-divider class="mb-3"></v-divider>
                    <v-card-text class="fill-height">
                         <v-row>
                           <v-col cols="6" v-for="item in dailyCoopProduction" :key="item.key">
                                <v-card 
                                    class="text-center pa-2" 
                                    :color="item.hasSickChicken ? 'red-lighten-2' : 'green-lighten-1'"
                                >
                                    <v-card-title>{{ item.title }}</v-card-title>
                                    <v-card-subtitle>{{ item.value }} Eggs</v-card-subtitle>
                                </v-card>
                            </v-col>
                        </v-row>
                        <!-- View Chicken List Button -->
                        <v-row class="mt-4">
                            <v-col cols="12" class="text-center">
                                <v-btn 
                                    color="primary" 
                                    large 
                                    @click="navigateToCoopList"
                                >
                                    <v-icon left>mdi-chicken</v-icon>
                                    View Chicken List
                                </v-btn>
                            </v-col>
                        </v-row>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>

        <!-- Additional Stats Row -->
        <v-row class="mt-4">
            <v-col cols="12" sm="6" md="3">
                <v-card color="blue lighten-3" class="text-center pa-4">
                    <v-card-title class="text-h6">Total Chickens</v-card-title>
                    <div class="text-h3 font-weight-bold">{{ totalChickens }}</div>
                </v-card>
            </v-col>
            <v-col cols="12" sm="6" md="3">
                <v-card color="blue lighten-3" class="text-center pa-4">
                    <v-card-title class="text-h6">Total Eggs</v-card-title>
                    <div class="text-h3 font-weight-bold">{{ totalEggs }}</div>
                </v-card>
            </v-col>
            <v-col cols="12" sm="6" md="3">
                <v-card color="blue lighten-3" class="text-center pa-4">
                    <v-card-title class="text-h6">Active Coops</v-card-title>
                    <div class="text-h3 font-weight-bold">{{ activeCoops }}</div>
                </v-card>
            </v-col>
            <v-col cols="12" sm="6" md="3">
                <v-card color="blue lighten-3" class="text-center pa-4">
                    <v-card-title class="text-h6">Avg/Day</v-card-title>
                    <div class="text-h3 font-weight-bold">{{ avgPerDay }}</div>
                </v-card>
            </v-col>
        </v-row>        
    </v-container>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useChickenStore } from '@/stores/chicken'
import EggProductionSparkline from '@/components/EggProductionSparkline.vue'

const router = useRouter()
const chickenStore = useChickenStore()

// Navigation method
const navigateToCoopList = () => {
  router.push('/CoopList')
}

// Daily production by coop
const dailyCoopProduction = computed(() => {
  if (!chickenStore.eggProductions.length || !chickenStore.chickens.length) {
    return []
  }

  // Get today's date in the format used by the API
  const DATE_OPTIONS = { timeZone: 'Asia/Singapore' }
  const today = new Date().toLocaleDateString('en-CA', DATE_OPTIONS)

  // Create chicken to coop mapping and track sick chickens
  const chickenCoopMap = new Map()
  const coopSickMap = new Map()
  chickenStore.chickens.forEach(chicken => {
    chickenCoopMap.set(chicken.chicken_id, chicken.coop)
    if (chicken.health_status === 'Sick') {
      coopSickMap.set(chicken.coop, true)
    }
  })

  // Group production by coop for today only
  const coopProduction = new Map()
  chickenStore.eggProductions.forEach(production => {
    const prodDate = new Date(production.production_date).toLocaleDateString('en-CA', { timeZone: 'Asia/Singapore' })
    if (prodDate === today) {
      const coop = chickenCoopMap.get(production.chicken_id)
      if (coop) {
        coopProduction.set(coop, (coopProduction.get(coop) || 0) + production.egg_count)
      }
    }
  })

  // Convert to array and add sick chicken status
  return Array.from(coopProduction.entries()).map(([coop, eggs], index) => ({
    key: index + 1,
    title: `Coop ${coop}`,
    value: eggs,
    hasSickChicken: coopSickMap.get(coop) || false
  })).sort((a, b) => b.value - a.value)
})

// Dashboard stats
const totalChickens = computed(() => chickenStore.chickensCount)
const totalEggs = computed(() => {
  // Sum all egg_count values from all egg production records
  return chickenStore.eggProductions.reduce(
    (sum, production) => sum + production.egg_count, 0
  )
})
const activeCoops = computed(() => {
  const coops = new Set(chickenStore.chickens.map(c => c.coop))
  return coops.size
})
const avgPerDay = computed(() => {
  if (chickenStore.eggProductions.length === 0) return 0
  
  // Get unique dates from egg productions
  const uniqueDates = new Set(
    chickenStore.eggProductions.map(prod => 
      new Date(prod.production_date).toLocaleDateString('en-CA', { timeZone: 'Asia/Singapore' })
    )
  )
  
  // Calculate total eggs across all productions
  const totalEggsProduced = chickenStore.eggProductions.reduce(
    (sum, production) => sum + production.egg_count, 0
  )
  
  // Calculate average per day
  return uniqueDates.size > 0 ? Math.round(totalEggsProduced / uniqueDates.size) : 0
})

// Load data on mount
onMounted(async () => {
  await chickenStore.initializeData()
})
</script>