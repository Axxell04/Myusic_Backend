<script lang="ts">
	import { scale } from "svelte/transition";

    interface Props {
        modalNewPlsIsVisible: boolean
        toggleModalNewPlsIsVisible: (visible?: boolean)=>void
        sendMessage: (command: string, content: object | string) => void
    }

    let { modalNewPlsIsVisible, toggleModalNewPlsIsVisible, sendMessage }: Props = $props()

    let nameNewPls = $state("");

    // AlertsInput
    let alertsInput = $state({
        name: false
    })

    function closeModal (e: Event) {
        toggleModalNewPlsIsVisible();
        e.stopImmediatePropagation();
    }

    function createNewPls () {
        if (nameNewPls) {
            sendMessage("create_playlist", {name: nameNewPls});
            nameNewPls = "";
        } else {
            alertsInput.name = true;
            setTimeout(() => {
                alertsInput.name = false;
            }, 2000)
        }
    }

</script>

{#if modalNewPlsIsVisible}
<div transition:scale role="button" tabindex="0" onkeydown={()=>{}} class="absolute flex flex-col h-dvh w-full bg-stone-800/50 backdrop-blur-sm place-items-center place-content-center"  onclick={(e) => {closeModal(e)}}>
    <div role="button" tabindex="0" onkeydown={()=>{}} class="flex flex-col cursor-default border border-lime-600 p-3 bg-zinc-900 rounded-xl gap-2" onclick={(e)=>{e.stopPropagation()}}>
        <div class="flex flex-col gap-1 place-items-center">
            <label for="name">Nueva playlist</label>
            <input bind:value={nameNewPls} placeholder="Nombre de la playlist" class="text-center border {alertsInput.name ? 'border-red-500' :'border-lime-500'} bg-transparent outline-none rounded-md px-1" type="text">
        </div>
        <div class="flex flex-row gap-2 place-content-center">
            <button class="border border-lime-500 hover:bg-lime-400 hover:text-zinc-900 px-2 py-1 rounded-md" onclick={createNewPls}>
                Crear
            </button>
            <button class="border border-red-500 hover:bg-red-400 hover:text-zinc-900 px-2 py-1 rounded-md" onclick={()=>toggleModalNewPlsIsVisible()}>
                Cerrar
            </button>
        </div>
    </div>
</div>
{/if}