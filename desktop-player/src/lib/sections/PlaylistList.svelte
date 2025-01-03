<script lang="ts">
	import type { Playlist } from "$lib/interfaces/playlist.js";
	import { slide } from "svelte/transition";

    interface Props {
        playlists: Playlist[]
        playlistIsVisible: boolean
        getMusics: (valueToSearch?: string, playlistId?: number) => void
    }

    let {playlistIsVisible, playlists, getMusics}: Props = $props()

</script>

{#if playlistIsVisible}
<div transition:slide={{axis: "x", }} class="flex flex-col gap-1 p-2 bg-zinc-900/80 backdrop-blur overflow-auto h-full border-r border-lime-400">
    {#each playlists as playlist}
    <button class="hover:text-lime-300 text-start rounded-full py-1 px-3 border border-transparent hover:border-lime-400" onclick={()=>getMusics('', playlist.id)}>
        <div>
            <span class="line-clamp-1">
                {playlist.name}
            </span>
        </div>
    </button>
    {/each}
</div>
{/if}