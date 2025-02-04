<script lang="ts">
	import type { Playlist } from "$lib/interfaces/playlist.js";
	import Icon from "@iconify/svelte";
	import { slide } from "svelte/transition";

    interface Props {
        playlists: Playlist[]
        playlistIsVisible: boolean
        getMusics: (valueToSearch?: string, playlist?: Playlist) => void
        WS?: WebSocket
        playlistSelected: Playlist | undefined
        toggleModalNewPlsIsVisible: () => void
        toggleModalDeletePlsIsVisible: () => void
    }

    let {playlistIsVisible, playlists, getMusics, WS, playlistSelected, toggleModalNewPlsIsVisible, toggleModalDeletePlsIsVisible}: Props = $props()

    

</script>

{#if playlistIsVisible}
<div transition:slide={{axis: "x", }} class="flex flex-col gap-1 p-2 bg-zinc-900/80 backdrop-blur overflow-auto h-full border-r border-lime-400">
    <div class="flex flex-row gap-2 text-zinc-900 w-full place-content-center">
        <button class="flex flex-row gap-1 bg-lime-500 hover:bg-lime-400 rounded-xl px-2 py-1 place-items-center" onclick={toggleModalNewPlsIsVisible}>
            <Icon icon="fa-solid:plus" />
            <span>
                Playlist
            </span>
        </button>
        <button class="flex flex-row gap-1 bg-red-400 hover:bg-red-300 rounded-xl px-2 py-1 place-items-center" onclick={toggleModalDeletePlsIsVisible}>
            <Icon icon="fa-solid:trash-alt" />
            <span>
                Playlist
            </span>
        </button>
    </div>
    {#each playlists as playlist}
    <button class="hover:text-lime-300 text-start rounded-full py-1 px-3 border border-transparent hover:border-lime-400" onclick={()=>getMusics('', playlist)}>
        <div>
            <span class="line-clamp-1 {playlistSelected?.id === playlist.id ? 'text-lime-400' : '' }">
                {playlist.name}
            </span>
        </div>
    </button>
    {/each}
</div>
{/if}