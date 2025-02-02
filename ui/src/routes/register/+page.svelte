<script lang="ts">
    import { register } from '$lib/auth';
    import { goto } from '$app/navigation';

    let username = '';
    let email = '';
    let password = '';
    let confirmPassword = '';
    let error = '';

    function validatePasswords() {
        if (password !== confirmPassword) {
            error = 'Passwords do not match';
            return false;
        }
        if (password.length < 8) {
            error = 'Password must be at least 8 characters long';
            return false;
        }
        return true;
    }

    async function handleSubmit() {
        error = '';
        
        if (!validatePasswords()) {
            return;
        }

        try {
            await register(username, email, password);
            goto('/login');
        } catch (e) {
            error = 'Registration failed. Please try again.';
        }
    }
</script>

<div class="min-h-screen bg-gray-100 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">Create your account</h2>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
            <form class="space-y-6" on:submit|preventDefault={handleSubmit}>
                {#if error}
                    <div class="bg-red-50 p-4 rounded-md">
                        <p class="text-sm text-red-700">{error}</p>
                    </div>
                {/if}
                <div>
                    <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
                    <div class="mt-1">
                        <input 
                            id="username" 
                            name="username" 
                            type="text" 
                            required 
                            bind:value={username}
                            class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" 
                        />
                    </div>
                </div>
                <div>
                    <label for="email" class="block text-sm font-medium text-gray-700">Email address</label>
                    <div class="mt-1">
                        <input 
                            id="email" 
                            name="email" 
                            type="email" 
                            required 
                            bind:value={email}
                            class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" 
                        />
                    </div>
                </div>

                <div>
                    <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
                    <div class="mt-1">
                        <input 
                            id="password" 
                            name="password" 
                            type="password" 
                            required 
                            minlength="8"
                            bind:value={password}
                            class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" 
                        />
                    </div>
                    <p class="mt-1 text-xs text-gray-500">Must be at least 8 characters long</p>
                </div>

                <div>
                    <label for="confirm-password" class="block text-sm font-medium text-gray-700">Confirm Password</label>
                    <div class="mt-1">
                        <input 
                            id="confirm-password" 
                            name="confirm-password" 
                            type="password" 
                            required 
                            bind:value={confirmPassword}
                            class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" 
                        />
                    </div>
                </div>

                <div class="flex items-center">
                    <input 
                        id="terms" 
                        name="terms" 
                        type="checkbox" 
                        required
                        class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded" 
                    />
                    <label for="terms" class="ml-2 block text-sm text-gray-900">
                        I agree to the <a href="/terms" class="text-indigo-600 hover:text-indigo-500">Terms and Conditions</a> and <a href="/privacy" class="text-indigo-600 hover:text-indigo-500">Privacy Policy</a>
                    </label>
                </div>

                <div>
                    <button 
                        type="submit"
                        class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    >
                        Register
                    </button>
                </div>
            </form>

            <div class="mt-6">
                <div class="relative">
                    <div class="relative flex justify-center text-sm">
                        <span class="px-2 bg-white text-gray-500">
                            Already have an account? <a href="/login" class="font-medium text-indigo-600 hover:text-indigo-500">Sign in</a>
                        </span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>