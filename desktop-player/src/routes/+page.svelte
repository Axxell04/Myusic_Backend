<script lang="ts">
	import type { Music } from "$lib/interfaces/music.js";
	import type { Playlist } from "$lib/interfaces/playlist.js";
	import MusicsList from "$lib/sections/MusicsList.svelte";
	import PlayerBar from "$lib/sections/PlayerBar.svelte";
	import PlaylistList from "$lib/sections/PlaylistList.svelte";
	import TopBar from "$lib/sections/TopBar.svelte";
	import { onMount } from "svelte";

    // Info player
    let playerCurrentTime = $state({asNumber: 0, asString: '00:00'})
    let playerTotalTime = $state({asNumber: 0, asString: '00:00'})
    let playerVolume = $state(0)
    let playing = $state(false);
    let randomMode = $state(false);

    let audioELement: HTMLAudioElement;

    // Visibility Elements
    let playlistIsVisible = $state(true);

    // Playlists
    let playlists: Playlist[] = $state([])

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
    let musicURL = $derived(musicSelected ? ` ${window.location.origin}/download/${musicSelected.id}` : '')

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

    //External controls funtions

    function updatePlayerCurrentTime (e: Event) {
        const target = e.target as HTMLInputElement;
        const value = parseInt(target.value);

        if (audioELement) {
            audioELement.currentTime = value;
        }
    }

    function updatePlayerVolume (e: Event) {
        const target = e.target as HTMLInputElement;
        const value = parseFloat(target.value);
        if (audioELement) {
            audioELement.volume = value;
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

    //Capture AudioElement updates
    
    function captureCurrentTime (e: Event) {
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

    function captureVolume (e: Event) {
        //console.log(e)
        const target = e.target as HTMLAudioElement;
        const volume = target.volume;
        playerVolume = volume;
    }

    // Request functions
    async function getMusics (valueToSearch: string = '', playlistId: number = 0) {
        const res = await fetch(`${window.location.origin}/get_musics/?value_search=${valueToSearch}&playlist_id=${playlistId}`)
        const data: Music[] = await res.json();
        musics = data;
        musicsNormalList = musics.slice();
        musicsRandomList = randomizer(musics);
        randomMode = false;
    }

    async function getPlaylist () {
        const res = await fetch(`${window.location.origin}/get_playlists/`)
        const data: Playlist[] = await res.json();
        playlists = [{id: 0, name: "Todas la canciones"}, ...data];
    }

    // Toggle visibility elements
    function togglePlaylistIsVisible () {
        playlistIsVisible = !playlistIsVisible;
    }

    $inspect(musics)
    onMount(() => {
        getMusics();
        getPlaylist()
    })

</script>

<main class="flex flex-col h-dvh max-h-dvh w-full overflow-hidden">
    <audio src={musicURL} class="fixed hidden" bind:this={audioELement} controls autoplay onloadstart={e=>captureVolume(e)} onvolumechange={e=>captureVolume(e)} ontimeupdate={e=>captureCurrentTime(e)} onplay={()=>playing = true} onpause={()=>playing = false}>
    </audio>
    <TopBar {getMusics} {togglePlaylistIsVisible} {playlistIsVisible} />
    <section class="h-full overflow-auto flex flex-row">
        <PlaylistList {playlistIsVisible} {getMusics} {playlists} />
        <MusicsList {musics} {selectMusic} {musicSelected} />
    </section>
    <section class="relative mt-auto">
        <PlayerBar {playerCurrentTime} {playerTotalTime} {playerVolume} {updatePlayerCurrentTime} {updatePlayerVolume} {playing} {play} {pause} {playNextMusic} {playPreviusMusic} {musicSelected} {randomMode} {toggleRandomMode} />
    </section> 
</main>