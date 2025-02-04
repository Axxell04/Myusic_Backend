<script lang="ts">
	import FuncWebSocket from "$lib/functionalities/FuncWebSocket.svelte";
    import type { MessageRes } from "$lib/interfaces/messageWS.js";
	import type { Music } from "$lib/interfaces/music.js";
	import type { Playlist } from "$lib/interfaces/playlist.js";
	import ManagerMenu from "$lib/sections/ManagerMenu.svelte";
	import ModalDeletePls from "$lib/sections/Modals/ModalDeletePls.svelte";
	import ModalNewPls from "$lib/sections/Modals/ModalNewPls.svelte";
	import MusicsList from "$lib/sections/MusicsList.svelte";
	import PlayerBar from "$lib/sections/PlayerBar.svelte";
	import PlaylistList from "$lib/sections/PlaylistList.svelte";
	import ToastMessage from "$lib/sections/ToastMessage.svelte";
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
    let managerMenuIsVisible = $state(false);
    let modalNewPlsIsVisible = $state(false);
    let modalDeletePlsIsVisible = $state(false);

    // Playlists
    let playlists: Playlist[] = $state([])
    let playlistSelected: Playlist | undefined = $state()

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
    let musicURL = $derived(musicSelected ? `http://${window.location.hostname}:8000/download/${musicSelected.id}` : '')

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
    async function getMusics (valueToSearch: string = '', playlist: Playlist = {id: 0, name: ""}) {
        const res = await fetch(`http://${window.location.hostname}:8000/get_musics/?value_search=${valueToSearch}&playlist_id=${playlist.id}`)
        const data: Music[] = await res.json();
        musics = data;
        musicsNormalList = musics.slice();
        musicsRandomList = randomizer(musics);
        randomMode = false;
        if (playlist.id && playlist.name) {
            playlistSelected = playlist;
        } else if (playlist.name === "Todas las canciones") {
            playlistSelected = {id: 0, name: playlist.name};
        } else {
            playlistSelected = undefined;
        }
    }

    async function getPlaylists (target?: Playlist[]) {
        const res = await fetch(`http://${window.location.hostname}:8000/get_playlists/`)
        const data: Playlist[] = await res.json();
        if (typeof target !== "undefined") {
            return data
        } else {
            playlists = [{id: 0, name: "Todas las canciones"}, ...data];
        }
    }

    // Toggle visibility elements
    function togglePlaylistIsVisible () {
        playlistIsVisible = !playlistIsVisible;
    }

    function toggleManagerMenuIsVisible () {
        managerMenuIsVisible = !managerMenuIsVisible;
    }

    function toggleModalNewPlsIsVisible (visible?: boolean) {
        if (typeof visible !== "undefined") {
            modalNewPlsIsVisible = visible;
        } else {
            modalNewPlsIsVisible = !modalNewPlsIsVisible;
        }
    }

    function toggleModalDeletePlsIsVisible (visible?: boolean) {
        if (typeof visible !== "undefined") {
            modalDeletePlsIsVisible = visible;
        } else {
            modalDeletePlsIsVisible = !modalDeletePlsIsVisible;
        }
    }

    // WEBSOCKETS

    let WS: WebSocket | undefined = $state();
    let message = $state("");

    function setToastMessage (m: string) {
        message = m;
    }

    function initWS () {
        WS = new WebSocket(`ws://${window.location.hostname}:8000`);
    }

    function sendMessage (command: string, content: object | string) {
        if (WS) {
            if (WS.OPEN) {
                WS.send(JSON.stringify({
                    command: command,
                    content: content
                }))
            }
        }
    }
    
    $effect(() => {
        if (message) {
            setTimeout(() => {
                message = "";
            }, 4000)
        }
    })

    // $inspect(modalNewPlsIsVisible)
    onMount(() => {
        getMusics('', {id: 0, name: "Todas las canciones"});
        getPlaylists();
        initWS();
    })

</script>

<main class="flex flex-col h-dvh max-h-dvh w-full overflow-hidden">
    <FuncWebSocket {getPlaylists} {WS} {setToastMessage} {toggleModalNewPlsIsVisible} {toggleModalDeletePlsIsVisible} />
    <audio src={musicURL} class="fixed hidden" bind:this={audioELement} controls autoplay onloadstart={e=>captureVolume(e)} onvolumechange={e=>captureVolume(e)} ontimeupdate={e=>captureCurrentTime(e)} onplay={()=>playing = true} onpause={()=>playing = false}>
    </audio>
    <ToastMessage {message} />
    <TopBar {getMusics} {togglePlaylistIsVisible} {playlistIsVisible} {toggleManagerMenuIsVisible} {managerMenuIsVisible} />
    <ManagerMenu {managerMenuIsVisible} {WS} {sendMessage} />
    <section class="h-full overflow-auto flex flex-row">
        <PlaylistList {playlistIsVisible} {getMusics} {playlists} {WS} {playlistSelected} {toggleModalNewPlsIsVisible} {toggleModalDeletePlsIsVisible} />
        <MusicsList {musics} {selectMusic} {musicSelected} />
    </section>
    <section class="relative mt-auto">
        <PlayerBar {playerCurrentTime} {playerTotalTime} {playerVolume} {updatePlayerCurrentTime} {updatePlayerVolume} {playing} {play} {pause} {playNextMusic} {playPreviusMusic} {musicSelected} {randomMode} {toggleRandomMode} />
    </section> 

    <ModalNewPls {modalNewPlsIsVisible} {toggleModalNewPlsIsVisible} {sendMessage} />
    {#if modalDeletePlsIsVisible}
    <ModalDeletePls {modalDeletePlsIsVisible} {toggleModalDeletePlsIsVisible} {sendMessage} {getPlaylists} />
    {/if}
</main>