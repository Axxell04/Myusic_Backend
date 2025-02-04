<script lang="ts">
	import { scale } from "svelte/transition";

    interface Props {
        message: string
    }

    let { message }: Props = $props()

</script>

{#if message}
<section transition:scale class="w-full absolute top-5">
    <div class="w-fit mx-auto py-2 px-3 rounded-lg bg-zinc-800 border border-lime-500 text-lime-400">
        {message}
    </div>
</section>
{/if}