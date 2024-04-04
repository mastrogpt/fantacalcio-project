module.exports = {
    // ...
    extends: ['plugin:svelte/recommended'],
    // ...
    parser: '@typescript-eslint/parser',
    parserOptions: {
        ecmaVersion: 2020,
        sourceType: 'module',
        tsconfigRootDir: __dirname,
        project: './tsconfig.json',
        extraFileExtensions: ['.svelte'] // This is a required setting in `@typescript-eslint/parser` v4.24.0.
    },
    env: {
        es6: true,
        browser: true
    },
    overrides: [
        {
            files: ['*.svelte'],
            parser: 'svelte-eslint-parser',
            // Parse the `<script>` in `.svelte` as TypeScript by adding the following configuration.
            parserOptions: {
                parser: '@typescript-eslint/parser'
            }
        }
        // ...
    ]
    // ...
};

