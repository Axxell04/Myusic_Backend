<script lang="ts">
	import type { Playlist } from "$lib/interfaces/playlist.js";
	import { onMount } from "svelte";
	import { scale } from "svelte/transition";

    interface Props {
        modalDeletePlsIsVisible: boolean
        toggleModalDeletePlsIsVisible: (visible?: boolean)=>void
        sendMessage: (command: string, content: object | string) => void
        getPlaylists: (returning?: boolean) => Promise<Playlist[] | undefined>
    }

    let { modalDeletePlsIsVisible, toggleModalDeletePlsIsVisible, sendMessage, getPlaylists }: Props = $props()

    let listPls: Playlist[] = $state([]);
    let selectedPls: Playlist | undefined = $state();

    function closeModal (e: Event) {
        toggleModalDeletePlsIsVisible();
        e.stopImmediatePropagation();
    }

    function deletePls () {
        if (selectedPls) {
            sendMessage("delete_playlist", {id: selectedPls.id});
            selectedPls = undefined;
        }
    }

    async function initFunction () {
        const data = await getPlaylists(true);
        if (typeof data !== "undefined") {
            listPls = data;
        }
    }

    function selectThis (e: Event, pls: Playlist) {
        const target = e.target as HTMLButtonElement;
        selectedPls = pls;
    }

    onMount(() => {
        initFunction();
        console.log("Mounted")
    })

</script>

{#if modalDeletePlsIsVisible}
<div transition:scale|global role="button" tabindex="0" onkeydown={()=>{}} class="absolute flex flex-col h-dvh w-full p-10 bg-stone-800/50 backdrop-blur-sm place-items-center place-content-center max-h-dvh"  onclick={(e) => {closeModal(e)}}>
    <div role="button" tabindex="0" onkeydown={()=>{}} class="flex flex-col max-h-full max-w-96 cursor-default border border-lime-600 p-3 bg-zinc-900 rounded-xl gap-4" onclick={(e)=>{e.stopPropagation()}}>
        <div class="flex flex-col flex-grow gap-4 place-items-center overflow-y-auto">
            <h3 class="font-semibold text-lg">
                Eliminar playlist
            </h3>            

            <div class="flex flex-col overflow-y-auto">
                <ul class="max-h-full">
                    {#each listPls as pls}
                    <li class="hover:bg-lime-400 hover:text-zinc-900 {selectedPls?.id === pls.id ? 'bg-lime-600' : ''}">
                        <button class="w-full p-1" onclick={(e) => selectThis(e, pls)}>
                            {pls.name}
                        </button>
                    </li>
                    {/each}
                </ul>
            </div>
        </div>
        <div class="flex flex-row gap-2 place-content-center">
            <button class="border border-lime-500 hover:bg-lime-400 hover:text-zinc-900 px-2 py-1 rounded-md" onclick={deletePls}>
                Eliminar
            </button>
            <button class="border border-red-500 hover:bg-red-400 hover:text-zinc-900 px-2 py-1 rounded-md" onclick={()=>toggleModalDeletePlsIsVisible()}>
                Cerrar
            </button>
        </div>
    </div>
</div>
{/if}