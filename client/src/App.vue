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
import {useDateFormat} from '@vueuse/core'

use([
  CanvasRenderer,
  LineChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  PieChart,
  GridComponent
]);

// provide(THEME_KEY, "dark");

const option = ref({
  xAxis: {
    type: 'category',
    data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      data: [820, 932, 901, 934, 1290, 1330, 1320],
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
  const data = await fetch(import.meta.env.VITE_API + '/pingjun').then(r => r.json())
  option.value.series[0].data.push(data.pingjun)
  option.value.series[0].data.shift()
  option.value.xAxis.data.push(useDateFormat(new Date(),'HH:mm:ss').value)
  option.value.xAxis.data.shift()
  console.log(data)
}, 300)
</script>

<template>
  <div class="h-screen">
    <v-chart class="h-[567px]" :option="option" />
    <button class="bg-black text-white rounded-md p-2">按钮</button>
  </div>
</template>
