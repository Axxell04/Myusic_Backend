<script lang="ts">
	import type { Music } from "$lib/interfaces/music.js";
	import type { PlayerTime } from "$lib/interfaces/playerTime.js";
    import Icon from "@iconify/svelte";
	import { scale, slide } from "svelte/transition";

    interface Props {
        playerCurrentTime: PlayerTime
        playerTotalTime: PlayerTime
        playerVolume: number
        playing: boolean
        randomMode: boolean
        musicSelected: Music | undefined
        updatePlayerCurrentTime: (e: Event) => void
        updatePlayerVolume: (e: Event) => void
        play: () => void
        pause: () => void
        playNextMusic: () => void
        playPreviusMusic: () => void
        toggleRandomMode: () => void
    }

    let {playerCurrentTime, playerTotalTime, playerVolume, playing, updatePlayerCurrentTime, updatePlayerVolume, play, pause, playNextMusic, playPreviusMusic, musicSelected, randomMode, toggleRandomMode}:Props = $props()

    let volumeIsVisible = $state(false);

    let previusIsPressed = $state(false);
    let nextIsPressed = $state(false);
    let randomIsPressed = $state(false);
    let volumeIsPressed = $state(false);

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

    function randomPressed () {
        toggleRandomMode();
        randomIsPressed = true;
        setTimeout(() => {
            randomIsPressed = false;
        }, 100)
    }

    function volumePressed () {
        toggleVolume();
        volumeIsPressed = true;
        setTimeout(() => {
            volumeIsPressed = false;
        }, 100)
    }

    function toggleVolume () {
        volumeIsVisible = !volumeIsVisible;
    }


</script>

{#if volumeIsVisible}
<div transition:slide={{axis: "y"}} class="flex flex-col px-3 border-lime-400 bg-zinc-950/30">
    <div class="flex">
        <span class="mx-auto">
            {(playerVolume*100).toFixed(0)}
        </span>
    </div>
    <div class="">
        <input type="range" class="w-full outline-none" max={1} min={0} step={0.01} value={playerVolume} oninput={e=>updatePlayerVolume(e)}>
    </div>
</div>
{/if}

<div class="flex flex-row p-3 gap-4 place-items-center border-lime-400 bg-zinc-950/30">
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
    <section class="flex flex-col gap-1 min-w-[40.70px]">
        <button onclick={()=>{volumePressed()}}>
            {#if !volumeIsPressed}
                <div in:scale>
                    <Icon icon="fa-solid:{playerVolume >= .9 ? 'volume-up' : (playerVolume >= .5 ? 'volume' : (playerVolume > .0 ? 'volume-down' : 'volume-off'))}" class="text-lime-500 text-4xl" />
                </div>
            {:else}    
                <div class="opacity-0">
                    <Icon icon="fa-solid:volume" class=" text-4xl" />
                </div>
            {/if}
        </button>
        <button onclick={()=>{randomPressed()}}>
            {#if !randomIsPressed}
                <div in:scale>
                    <Icon icon="fa-solid:random" class="{randomMode ? 'text-lime-500': 'text-lime-500/60'} text-4xl" />
                </div>
            {:else}    
                <div class="opacity-0">
                    <Icon icon="fa-solid:random" class=" text-4xl" />
                </div>
            {/if}
        </button>
    </section>
</div>