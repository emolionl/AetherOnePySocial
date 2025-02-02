<script lang="ts">
    import { onMount } from 'svelte';
    import { token } from '$lib/auth';
    import { getKeys } from '$lib/auth';
    import { goto } from '$app/navigation';

    let keys: any[] = [];
    let error = '';

    onMount(async () => {
        if (!$token) {
            goto('/login');
            return;
        }

        try {
            keys = await getKeys($token);
        } catch (e) {
            error = 'Failed to load keys';
        }
    });

    function viewKeyDetails(keyId: string) {
        goto(`/session-keys/${keyId}`);
    }
</script>

<div class="min-h-screen bg-gray-100">
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div class="px-4 py-6 sm:px-0">
            <h1 class="text-3xl font-bold text-gray-900">Your Keys</h1>

            {#if error}
                <div class="mt-4 bg-red-50 p-4 rounded-md">
                    <p class="text-sm text-red-700">{error}</p>
                </div>
            {/if}

            <div class="mt-6 bg-white shadow overflow-hidden sm:rounded-md">
                <ul class="divide-y divide-gray-200">
                    {#each keys as key}
                        <li>
                            <button
                                on:click={() => viewKeyDetails(key.id)}
                                class="w-full block hover:bg-gray-50 focus:outline-none focus:bg-gray-50 transition duration-150 ease-in-out"
                            >
                                <div class="px-4 py-4 sm:px-6">
                                    <div class="flex items-center justify-between">
                                        <div class="text-sm leading-5 font-medium text-blue-600 truncate">
                                            {key.name || key.id}
                                        </div>
                                        <div class="ml-2 flex-shrink-0 flex">
                                            <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                                                Active
                                            </span>
                                        </div>
                                    </div>
                                    <div class="mt-2 sm:flex sm:justify-between">
                                        <div class="sm:flex">
                                            <div class="mr-6 flex items-center text-sm leading-5 text-gray-500">
                                                Created: {new Date(key.created_at).toLocaleDateString()}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </button>
                        </li>
                    {/each}
                </ul>
            </div>
        </div>
    </div>
</div>