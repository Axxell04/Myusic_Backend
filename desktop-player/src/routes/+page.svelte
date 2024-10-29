<script lang="ts">
	import type { Music } from "$lib/interfaces/music.js";
	import MusicsList from "$lib/sections/MusicsList.svelte";
	import PlayerBar from "$lib/sections/PlayerBar.svelte";
	import { onMount } from "svelte";

    // Info player
    let playerCurrentTime = $state({asNumber: 0, asString: '00:00'})
    let playerTotalTime = $state({asNumber: 0, asString: '00:00'})
    let playing = $state(false);

    let audioELement: HTMLAudioElement;

    // Musics
    let musics: Music[] = $state([])
    let previusMusic: Music | undefined = $state()
    let nextMusic: Music | undefined = $state();
    let musicSelected: Music | undefined = $state();
    let musicURL = $derived(musicSelected ? `http://localhost:8000/download/${musicSelected.id}` : '')

    // Player functions 
    function play () {
        if (audioELement) {
            audioELement.play();
        }
    }

    function pause () {
        if (audioELement) {
            audioELement.pause();
        }
    }

    function selectMusic (music: Music) {
        musicSelected = music;
        const indexPrev = musics.indexOf(musicSelected) - 1
        const indexNext = musics.indexOf(musicSelected) + 1

        if (indexPrev >= 0) {
            previusMusic = musics[indexPrev];
        } else {
            previusMusic = undefined;
        }

        if (indexNext < musics.length) {
            nextMusic = musics[indexNext];
        } else {
            nextMusic = undefined;
        }
    }
    
    function playPreviusMusic () {
        if (previusMusic) {
            selectMusic(previusMusic);
        }
    }

    function playNextMusic () {
        if (nextMusic) {
            selectMusic(nextMusic);
        }
    }

    function updatePlayerCurrentTime (e: Event) {
        const target = e.target as HTMLInputElement;
        const value = parseInt(target.value);

        if (audioELement) {
            audioELement.currentTime = value;
        }
    }

    function convertTime (time: number) {
        let result = ''
        const minutes = Math.floor(time / 60);
        const seconds = Math.floor(time % 60);
        if (!Number.isNaN(minutes) && !Number.isNaN(seconds)) {
            result = `${minutes < 10 ? '0' : ''}${minutes}:${seconds < 10 ? '0' : ''}${seconds}`
        }

        return result
    }
    
    function printCurrentTime (e: Event) {
        const target = e.target as HTMLAudioElement;
        const currentTime = target.currentTime;
        const totalTime = target.duration;
        
        playerTotalTime.asNumber = Math.floor(totalTime);
        playerCurrentTime.asNumber = Math.floor(currentTime);
        playerTotalTime.asString = convertTime(totalTime);
        playerCurrentTime.asString = convertTime(currentTime);

        if (currentTime === totalTime && nextMusic) {
            selectMusic(nextMusic);
        }
    }

    async function getMusics () {
        const res = await fetch('http://localhost:8000/get_musics/')
        const data: Music[] = await res.json();
        musics = data;
    }

    onMount(getMusics)

</script>

<main class="flex flex-col h-dvh max-h-dvh w-full">
    <audio src={musicURL} class="hidden" bind:this={audioELement} controls autoplay ontimeupdate={e=>printCurrentTime(e)} onplay={()=>playing = true} onpause={()=>playing = false}>
    </audio>
    <MusicsList {musics} {selectMusic} {musicSelected} />
    <section class="mt-auto">
        <PlayerBar {playerCurrentTime} {playerTotalTime} {updatePlayerCurrentTime} {playing} {play} {pause} {playNextMusic} {playPreviusMusic} {musicSelected} />
    </section> 
</main>