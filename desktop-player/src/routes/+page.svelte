<script lang="ts">
	import type { Music } from "$lib/interfaces/music.js";
	import MusicsList from "$lib/sections/MusicsList.svelte";
	import PlayerBar from "$lib/sections/PlayerBar.svelte";
	import TopBar from "$lib/sections/TopBar.svelte";
	import { onMount } from "svelte";

    // Info player
    let playerCurrentTime = $state({asNumber: 0, asString: '00:00'})
    let playerTotalTime = $state({asNumber: 0, asString: '00:00'})
    let playing = $state(false);
    let randomMode = $state(false);

    let audioELement: HTMLAudioElement;

    // Musics
    let musics: Music[] = $state([])
    let musicsNormalList: Music[] = $state([])
    let musicsRandomList: Music[] = $state([])
    let musicSelected: Music | undefined = $state();
    let previusMusic: Music | undefined = $derived.by(() => {
        if (musicSelected && musics) {
            const indexPrev = musics.indexOf(musicSelected) - 1
            
            if (indexPrev < musics.length) {
                return musics[indexPrev];
            } 
        }
        return undefined
    });
    let nextMusic: Music | undefined = $derived.by(() => {
        if (musicSelected && musics) {
            const indexNext = musics.indexOf(musicSelected) + 1
            
            if (indexNext < musics.length) {
                return musics[indexNext];
            } else {
                return musics[0];
            }
        }
        return undefined
    });
    let musicURL = $derived(musicSelected ? `http://192.168.3.129:8000/download/${musicSelected.id}` : '')

    // Randomizer musics
    function randomizer (listMusic: Music[]) {
        let finalList = listMusic.slice();
        
        for (let i = finalList.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [finalList[i], finalList[j]] = [finalList[j], finalList[i]];
        }

        return finalList
    }

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

    function toggleRandomMode () {
        randomMode = !randomMode;
        
        if (randomMode) {
            musics = musicsRandomList.slice()
        } else {
            musics = musicsNormalList.slice()
            musicsRandomList = randomizer(musicsRandomList);
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

    async function getMusics (valueToSearch: string = '') {
        const res = await fetch(`http://192.168.3.129:8000/get_musics/?value_search=${valueToSearch}`)
        const data: Music[] = await res.json();
        musics = data;
        musicsNormalList = musics.slice();
        musicsRandomList = randomizer(musics);
    }

    onMount(getMusics)

</script>

<main class="flex flex-col h-dvh max-h-dvh w-full">
    <audio src={musicURL} class="hidden" bind:this={audioELement} controls autoplay ontimeupdate={e=>printCurrentTime(e)} onplay={()=>playing = true} onpause={()=>playing = false}>
    </audio>
    <TopBar {getMusics} />
    <MusicsList {musics} {selectMusic} {musicSelected} />
    <section class="mt-auto">
        <PlayerBar {playerCurrentTime} {playerTotalTime} {updatePlayerCurrentTime} {playing} {play} {pause} {playNextMusic} {playPreviusMusic} {musicSelected} {randomMode} {toggleRandomMode} />
    </section> 
</main>