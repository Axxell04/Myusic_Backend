<script lang="ts">
	import type { Music } from "$lib/interfaces/music.js";
	import Icon from "@iconify/svelte";

    interface Props {
        getMusics: (valueToSearch?: string) => void
    }

    let {getMusics}: Props = $props();

    let valueToSearch = $state("")

    function clearValueToSearch () {
        valueToSearch = '';
        getMusics();
    }

</script>


<section class="flex flex-row gap-2 p-4">
    <div class="flex flex-row gap-2 p-1 border border-lime-400 bg-transparent rounded-full">
        <input bind:value={valueToSearch} type="text" class="bg-transparent outline-none pl-1 text-zinc-50" oninput={()=>getMusics(valueToSearch)} spellcheck="false" placeholder="Buscar...">
        <div class="flex flex-row gap-1">
            <button onclick={clearValueToSearch}>
                <Icon icon="mynaui:x-circle" class="text-xl {valueToSearch ? 'text-lime-400' : 'text-lime-400/50'}" />
            </button>
            <button class="bg-lime-400 p-1 rounded-full hover:bg-lime-300" onclick={()=>getMusics(valueToSearch)}>
                <Icon icon="fa-solid:search" class="text-2xl text-zinc-900" />
            </button>
        </div>
    </div>
</section>