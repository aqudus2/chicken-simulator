<template>
  <v-card
    class="mx-auto text-center"
    color="blue darken-2"
    max-width="600"
    dark
  >
    <v-card-text>
      <v-sheet color="rgba(0, 0, 0, .12)">
        <v-sparkline
          :model-value="eggProductionValues"
          color="rgba(255, 255, 255, .9)"
          height="150"
          padding="32"
          stroke-linecap="round"
          smooth
          :gradient="['#FFA726', '#FF7043']"
          line-width="3"
          auto-line-width
          show-labels
        >
          <template v-slot:label="item">
            <div class="sparkline-tooltip">
              {{ formatLabel(item.value) }}
            </div>
          </template>
        </v-sparkline>
      </v-sheet>
    </v-card-text>

    <v-card-text>
      <div class="text-h4 font-weight-thin">
        Egg Production Last {{ days }}d
      </div>
      <div class="text-subtitle-1 mt-2">
        Total: {{ totalEggs }} eggs | Avg: {{ averageEggs }}/day
      </div>      
    </v-card-text>

    <v-divider></v-divider>
  </v-card>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useChickenStore } from '@/stores/chicken'
import { useRouter } from 'vue-router'

const chickenStore = useChickenStore()
const router = useRouter()
const days = ref(30)

// Format label function
const formatLabel = (value) => {
  if (value === 0) return '0'
  return `${value}🥚`
}

// Existing computed properties...
const eggProductionValues = computed(() => {
  if (!chickenStore.eggProductions.length) return []

  const dateEggMap = new Map()
  const endDate = new Date()
  const startDate = new Date()
  startDate.setDate(endDate.getDate() - days.value)

  for (let d = new Date(startDate); d <= endDate; d.setDate(d.getDate() + 1)) {
    const dateKey = d.toISOString().split('T')[0]
    dateEggMap.set(dateKey, 0)
  }

  chickenStore.eggProductions.forEach(production => {
    const productionDate = new Date(production.production_date)
    const dateKey = productionDate.toISOString().split('T')[0]
    
    if (dateEggMap.has(dateKey)) {
      dateEggMap.set(dateKey, dateEggMap.get(dateKey) + production.egg_count)
    }
  })

  return Array.from(dateEggMap.values())
})

const totalEggs = computed(() => {
  return eggProductionValues.value.reduce((sum, value) => sum + value, 0)
})

const averageEggs = computed(() => {
  const total = totalEggs.value
  const dayCount = eggProductionValues.value.length
  return dayCount > 0 ? (total / dayCount).toFixed(1) : '0'
})

onMounted(async () => {
  if (!chickenStore.eggProductions.length) {
    await chickenStore.fetchEggProductions()
  }
})
</script>

<style scoped>
.sparkline-tooltip {
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 11px;
  font-weight: 600;
  white-space: nowrap;
  box-shadow: 0 2px 4px rgba(0,0,0,0.3);
}
</style>