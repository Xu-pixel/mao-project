<template>
    <div class="p-8 items-center justify-center flex gap-4">
        <button class="bg-black text-white rounded-md p-2 shadow-black/50 shadow-md" v-for="cmd in cmds" @click="handleCMD(cmd)">{{ cmd }}</button>
    </div>
</template>

<script setup>
import { useMessage } from 'naive-ui'
import { useFetch } from '@vueuse/core';
const cmds = [
    'a.',
    'b.',
    'c.',
    'd.'
]
const message = useMessage()
async function handleCMD(cmd) {
    const { data } = await useFetch(import.meta.env.VITE_API + '/send').post({ cmd }).json()
    message.info(JSON.stringify(data.value))
}
</script>