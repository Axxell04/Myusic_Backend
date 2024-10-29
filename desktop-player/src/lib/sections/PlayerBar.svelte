<script lang="ts">
	import type { Music } from "$lib/interfaces/music.js";
	import type { PlayerTime } from "$lib/interfaces/playerTime.js";
    import Icon from "@iconify/svelte";
	import { scale } from "svelte/transition";

    interface Props {
        playerCurrentTime: PlayerTime
        playerTotalTime: PlayerTime
        playing: boolean
        musicSelected: Music | undefined
        updatePlayerCurrentTime: (e: Event) => void
        play: () => void
        pause: () => void
        playNextMusic: () => void
        playPreviusMusic: () => void
    }

    let previusIsPressed = $state(false)
    let nextIsPressed = $state(false);

    function previusPressed () {
        previusIsPressed = true;
        setTimeout(() => {
            previusIsPressed = false;
        }, 100)
    }

    function nextPressed () {
        nextIsPressed = true;
        setTimeout(() => {
            nextIsPressed = false;
        }, 100)
    }

    let {playerCurrentTime, playerTotalTime, playing, updatePlayerCurrentTime, play, pause, playNextMusic, playPreviusMusic, musicSelected}:Props = $props()

</script>

<div class="flex flex-row p-3 gap-4 place-items-center border-t border-lime-400">
    <section class="flex flex-row gap-2">
        <button onclick={()=>{playPreviusMusic(); previusPressed()}}>
            {#if !previusIsPressed}
                <div in:scale>
                    <Icon icon="fa-solid:step-backward" class="text-lime-500 text-3xl" />
                </div>
            {:else}
                <div class="opacity-0">
                    <Icon icon="fa-solid:step-backward" class="text-lime-500 text-3xl" />
                </div>
            {/if}
        </button>
        <button onclick={playing ? pause : play}>
            {#if playing}
                <div in:scale>
                    <Icon icon="fa-solid:pause" class="text-lime-500 text-3xl" />
                </div>
            {:else}    
                <div in:scale>
                    <Icon icon="fa-solid:play" class="text-lime-500 text-3xl" />
                </div>
            {/if}
        </button>
        <button onclick={()=>{playNextMusic(); nextPressed()}}>
            {#if !nextIsPressed}
                <div in:scale>
                    <Icon icon="fa-solid:step-forward" class="text-lime-500 text-3xl" />            
                </div>
            {:else}   
                <div class="opacity-0">
                    <Icon icon="fa-solid:step-forward" class="text-lime-500 text-3xl" />            
                </div>
            {/if}
        </button>
    </section>
    <section class="flex flex-col flex-grow gap-1">
        <div class="flex flex-col place-items-start">
            <span class="text-lg line-clamp-1">{musicSelected ? musicSelected.name : '----------------'}</span>
            <span class="font-light text-stone-400">{musicSelected ? musicSelected.author : '-------'}</span>
        </div>
        <div class="flex flex-col">
            <input class="outline-none" type="range" name="" id="" value={playerCurrentTime.asNumber} max={playerTotalTime.asNumber} oninput={(e)=>updatePlayerCurrentTime(e)}>
            <div class="flex flex-row justify-between text-stone-400 font-light">
                <span>{!playerCurrentTime.asString ? '00:00' : playerCurrentTime.asString}</span>
                <span>{!playerTotalTime.asString ? '00:00' : playerTotalTime.asString}</span>
            </div>
        </div>
    </section>
    <section class="">
        <button>
            <Icon icon="fa-solid:chevron-circle-up" class="text-lime-500 text-4xl" />
        </button>
    </section>
</div>