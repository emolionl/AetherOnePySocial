<script lang="ts">
    import { token } from '$lib/auth';
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    
    onMount(() => {
        if ($token) {
            goto('/keys');
        }
    });
</script>

<div class="min-h-screen bg-gradient-to-br from-indigo-50 to-purple-50">
    <nav class="bg-white shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16">
                <div class="flex items-center">
                    <span class="text-xl font-semibold text-gray-900">AetherOneSocial</span>
                </div>
                <div class="flex items-center space-x-4">
                    <a href="/login" class="text-gray-600 hover:text-gray-900">Login</a>
                    <a href="/register" class="px-4 py-2 rounded-md bg-indigo-600 text-white hover:bg-indigo-700 transition-colors">
                        Join Community
                    </a>
                </div>
            </div>
        </div>
    </nav>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center py-20">
            <h1 class="text-5xl font-bold text-gray-900 mb-6">
                Quantum-Powered<br/>Collaborative Insights
            </h1>
            <p class="text-xl text-gray-600 mb-12 max-w-2xl mx-auto">
                Connect with the AetherOneSocial community to share and explore True Random Number Generator (TRNG) results. Harness quantum-level randomness for meaningful answers to your questions.
            </p>
            <div class="flex justify-center space-x-4">
                <a href="/register" class="px-8 py-3 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors text-lg font-medium">
                    Start Collaborating
                </a>
                <a href="/login" class="px-8 py-3 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-50 transition-colors text-lg font-medium">
                    Sign In
                </a>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 py-16">
            <div class="p-6 bg-white rounded-lg shadow-sm">
                <div class="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center mb-4">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                    </svg>
                </div>
                <h3 class="text-xl font-semibold text-gray-900 mb-2">Quantum Randomness</h3>
                <p class="text-gray-600">Access true random numbers generated at the quantum level for more accurate and meaningful results.</p>
            </div>
            <div class="p-6 bg-white rounded-lg shadow-sm">
                <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                </div>
                <h3 class="text-xl font-semibold text-gray-900 mb-2">Community Collaboration</h3>
                <p class="text-gray-600">Share your results, insights, and experiences with a community of like-minded researchers and enthusiasts.</p>
            </div>
            <div class="p-6 bg-white rounded-lg shadow-sm">
                <div class="w-12 h-12 bg-pink-100 rounded-lg flex items-center justify-center mb-4">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-pink-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                </div>
                <h3 class="text-xl font-semibold text-gray-900 mb-2">Meaningful Insights</h3>
                <p class="text-gray-600">Transform quantum randomness into actionable insights and answers to your most important questions.</p>
            </div>
        </div>
    </main>

    <footer class="bg-white border-t border-gray-200 mt-20">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <div class="text-center">
                <div class="text-gray-500 mb-4">
                    © 2024 AetherOneSocial Community. All rights reserved.
                </div>
                <div class="flex justify-center space-x-4 text-sm text-gray-500">
                    <a href="/terms" class="hover:text-gray-900">Terms & Conditions</a>
                    <span>•</span>
                    <a href="/privacy" class="hover:text-gray-900">Privacy Policy</a>
                </div>
            </div>
        </div>
    </footer>
</div>

<style>
    :global(body) {
        @apply antialiased;
    }
</style>