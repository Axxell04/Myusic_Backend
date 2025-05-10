<script lang="ts">
	import type { Playlist } from "$lib/interfaces/playlist.js";
import Icon from "@iconify/svelte";
	import { fade, fly, scale, slide } from "svelte/transition";


    interface Props {
        managerMenuIsVisible: boolean
        WS?: WebSocket
        sendMessage: (command: string, content: object | string) => void
        toggleModalAddMusicIsVisible: (visible?: boolean) => void
        toggleModalRemoveMusicIsVisible: (visible?: boolean) => void
        playlistSelected: Playlist | undefined
    }

    let { managerMenuIsVisible, WS, sendMessage, toggleModalAddMusicIsVisible, playlistSelected, toggleModalRemoveMusicIsVisible }: Props = $props()

    let urlToDownload = $state("");
    let alertsInput = $state({
        url: false
    });

    $effect(() => {
        if (urlToDownload) {
            alertsInput.url = false;
        }
    })

    function downloadNew () {
        if (urlToDownload) {
            sendMessage("download", urlToDownload);
            urlToDownload = "";
        } else {
            alertsInput.url = true;
            setTimeout(() => {
                alertsInput.url = false;
            }, 2000)
        }
    }

    $inspect(alertsInput)

</script>

{#if managerMenuIsVisible}
<div transition:fly class="flex flex-wrap gap-2 px-3 pb-3 ">
    <div class="flex flex-wrap gap-2 place-items-center">
        <button class="text-center text-zinc-900 rounded-full py-1 px-3 border border-transparent bg-lime-500 hover:bg-lime-400 hover:border-lime-600"
        onclick={downloadNew}
        >
            Descargar Nuevo
        </button>

        <input bind:value={urlToDownload} class="w-28 h-7 outline-none px-1 border {alertsInput.url ? 'border-red-500' : 'border-lime-500'} bg-transparent rounded-lg" placeholder="Link.." type="text">

    </div>

    {#if playlistSelected?.id !== 0 }
    <div transition:fade class="flex flex-row gap-2 text-zinc-900 place-content-center mx-auto">
        <button class="flex flex-row gap-1 bg-lime-500 hover:bg-lime-400 rounded-xl px-2 py-1 place-items-center" 
        onclick={() => toggleModalAddMusicIsVisible()}
        >
            <Icon icon="fa-solid:plus" />
            <span>
                Canción
            </span>
        </button>
        <button class="flex flex-row gap-1 bg-red-400 hover:bg-red-300 rounded-xl px-2 py-1 place-items-center"
        onclick={() => toggleModalRemoveMusicIsVisible()}
        >
            <Icon icon="fa-solid:trash-alt" />
            <span>
                Canción
            </span>
        </button>
    </div>
    {/if}

</div>
{/if}