<script lang="ts">
	import MusicItem from "$lib/components/MusicItem.svelte";
import type { Music } from "$lib/interfaces/music.js";

    interface Props {
        musics: Music[]
        musicSelected: Music | undefined
        selectMusic: (music: Music) => void
    }

    let {musics, selectMusic, musicSelected}: Props = $props()

</script>

<!-- <div class="flex flex-col max-h-full gap-2 overflow-auto p-2"> -->
<div class="scroll-app flex flex-col gap-2 p-2 h-full overflow-auto w-full">
    {#each musics as music}
        <MusicItem {musicSelected} {music} {selectMusic} />
    {/each}
</div>