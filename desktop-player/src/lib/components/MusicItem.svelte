<script lang="ts">
	import type { Music } from "$lib/interfaces/music.js";

    interface Props {
        music: Music
        musicSelected: Music | undefined
        selectMusic: (music: Music) => void
    }

    let {music, musicSelected, selectMusic}: Props = $props()

    let isSelected = $derived(music.id === musicSelected?.id);

</script>

<button onclick={()=>selectMusic(music)}>
    <div class="flex flex-col hover:bg-stone-100/10 px-4 py-1.5 border rounded-full {isSelected ? 'border-lime-400' : 'border-transparent'}">
        <span class="line-clamp-1 text-start">
            {music.name}
        </span>
        <div class="flex flex-row justify-between font-light text-stone-400">
            <span>
                {music.author}
            </span>
            <span>
                {music.duration}
            </span>
        </div>
    </div>
</button>