<template>
  <v-container>
    <!-- Header -->
    <v-row>
      <v-col cols="12">
        <v-card color="blue lighten-2" dark class="text-center">
          <v-card-title class="headline justify-center">
            <v-icon left>mdi-chicken</v-icon>
            Chicken Details
          </v-card-title>
        </v-card>
      </v-col>
    </v-row>

    <!-- Back Button -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-btn color="grey" @click="navigateToChickenSim">
          <v-icon left>mdi-arrow-left</v-icon>
          Back to Dashboard
        </v-btn>
      </v-col>
    </v-row>

    <!-- Filter Section -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-card-title>
            <v-icon left>mdi-filter</v-icon>
            Filters
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" sm="6" md="4">
                <v-select
                  v-model="selectedBreed"
                  :items="breedOptions"
                  label="Filter by Breed"
                  clearable
                  outlined
                  dense
                  @change="applyFilters"
                ></v-select>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-select
                  v-model="selectedCoop"
                  :items="coopOptions"
                  label="Filter by Coop"
                  clearable
                  outlined
                  dense
                  @change="applyFilters"
                ></v-select>
              </v-col>
              <v-col cols="12" sm="6" md="4" class="d-flex align-center">
                <v-btn color="primary" @click="resetFilters" class="ml-2">
                  <v-icon left>mdi-refresh</v-icon>
                  Reset Filters
                </v-btn>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Chicken Details Table -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-card-title>
            <v-icon left>mdi-format-list-bulleted</v-icon>
            Chickens ({{ filteredChickens.length }})
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <!-- Loading state -->
            <div v-if="loading" class="text-center pa-4">
              <v-progress-circular indeterminate color="primary"></v-progress-circular>
              <div class="mt-2">Loading chickens...</div>
            </div>

            <!-- Chicken List -->
            <v-row v-else-if="groupedChickens.length">
              <v-col 
                v-for="group in groupedChickens" 
                :key="group.coop" 
                cols="12" 
                md="6"
                class="mb-4"
              >
                <v-card>
                  <v-subheader class="text-h6 primary--text coop-header">
                    <span class="coop-title">Coop {{ group.coop }}</span>
                    <v-chip small class="ml-2" outlined>
                      {{ group.chickens.length }} chickens
                    </v-chip>
                  </v-subheader>
                  
                  <v-list dense>
                    <v-list-item
                      v-for="chicken in group.chickens"
                      :key="chicken.chicken_id"
                      class="mb-2"
                    >
                      <v-list-item-content>
                        <v-list-item-title class="d-flex align-center mb-2">
                          <v-chip small color="primary" class="mr-2">
                            ID: {{ chicken.chicken_id }}
                          </v-chip>
                          <v-chip small color="purple" class="mr-2">
                            {{ chicken.breed }}
                          </v-chip>
                          <v-chip 
                            small 
                            :color="getHealthColor(chicken.health_status)"
                            text-color="white"
                            class="mr-2"
                          >
                            {{ chicken.health_status }}
                          </v-chip>
                        </v-list-item-title>
                        
                        <v-list-item-subtitle>
                          <div class="d-flex align-center flex-wrap">
                            <span class="mr-4">
                              <v-icon small class="mr-1">mdi-calendar</v-icon>
                              Age: {{ chicken.age }} years
                            </span>
                            <span class="mr-4">
                              <v-icon small class="mr-1">mdi-egg</v-icon>
                              Eggs: {{ chickenEggCounts[chicken.chicken_id] || 0 }}
                            </span>
                            <span class="mr-4">
                              <v-icon small class="mr-1">mdi-clock</v-icon>
                              Last Checked: {{ formatDateTime(chicken.last_checked_time) }}
                            </span>
                          </div>
                        </v-list-item-subtitle>
                      </v-list-item-content>
                      
                      <v-list-item-action>
                        <v-btn 
                          icon 
                          small 
                          @click="viewChickenDetails(chicken.chicken_id)"
                          color="primary"
                        >
                          <v-icon>mdi-eye</v-icon>
                        </v-btn>
                      </v-list-item-action>
                    </v-list-item>
                  </v-list>
                </v-card>
              </v-col>
            </v-row>
            
            <!-- No Results Message -->
            <div v-else class="text-center pa-4">
              <v-icon large color="grey">mdi-alert-circle-outline</v-icon>
              <div class="mt-2">No chickens found with the selected filters.</div>
              <v-btn color="primary" text @click="resetFilters" class="mt-2">
                Reset Filters
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Chicken Detail Dialog -->
    <v-dialog v-model="detailDialog" max-width="600px">
      <v-card v-if="selectedChicken">
        <v-card-title>
          <v-icon left>mdi-chicken</v-icon>
          Chicken #{{ selectedChicken.chicken.chicken_id }} Details
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <v-row>
            <v-col cols="6">
              <strong>ID:</strong> {{ selectedChicken.chicken.chicken_id }}
            </v-col>
            <v-col cols="6">
              <strong>Breed:</strong> {{ selectedChicken.chicken.breed }}
            </v-col>
            <v-col cols="6">
              <strong>Coop:</strong> {{ selectedChicken.chicken.coop }}
            </v-col>
            <v-col cols="6">
              <strong>Age:</strong> {{ selectedChicken.chicken.age }} years
            </v-col>
            <v-col cols="6">
              <strong>Health Status:</strong> 
              <v-chip 
                small 
                :color="getHealthColor(selectedChicken.chicken.health_status)"
                text-color="white"
                class="ml-2"
              >
                {{ selectedChicken.chicken.health_status }}
              </v-chip>
            </v-col>
            
            <v-col cols="12">
              <strong>Last Checked:</strong> {{ formatDateTime(selectedChicken.chicken.last_checked_time) }}
            </v-col>
          </v-row>
          
          <v-divider class="my-4"></v-divider>
          
          <div class="text-h6 mb-2">Production Summary</div>
          <v-row>            
            <v-col cols="6">
              <strong>Total Eggs Produced:</strong> {{ selectedChicken.total_eggs_produced }}
            </v-col>
          </v-row>
          
          <div class="text-h6 mt-4 mb-2">Recent Production History</div>
          <v-list dense>
            <v-list-item 
              v-for="production in selectedChicken.production_history.slice(0, 5)" 
              :key="production.production_id"
            >
              <v-list-item-content>
                <v-list-item-title>
                  {{ formatDate(production.production_date) }} - {{ production.egg_count }} eggs
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" text @click="detailDialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
// In the script setup section
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const navigateToChickenSim = () => {
  router.push('/chicken-sim')
}

const chickens = ref([])
const eggProductions = ref([])
const loading = ref(false)
const detailDialog = ref(false)
const selectedChicken = ref(null)

// Filter state
const selectedBreed = ref('')
const selectedCoop = ref('')

const API_BASE_URL = 'http://localhost:8000'

// Computed property to calculate total eggs per chicken from egg_production
const chickenEggCounts = computed(() => {
  const counts = {}
  eggProductions.value.forEach(production => {
    if (!counts[production.chicken_id]) {
      counts[production.chicken_id] = 0
    }
    counts[production.chicken_id] += production.egg_count
  })
  return counts
})

// Computed property for unique breed options
const breedOptions = computed(() => {
  const breeds = [...new Set(chickens.value.map(chicken => chicken.breed))]
  return breeds.sort()
})

// Computed property for unique coop options
const coopOptions = computed(() => {
  const coops = [...new Set(chickens.value.map(chicken => chicken.coop))]
  return coops.sort()
})

// Computed property for filtered chickens
const filteredChickens = computed(() => {
  return chickens.value.filter(chicken => {
    const breedMatch = !selectedBreed.value || chicken.breed === selectedBreed.value
    const coopMatch = !selectedCoop.value || chicken.coop === selectedCoop.value
    return breedMatch && coopMatch
  })
})

// Add after other computed properties
const groupedChickens = computed(() => {
  const grouped = filteredChickens.value.reduce((acc, chicken) => {
    if (!acc[chicken.coop]) {
      acc[chicken.coop] = []
    }
    acc[chicken.coop].push(chicken)
    return acc
  }, {})
  
  // Convert to sorted array
  return Object.entries(grouped)
    .sort(([coopA], [coopB]) => coopA.localeCompare(coopB))
    .map(([coop, chickens]) => ({
      coop,
      chickens
    }))
})

// Filter functions
const applyFilters = () => {
  // Filters are automatically applied through the computed property
}

const resetFilters = () => {
  selectedBreed.value = ''
  selectedCoop.value = ''
}

const getHealthColor = (status) => {
  switch(status?.toLowerCase()) {
    case 'good': return 'green'
    case 'sick': return 'red'    
    default: return 'grey'
  }
}

const formatDateTime = (dateTime) => {
  if (!dateTime) return 'N/A'
  return new Date(dateTime).toLocaleString()
}

const formatDate = (date) => {
  if (!date) return 'N/A'
  return new Date(date).toLocaleDateString()
}

const fetchChickens = async () => {
  loading.value = true
  try {
    const response = await fetch(`${API_BASE_URL}/chickens/`)
    if (response.ok) {
      chickens.value = await response.json()
    } else {
      console.error('Failed to fetch chickens')
    }
  } catch (error) {
    console.error('Error fetching chickens:', error)
  } finally {
    loading.value = false
  }
}

const populateChickens = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/chickens/populate`, {
      method: 'POST'
    })
    if (response.ok) {
      await fetchChickens()
    } else {
      console.error('Failed to populate chickens')
    }
  } catch (error) {
    console.error('Error populating chickens:', error)
  }
}

const viewChickenDetails = async (chickenId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/chickens/${chickenId}/details`)
    if (response.ok) {
      selectedChicken.value = await response.json()
      detailDialog.value = true
    } else {
      console.error('Failed to fetch chicken details')
    }
  } catch (error) {
    console.error('Error fetching chicken details:', error)
  }
}

// Add this function to fetch egg production data
const fetchEggProductions = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/egg-production/`)
    if (response.ok) {
      eggProductions.value = await response.json()
    } else {
      console.error('Failed to fetch egg productions')
    }
  } catch (error) {
    console.error('Error fetching egg productions:', error)
  }
}

// Update the onMounted function to fetch both chickens and egg productions
onMounted(async () => {
  loading.value = true
  try {
    await Promise.all([
      fetchChickens(),
      fetchEggProductions()
    ])
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.v-chip {
  margin: 2px;
}

.v-subheader {
  background-color: #f5f5f5;
  border-radius: 4px;
  margin-bottom: 8px;
}

.v-list-item {
  margin-left: 16px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  margin-bottom: 8px;
}

.v-list-item:hover {
  background-color: #f5f5f5;
}

.v-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.v-list {
  flex-grow: 1;
}

.coop-header {
  padding: 16px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.coop-title {
  margin-left: 12px;
  font-weight: 500;
  font-size: 1.125rem;
}
</style>