<script lang="ts">
    import { onMount } from 'svelte';
    import { token } from '$lib/auth';
    import { getKeyDetails } from '$lib/auth';
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';

    let keyDetails: any = null;
    let error = '';

    onMount(async () => {
        if (!$token) {
            goto('/login');
            return;
        }

        try {
            const keyId = $page.params.id;
            keyDetails = await getKeyDetails($token, keyId);
        } catch (e) {
            error = 'Failed to load key details';
        }
    });
</script>

<div class="min-h-screen bg-gray-100">
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div class="px-4 py-6 sm:px-0">
            <div class="flex items-center justify-between">
                <h1 class="text-3xl font-bold text-gray-900">Key Details</h1>
                <a href="/keys" class="text-blue-600 hover:text-blue-800">Back to Keys</a>
            </div>

            {#if error}
                <div class="mt-4 bg-red-50 p-4 rounded-md">
                    <p class="text-sm text-red-700">{error}</p>
                </div>
            {/if}

            {#if keyDetails}
                <div class="mt-6 bg-white shadow overflow-hidden sm:rounded-lg">
                    <div class="px-4 py-5 sm:px-6">
                        <h3 class="text-lg leading-6 font-medium text-gray-900">
                            Key Information
                        </h3>
                    </div>
                    <div class="border-t border-gray-200">
                        <dl>
                            <div class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                                <dt class="text-sm font-medium text-gray-500">
                                    Key ID
                                </dt>
                                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                    {keyDetails.id}
                                </dd>
                            </div>
                            <div class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                                <dt class="text-sm font-medium text-gray-500">
                                    Created At
                                </dt>
                                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                    {new Date(keyDetails.created_at).toLocaleString()}
                                </dd>
                            </div>
                            <!-- Add more key details as needed -->
                        </dl>
                    </div>
                </div>
            {/if}
        </div>
    </div>
</div>