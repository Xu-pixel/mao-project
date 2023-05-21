<script setup>
import { ref, provide, reactive } from 'vue'
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { LineChart, PieChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
} from "echarts/components";
import VChart, { THEME_KEY } from "vue-echarts";
import { useDateFormat, useFetch } from '@vueuse/core'
import { NMessageProvider } from 'naive-ui'
import Operations from './components/Operations.vue';
use([
  CanvasRenderer,
  LineChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  PieChart,
  GridComponent
]);

const option = ref({
  title:{
    text:'MAO.'
  },
  xAxis: {
    type: 'category',
    data: Array(10).fill('-')
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      data: Array(10).fill(0),
      type: 'line',
      itemStyle: {
        color: 'rgb(255, 200, 100)'
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [
            {
              offset: 0,
              color: 'rgb(255, 200, 100)' // 0% 处的颜色
            },
            {
              offset: 1,
              color: 'rgba(255, 200, 100,0.05)' // 100% 处的颜色
            }
          ]
        }
      },
      smooth: true
    },
  ],
});

setInterval(async () => {
  const { data } = await useFetch(import.meta.env.VITE_API + '/pingjun').json()
  option.value.series[0].data.push(data.value.pingjun)
  option.value.series[0].data.shift()
  option.value.xAxis.data.push(useDateFormat(new Date(), 'HH:mm:ss').value)
  option.value.xAxis.data.shift()
}, 1000)
</script>

<template>
  <div class="h-screen  font-major">
    <NMessageProvider>
      <div class="bg-yellow-50 h-16 p-4 flex items-center shadow-md justify-between">
        <p class="text-xl font-bold ">
          Mao.
        </p>
        <p>
          Version 0.1
        </p>
      </div>
      <div class="p-8">
        <v-chart class="h-[567px] p-6 rounded-xl shadow-xl" :option="option" autoresize />
      </div>
      <Operations />
    </NMessageProvider>
  </div>
</template>
