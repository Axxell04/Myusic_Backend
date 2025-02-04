<script lang="ts">
	import type { MessageRes } from "$lib/interfaces/messageWS.js";
	import type { Playlist } from "$lib/interfaces/playlist.js";
	import { onMount } from "svelte";

    interface Props {
        setToastMessage: (m: string) => void
        WS?: WebSocket
        toggleModalNewPlsIsVisible: (visible?: boolean) => void
        toggleModalDeletePlsIsVisible: (visible?: boolean) => void
        getPlaylists: (target?: Playlist[]) => Promise<Playlist[] | undefined>
    }

    let { setToastMessage, WS, toggleModalNewPlsIsVisible, getPlaylists, toggleModalDeletePlsIsVisible }: Props = $props();
    
    
    function setWSEvents (ws: WebSocket) {
        ws.onopen = (ev: Event) => {
            console.log("WS Conectado")
            // setInterval(() => {
            //     WS.send(JSON.stringify({type: 'ping'}))
            // }, 2000)
        }
    
        ws.onmessage = (ev: MessageEvent) => {
            const data: MessageRes = JSON.parse(ev.data);
            console.log(data)
            if (data.command_received === "download") {
                // message = data.message;
                if (data.message.toLowerCase() === "success") {
                    setToastMessage("Descarga realizada");
                }
            } else if (data.command_received === "create_playlist") {
                toggleModalNewPlsIsVisible(false);
                getPlaylists();
                setToastMessage(data.message);
            } else if (data.command_received === "delete_playlist") {
                toggleModalDeletePlsIsVisible(false);
                getPlaylists();
                setToastMessage(data.message);
            }
        }
        
    }

    $effect(() => {
        if (WS) {
            setWSEvents(WS)
        }
    })

</script>
