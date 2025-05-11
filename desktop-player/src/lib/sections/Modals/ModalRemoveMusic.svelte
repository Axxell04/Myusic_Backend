<script lang="ts">
	import type { Music } from "$lib/interfaces/music.js";
	import type { Playlist } from "$lib/interfaces/playlist.js";
	import { onMount } from "svelte";
	import { scale } from "svelte/transition";

    interface Props {
        modalRemoveMusicIsVisible: boolean
        toggleModalRemoveMusicIsVisible: (visible?: boolean)=>void
        sendMessage: (command: string, content: object | string) => void
        getMusics: (valueToSearch?: string, playlist?: Playlist, returning?: boolean) => Promise<Music[] | undefined>
        musicsOfPls: Music[]
        playlistSelected: Playlist | undefined
    }

    let { modalRemoveMusicIsVisible, toggleModalRemoveMusicIsVisible, sendMessage, getMusics, musicsOfPls, playlistSelected }: Props = $props()

    let listMusics: Music[] = $state([]);
    let selectedMusics: Music[] | undefined = $state([]);

    function closeModal (e: Event) {
        toggleModalRemoveMusicIsVisible();
        e.stopImmediatePropagation();
    }

    function removeMusics () {
        if (selectedMusics) {
            if (playlistSelected?.id === 0) {
                sendMessage('delete_musics', {
                    id_list: selectedMusics.map((m) => {
                        return m.id
                    })
                })
            } else {
                sendMessage('remove_music_of_playlist', {
                    playlist_id: playlistSelected?.id,
                    musics_id: selectedMusics.map((m) => {
                        return m.id
                    })
                })
            }
            // sendMessage("delete_playlist", {id: selectedMusic.id});
            // selectedMusic = undefined;
        }
    }

    async function initFunction () {
        // const data = await getMusics('', playlistSelected, true);
        // if (typeof data !== "undefined") {
        //     // listMusics = data;
        //     // listMusics = data.filter((music) => {
        //     //     if (!musicsOfPls.find((mp) => mp.id === music.id)) {
        //     //         return true;
        //     //     }
        //     // })
        // }
        listMusics = musicsOfPls;
    }

    function selectThis (e: Event, music: Music) {
        const target = e.target as HTMLButtonElement;
        if (selectedMusics?.find((m) => m.id === music.id)) {
            selectedMusics = selectedMusics.filter((m) => m.id !== music.id);
        } else {
            selectedMusics?.push(music);
        }
        // selectedMusics = ;
    }

    function thisIsSelected (music: Music) {
        if (selectedMusics?.find((m) => m.id === music.id)) {
            return true;
        }
        return false;
    }

    onMount(() => {
        initFunction();
    })

</script>

{#if modalRemoveMusicIsVisible}
<div transition:scale|global role="button" tabindex="0" onkeydown={()=>{}} class="absolute flex flex-col h-dvh w-full p-10 bg-stone-800/50 backdrop-blur-sm place-items-center place-content-center max-h-dvh"  onclick={(e) => {closeModal(e)}}>
    <div role="button" tabindex="0" onkeydown={()=>{}} class="flex flex-col max-h-full max-w-96 cursor-default border border-lime-600 p-3 bg-zinc-900 rounded-xl gap-4" onclick={(e)=>{e.stopPropagation()}}>
        <div class="flex flex-col flex-grow gap-4 place-items-center overflow-y-auto">
            <h3 class="font-semibold text-lg">
                {#if playlistSelected?.id === 0}
                Eliminar canción
                {:else}
                Remover canción
                {/if}
            </h3>            

            <div class="flex flex-col overflow-y-auto">
                <ul class="max-h-full flex flex-col gap-1">
                    {#each listMusics as music}
                    <li class="{thisIsSelected(music) ? 'hover:bg-red-400' : 'hover:bg-lime-400'} hover:text-zinc-900 {thisIsSelected(music) ? 'bg-lime-600' : ''}">
                        <button class="w-full p-1" onclick={(e) => selectThis(e, music)}>
                            {music.name}
                        </button>
                    </li>
                    {/each}
                </ul>
            </div>
        </div>
        <div class="flex flex-row gap-2 place-content-center">
            <button class="border border-lime-500 hover:bg-lime-400 hover:text-zinc-900 px-2 py-1 rounded-md" 
            onclick={removeMusics}
            >
                {#if playlistSelected?.id === 0}
                Eliminar
                {:else}
                Remover
                {/if}
            </button>
            <button class="border border-red-500 hover:bg-red-400 hover:text-zinc-900 px-2 py-1 rounded-md" onclick={()=>toggleModalRemoveMusicIsVisible()}>
                Cerrar
            </button>
        </div>
    </div>
</div>
{/if}