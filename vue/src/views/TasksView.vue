<script setup lang="ts">
import { onMounted } from 'vue';
import { getTasks } from '@/api/tasks.api';

onMounted(async () => {
    const response = await getTasks()
    console.log(response.data)
})

</script>



<template>
    <div class="o-4">TASKS</div>
</template>